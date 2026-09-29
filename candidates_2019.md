# 2019 candidate papers

Screening notes for the `2019` branch. Cut from `main`, so it starts from the six Jiang 2024 PRIME
datasets and nothing else.

Part of the **2009–2020 MaveDB enzyme cohort**. The discovery work and the backlog files live on the
`2015` branch (`candidates_2015.md`, `backlog_pre2022.tsv`); this file records only what 2019 yielded.

## Scope — enzymes and enzyme-adjacent

Set on 2026-08-31 on the `2022` branch. Carried here verbatim.

**In scope**: catalysts, and proteins whose measured phenotype is catalytic machinery — nucleases,
polymerases, helicases, ATP-driven transporters.

**Out of scope**: fluorescent proteins, binding domains, ion channels, structural and scaffold
proteins, viral surface glycoproteins.

Src is a tyrosine kinase and the readout is its phosphotransferase activity, so it passes on both
halves. Human, so `datasets_human/`.

## Shipped — 2 datasets, 16,088 variants

### Ahler 2019, Src kinase — 3,714 variants

`10.1016/j.molcel.2019.02.003`, *A Combined Approach Reveals a Regulatory Mechanism Coupling Src's
Kinase Activity, Localization, and Phosphotransferase-Independent Functions*, Mol Cell 2019. From
`urn:mavedb:00000041` (CC0), in `datasets_human/Activity/CatalyticActivity/DMS/`.

This one needed three decisions, all of them caught by checks rather than noticed by eye.

**1. The deposit's target record is wrong for one of its two sets.** MaveDB labels both score sets
`Src catalytic domain`. A pooled label check against that 250-residue target gave `bad = 323`, and no
constant offset fixed it. Split per set, the picture resolves:

| set | region | positions | offset onto P12931 | bad after offset |
|---|---|---|---|---|
| `a-1` | catalytic domain | 1–250 | **+269** (the excerpt is P12931 270–519 verbatim) | 0 |
| `b-1` | SH4 domain | 1–18 | **+1** | 0 |

The SH4 offset is +1 because the initiator Met is cleaved for myristoylation, so the mature protein is
numbered from Gly. The labels imply `GSNKSKPKDASQRRRSLE`, which is P12931 2–19 exactly. Both sets are
renumbered onto **full-length P12931**, which is also the molecule actually assayed.

**2. The readout runs backwards, and the nonsense variants are what show it.** Under the deposit's
`score`, the 152 nonsense variants — a dead kinase — sat **above** the substitutions, median +1.61 and
+1.64 against +0.45 and −0.02. Active Src is growth-inhibitory in yeast, so a growth-derived score is
inverted with respect to activity. The deposit ships `activity_score`, which is exactly `-score` on
all 3,866 rows and puts the nonsense variants below. **`activity_score` is the readout.**

This is the check the `2025` branch's method notes demand after the EnvZ 37 °C arm, whose nonsense
variants also scored above wild type: *"When a source ships an internal control — nonsense variants, an
empty-vector lane, a wild-type row — check them before shipping."* Nothing mechanical would have caught
it; `validate.py` passes either way.

**3. Two sets, one work item.** Same protein, same assay, same quantity, two library regions — which
under Phase 1 is more rows, not more work items. They share **no variant**, so the merge rests entirely
on a control, and here the control holds: the dead-variant anchors agree to **0.033** (−1.606 against
−1.639). The build asserts that agreement rather than assuming it, and refuses to merge if the anchors
drift more than 0.2 apart.

No wild-type row exists in either set, so `wt_readout` is empty.

## Not done

- **The article is not staged in `papers/`.** `PMC6474823` exists but Europe PMC reports the paper as not
  open access.
- **Phase 7 has no re-derived prose number.** The internal checks are the offsets landing at bad = 0, the
  nonsense anchors agreeing across blocks, and the row arithmetic closing at 3,866 = 3,714 + 152.
- The paper's **phosphotransferase-independent** functions, which its title highlights, are not in this
  deposit. If they were measured per variant, they would be a second work item with a different
  property.

## Other 2019 items seen and not taken

From the MaveDB enumeration on the `2015` branch:

- **`10.1016/j.jmb.2019.04.030`** — TEM-1 single amino acid insertions and deletions. **Rejected on the
  format, not on merit**: an indel has no `{WT}{position}{MUT}` form. Recorded on `2015` too.
### Gonzalez 2019, TEM-1 pairwise doubles — CURATED, 12,374 variants

`10.1016/j.jmb.2019.03.020`, *Pervasive Pairwise Intragenic Epistasis among Sequential Mutations in
TEM-1 β-Lactamase*, J Mol Biol 2019. The supplement was fetched by hand on 2026-09-29 from
ScienceDirect and is staged as `Gonzalez 2019-DMS-Journal of Molecular Biology-mmc2.xlsx` (+ `mmc1.docx`).
Dataset in `Activity/DrugResistance/DMS/`.

**Every genotype is a double mutant at two consecutive positions**, joined with `:`. This is the only
file in the repo that is *entirely* pairwise epistasis — 12,374 doubles spanning 281 of the 285
possible consecutive position pairs. Readout is sheet S2's `Double Mutant Fitness`.

Sequence is UniProt P62593 exactly, 286 aa, and all 12,374 wild-type *pairs* verify against it at both
positions. No duplicate genotypes, no rows without a fitness value.

**The Ambler mapping is confirmed a fourth time.** The sheet carries its own Ambler column and gives
the offset as +2 over sequential 1–236, +3 for 237–249, +4 for 250–286 — matching what `2015` derived
from motifs, `2014` read from its deposit's `ambler` column, and `2016` inferred from the ESBL allele
identities.

**`wt_readout` is left empty, deliberately.** There is no wild-type row in S2, and while the scale is
the same band-pass fitness as `Firnberg 2014-DMS-TEM1` on the `2014` branch — whose *measured* wild
type reads **1.0299** — that means wild type is about 1 rather than exactly 1 by definition. Typing
1.0 would assert a definition the assay does not make.

**Phase 7 re-derives both of the abstract's numbers.** It claims "~12,000 pairs of consecutive amino
acid substitutions" and epistasis "for over 8000 mutation pairs": the sheet holds **12,374** pairs and
**8,302** with a computed epistasis value.

**Not extracted, and why.** The `Epistasis` column is a derived difference between the double mutant and
the additive expectation of its two singles, and it has **no higher-is-better orientation** — positive
epistasis is not "better", it is a different shape of interaction — so it cannot be oriented as a
FitnessBench readout. Same for the `Positive`/`Negative Sign Epistasis` flags (17 and 522 rows). The
`Mut 1`/`Mut 2 Fitness` columns are the single-substitution values from the earlier study, already
shipped on `2014`. Sheets S1 and S3 are raw sequencing counts across eleven ampicillin concentrations,
not a per-variant phenotype.

## How this one was reached, for the record

`PMC6502654`, `10.1016/j.jmb.2019.03.020`.

**Why it is worth the trouble.** The abstract reports the fitness effect of **~12,000 pairs of
consecutive amino acid substitutions**, with epistasis computed for **over 8,000 pairs** against the
single-substitution study already curated on the `2014` branch. Same lab, same band-pass selection
system, same TEM-1 wild type — so it joins the `2014` and `2016` datasets directly. Pairwise epistasis
is the thing this benchmark is shortest of: only E4B on `2013`, the four DHFR doubles on `2020` and the
UBE2I BarSeq library on `2017` carry any at all.

**What was tried, and why it stopped.** No MaveDB deposit exists — searched `epistasis`, `pairwise` and
`TEM-1 epistasis`, and none of the 20 matching score sets carries this DOI. Europe PMC reports
`inEPMC: Y` and `hasSuppl: Y`, but its `supplementaryFiles` endpoint returns 296 bytes that are not a
zip and `fullTextXML` returns HTTP 500. That is the trap the `2025` branch's method notes name: Europe
PMC's flags describe its own holdings and licence record, not what it will actually serve. Unpaywall
calls the article **bronze OA** — free at the publisher — but supplies no `url_for_pdf`.

**What is needed**: the article's supplementary tables from ScienceDirect at
<https://doi.org/10.1016/j.jmb.2019.03.020>, dropped into `original_datasets/` under the publisher's
own filenames. Renaming is mine to do. The per-variant table wanted is the one behind the ~12,000
consecutive pairs; the single-mutant study it is compared against is already on `2014` as
`Firnberg 2014-DMS-TEM1-drugresistance-fitness_bandpass_amp.csv`.

## Other 2019 items seen and not taken
