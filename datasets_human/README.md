# `datasets_human/`

Datasets whose source organism is *Homo sapiens*, held separately from `datasets/`.

The benchmark's focus is cellular non-human organisms — bacteria, archaea, yeast, plants.
Viral proteins are split out the same way, into `datasets_virus/`. Human variant scans are abundant in the 2025 literature and are
perfectly good measurements, but mixing them into `datasets/` would let them dominate a
set meant to be about something else. Keeping them here means a consumer of the benchmark
chooses whether to include them, rather than having to filter by `source_organism` after
the fact.

## Layout

Identical to `datasets/` in every respect — `{Category}/{Property}/{Source}/`, the same
four-column CSV, the same eleven-column `reference.csv` per category. Only the root
differs, and nothing about the format or the curation protocol changes.

The organism deliberately does **not** appear anywhere inside either tree's directory
levels. Those describe *what was measured*, never whose protein it is; that rule is what
keeps the hierarchy scalable, and splitting at the root is what avoids breaking it.

## Validating

`validate.py` takes the dataset root as an argument, so this tree is checked the same way:

```bash
python validate.py                                # datasets/
python validate.py --datasets-dir datasets_human  # this tree
python validate.py --datasets-dir datasets_virus  # viral proteins
```

Both must pass. `papers/` and `original_datasets/` are shared between the two trees and
are not duplicated — the validator resolves a dataset's sources against the repository
root either way.

## What is in here

| Paper | Datasets | Protein |
|---|---|---|
| Estevam 2025, `10.7554/eLife.101882` | 12 | MET receptor tyrosine kinase domain, one dataset per inhibitor plus a DMSO control |
