# FitnessBench

A benchmark of experimentally measured protein variant fitness, curated from the
primary literature into a single uniform format.

Every dataset is one CSV with four columns, a reconstructed and verified wild-type
sequence, and a `normalized-score` oriented so that **higher is always better** —
regardless of whether the underlying assay reports a melting temperature, a reaction
rate, or a half-maximal effective concentration.

---

## Repository layout

```
FitnessBench/
├── datasets/
│   ├── Stability/
│   │   ├── reference.csv            # one row per CSV in this category
│   │   ├── ThermalStability/
│   │   ├── AlkalineStability/
│   │   └── ...
│   ├── Activity/
│   │   ├── reference.csv
│   │   ├── CatalyticActivity/
│   │   └── ...
│   ├── Binding/
│   │   ├── reference.csv
│   │   ├── BindingAffinity/
│   │   └── ...
│   └── ...
├── papers/                          # source publications (PDF)
└── original_datasets/               # source supplementary data, unmodified
```

The directory hierarchy is `{Category}/{Property}/{Source}/`. The category and
property levels describe **what was measured**; the protein and the paper live in the
filename, never in the directory name. Naming directories after protein families does
not scale — a new dataset should always have an obvious home.

---

## Dataset format

Each dataset CSV has exactly four columns:

| Column | Description |
|---|---|
| `mutant` | Substitutions in `{WT}{position}{MUT}` form, 1-indexed against `sequence`. Multi-site variants join with `:` (e.g. `S962K:I976L`). The unmutated reference is `WT`. |
| `sequence` | The full variant sequence, with all substitutions applied. |
| `readout` | The experimental measurement, in the units given by `reference.csv`. |
| `normalized-score` | Within-dataset z-score. **Higher is better.** |

Example:

```csv
mutant,sequence,readout,normalized-score
WT,MSKLEKFTNCYSLSKTLRFKAIPVGKT...,41.9,-0.590217
H370K,MSKLEKFTNCYSLSKTLRFKAIPVGKT...,40.7,-0.983943
S962K:I976L,MSKLEKFTNCYSLSKTLRFKAIPVGKT...,45.05,0.443315
```

> **Note on direction.** When a *lower* raw value means better fitness — EC50, IC50,
> Kd, error rates — `readout` stores the inverted value, so it increases with fitness
> like every other dataset. `reference.csv` states exactly what is stored, e.g.
> `1/EC50 (nM^-1)` rather than `EC50 (nM)`.

### Normalization

```
normalized-score = (x - mean(X)) / std(X)
```

A standard z-score over `X`, the `readout` column of that dataset, using the
population standard deviation (as in `scipy.stats.zscore`). No log or other transform
is applied.

Note that the zero point is the dataset mean, not the wild type: `normalized-score > 0`
does *not* mean "better than wild type". For that, compare `readout` against
`wt_readout` in `reference.csv`. Anchoring on the mean is also what lets a dataset with
no wild-type row be normalized like the rest.

### File naming

```
{FirstAuthor} {Year}-{Model or platform}-{Protein}-{Property}-{Readout}.csv
```

e.g. `Jiang 2024-PRIME-LbCas12a-thermalstability-Tm.csv`. The `{Model or platform}`
field identifies the paper's method, not how any individual variant was chosen. Files
in `papers/` and `original_datasets/` share the same prefix, which is what links a
dataset back to its source.

---

## `reference.csv`

One per category, one row per dataset, 11 columns:

| Column | Description |
|---|---|
| `filename` | Path relative to the category directory. Primary key. |
| `protein` | Protein name and a short functional description. |
| `source_organism` | Organism of origin. |
| `seq_len` | Length of the reference sequence. |
| `property` | Property measured. |
| `readout` | What `readout` holds, including units. |
| `wt_readout` | Wild-type value, for "better than WT" comparisons. |
| `assay_method` | Assay, instrument, and conditions. |
| `n_variants` | Number of variants, excluding the WT row. |
| `doi` | Source publication. |
| `remark` | **Only what differs from the source data** — rows dropped and why, values merged, data deliberately left out. Properties inherited unchanged from the source are not repeated here. |

---

## Usage

```python
import pandas as pd
from scipy.stats import spearmanr

ref = pd.read_csv("datasets/Stability/reference.csv")
row = ref[ref.filename.str.contains("LbCas12a")].iloc[0]
df  = pd.read_csv(f"datasets/Stability/{row.filename}")

wt = df[df.mutant == "WT"].sequence.iloc[0]
singles = df[~df.mutant.str.contains(":") & (df.mutant != "WT")]

# scores must be oriented so that higher = better
print(spearmanr(my_model(singles.sequence), singles["normalized-score"]))

# "better than wild type" comes from readout, not normalized-score
print((singles.readout > float(row.wt_readout)).sum())
```

---

## Sources

Datasets arrive two ways, and are recorded identically once here:

- **Curated from a publication's supplementary data**, following `example_workflow.md`.
  `papers/` and `original_datasets/` hold the untouched source.
- **Converted in bulk from a published database.** `scripts/convert_enzengdb.py` imports
  the EnzEngDB record table (*Nucleic Acids Research* 2026, D564). `original_datasets/`
  holds the subset of records each dataset came from; the source publications are
  paywalled and are not redistributed here.

The conversion does not trust EnzEngDB's `variant_aa` column. For part of that table it
disagrees with the row's own mutation labels, because a mutation was applied at the
wrong position — their pipeline flags many of these itself as "position 0 and 1 index
had same AA". Sequences are instead rebuilt by applying the stated labels to the parent,
requiring a single numbering offset to fit *every* label in the dataset. Records that
fail that, that carry indels, or whose repeat measurements disagree by more than 2% are
dropped and counted in `remark`.

Source organism and assay conditions are not in EnzEngDB. They were read out of the
source publications by hand and live in `PUBLICATIONS` in the converter, so a dataset
with no entry there is reported but never written. Where the publication's supporting
information is paywalled, `remark` names the specific conditions that could not be
confirmed rather than leaving the gap silent.

---

## Validation

```bash
python validate.py            # errors fail, warnings are advisory
python validate.py --strict   # warnings fail too
python test_validate.py       # confirm the checks still catch what they claim to
```

`validate.py` is stdlib-only and enforces everything in `example_workflow.md`
mechanically, so a contribution is cheap to trust. It checks, per dataset:

- the four columns, in order; unique `mutant` labels; one sequence length; standard residues only
- **every row against the reference sequence.** Reverting a row's substitutions must
  land on the same sequence for every row — which does not need a `WT` row to exist,
  and catches numbering offsets, substitutions that silently never landed, and a
  residue drifting at a position the row does not mutate
- Hamming distance from WT, computed from the *output* sequence rather than the label
- `normalized-score` reproduced from `readout` to 1e-6 (`sd == 0` means all zeros)

and per `reference.csv`:

- the eleven columns; required fields non-empty; `doi` a bare DOI, not a URL
- `filename` unique and resolving, and no dataset left unlisted (union-merge on this
  file makes both worth checking on every merge)
- `seq_len`, `n_variants` and `wt_readout` re-derived from the CSV, so they cannot drift

`test_validate.py` corrupts a copy of the data twenty different ways and asserts the
validator fails with the right message each time. A check nobody has watched fail is
not evidence of anything.

Two things stay human: whether the readout is the quantity the experiment actually
compares, and re-deriving a number the paper states in prose.

---

## License

Dataset CSVs are derived from the supplementary data of the cited publications;
please cite the original papers. Source PDFs in `papers/` are redistributed under
their publishers' terms.
