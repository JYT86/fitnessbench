#!/usr/bin/env python3
"""Validate every dataset in FitnessBench against the rules in example_workflow.md.

Stdlib only, no dependencies. Run from the repository root:

    python validate.py            # errors fail, warnings are advisory
    python validate.py --strict   # warnings fail too
    python validate.py -v         # list every file, not just the failing ones

Exit status is 0 when nothing failed, 1 otherwise.
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import statistics
import sys
from collections import defaultdict

DATASET_COLUMNS = ["mutant", "sequence", "readout", "normalized-score"]

REFERENCE_COLUMNS = [
    "filename", "protein", "source_organism", "seq_len", "property", "readout",
    "wt_readout", "assay_method", "n_variants", "doi", "remark",
]

# remark records only deviations from the source, so it is allowed to be empty
REFERENCE_REQUIRED = [c for c in REFERENCE_COLUMNS if c != "remark"]

AMINO_ACIDS = set("ACDEFGHIKLMNPQRSTVWY")
MUTATION_RE = re.compile(r"([A-Z])(\d+)([A-Z])")
DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$")
# "{FirstAuthor} {Year}-{Model}-{Protein}-{Property}-{Readout}.csv"
FILENAME_RE = re.compile(r"^.+ (\d{4})-([^-]+)-(.+)-(.+)-(.+)\.csv$")

Z_TOL = 1e-6


class Report:
    """Collects issues per file and prints them grouped."""

    def __init__(self, verbose: bool = False) -> None:
        self.verbose = verbose
        self.issues: dict[str, list[tuple[str, str]]] = defaultdict(list)
        self.checked: list[str] = []

    def error(self, where: str, msg: str) -> None:
        self.issues[where].append(("ERROR", msg))

    def warn(self, where: str, msg: str) -> None:
        self.issues[where].append(("WARN", msg))

    def seen(self, where: str) -> None:
        self.checked.append(where)

    def counts(self) -> tuple[int, int]:
        errors = sum(1 for v in self.issues.values() for lvl, _ in v if lvl == "ERROR")
        warns = sum(1 for v in self.issues.values() for lvl, _ in v if lvl == "WARN")
        return errors, warns

    def render(self) -> None:
        for where in self.checked:
            found = self.issues.get(where, [])
            if not found and not self.verbose:
                continue
            mark = "ok " if not found else ("ERR" if any(l == "ERROR" for l, _ in found) else "warn")
            print(f"[{mark}] {where}")
            for level, msg in found:
                print(f"       {level}: {msg}")
        # anything reported against a path we never registered (e.g. orphan files)
        for where, found in self.issues.items():
            if where in self.checked:
                continue
            print(f"[ERR] {where}")
            for level, msg in found:
                print(f"       {level}: {msg}")


def parse_mutant(mutant: str) -> list[tuple[str, int, str]] | None:
    """Return [(wt, pos, mut), ...] for a mutant label, or None if malformed."""
    out = []
    for part in mutant.split(":"):
        m = MUTATION_RE.fullmatch(part)
        if not m:
            return None
        out.append((m.group(1), int(m.group(2)), m.group(3)))
    return out


def rounding_tolerance(printed: str) -> float:
    """Half a unit in the last printed decimal place, so a rounded value still matches."""
    decimals = len(printed.split(".")[1].strip()) if "." in printed else 0
    return 0.5 * 10 ** (-decimals) * 1.01


def check_dataset(path: str, rel: str, rep: Report) -> dict | None:
    """Validate one dataset CSV. Returns the facts the reference.csv check needs."""
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        header = reader.fieldnames or []
        rows = list(reader)

    if header != DATASET_COLUMNS:
        rep.error(rel, f"columns are {header}, expected exactly {DATASET_COLUMNS}")
        return None
    if not rows:
        rep.error(rel, "file has no data rows")
        return None

    # --- mutant labels -----------------------------------------------------
    mutants = [r["mutant"] for r in rows]
    dupes = {m for m in mutants if mutants.count(m) > 1}
    if dupes:
        rep.error(rel, f"duplicate mutant labels: {sorted(dupes)[:5]}")

    parsed: dict[str, list[tuple[str, int, str]]] = {}
    for m in mutants:
        if m == "WT":
            continue
        subs = parse_mutant(m)
        if subs is None:
            rep.error(rel, f"malformed mutant label {m!r} (expected {{WT}}{{pos}}{{MUT}} joined by ':')")
            continue
        parsed[m] = subs
        positions = [p for _, p, _ in subs]
        if len(set(positions)) != len(positions):
            rep.error(rel, f"{m}: same position substituted more than once")
        for wt, _, mut in subs:
            if wt == mut:
                rep.error(rel, f"{m}: synonymous substitution ({wt} to {mut})")

    # --- sequences ---------------------------------------------------------
    lengths = {len(r["sequence"]) for r in rows}
    if len(lengths) != 1:
        rep.error(rel, f"sequences have differing lengths: {sorted(lengths)}")
        return None
    seq_len = lengths.pop()

    odd = set("".join(r["sequence"] for r in rows)) - AMINO_ACIDS
    if odd:
        rep.error(rel, f"non-standard residues in sequences: {sorted(odd)}")

    # --- reference sequence, and every row checked against it ---------------
    # Reverting a row's substitutions must land on the same reference sequence for
    # every row. This is the step-4 check from the workflow, run without needing a
    # WT row to exist: it catches numbering offsets, substitutions that never
    # landed, and unmutated positions drifting between rows.
    wt_rows = [r for r in rows if r["mutant"] == "WT"]
    if len(wt_rows) > 1:
        rep.error(rel, "more than one WT row")
    reference = wt_rows[0]["sequence"] if wt_rows else None

    reverted: dict[str, list[str]] = defaultdict(list)
    for r in rows:
        m = r["mutant"]
        if m == "WT" or m not in parsed:
            continue
        seq = list(r["sequence"])
        ok = True
        for wt, pos, mut in parsed[m]:
            if not 1 <= pos <= seq_len:
                rep.error(rel, f"{m}: position {pos} outside sequence (length {seq_len})")
                ok = False
                continue
            if seq[pos - 1] != mut:
                rep.error(rel, f"{m}: sequence carries {seq[pos - 1]} at {pos}, label says {mut}")
                ok = False
                continue
            seq[pos - 1] = wt
        if ok:
            reverted["".join(seq)].append(m)

    if reverted:
        derived = max(reverted, key=lambda s: len(reverted[s]))
        if len(reverted) > 1:
            for seq, labels in reverted.items():
                if seq == derived:
                    continue
                sites = [i + 1 for i, (a, b) in enumerate(zip(seq, derived)) if a != b]
                rep.error(rel, f"reverting {labels[:3]} disagrees with the other rows at position(s) {sites[:5]}")
        if reference is None:
            reference = derived
        elif reference != derived:
            sites = [i + 1 for i, (a, b) in enumerate(zip(reference, derived)) if a != b]
            rep.error(rel, f"WT row disagrees with the sequence implied by the mutants at position(s) {sites[:5]}")

    # hamming distance computed from the output, not the labels: catches a
    # position mutated twice or a substitution that silently never landed
    if reference is not None:
        for r in rows:
            m = r["mutant"]
            if m == "WT" or m not in parsed:
                continue
            observed = sum(a != b for a, b in zip(reference, r["sequence"]))
            expected = len({p for _, p, _ in parsed[m]})
            if observed != expected:
                rep.error(rel, f"{m}: {observed} residue(s) differ from WT, label declares {expected}")

    # --- readout and normalization -----------------------------------------
    try:
        readouts = [float(r["readout"]) for r in rows]
    except ValueError as exc:
        rep.error(rel, f"non-numeric readout: {exc}")
        return None
    if any(x != x or x in (float("inf"), float("-inf")) for x in readouts):
        rep.error(rel, "readout contains NaN or infinity")
        return None

    try:
        scores = [float(r["normalized-score"]) for r in rows]
    except ValueError as exc:
        rep.error(rel, f"non-numeric normalized-score: {exc}")
        return None

    mean = statistics.fmean(readouts)
    sd = statistics.pstdev(readouts)
    if sd == 0:
        if any(s != 0 for s in scores):
            rep.error(rel, "readout is constant, so every normalized-score must be 0")
    else:
        for r, x, s in zip(rows, readouts, scores):
            expected_z = (x - mean) / sd
            if abs(expected_z - s) > Z_TOL:
                rep.error(rel, f"{r['mutant']}: normalized-score is {s}, z-score of readout is {expected_z:.6f}")
                break  # one example is enough, the whole column is regenerated anyway

    if wt_rows and rows[0]["mutant"] != "WT":
        rep.warn(rel, "WT row is present but is not the first row")

    return {
        "seq_len": seq_len,
        "n_variants": len(rows) - len(wt_rows),
        "wt_readout": float(wt_rows[0]["readout"]) if wt_rows else None,
        "has_wt_row": bool(wt_rows),
    }


def check_reference(category_dir: str, facts: dict[str, dict], rep: Report) -> None:
    ref_path = os.path.join(category_dir, "reference.csv")
    rel = os.path.relpath(ref_path).replace(os.sep, "/")
    rep.seen(rel)

    if not os.path.exists(ref_path):
        rep.error(rel, "category has no reference.csv")
        return

    with open(ref_path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        header = reader.fieldnames or []
        rows = list(reader)

    if header != REFERENCE_COLUMNS:
        rep.error(rel, f"columns are {header}, expected exactly {REFERENCE_COLUMNS}")
        return

    listed = set()
    for row in rows:
        name = row["filename"]
        where = f"{rel} [{name}]"
        if name in listed:
            rep.error(where, "filename listed more than once")
            continue
        listed.add(name)

        target = os.path.join(category_dir, name)
        if not os.path.exists(target):
            rep.error(where, "filename does not resolve to a file")
            continue

        for col in REFERENCE_REQUIRED:
            if not row[col].strip():
                rep.error(where, f"{col} is empty")

        if not DOI_RE.match(row["doi"].strip()):
            rep.error(where, f"doi {row['doi']!r} is not a bare DOI (expected 10.xxxx/...)")

        # the property column should agree with the directory it sits in
        prop_dir = name.split("/")[0]
        if prop_dir.lower() != row["property"].replace(" ", "").lower():
            rep.warn(where, f"property {row['property']!r} does not match directory {prop_dir!r}")

        fact = facts.get(os.path.normpath(target))
        if fact is None:
            continue  # the dataset itself failed hard, its errors are already reported

        # seq_len, n_variants and wt_readout are derived from the CSV, so they
        # cannot be allowed to drift from it
        if row["seq_len"].strip() != str(fact["seq_len"]):
            rep.error(where, f"seq_len is {row['seq_len']}, dataset has {fact['seq_len']}")
        if row["n_variants"].strip() != str(fact["n_variants"]):
            rep.error(where, f"n_variants is {row['n_variants']}, dataset has {fact['n_variants']}")

        printed = row["wt_readout"].strip()
        if fact["has_wt_row"]:
            try:
                stated = float(printed)
            except ValueError:
                rep.error(where, f"wt_readout {printed!r} is not numeric")
            else:
                if abs(stated - fact["wt_readout"]) > rounding_tolerance(printed):
                    rep.error(where, f"wt_readout is {printed}, WT row reads {fact['wt_readout']}")
        elif printed:
            try:
                float(printed)
            except ValueError:
                rep.error(where, f"wt_readout {printed!r} is not numeric")

    # every dataset under this category must be listed
    for path in sorted(facts):
        name = os.path.relpath(path, category_dir).replace(os.sep, "/")
        if name.startswith(".."):
            continue
        if name not in listed:
            rep.error(f"{rel} [{name}]", "dataset exists but has no row in reference.csv")


def check_layout(path: str, rel: str, root: str, rep: Report) -> None:
    parts = os.path.relpath(path, root).replace(os.sep, "/").split("/")
    if len(parts) != 4:
        rep.error(rel, "expected datasets/{Category}/{Property}/{Source}/{file}.csv")
        return
    if not FILENAME_RE.match(parts[-1]):
        rep.warn(rel, "filename does not follow '{Author} {Year}-{Model}-{Protein}-{Property}-{Readout}.csv'")


def check_sources(path: str, rel: str, repo_root: str, rep: Report) -> None:
    """papers/ and original_datasets/ share the dataset's '{Author} {Year}-{Model}' prefix."""
    bits = os.path.basename(path).split("-")
    if len(bits) < 2:
        return
    prefix = "-".join(bits[:2])
    for folder in ("papers", "original_datasets"):
        d = os.path.join(repo_root, folder)
        if not os.path.isdir(d):
            continue
        if not any(f.startswith(prefix) for f in os.listdir(d)):
            rep.warn(rel, f"no file in {folder}/ starts with {prefix!r}")


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--datasets-dir", default="datasets",
                    help="root of the dataset tree (default: datasets)")
    ap.add_argument("--strict", action="store_true", help="treat warnings as failures")
    ap.add_argument("-v", "--verbose", action="store_true", help="list files that passed as well")
    args = ap.parse_args()

    root = args.datasets_dir
    if not os.path.isdir(root):
        print(f"no such directory: {root}", file=sys.stderr)
        return 2
    repo_root = os.path.dirname(os.path.abspath(root)) or "."

    rep = Report(verbose=args.verbose)
    by_category: dict[str, dict[str, dict]] = defaultdict(dict)

    dataset_paths = []
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            if name.endswith(".csv") and name != "reference.csv":
                dataset_paths.append(os.path.join(dirpath, name))
    dataset_paths.sort()

    if not dataset_paths:
        print(f"no dataset CSVs found under {root}/", file=sys.stderr)
        return 2

    for path in dataset_paths:
        rel = os.path.relpath(path).replace(os.sep, "/")
        rep.seen(rel)
        check_layout(path, rel, root, rep)
        check_sources(path, rel, repo_root, rep)
        facts = check_dataset(path, rel, rep)
        category = os.path.join(root, os.path.relpath(path, root).replace(os.sep, "/").split("/")[0])
        by_category.setdefault(category, {})
        if facts is not None:
            by_category[category][os.path.normpath(path)] = facts

    for category in sorted(by_category):
        check_reference(category, by_category[category], rep)

    rep.render()
    errors, warns = rep.counts()
    n_variants = sum(f["n_variants"] for c in by_category.values() for f in c.values())
    print(f"\n{len(dataset_paths)} dataset(s), {n_variants} variants, {len(by_category)} categor(ies): "
          f"{errors} error(s), {warns} warning(s)")

    return 1 if errors or (args.strict and warns) else 0


if __name__ == "__main__":
    sys.exit(main())
