# 2024 candidate papers

Screening notes for the `2024-WJ` branch.

This file is late. The 2024 sweep shipped 31 papers and ~100 datasets without one, which an audit on
2026-09-25 flagged: with no shortlist there is no record of what was screened and rejected, so the only
surviving evidence of a decision is whatever a `remark` happens to mention. What follows is not a
reconstruction of that sweep — it is the record from here on.

## Repairs, 2026-09-28

The branch had never been validated. `validate.py` lives on `add-validation`, and GitHub Actions runs
the workflow from the branch being pushed, so no year branch was ever checked. The first run reported
**181,598 errors**. After repair it reports **1**.

| What was wrong | Scale | Fix |
|---|---|---|
| `sequence` held the **wild type on every row** in Judge 2024 CTX-M-14 (×2) and Rouleau 2024 PjDHFR (×3) — the substitutions were never applied | 90,788 rows | Each row's own substitutions applied. Deterministic: the labels and their numbering verified against the wild type, so no source re-read was needed. |
| `normalized-score` computed from full-precision `readout` then rounded alongside it, so recomputation missed by up to 8.8e-06 — over the 1e-6 tolerance | 19 datasets | Regenerated from the `readout` on disk. Every one now lands at 5.0e-07, the floor for a six-decimal column. |
| Two Dadonaite spike datasets carried the terminal stop as `*` at position 1250 of every sequence | 13,189 rows | Truncated; `seq_len` 1250 → 1249. |
| `property` read `Haemolysis` against a `Hemolysis/` directory | 1 row | Aligned to the directory. |

`readout` and `mutant` are untouched in all 23 files, verified column by column against the previous
commit. No measurement moved.

**The lesson worth carrying**: none of this was catchable by eye, and all of it was catchable by
`validate.py`. The 19 rounding cases are the [Phase 5] instruction "round the readout before computing
the score" being skipped; the five wild-type-sequence files are Phase 4's substitution loop never
running. Both shipped because nothing ran the checks.

## The one remaining error: Belli 2024

`datasets/Activity/ReceptorActivation/PE/Belli 2024-PE-EGFR-receptoractivation-activation_LFC.csv`
— 1,781 rows, `seq_len` 1210, positions 1–1210 across 942 sites, no `reference.csv` row, no PDF in
`papers/`, no file in `original_datasets/`. It is the only unreferenced dataset in the repo.

**The source is identified.** Belli O, Karava K, Farouni R, Platt RJ, *Multimodal scanning of genetic
variants with base and prime editing*, **`10.1038/s41587-024-02439-1`**, Nature Biotechnology, online
2024-11-12. `PMC12440817`, open access, supplements reachable — the 20 MB bundle downloads cleanly from
Europe PMC. `seq_len` 1210 is EGFR, and all 1,781 labels are real EGFR variants.

**But the per-variant phenotype is not in the paper.** Where the numbers come from, checked sheet by
sheet across all four supplementary workbooks:

- The **variant labels** match `MOESM3 › Supplementary_table_6` — all 1,781 of them. That sheet is the
  **epegRNA library design**: 54,007 pegRNA rows, 2,550 distinct intended AA changes, with spacer, PAM,
  PBS/RTT lengths, barcodes and ClinVar/COSMIC annotations. It has **no phenotype column** — every
  numeric column in it was tested against the shipped `readout` and none matches.
- The **measurements** live in `MOESM4`/`MOESM5`, keyed by **`sgrna`**, ~2,006 guides per sheet, with
  `control_count | treatment_count | LFC | p | FDR`.

So the shipped file joins library-design labels to guide-level measurements. **Every one of the 2,550
variants is designed with more than one pegRNA** — median about six, maximum 120 — so producing one
number per variant required an aggregation that is recorded nowhere, there being no reference row.

That is the defect the `2023` branch already names for base-editor screens: NaV1.2 and DNMT3A "measure
gRNAs, not variants", and converting them "means assigning genotypes the assay did not resolve". It is
also why `10.1038/s41467-018-03917-2` (PARP1, 93,047 variants) was rejected on the `2018` branch.

**Recommendation: delete the file.** Three independent reasons, any one sufficient:

1. **No reference row**, so it is not shipped under the repo's own definition of shipped.
2. **The readout is guide-level**, attributed to genotypes the assay did not individually resolve.
3. **Receptor activation fails the enzyme scope on the readout half.** EGFR is a kinase, but activation
   reports signalling rather than catalysis — the same test that excludes a surface-display level.

It is left in place pending that decision rather than removed unilaterally.

## Scope

The enzyme scope was set on 2026-08-31; this sweep ran 2026-09-09 to 09-16, after that date but from a
skill file that did not yet carry it as a Phase 1 gate. **Roughly 45 of 107 datasets are outside it** —
viral surface glycoproteins (Dadonaite, Lei, Desautels, Langedijk), binding domains and minibinders
(Faure GRB2-SH3, Huang, Jiang VHH, Lv, Chen P, Freschlin GB1), a fluorescent sensor (Wait jGCaMP7s),
capsid and scaffold proteins (Raguram), and non-catalytic peptides (Randall PG1, Gould TP53, Liu
Salivaricin B, Ding ParD3).

Following `2023`'s precedent in `319ec4e`: **nothing is removed.** Every dataset here is verified and
validates cleanly; the scope is a decision about what to curate next, not a judgment on work already
done. But a reviewer should know which rows predate it, and no future sweep should read them as
precedent.
