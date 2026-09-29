# 2020 candidate papers

Screening notes for the `2020` branch. Cut from `main`, as `2015` and `2022`–`2026` were, so it
starts from the six Jiang 2024 PRIME datasets and nothing else.

Part of the **2009–2020 MaveDB enzyme cohort**, which no branch covered until now. The discovery
work, the full enumeration and the two backlog files live on the `2015` branch
(`candidates_2015.md`, `backlog_pre2022.tsv`); this file records only what 2020 itself yielded.

## Scope — enzymes and enzyme-adjacent

Set on 2026-08-31 on the `2022` branch. Carried here verbatim.

**In scope**: catalysts, and proteins whose measured phenotype is catalytic machinery — nucleases,
polymerases, helicases, ATP-driven transporters.

**Out of scope**: fluorescent proteins, binding domains, ion channels, structural and scaffold
proteins, viral surface glycoproteins.

## Shipped — 16 datasets, 65,622 variants

### Chen 2020, VIM-2 metallo-β-lactamase — 9 datasets, 45,213 variants

`10.7554/eLife.56707`, from `urn:mavedb:00000073` (CC0). Nine conditions on one wild type:
ampicillin at 2, 16 and 128 µg/mL crossed with 25 and 37 °C, cefotaxime at 0.5 and 4 µg/mL, and
meropenem at 0.031 µg/mL at 37 °C. `Activity/DrugResistance/DMS/`.

**This is the table the `2024` branch recorded as unobtainable.** Its Chen J 2024 remark says the
VIM-2 scan "was published previously (refs 5 and 50) and whose per-variant table this paper does not
carry" — same first author, and the table was CC0 in MaveDB the whole time.

The construct is UniProt Q5U7L7 plus one Gly after the initiator Met, which the methods say creates
an NcoI cloning site, so positions run **+1 from native VIM-2 numbering** from residue 2 on. It also
carries I at construct 186 where all ten deposited VIM-2 references have V — an allele difference,
not an engineered one.

The +1 offset is corroborated six times by chemistry rather than by alignment: the subclass B1 zinc
ligands H114, H116, D118, H179, C198 and H240 all land at construct +1 exactly, and variants at
those sites have median fitness **−7.685 against −2.231** overall at 128 µg/mL ampicillin.

Signal-peptide mutations (construct 2–27) come out at median **+0.105** against **−2.726** for the
mature enzyme — the asymmetry the paper included the signal peptide in order to measure.

### Thompson 2020, *E. coli* DHFR — 2 datasets, 4,894 variants

`10.7554/eLife.53476`, from `urn:mavedb:00000063` (CC0). Two hosts, one with a functioning Lon
protease and one deficient in it. Opens `Fitness/GrowthFitness/DMS/` on this branch.

Sequence matches UniProt P0ABQ4 exactly with bad = 0 over 3,008 substitutions covering **all 159
positions**, so nothing rests on provenance alone. Catalytic Asp27 is at position 27 and the four
positions the deposit's doubles use — F31, M42, L54, G121 — are the canonical trimethoprim sites.

About a fifth of each file is dropped and the remarks say so: 615 and 481 substitutions carry no
score, and 153 and 158 nonsense rows go.

**The four double mutants are the only epistasis in the set and it is real.** Recomputed from the
shipped files: L54I:G121V observed −2.938 against an additive −2.075, F31Y:L54I −2.468 against
−0.619, so between −0.08 and −1.85 per pair.

Across the 2,271 variants measured in both hosts the conditions correlate at r = 0.808, and the
Lon-deficient host is the more permissive, median −0.017 against −0.122 — the paper's own claim.

### Sun 2020, human CBS — 2 datasets, 14,208 variants → `datasets_human/`

`10.1186/s13073-020-0711-1`, from `urn:mavedb:00000005` (CC0). Yeast *cys4Δ* complementation at low
and high vitamin B6, reading out B6 remediability. Opens `datasets_human/` on this branch.

Sequence is identical to UniProt P35520, 551 aa, bad = 0 over 7,451 substitutions across positions
2–551. The **raw** score sets are used; the four imputed-and-refined sets covering the same two
conditions are not curated, imputed values being computed rather than measured.

Two collapses, both diagnosed before being made. ~2,300 rows per condition are the same protein
variant reached by different codons, with spread **exactly zero** in every group — the deposit
reports one protein-level score and repeats it per codon route — so averaging is lossless and the
build asserts that zero rather than assuming it. The ~500 synonymous rows are the wild-type protein
and collapse to one WT row at 0.978 and 0.983, the scores being normalised so wild type reads ≈ 1.

The article is open access but neither Europe PMC's `fullTextPDF` route nor the publisher's
`counter/pdf` link returns a PDF to an automated request, so it is not staged in `papers/`.

### Chiasson 2020, VKOR — CURATED, 2 datasets in two categories

`10.7554/eLife.58026`, from `urn:mavedb:00000078` (CC0). Vitamin K epoxide reductase measured two ways:
carboxylation activity by FACS on a carboxylation-specific antibody (**697 variants** →
`datasets_human/Activity/CatalyticActivity/`) and steady-state abundance by VAMP-seq (**2,695** →
`datasets_human/Stability/FoldingStability/`). Two work items, not two readouts of one, because the
property differs.

Sequence is UniProt Q9BQB6 exactly, 163 aa, `bad = 0` over 2,827 substitutions across positions 2–163.
Each dataset keeps a WT row collapsed from its synonymous rows, landing at 0.842 and 0.953 on scales
normalised so wild type reads about 1.

The activity arm ships **exactly 697** variants, which is the number of missense mutations the
deposit's own methods state the library contains — a stated number re-derived from the finished file.

## Decided against at 2020

| Item | URN / DOI | Decision |
|---|---|---|
| **HMGCR** | `urn:mavedb:00000035-a` | **Rejected.** All three sets — no statin, rosuvastatin, atorvastatin, 18,448 each — are "imputed and refined". There is no raw version in the deposit, and Phase 1 excludes computed columns, so an imputed score set is not a weak dataset but a different kind of thing. Reopen only if the authors deposit the measured scores. |
### Sirr 2020, PSAT1 — CURATED, 1,915 variants → `datasets_human/`, under CC BY-NC-SA 4.0

`10.1002/jimd.12227`, *A yeast-based complementation assay elucidates the functional impact of 200
missense variants in human PSAT1*, J Inherit Metab Dis 2020. From `urn:mavedb:00000107`, in
`datasets_human/Fitness/GrowthFitness/DMS/`.

**This is the only dataset in the cohort that is not CC0**, and the licence terms are recorded first in
its `remark` and in full in [`DATA_LICENSES.md`](DATA_LICENSES.md): attribution to the authors and to
the MaveDB URN, no commercial use, and ShareAlike on any adaptation. Shipping it beside CC0 data is
sound because the repository is a *collection* — each dataset under its own terms — which is
aggregation rather than adaptation. What would change that is anything merging them into one derived
work.

Sequence is UniProt Q9Y617 exactly, 370 aa, `bad = 0`.

**The deposit's two score sets are joined into one dataset.** They are the same assay measuring the
same quantity on overlapping libraries — a 200-variant solid-growth panel and a 1,914-variant
SNV-accessible scan. 196 variants are measured in both, and **no value is identical between them**, so
they are independent measurements rather than a reupload. They are averaged, and the agreement is the
only empirical check the merge gets: **Pearson r = 0.9708**, worst disagreement 0.256.

3 frameshift rows are dropped — an indel has no `{WT}{position}{MUT}` form. Neither set carries a
wild-type or synonymous row, so `wt_readout` is empty, though the scale is one on which wild type reads
about 1.

## Method note

MaveDB's `POST /score-sets/search` caps at 100 results and ignores `limit`/`offset`, so a score set
that a keyword search cannot reach is still fetchable directly at
`GET /score-sets/{urn}` with the URN percent-encoded. Both the DHFR and CBS sets here were invisible
to a text search for their own protein name and had to be fetched that way.

Two article PDFs came from the **eLife CDN** (`cdn.elifesciences.org/articles/{id}/elife-{id}-v2.pdf`)
after Europe PMC's `?pdf=render` returned 403 and its `fullTextPDF` route 404'd. Worth trying first
for any eLife paper.
