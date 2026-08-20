#!/usr/bin/env python3
"""Check that validate.py actually catches the mistakes it claims to catch.

Each case copies the dataset tree to a temporary directory, introduces one
specific corruption, and asserts that validate.py fails and says why. A
validator that has only ever seen clean data is not evidence of anything.

    python test_validate.py
"""

from __future__ import annotations

import csv
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
VALIDATE = os.path.join(HERE, "validate.py")
DATASETS = os.path.join(HERE, "datasets")

# a small dataset with a WT row, used as the target for most corruptions.
# TARGET is category-relative, the same form reference.csv stores in `filename`.
CATEGORY = "Stability"
TARGET = "ThermalStability/PRIME/Jiang 2024-PRIME-Creatinase-thermalstability-Tm.csv"


def read_csv(path: str) -> tuple[list[str], list[dict]]:
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: str, header: list[str], rows: list[dict]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)


def target_path(root: str) -> str:
    return os.path.join(root, CATEGORY, *TARGET.split("/"))


def reference_path(root: str) -> str:
    return os.path.join(root, CATEGORY, "reference.csv")


def edit_target(root: str, fn) -> None:
    path = target_path(root)
    header, rows = read_csv(path)
    header, rows = fn(header, rows)
    write_csv(path, header, rows)


def edit_reference(root: str, fn) -> None:
    path = reference_path(root)
    header, rows = read_csv(path)
    for row in rows:
        if row["filename"] == TARGET:
            fn(row)
    write_csv(path, header, rows)


def swap_residue(seq: str, pos: int, aa: str) -> str:
    return seq[: pos - 1] + aa + seq[pos:]


def first_variant(rows: list[dict]) -> dict:
    return next(r for r in rows if r["mutant"] != "WT")


# --- corruptions -----------------------------------------------------------


def tamper_score(header, rows):
    rows[1]["normalized-score"] = str(float(rows[1]["normalized-score"]) + 0.01)
    return header, rows


def tamper_readout_only(header, rows):
    # readout edited without regenerating normalized-score
    rows[1]["readout"] = str(float(rows[1]["readout"]) + 5)
    return header, rows


def drift_unmutated_position(header, rows):
    # a residue changes in one row at a position that row does not mutate
    row = first_variant(rows)
    pos = int(row["mutant"][1:-1])
    other = 1 if pos != 1 else 2
    aa = "W" if row["sequence"][other - 1] != "W" else "Y"
    row["sequence"] = swap_residue(row["sequence"], other, aa)
    return header, rows


def label_disagrees_with_sequence(header, rows):
    # label says one substitution, the sequence carries a different residue
    row = first_variant(rows)
    wt, pos, mut = row["mutant"][0], int(row["mutant"][1:-1]), row["mutant"][-1]
    row["mutant"] = f"{wt}{pos}{'W' if mut != 'W' else 'Y'}"
    return header, rows


def substitution_never_landed(header, rows):
    # multi-site label, but only one of the substitutions is in the sequence
    row = first_variant(rows)
    wt, pos, mut = row["mutant"][0], int(row["mutant"][1:-1]), row["mutant"][-1]
    other = pos + 1 if pos + 1 <= len(row["sequence"]) else pos - 1
    row["mutant"] = f"{wt}{pos}{mut}:{row['sequence'][other - 1]}{other}W"
    return header, rows


def wt_row_altered(header, rows):
    wt_row = next(r for r in rows if r["mutant"] == "WT")
    pos = 3
    aa = "W" if wt_row["sequence"][pos - 1] != "W" else "Y"
    wt_row["sequence"] = swap_residue(wt_row["sequence"], pos, aa)
    return header, rows


def duplicate_mutant(header, rows):
    rows.append(dict(rows[1]))
    return header, rows


def synonymous_label(header, rows):
    row = first_variant(rows)
    wt, pos = row["mutant"][0], int(row["mutant"][1:-1])
    row["sequence"] = swap_residue(row["sequence"], pos, wt)
    row["mutant"] = f"{wt}{pos}{wt}"
    return header, rows


def malformed_label(header, rows):
    first_variant(rows)["mutant"] = "not-a-mutation"
    return header, rows


def nonstandard_residue(header, rows):
    row = first_variant(rows)
    row["sequence"] = swap_residue(row["sequence"], 5, "X")
    return header, rows


def ragged_sequence(header, rows):
    row = first_variant(rows)
    row["sequence"] = row["sequence"][:-1]
    return header, rows


def extra_column(header, rows):
    header = header + ["extra"]
    for row in rows:
        row["extra"] = "1"
    return header, rows


def non_numeric_readout(header, rows):
    first_variant(rows)["readout"] = "no expression"
    return header, rows


def drop_reference_row(root: str) -> None:
    path = reference_path(root)
    header, rows = read_csv(path)
    write_csv(path, header, [r for r in rows if r["filename"] != TARGET])


CASES = [
    ("normalized-score does not match readout", lambda r: edit_target(r, tamper_score),
     "z-score of readout"),
    ("readout edited without renormalizing", lambda r: edit_target(r, tamper_readout_only),
     "z-score of readout"),
    ("residue drifts at an unmutated position", lambda r: edit_target(r, drift_unmutated_position),
     "disagrees with"),
    ("label disagrees with the sequence", lambda r: edit_target(r, label_disagrees_with_sequence),
     "sequence carries"),
    ("declared substitution never landed", lambda r: edit_target(r, substitution_never_landed),
     "label declares"),
    ("WT row contradicts the mutants", lambda r: edit_target(r, wt_row_altered),
     "WT row disagrees"),
    ("duplicate mutant label", lambda r: edit_target(r, duplicate_mutant),
     "duplicate mutant"),
    ("synonymous substitution", lambda r: edit_target(r, synonymous_label),
     "synonymous"),
    ("malformed mutant label", lambda r: edit_target(r, malformed_label),
     "malformed mutant label"),
    ("non-standard residue", lambda r: edit_target(r, nonstandard_residue),
     "non-standard residues"),
    ("sequences of differing length", lambda r: edit_target(r, ragged_sequence),
     "differing lengths"),
    ("unexpected column", lambda r: edit_target(r, extra_column),
     "expected exactly"),
    ("non-numeric readout", lambda r: edit_target(r, non_numeric_readout),
     "non-numeric readout"),
    ("seq_len drifted from the data",
     lambda r: edit_reference(r, lambda row: row.update(seq_len="999")),
     "seq_len is 999"),
    ("n_variants drifted from the data",
     lambda r: edit_reference(r, lambda row: row.update(n_variants="999")),
     "n_variants is 999"),
    ("wt_readout drifted from the WT row",
     lambda r: edit_reference(r, lambda row: row.update(wt_readout="12.3")),
     "wt_readout is 12.3"),
    ("reference points at a missing file",
     lambda r: edit_reference(r, lambda row: row.update(filename=TARGET + ".gone")),
     "does not resolve"),
    ("doi is a URL rather than a DOI",
     lambda r: edit_reference(r, lambda row: row.update(doi="https://doi.org/10.1126/sciadv.adr2641")),
     "not a bare DOI"),
    ("required reference field left empty",
     lambda r: edit_reference(r, lambda row: row.update(assay_method="")),
     "assay_method is empty"),
    ("dataset missing from reference.csv", drop_reference_row,
     "no row in reference.csv"),
]


def run_validator(root: str) -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, VALIDATE, "--datasets-dir", root, "--strict"],
        capture_output=True, text=True, encoding="utf-8", cwd=HERE,
    )
    return proc.returncode, proc.stdout + proc.stderr


def main() -> int:
    if not os.path.isdir(DATASETS):
        print("run this from the repository root", file=sys.stderr)
        return 2

    # the real data must pass, otherwise every case below is meaningless
    code, out = run_validator(DATASETS)
    if code != 0:
        print("FAIL  the committed datasets do not validate:\n" + out)
        return 1
    print("pass  committed datasets validate cleanly")

    failures = 0
    for name, corrupt, expected in CASES:
        with tempfile.TemporaryDirectory() as tmp:
            root = os.path.join(tmp, "datasets")
            shutil.copytree(DATASETS, root)
            corrupt(root)
            code, out = run_validator(root)

        if code == 0:
            print(f"FAIL  {name}: validator accepted corrupted data")
            failures += 1
        elif expected not in out:
            print(f"FAIL  {name}: expected {expected!r} in output, got:\n{out}")
            failures += 1
        else:
            print(f"pass  {name}")

    print(f"\n{len(CASES) + 1} check(s), {failures} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
