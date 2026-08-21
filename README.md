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
├── original_datasets/               # source supplementary data, unmodified
└── skill/
    └── fitnessbench-digger/         # the curation workflow, as a Claude Code skill
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

## Curation

New datasets are curated with the **`fitnessbench-digger`** skill, kept in this repo at
[`skill/fitnessbench-digger/SKILL.md`](skill/fitnessbench-digger/SKILL.md). It is the
authoritative description of the process: locating the real source data, extracting tables
from supplementary PDFs, establishing the wild-type sequence and its residue numbering,
assembling variants, orienting and normalizing the readout, and writing the dataset CSV
together with its `reference.csv` row under gated validation checks.

To use it with Claude Code, make it visible as a skill:

```bash
mkdir -p ~/.claude/skills
ln -s "$PWD/skill/fitnessbench-digger" ~/.claude/skills/fitnessbench-digger
```

Then point it at a paper. The argument is free text — a DOI, an article URL, or a local
path all work, and it resolves whichever you give it:

```
# by DOI
/fitnessbench-digger 10.1126/sciadv.adr2641

# by article URL
/fitnessbench-digger https://www.science.org/doi/10.1126/sciadv.adr2641

# by path to a PDF already in the repo
/fitnessbench-digger papers/Jiang 2024-PRIME-Science.pdf

# by path to a PDF anywhere on disk — it reads the front matter for the DOI
/fitnessbench-digger ~/Downloads/gkaf1142.pdf

# narrow the scope up front, instead of picking from the Phase 1 candidate list
/fitnessbench-digger 10.1126/sciadv.adr2641 — only the LbCas12a and T7RNAP Tm data

# audit an existing dataset instead of adding one (skips to Phase 7)
/fitnessbench-digger audit datasets/Stability/ThermalStability/PRIME/Jiang 2024-PRIME-LbCas12a-thermalstability-Tm.csv
```

Invoked with no argument at all, it asks which paper you mean and stops — it will not
guess from what is already in `datasets/`.

Anything that changes about the format described above should be changed in the skill as
well — the skill is what actually produces the files.

---

## License

Dataset CSVs are derived from the supplementary data of the cited publications;
please cite the original papers. Source PDFs in `papers/` are redistributed under
their publishers' terms.
