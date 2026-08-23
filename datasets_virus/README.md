# `datasets_virus/`

Datasets whose source organism is a virus, held separately from `datasets/`.

The benchmark's focus is cellular organisms — bacteria, archaea, yeast, plants. Viral
proteins are common engineering scaffolds and common deep-mutational-scanning targets, so
they accumulate quickly; keeping them here means a consumer of the benchmark chooses
whether to include them rather than filtering by `source_organism` afterwards. This is the
same reasoning, and the same layout, as `datasets_human/`.

## Layout

Identical to `datasets/` — `{Category}/{Property}/{Source}/`, the same four-column CSV,
the same eleven-column `reference.csv` per category. Only the root differs.

The organism deliberately does **not** appear in either tree's directory levels. Those
describe *what was measured*, never whose protein it is; splitting at the root is what
keeps that rule intact.

## Validating

```bash
python validate.py                                # datasets/
python validate.py --datasets-dir datasets_human  # human
python validate.py --datasets-dir datasets_virus  # this tree
```

All three must pass. `papers/` and `original_datasets/` are shared across the trees and
are not duplicated — the validator resolves a dataset's sources against the repository
root from any of them.

## What is in here

| Paper | Datasets | Protein | Organism |
|---|---|---|---|
| Huber 2025, `10.1038/s41467-025-60622-7` | 21 | TEV protease — a site-saturation scan plus one dataset per P1′ substrate residue | Tobacco etch virus |
| Jiang 2024, `10.1126/sciadv.adr2641` | 1 | T7 RNA polymerase, thermal stability | *Escherichia* phage T7 |

## One thing to know before merging

The Jiang 2024 T7 RNA polymerase dataset came from `main`, so moving it here **deletes a
line from `datasets/Stability/reference.csv`** that other branches still carry.
`.gitattributes` sets `merge=union` on those files, and a union merge keeps a line one
side deleted — so after merging with a branch that still has it, that row can reappear
while the file it names no longer sits under `datasets/`.

That failure is loud rather than silent: `validate.py` reports `filename does not resolve
to a file`. Run it after the merge, and drop the resurrected row.
