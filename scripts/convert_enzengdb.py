#!/usr/bin/env python3
"""Turn the EnzEngDB record table into FitnessBench datasets.

EnzEngDB (Nucleic Acids Research 2026, D564) publishes one row per measured
enzyme variant. FitnessBench wants one CSV per (protein, readout) pair.

    python scripts/convert_enzengdb.py                  # report what survives
    python scripts/convert_enzengdb.py --write          # write the datasets

Reporting is the default and writing is a separate step on purpose: a
reference.csv row needs a source organism and an assay method that EnzEngDB
does not record, so those are read out of the source publication by hand and
kept in PUBLICATIONS below. A dataset with no entry there is reported but never
written.
"""

from __future__ import annotations

import argparse
import collections
import csv
import os
import re
import statistics
import sys

MUTATION_RE = re.compile(r"^([A-Z])(\d+)([A-Z])$")

# EnzEngDB column names, verbatim, including the typo and the trailing space
COL_PARENT = "parent_aa"
COL_VARIANT = "variant_aa"
COL_LABELS = "aminoacid_mutations_from_parent"
COL_REACTION = "reaction_smiles"
COL_DOI = "doi"
COL_AUTHOR = "first author"
COL_TITLE = "paper title"
COL_DATE = "date published "
COL_ENZYME = "enzyme_name_from_paper"

# metric -> (category, property directory, property, EnzEngDB column)
METRICS = {
    "TTN": ("Activity", "CatalyticActivity", "Catalytic activity", "TTN (if applicable)"),
    "yield": ("Activity", "Yield", "Yield", "activity_for_reaction_% (if applicable)"),
    "ee": ("Selectivity", "Enantioselectivity", "Enantioselectivity",
           "selectivity(ee%),diastereo or chemo should be a separate smiles entry"),
}

# All three metrics already increase with fitness, so nothing is inverted.
# Signed ee is kept signed: a negative value means the enzyme favours the other
# enantiomer, so larger really is better with respect to the targeted product.
DUPLICATE_TOLERANCE = 0.02  # relative range below which repeats are one measurement
MODEL = "DE"  # every campaign here is directed evolution; the Source dir records EnzEngDB
SOURCE_DIR = "EnzEngDB"

CONVERSION_REMARK = (
    "Converted from the EnzEngDB record table (protein-evolution-database_V6.csv). "
    "Variant sequences were rebuilt by applying EnzEngDB's stated mutation labels to "
    "parent_aa rather than using its variant_aa column, which disagrees with its own "
    "labels for part of the table; a numbering offset of {offset} fits every label in "
    "this dataset. "
)

# Assay method and source organism are not in EnzEngDB. These were read from the
# source publications; the accompanying note says which parts could not be.
PUBLICATIONS = {
    ("10.1038/s41557-021-00794-z", "TTN"): {
        "author": "Liu", "year": "2021", "short": "P411-L1",
        "protein": "P411-L1 (engineered serine-ligated cytochrome P411 variant on a "
                   "cytochrome P450-BM3 / CYP102A1 background), 665 aa construct as recorded by EnzEngDB",
        "source_organism": "Bacillus megaterium (P450-BM3 parent); expressed in Escherichia coli",
        "readout": "TTN (total turnover number)", "slug": "TTN",
        "assay_method": (
            "Whole-cell biocatalysis in an anaerobic chamber (oxygen < 40 ppm). E. coli BL21 "
            "E. cloni expressing the P411 variant, resuspended in M9-N minimal medium pH 7.4 to "
            "OD600 = 30; 400 uL reactions containing 10.0 mM alpha-diazo-gamma-lactone (LAD), "
            "10.0 mM N-methylaniline and 25 mM D-glucose; sealed vials shaken at 550 rpm at room "
            "temperature for 4 h. Product quantified by reverse-phase HPLC against a calibration "
            "curve of the racemic standard, with p-methyl anisole as internal standard. TTN is "
            "product concentration divided by haem concentration from the hemochrome assay."),
        "note": "TTN is a lower bound: the hemochrome assay measures haem rather than active enzyme, "
                "as the source states.",
    },
    ("10.1038/s41557-021-00794-z", "yield"): {
        "author": "Liu", "year": "2021", "short": "P411-L1",
        "protein": "P411-L1 (engineered serine-ligated cytochrome P411 variant on a "
                   "cytochrome P450-BM3 / CYP102A1 background), 665 aa construct as recorded by EnzEngDB",
        "source_organism": "Bacillus megaterium (P450-BM3 parent); expressed in Escherichia coli",
        "readout": "Yield (%)", "slug": "percent",
        "assay_method": (
            "Whole-cell biocatalysis in an anaerobic chamber (oxygen < 40 ppm). E. coli BL21 "
            "E. cloni expressing the P411 variant, resuspended in M9-N minimal medium pH 7.4 to "
            "OD600 = 30; 400 uL reactions containing 10.0 mM alpha-diazo-gamma-lactone (LAD), "
            "10.0 mM N-methylaniline and 25 mM D-glucose; sealed vials shaken at 550 rpm at room "
            "temperature for 4 h. Yield quantified by reverse-phase HPLC against a calibration "
            "curve of the racemic standard, with p-methyl anisole as internal standard."),
        "note": "",
    },
    ("10.1021/jacs.4c09989", "yield"): {
        "author": "Alfonzo", "year": "2024", "short": "ApPgb",
        "protein": "L-ApPgb-alphaEsA (engineered protoglobin, ApPgb W59A/Y60G/F145G background); "
                   "dimeric, 195 aa per monomer",
        "source_organism": "Aeropyrum pernix; expressed in Escherichia coli",
        "readout": "Yield (%)", "slug": "percent",
        "assay_method": (
            "Whole-cell biocatalysis in E. coli, aerobic, at room temperature. 2.5 mM ethyl "
            "2-(4-fluorophenyl)acetate with O-pivaloylhydroxylamine triflic acid as nitrene "
            "precursor. Yield determined by HPLC against a calibration curve with internal standard."),
        "note": "Cell density, buffer and reaction time are not stated in the accessible text and "
                "the ACS supporting information is paywalled; the substrate concentration is as "
                "recorded by EnzEngDB.",
    },
    ("10.1021/jacs.4c09989", "ee"): {
        "author": "Alfonzo", "year": "2024", "short": "ApPgb",
        "protein": "L-ApPgb-alphaEsA (engineered protoglobin, ApPgb W59A/Y60G/F145G background); "
                   "dimeric, 195 aa per monomer",
        "source_organism": "Aeropyrum pernix; expressed in Escherichia coli",
        "readout": "Enantiomeric excess (% ee), signed toward the targeted enantiomer",
        "slug": "ee",
        "assay_method": (
            "Whole-cell biocatalysis in E. coli, aerobic, at room temperature. 2.5 mM ethyl "
            "2-(4-fluorophenyl)acetate with O-pivaloylhydroxylamine triflic acid as nitrene "
            "precursor. Enantiomeric excess determined by treating the product with Marfey's "
            "reagent, converting the enantiomers into diastereomers resolved by achiral HPLC-MS."),
        "note": "ee is kept signed: negative values mean the variant favours the opposite "
                "enantiomer, so larger remains better. Cell density, buffer and reaction time are "
                "not stated in the accessible text and the ACS supporting information is paywalled.",
    },
}

DATASET_COLUMNS = ["mutant", "sequence", "readout", "normalized-score"]
REFERENCE_COLUMNS = ["filename", "protein", "source_organism", "seq_len", "property", "readout",
                     "wt_readout", "assay_method", "n_variants", "doi", "remark"]


def to_float(raw: str) -> float | None:
    s = (raw or "").strip().replace("%", "").replace(",", "").lstrip("><~")
    try:
        value = float(s)
    except ValueError:
        return None
    return value if value == value and abs(value) != float("inf") else None


def parse_labels(listed: str) -> list[re.Match]:
    parts = listed.replace(",", "_").split("_")
    return [m for m in (MUTATION_RE.match(p.strip()) for p in parts) if m]


def rebuild(parent: str, listed: str) -> tuple[str | None, int | None, str]:
    """Apply EnzEngDB's stated labels to parent_aa, scanning for a numbering offset.

    EnzEngDB stores a `variant_aa` column, but it cannot be trusted: for part of
    the table it disagrees with the row's own mutation labels because a mutation
    was applied at the wrong position. Their pipeline flags many of these itself
    ("position 0 and 1 index had same AA used 1 index").

    So the sequence is rebuilt here instead, the way step 4 of the workflow
    prescribes. Every label names the wild-type residue it expects, so requiring
    all of them to match parent_aa at one constant offset is many independent
    checks at once: a numbering that fits every label is not a guess.
    """
    labels = parse_labels(listed)
    if not labels:
        return None, None, "no parseable mutation labels"
    for offset in range(-3, 4):
        positions = [int(m.group(2)) + offset for m in labels]
        if not all(1 <= p <= len(parent) for p in positions):
            continue
        if all(parent[p - 1] == m.group(1) for p, m in zip(positions, labels)):
            if len(set(positions)) != len(positions):
                return None, None, "same position substituted twice"
            seq = list(parent)
            for p, m in zip(positions, labels):
                seq[p - 1] = m.group(3)
            return "".join(seq), offset, ""
    return None, None, "no numbering offset fits the stated labels"


def substitutions(parent: str, variant: str) -> str:
    subs = [f"{a}{i + 1}{b}" for i, (a, b) in enumerate(zip(parent, variant)) if a != b]
    return ":".join(subs) if subs else "WT"


def load(path: str) -> list[dict]:
    csv.field_size_limit(10 ** 9)
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def build(rows: list[dict], metric: str, stats: collections.Counter) -> dict[tuple, dict]:
    column = METRICS[metric][3]
    groups: dict[tuple, dict] = collections.defaultdict(
        lambda: {"values": collections.defaultdict(list), "rows": [], "offsets": set()})

    for row in rows:
        parent = (row.get(COL_PARENT) or "").strip()
        if not parent:
            stats["no parent sequence"] += 1
            continue
        value = to_float(row.get(column, ""))
        if value is None:
            continue  # metric simply not measured for this row

        listed = (row.get(COL_LABELS) or "").strip()
        offset = 0
        if not listed or listed == "?":
            sequence = parent  # no mutations listed: the row is the parent itself
        else:
            sequence, offset, why = rebuild(parent, listed)
            if sequence is None:
                stats[why] += 1
                continue
            stored = (row.get(COL_VARIANT) or "").strip()
            if stored and stored != sequence:
                stats["EnzEngDB variant_aa disagrees with its own labels"] += 1

        key = (row[COL_DOI].strip(), parent, row[COL_REACTION].strip())
        groups[key]["values"][sequence].append(value)
        groups[key]["rows"].append(row)
        groups[key]["offsets"].add(offset)
    return groups


def collapse(group: dict, stats: collections.Counter) -> tuple[dict[str, float], list[str]]:
    """Average repeats that agree, drop repeats that do not, and say which."""
    readouts: dict[str, float] = {}
    dropped: list[str] = []
    for variant, values in group["values"].items():
        if len(values) == 1:
            readouts[variant] = values[0]
            continue
        if (max(values) - min(values)) / max(abs(max(values)), 1e-9) < DUPLICATE_TOLERANCE:
            readouts[variant] = statistics.fmean(values)
        else:
            dropped.append(variant)
            stats["repeat measurements disagree"] += 1
    return readouts, dropped


def normalise_doi(doi: str) -> str:
    return re.sub(r"^(https?://)?(dx\.)?doi\.org/|^DOI:\s*", "", doi.strip(), flags=re.I).strip()


def candidates(rows: list[dict], min_variants: int, stats: collections.Counter) -> list[dict]:
    found = []
    for metric in METRICS:
        for key, group in build(rows, metric, stats).items():
            readouts, dropped = collapse(group, stats)
            if len(readouts) < min_variants:
                continue
            doi = normalise_doi(key[0])
            found.append({
                "metric": metric, "doi": doi, "parent": key[1], "reaction": key[2],
                "readouts": readouts, "dropped": dropped,
                "offsets": group["offsets"], "row": group["rows"][0],
                "meta": PUBLICATIONS.get((doi, metric)),
            })
    found.sort(key=lambda d: (d["metric"], -len(d["readouts"])))
    return found


def write_dataset(cand: dict, datasets_dir: str) -> tuple[str, dict]:
    meta = cand["meta"]
    metric = cand["metric"]
    category, prop_dir, prop, _ = METRICS[metric]
    parent = cand["parent"]
    readouts = cand["readouts"]

    # WT first, then the variants in descending readout so the file reads usefully
    items = sorted(readouts.items(), key=lambda kv: (kv[0] != parent, -kv[1]))
    values = [v for _, v in items]
    mean, sd = statistics.fmean(values), statistics.pstdev(values)

    name = (f"{meta['author']} {meta['year']}-{MODEL}-{meta['short']}-"
            f"{prop.replace(' ', '').lower()}-{meta['slug']}.csv")
    rel = f"{prop_dir}/{SOURCE_DIR}/{name}"
    path = os.path.join(datasets_dir, category, prop_dir, SOURCE_DIR, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=DATASET_COLUMNS)
        writer.writeheader()
        for seq, value in items:
            writer.writerow({
                "mutant": substitutions(parent, seq),
                "sequence": seq,
                "readout": repr(value) if isinstance(value, float) else value,
                "normalized-score": (value - mean) / sd if sd else 0.0,
            })

    offset = ", ".join(str(o) for o in sorted(cand["offsets"]))
    remark = CONVERSION_REMARK.format(offset=offset)
    if cand["dropped"]:
        remark += (f"{len(cand['dropped'])} variant(s) dropped: EnzEngDB records repeat "
                   f"measurements for them that disagree by more than "
                   f"{int(DUPLICATE_TOLERANCE * 100)}%, so they were not averaged. ")
    if meta["note"]:
        remark += meta["note"]

    reference_row = {
        "filename": rel,
        "protein": meta["protein"],
        "source_organism": meta["source_organism"],
        "seq_len": str(len(parent)),
        "property": prop,
        "readout": meta["readout"],
        "wt_readout": repr(readouts[parent]) if parent in readouts else "",
        "assay_method": meta["assay_method"],
        "n_variants": str(len(items) - (1 if parent in readouts else 0)),
        "doi": cand["doi"],
        "remark": remark.strip(),
    }
    return os.path.join(datasets_dir, category), reference_row


def update_reference(category_dir: str, new_rows: list[dict]) -> None:
    path = os.path.join(category_dir, "reference.csv")
    existing: list[dict] = []
    if os.path.exists(path):
        with open(path, newline="", encoding="utf-8") as fh:
            existing = list(csv.DictReader(fh))
    keep = {r["filename"] for r in new_rows}
    merged = [r for r in existing if r["filename"] not in keep] + new_rows
    os.makedirs(category_dir, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=REFERENCE_COLUMNS)
        writer.writeheader()
        writer.writerows(merged)


def write_source_extract(cand: dict, rows: list[dict], repo_root: str) -> str:
    """The rows of the EnzEngDB table this dataset came from, kept as the source data."""
    meta = cand["meta"]
    out = os.path.join(repo_root, "original_datasets",
                       f"{meta['author']} {meta['year']}-{MODEL}-EnzEngDB-records.csv")
    subset = [r for r in rows if normalise_doi(r[COL_DOI]) == cand["doi"]]
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(subset)
    return os.path.relpath(out, repo_root).replace(os.sep, "/")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", default="EnzymeEngineeringDB/data/protein-evolution-database_V6.csv")
    ap.add_argument("--datasets-dir", default="datasets")
    ap.add_argument("--min-variants", type=int, default=15,
                    help="smallest dataset worth keeping (default: 15)")
    ap.add_argument("--write", action="store_true", help="write the datasets, not just report")
    args = ap.parse_args()

    if not os.path.exists(args.source):
        print(f"no such file: {args.source}", file=sys.stderr)
        return 2

    rows = load(args.source)
    stats: collections.Counter = collections.Counter()
    found = candidates(rows, args.min_variants, stats)
    repo_root = os.path.dirname(os.path.abspath(args.datasets_dir)) or "."

    by_category: dict[str, list[dict]] = collections.defaultdict(list)
    written = skipped = 0
    for cand in found:
        first = cand["row"]
        label = (f"{first[COL_AUTHOR].strip()} | {first[COL_ENZYME].strip()} | "
                 f"{cand['metric']} | n={len(cand['readouts'])}")
        if cand["meta"] is None:
            skipped += 1
            print(f"[skip] {label}\n       {cand['doi']} - no entry in PUBLICATIONS, "
                  f"needs source_organism and assay_method from the paper")
            continue
        if not args.write:
            print(f"[ready] {label}  ->  {METRICS[cand['metric']][0]}/{METRICS[cand['metric']][1]}/")
            continue
        category_dir, reference_row = write_dataset(cand, args.datasets_dir)
        by_category[category_dir].append(reference_row)
        extract = write_source_extract(cand, rows, repo_root)
        written += 1
        print(f"[write] {reference_row['filename']}\n        source: {extract}")

    if args.write:
        for category_dir, new_rows in by_category.items():
            update_reference(category_dir, new_rows)
            print(f"[ref]   {os.path.join(category_dir, 'reference.csv')}: "
                  f"{len(new_rows)} row(s)")

    print(f"\n{len(found)} candidate(s) at >= {args.min_variants} variants; "
          f"{written} written, {skipped} skipped for missing publication metadata")
    print("rows excluded:")
    for reason, n in stats.most_common():
        print(f"  {n:5d}  {reason}   (counted once per metric pass)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
