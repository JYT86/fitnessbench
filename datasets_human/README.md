# datasets_human/

Human protein variant datasets, in a tree of their own.

The benchmark's focus is microbial and other non-human proteins. Human variant scans are abundant
and would come to dominate a set meant to be about something else, so they live in a parallel tree
rather than mixed in. The split is at the root deliberately: the organism must not appear in the
directory levels, which describe what was measured and nothing else, so splitting anywhere below
the root would have broken that rule.

The layout is identical to `datasets/` in every respect --- `{Category}/{Property}/{Source}/`, the
same four-column CSV, the same eleven-column `reference.csv` per category. Only the root differs,
and nothing about the format or the curation protocol changes. `papers/` and `original_datasets/`
are shared with `datasets/`, not duplicated.

Validate it as a first-class tree:

```bash
python validate.py --datasets-dir datasets_human
```

The enzyme scope cuts across this tree rather than being relaxed inside it: a human protein is here
because of its organism, not because the scope was widened for it.

## What is in here

| Paper | Protein | Datasets |
|---|---|---|
| Sun 2020, Genome Med | CBS, cystathionine beta-synthase | 2 (low and high vitamin B6) |
