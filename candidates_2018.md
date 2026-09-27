# 2018 candidate papers

Screening notes for the `2018` branch. Cut from `main`, so it starts from the six Jiang 2024 PRIME
datasets and nothing else.

Part of the **2009–2020 MaveDB enzyme cohort**. The discovery work and the backlog files live on the
`2015` branch (`candidates_2015.md`, `backlog_pre2022.tsv`); this file records only what 2018 yielded.

## Scope — enzymes and enzyme-adjacent

Set on 2026-08-31 on the `2022` branch. Carried here verbatim.

**In scope**: catalysts, and proteins whose measured phenotype is catalytic machinery — nucleases,
polymerases, helicases, ATP-driven transporters.

**Out of scope**: fluorescent proteins, binding domains, ion channels, structural and scaffold
proteins, viral surface glycoproteins.

PTEN is a lipid phosphatase and the readout is its phosphatase activity, so it passes on both halves.
It is human, so it goes to `datasets_human/`, which this branch opens.

## Shipped — 1 dataset, 7,260 variants

### Mighell 2018, PTEN lipid phosphatase — 7,260 variants

`10.1016/j.ajhg.2018.03.018`, *A Saturation Mutagenesis Approach to Understanding PTEN Lipid
Phosphatase Activity and Genotype-Phenotype Relationships*, Am J Hum Genet 2018. From
`urn:mavedb:00000054` (CC0), in `datasets_human/Activity/CatalyticActivity/DMS/`.

Sequence is UniProt P60484 exactly, 403 aa, `bad = 0` over 7,657 substitutions covering **every one of
positions 1–403**. Nothing rests on provenance alone.

The row accounting, which is the interesting part of this one:

| class | scored | no score | total |
|---|---|---|---|
| substitution | **7,260 kept** | 397 | 7,657 |
| single-residue deletion | 377 | 26 | 403 |
| nonsense | 375 | 28 | 403 |
| synonymous | 0 | 217 | 217 |
| `_wt` | 1 | 0 | 1 |

**All 403 deletions are dropped on the format, not on merit.** An indel has no
`{WT}{position}{MUT}` form. This is the same wall that rejects `10.1016/j.jmb.2019.04.030`, the TEM-1
insertion-and-deletion scan, outright — the difference is only that there deletions were the whole
dataset and here they are a fifth of it.

The wild-type row is the deposit's own `_wt` entry and reads exactly **1**, the score being defined
against wild type.

**The deposit ships more than was used**: a `High_conf` flag and per-replicate columns for two
biological and six technical replicates. The shipped readout is the combined score used as it stands,
with **no confidence filter applied** — filtering on `High_conf` would be a curation decision that
changes which variants exist, so it is left to whoever wants it.

## Not done

- **The article is not staged in `papers/`.** `PMC5986715` exists but Europe PMC reports the paper as not
  open access.
- **Phase 7 has no re-derived prose number.** The abstract's figures are in the text rather than the
  deposit, and the paper is not fetchable here. The checks that ran are internal: the label check over
  all 403 positions, row arithmetic closing exactly at 8,681, and zero duplicate genotypes.
- **A `High_conf`-filtered variant of this dataset** is a legitimate second version if the project ever
  wants one, but it is not a second work item — same measurement, same quantity.

## Other 2018 items seen and not taken

From the MaveDB enumeration on the `2015` branch:

- **`10.1038/s41467-018-03917-2`** — PARP1, 93,047 variants over two dense CRISPR screens. PARP1 is an
  enzyme, but the scores are per-guide rather than per-variant, which is the defect the `2023` branch
  records for base-editor screens: converting them "means assigning genotypes the assay did not
  resolve". Rejected unless a per-variant table surfaces.
- **`10.1038/s41588-018-0204-y`** — TP53. A transcription factor, so out of scope, and the `2024`
  branch already flags its own TP53 datasets as out.
