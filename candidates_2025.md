# 2025 candidate papers

Screening notes for the `2025` branch — papers published in 2025 that may yield
FitnessBench datasets. Nothing here is curated yet; this is the shortlist that
step 1 of `example_workflow.md` should start from.

## Where these came from

**First sweep.** Two nature.com searches, both restricted to `date_range=2025-2025`,
ordered by relevance:

- `machine learning guided enzyme engineering in prokaryotes` — **6 results**
- `machine learning guided enzyme engineering in eukaryotes` — **16 results**

20 unique articles, 22 hits (2 appear in both).

**Second sweep.** The same query with the organism clause dropped —
`machine learning guided enzyme engineering` — which is a superset of the first two.
nature.com was rate-limited at the time, returning its 3 KB `Client Challenge` page, so
the sweep ran against Europe PMC over the same corpus restricted to Nature-family
journals and 2025: **481 hits, top 100 screened by relevance**. Europe PMC ranks
differently from nature.com, so this list is not the site's own ordering and is worth
re-running against the site itself.

Everything is screened on title, abstract and data-availability statement. Supplementary
files have **not** been opened for anything still marked as a candidate, so variant
counts are the papers' own claims rather than verified sheet contents.

## Shortlist from the first sweep — all three curated

All three are on the `2025` branch: 31 datasets, 387,910 variants, validator clean.


### 1. Zhang 2025 — PylRS, machine-learning-guided evolution
*Machine learning-guided evolution of pyrrolysyl-tRNA synthetase for improved
incorporation efficiency of diverse noncanonical amino acids*
Nature Communications, 2025-07-19 · `10.1038/s41467-025-61952-2`

- **Protein** pyrrolysyl-tRNA synthetase (PylRS) tRNA-binding domain; archaeal/bacterial origin, expressed in *E. coli*
- **Model/platform** FFT-PLSR, with mutation sites nominated by ESM-1v, MutCompute and ProRefiner
- **Readout** stop-codon suppression (SCS) efficiency, reported as fold-change vs parent; also `kcat/Km(tRNA)` for a few variants
- **Scale** several hundred variants characterised in tranches — 38 single/double/triple in the first training set, 44 MutCompute singles, 92 combinatorial doubles, plus top-20 prediction rounds
- **Data** Supplementary Data + Source Data `.xlsx`; enzyme data also as EnzymeML JSON at `github.com/zjuhaoran/FPFORCOM` and Zenodo
- **Home** `Activity/CatalyticActivity/`
- **Watch for** the readout is normalised to a parent that changes between rounds (WT → Com1-IFRS). Rounds with different parents are different datasets, not one.

### 2. Huber 2025 — protease specificity, DNA-recording + epistasis-aware ML
*Data-driven protease engineering by DNA-recording and epistasis-aware machine learning*
Nature Communications, 2025-07-01 · `10.1038/s41467-025-60622-7`

- **Protein** engineered proteases profiled in *E. coli*
- **Model/platform** ProtRec DNA recorder + epistasis-aware deep learning (MLDEEP)
- **Readout** per-pair activity from the DNA recorder; 29,716 protease variants against up to 134 substrates, ~600,000 protease–substrate pairs
- **Data** Supplementary `.xlsx` + Source Data; processed data CC-BY-4.0 at `github.com/JeschekLab/ProtRec` and `github.com/BorgwardtLab/MLDEEP`
- **Home** `Activity/CatalyticActivity/`, and `Selectivity/` for on- vs off-target
- **Watch for** by far the largest of the three, and the only one that needs a decision before curation: one `(protein, readout)` pair means **one substrate per CSV**, so pick the substrates the paper itself analyses rather than emitting 134 files.

### 3. Duan 2025 — RNA Pol II trigger loop deep mutational scan
*Widespread epistasis shapes RNA polymerase II active site function and evolution*
Nature Communications, 2025-08-27 · `10.1038/s41467-025-63304-6`

- **Protein** RNA polymerase II Rpb1 trigger loop, *Saccharomyces cerevisiae*
- **Model/platform** deep mutational scanning; modelling is logistic-regression GOF/LOF classification, not ML-guided design
- **Readout** growth fitness per variant across selective conditions (SC-Leu+MPA, SC-Lys, YPRafGal)
- **Scale** 15,174 variants designed in ten libraries; 620 single mutants, 7,276 double mutants passing the reproducibility filter
- **Data** Supplementary `.xlsx` + Source Data; processed counts and fitness at `github.com/Kaplan-Lab-Pitt/TLs_Screening` and Zenodo `10.5281/zenodo.16370006`
- **Home** `Activity/` (growth fitness) — needs a property name; `GrowthFitness` if we take it
- **Watch for** the only eukaryotic-host dataset of the three, and the cleanest large fitness landscape. Not ML-guided, so take it only if the benchmark wants DMS landscapes as well as engineering campaigns — worth asking Yutong.

## Second sweep — new candidates

Nothing here is curated yet except Landwehr, which shipped. All five originally in Tier A are open access with per-variant data
confirmed from the data-availability statement, and all are small — a thousand-variant
enzyme is a few MB, not the tens of MB Duan cost.

### Tier A

| # | Paper | DOI | What it holds | Where the data is |
|---|---|---|---|---|
| 1 | Landwehr 2025, *Accelerated enzyme engineering by machine-learning guided cell-free expression* | `10.1038/s41467-024-55399-0` | 1,217 amide synthetase variants across 10,953 reactions, variants optimised for 9 pharmaceuticals | Source Data + `github.com/grantlandwehr/accelerated-enzyme-engineering`; protein **and DNA sequences for every enzyme are in the SI**, so Phase 3 is a stated sequence |
| 2 | Yang 2025, *Active learning-assisted directed evolution* (ALDE) | `10.1038/s41467-025-55987-8` | five epistatic active-site residues, three wet-lab rounds, 12% → 93% yield on a non-native cyclopropanation | `github.com/jsunn-y/ALDE` + Zenodo `12196802` |
| 4 | Zhao lab 2025, *AI-powered autonomous enzyme engineering* | `10.1038/s41467-025-61209-y` | AtHMT (90-fold substrate preference) and YmPhytase | Supplementary Data 3 and 4, named explicitly as the mutant screening data |
| 5 | *Integrating protein language models and automatic biofoundry* | `10.1038/s41467-025-56751-8` | tRNA synthetase, four rounds x 96 ESM-2-nominated variants, activity up 2.4-fold | within the paper and its supplementary files |

Two of these carry public benchmark data that is **out of scope** and must not be
curated under their name: ALDE simulates on GB1 and others, and the biofoundry paper
uses GB1, UBC9 and ubiquitin. Those belong to whoever measured them.

### Worked and rejected

**iCASE 2025**, *Tailoring industrial enzymes for thermostability and activity*,
`10.1038/s41467-025-55944-5` — **rejected, no work item reaches 20 variants.** Taken
through Phase 0 and 1 on the strength of its six enzymes and two properties, which
looked like the largest yield of any candidate. The Source Data workbook has 63 sheets
and every one whose first column carries mutant labels holds **at most 16 rows**:
PG 14 variants for both specific activity and melting temperature, PES-H1 15, and the
XY, GADA, MTGase and laccase panels 6 to 7 each. The large sheets are simulation output
— DSI values, compressibility, binding free energies — which is not an experimental
measurement and is `no` on separate grounds.

The paper's strength is the computational strategy; it validates with small targeted
mutant sets rather than screens, which is exactly what the 20-variant floor exists to
catch. Nothing from it ships, so there is no `remark` anywhere to record this in — hence
the note here.

### Tier B — worked

- `10.1038/s41586-025-09021-y` — **PAMmla**, *Nature*. **Curated**: 64 datasets, 1,078
  SpCas9 variants each. The article is paywalled and returns HTML in place of a PDF, but
  the supplementary tables are open, which is all the readouts needed.
- `10.1038/s41929-025-01436-0` — artificial metathase, *Nature Catalysis*. **Rejected, no
  variant table.** Ships one spreadsheet per figure; every sheet holds between 4 and 38
  non-empty rows of kinetics and titration data, and none is a per-variant list.
- `10.1038/s41467-025-63802-7` — Kemp eliminase distal mutations. **Rejected, no variant
  table.** Four sheets of kinetic traces and stopped-flow raw data, no mutant-labelled
  block anywhere in the source data.

### Maybes — worked

- **Alamos 2025**, ENTRAP-seq, `10.1038/s41587-025-02880-w` — **curated.** Table S3 holds
  243 single substitutions of the CONSTANS activation domain with enrichment ratios; the
  1,495-virus and Arabidopsis tile libraries are fragments of thousands of unrelated
  proteins and are not variants of one wild type, so they are out of scope.
- **Wong 2025**, PglB glycosylation, `10.1038/s41467-025-60526-6` — **not curated, and
  the reason is a search limit rather than a proven absence.** Supplementary Data 1
  enumerates the mutant OST constructs, 14 saturated positions with roughly 19
  substitutions each, but I could not locate a per-variant activity table for them: the
  four Source Data workbooks hold per-figure panels and three sheets of ~345,000 rows
  that are sequencing or mass-spectrometry output, and the PglB screen is not obviously
  among them. Worth one more look by someone with the paper open before it is written
  off.

### Tier B — original notes

- `10.1038/s41586-025-09021-y` — **PAMmla**, *Nature*. ~1,000 engineered SpCas9 enzymes
  characterised for PAM specificity. Good shape, but the only one of these **not** open
  access in PMC, so retrieval may need a hand-off.
- `10.1038/s41929-025-01436-0` — artificial metathase, *Nature Catalysis*. De novo design
  plus directed evolution; variant count unknown and possibly under the 20 floor.
- `10.1038/s41467-025-63802-7` — distal mutations in three de novo Kemp eliminases;
  likely a handful of mutants each.

### Rejected from the second sweep

The bulk of the 481 hits are **prediction tools trained and evaluated on other people's
data** — CatPred, CataPro, TopEC, PreMode, DeepMVP, ABACUS-T, LassoESM, the
cross-attention specificity GNN, the biophysics-based protein language models. Phase 1
of the skill rules these out by name: a dataset a paper merely evaluates on belongs to
the publication that measured it. Also rejected: `10.1038/s41586-025-09298-z` (AI-designed
editors are not variants of one wild type) and the reviews — *Machine learning applied to
biocatalysis research*, the PET hydrolase standardisation guidelines, the C1 utilisation
review.

## Third sweep — past Springer Nature

The first two sweeps only ever saw Springer Nature journals, and both queried "enzyme
engineering", which misses papers that never use the phrase. Widening on both axes at
once, via Europe PMC across all publishers:

`("deep mutational scanning" OR "deep mutational scan" OR "variant effect map" OR
"massively parallel mutagenesis" OR "site-saturation mutagenesis")`, 2025, open access —
**544 hits**, against 481 for the enzyme-engineering query and 20 for the original pair.

The journal spread is the point: PNAS, eLife, JBC, Cell Genomics, Cell Reports, ACS
Central Science, Science Advances, J Virol, Angew Chem. Nature Communications is the
single largest source at 18 of the first 100, but it is a minority.

### Curated from this sweep

**Estevam 2025**, *Mapping kinase domain resistance mechanisms for the MET receptor
tyrosine kinase via deep mutational scanning*, eLife, `10.7554/eLife.101882` — 12
datasets, roughly 3,600 to 3,950 variants each, one per inhibitor plus the DMSO control.
Data on GitHub at `fraser-lab/MET_kinase_Inhibitor_DMS`.

### Chased from the shortlist, and what happened

| Paper | DOI | Outcome |
|---|---|---|
| DMS in *E. coli* periplasm | `10.1073/pnas.2516165122` | **Checked, deprioritized.** The "protein of interest" is human Aβ42, and the readout is amyloid aggregation propensity via a bacterial reporter (TPBLA), not an enzyme fitness — the assay host is bacterial, the protein is not. Human, so `datasets_human/` if ever built. |
| Reshaping a glycoside hydrolase active site | `10.1021/acscentsci.5c01227` | **Checked, rejected.** A 330,000-clone droplet-microfluidics library was screened, but only a handful of named winners (M1, M2, ...) are individually characterised with a quantitative readout; no systematic per-variant table exists in the paper or its PDF-only supplement. |

### Shortlist, chased to completion

| Paper | DOI | Outcome |
|---|---|---|
| Deep mutational scanning of the multi-domain phosphatase SHP2 | `10.1038/s41467-025-60641-4` | **curated** — see below, 2 datasets, 16,181 variants |
| Deep Mutational Scanning of FDX1 | `10.1038/s41467-025-67869-0` | **rejected.** Data availability names a FigShare repository, but it holds only raw Enrich2-style per-sample counts (2.1 GB of intermediates) — recovering per-variant scores means reimplementing the authors' analysis pipeline, not reading a table. The paper's own Source Data has only anonymized score *distributions* (no genotype column) and position-*averaged* values, neither of which gives a per-variant readout. |
| EGFR resistance to 4th-generation TKIs | `10.1038/s41698-025-01086-2` | **rejected.** Same shape as MET (Ba/F3, saturation library, ~17,000 variants) but without that paper's GitHub deposit: Data availability names only raw sequencing reads at GEO, and the 12-page PDF-only supplement holds figures and free-energy-perturbation calculations for a handful of representative isoforms, not a per-variant table. |
| Glucokinase variant characterization | `10.3390/ijms27010156` | **rejected.** 25 individually chosen clinical variants, well under the floor — not a saturation library, despite citing that "deep mutational scanning datasets for GCK" exist elsewhere (an earlier paper, not this one, not chased). |

### Sherekar 2025 ... correction, Jiang 2025 — SHP2 phosphatase

*Deep mutational scanning of the multi-domain phosphatase SHP2 reveals mechanisms of
regulation and pathogenicity*, Nature Communications, `10.1038/s41467-025-60641-4`.

Two datasets, both `datasets_human/Activity/CatalyticActivity/DMS/`: full-length SHP2
(10,899 variants) and its isolated PTP domain expressed as a separate truncated construct
(5,282 variants, renumbered to the construct's own 1-indexed start). A yeast
growth-rescue assay, enrichment relative to wild type. The real per-variant table was in
the article's own Source Data (`Fig 2b/2c column` sheets) rather than the three files the
paper itself labels "Supplementary Data" — those turned out to be library-design oligo
pools, WT-only kinetics, and a 595-row clinical cross-reference of this same data. Worth
remembering: a paper's own "Supplementary Data N" numbering is not a reliable signal for
where the primary result lives; check Source Data regardless.

### Also checked this round, all rejected

Found through a broader PNAS/Cell Press pass while chasing the above, none surviving:

| Paper | DOI | Why rejected |
|---|---|---|
| Directed evolution of a beta-lactamase (conformational states) | `10.1002/pro.70322` | 3 successive mutants + WT, well under the floor |
| Deep structure-function analysis of Mus81 with dominant mutational scanning | `10.1073/pnas.2506043122` | deposited data is a binary Y/N hit classification (dominant / fails-to-complement), not a quantitative per-variant score; the underlying graded growth-sensitivity data was not deposited |
| Pyranose oxidase oligomerization engineering | `10.1111/febs.70004` | Zenodo deposit is models/docking scores only; experimental data "available upon request" |
| Isophthalate dioxygenase engineering | `10.1128/jb.00221-25` | no data-availability statement found |
| Confocal absorbance-activated droplet sorting (cAADS) | `10.1002/advs.202505324` | "available from the corresponding author upon reasonable request" |
| Directed evolution of a plant Rubisco chaperone | `10.1073/pnas.2510701122` | PDF-only SI; text says "selected" variants, not a full library table |
| In vivo directed evolution of an ultrafast Rubisco | `10.1073/pnas.2505083122` | kinetic characterisation covers only ~7 named substitutions; the 292-row dataset is population allele-frequency trajectories per locus, not per-clone fitness |
| Directed evolution of a covalent RNA-labeling tag | `10.1073/pnas.2422085122` | PDF-only SI |
| Nanobody-antigen interface optimisation | `10.1073/pnas.2426438122` | PDF-only SI |

Beyond these, the sweep is full of antibody-escape and human disease-variant scans —
spike, EGFR, MC4R, P2RY8, THAP1. That scope question is now settled: **the benchmark
prefers bacterial, archaeal, yeast, plant and viral proteins**, and human datasets are
kept apart in `datasets_human/` rather than mixed into `datasets/`. They are good
measurements and the format holds them, but they are abundant enough in the 2025
literature to swamp a set meant to be about something else.

Viral proteins are split the same way, into `datasets_virus/`. The benchmark's focus is
cellular non-human organisms — bacteria, archaea, yeast, plants — and viral scaffolds and
escape scans accumulate fast enough to crowd that out. So the tree a dataset lands in is:

| Source organism | Tree |
|---|---|
| bacteria, archaea, yeast, plants | `datasets/` |
| viruses, including bacteriophage | `datasets_virus/` |
| *Homo sapiens* | `datasets_human/` |

Two consequences for screening. Human and viral scans drop below cellular non-human ones
in priority rather than being rejected — EGFR resistance in the shortlist above is the
clearest example, being the human analogue of a study already curated, and the sweep's
spike and antibody-escape papers are the viral case. And `source_organism` is worth
reading at Phase 1, not at Phase 6: it decides which tree a dataset lands in, so it is
cheaper to know before the work than after.

### Still missing

Neither this sweep nor the earlier ones reach **bioRxiv** at scale, or the directed
evolution literature that describes itself as neither "enzyme engineering" nor "deep
mutational scanning". A fourth axis — "fitness landscape", "epistasis", "combinatorial
library" — would likely surface a further tranche.

## Fourth sweep — ACS journals

Both direct access and a title-then-abstract screen through Europe PMC, restricted to
ACS Catal, ACS Cent Sci, ACS Synth Biol, JACS and Biochemistry, 2025, open access.

**Curated:**

- **Wysocki 2025**, *High-Throughput Detection of Cyanobacterial Form I Rubisco
  Assembly*, ACS Synth Biol, `10.1021/acssynbio.5c00591` — 2 datasets, 6608 variants each,
  a phage-selection site-saturation library on RbcL (Halothiobacillus neapolitanus).
  Wild type is a real measurement rather than synthesized, and a fitness of exactly 0 is
  an explicit censoring sentinel covering up to 79% of one condition — read the remark
  before using this one.
- **Thornton 2025**, *Cell-Free Protein Synthesis as a Method to Rapidly Screen
  Machine Learning-Generated Protease Variants*, ACS Synth Biol,
  `10.1021/acssynbio.5c00062` — 2 datasets, 48 variants each, on Con1, a designed
  consensus potyviral protease rather than a natural sequence. Filed under
  `datasets_virus/`. Its supplement's `?pdf=render` route on europepmc.org is the one
  that worked when `fullTextXML` 404'd — worth trying first if that happens again.

**Rejected, no per-variant table:** PET hydrolases from natural diversity (a homolog
panel of ~400 distinct natural sequences, no shared wild type — same shape as the
Cas12a-orthologs rejection from the first sweep); the KdcA directed-evolution paper, the
DyP peroxidase thermostability paper, and the SPOT-library metallopeptide paper all ship
only a PDF supplement with no spreadsheet, and each reports a small number of named
variants (an 8-mutation final construct, a handful of recombinants) well under the floor
— PDF table extraction was not attempted given the likely yield.

**Access notes for this venue.** ACS blocks direct article and supplement access outright
(403 on both), so everything here came through Europe PMC. Two distinct routes were
needed across two papers: `supplementaryFiles` plus `fullTextXML` worked for Wysocki;
Thornton's `fullTextXML` 404'd and needed the `europepmc.org/articles/<pmcid>?pdf=render`
fallback instead. Try `fullTextXML` first, fall back to `?pdf=render` on a 404.

**Why the other four ACS candidates failed, precisely.** Not access — all four were
reachable. Each failed for a different reason, and the four together are most of the
failure modes this format runs into:

| Paper | Failure |
|---|---|
| PET hydrolases from natural diversity | homolog panel — ~400 distinct natural sequences, no shared wild type |
| KdcA directed evolution | PDF-only supplement, and the text names one 8-substitution final variant, not a library table |
| DyP peroxidase thermostability | PDF-only supplement, a handful of designed variants |
| SPOT metallopeptide library | PDF-only supplement, small named set |

None of the last three ship a spreadsheet at all — PDF table extraction was not
attempted given the likely yield (a handful of named variants each, from the abstracts).
Worth revisiting with actual extraction if the floor-check-from-abstract heuristic turns
out to be wrong.

## Fifth sweep — PNAS

Title-matched (protein/enzyme engineering terms, 30 hits) and abstract-matched
(landscape/library terms, 11 hits), 2025, open access, 41 unique papers.

Four credible candidates chased to their supplementary data, all rejected on the same
pattern seen elsewhere: a directed-evolution campaign that samples a large space but
individually characterises only a handful of final hits, rather than reporting a
systematic per-variant table.

| Paper | DOI | Why rejected |
|---|---|---|
| Directed evolution of a plant Rubisco chaperone | `10.1073/pnas.2510701122` | PDF-only SI; text says "selected" variants, not a full library table |
| In vivo directed evolution of an ultrafast Rubisco | `10.1073/pnas.2505083122` | four data files, but the kinetic characterisation covers only ~7 named substitutions; Dataset S2's 292 rows are population-level allele-frequency trajectories per locus across evolution rounds, not per-clone genotype-fitness pairs |
| Directed evolution of a covalent RNA-labeling tag | `10.1073/pnas.2422085122` | PDF-only SI |
| Nanobody-antigen interface optimisation | `10.1073/pnas.2426438122` | PDF-only SI; phage display down to a small validated set |

Nothing else in either sweep was both non-review and non-human-disease-focused enough to
be worth a floor-check — the abstract-matched set in particular was almost entirely
antibody/epistasis/prediction-tool papers already excluded on the same grounds as the
first Nature sweep.

## Sixth sweep — Cell Press

Broadened past `Cell Reports` and `Cell Genomics` to the full family (`Cell`, `Molecular
Cell`, `Cell Chemical Biology`, `Cell Systems`, `Structure`, `Cell Host & Microbe`,
`Immunity`, `Current Biology`, `Chem`, `iScience`, `Cell Reports Methods`, `Cell Reports
Physical Science`). Title-matched: 43 hits, almost entirely clinical-ML `iScience`
papers with no connection to protein engineering.

**Curated:** Teo 2025, *Probing the functional constraints of influenza A virus NEP by
deep mutational scanning*, Cell Reports, `10.1016/j.celrep.2024.115196` — found by title
sweep alone; it never uses the phrase "deep mutational scanning" prominently enough to
surface in an abstract-text query, which is worth remembering when a title sweep and an
abstract sweep disagree. 1894 variants of influenza NEP (A/WSN/1933 strain). The
processed fitness table was not in the article's own supplement — Cell Press's STAR
Methods convention points to a **Zenodo deposit of the analysis repository**
(`10.5281/zenodo.14291492`) instead, which held the real per-variant CSV where the
article and PMC supplement held only scripts and figure sources. Worth checking Zenodo
whenever a Cell Press paper's Data Availability section names one, even when the article
supplement looks complete.

Two more from this sweep, not chased further: F. rodentium Cas9 (structural/cryo-EM
paper, likely a handful of validated point mutants, no data-availability statement
found) and the ODM protein-design pipeline (generative-model paper, likely benchmarks on
public data per the Phase 1 exclusion for evaluated-on datasets).

## Checked against ProteinGym

Asked whether any of this duplicates ProteinGym. It does not, and as of this writing it
structurally cannot.

- Latest **data** release is `PG_v1.3`, 2025-04-28. Commits since then (to 2026-03-25)
  are benchmark-file and scoring fixes, not new assays.
- It holds **217 DMS substitution assays, the newest from 2023** — no 2024 or 2025 assays
  at all, so a 2025 sweep cannot collide with the current release.
- Searching its assay list for our proteins returns nothing: PylRS 0, TEV protease 0,
  RPB1/POLR2 0. The single "tev" hit is `MET_HUMAN_Estevam_2023`, a substring false
  positive.

Two caveats worth carrying forward:

- ProteinGym does hold `CAS9_STRP1_Spencer_2017_positive`. The PAMmla candidate is a
  separate PAM-specificity experiment on the same protein, so not duplication, but it is
  the one candidate whose protein already appears there.
- The scopes differ. ProteinGym collects deep mutational scans and clinical variants;
  engineering campaigns like Zhang 2025 and Huber 2025 are not DMS in that sense. Duan
  2025 is the closest in shape and is still absent.

And the trap this makes concrete: **ProteinGym is itself a compilation of other people's
measurements**, which is precisely the category Phase 1 excludes. A paper's ProteinGym
benchmark tables are never curatable under that paper's name.

## Maybes

- **Wong 2025**, *Characterizing and engineering post-translational modifications with
  high-throughput cell-free expression*, Nat Commun 2025-08-05,
  `10.1038/s41467-025-60526-6` — mutant oligosaccharyltransferases (*C. jejuni* PglB)
  with glycosylation efficiency by AlphaLISA. Likely a small variant set; four source
  data files. Worth opening the sheets before deciding.
- **Alamos 2025**, *Multiplexed profiling of transcriptional regulators in plant cells*,
  Nat Biotechnol 2025-11-25, `10.1038/s41587-025-02880-w` — the bulk is tiles from 1,495
  plant viruses, which is not a mutational landscape, but the machine-guided engineering
  of one plant transcription factor may be. Enrichment ratios in Supplementary Dataset 2.

## Rejected, with reasons

| Paper | DOI | Why not |
|---|---|---|
| Chen 2025, Cas12a variant profiling | `10.1038/s41467-025-57150-9` | "Variants" are 24 orthologs, and activity varies per target sequence, not per protein substitution — no single wild-type to normalise against |
| Zhu 2025, DropAI droplet screening | `10.1038/s41467-025-58139-0` | ML optimises the cell-free reaction composition, not protein sequence |
| m6A-IIN modification-site prediction | `10.1038/s42003-025-08265-8` | RNA modification sites, no protein variants |
| Nanozymes review | `10.1038/s41467-025-62063-8` | Review |
| CRISPR–Cas in agriculture | `10.1038/s41580-025-00834-3` | Review |
| CRISPR single-nucleotide diagnostics | `10.1038/s43856-025-00933-4` | Review |
| One-carbon biochemicals | `10.1038/s44160-025-00835-2` | Review |
| Antimicrobial peptides | `10.1038/s41579-025-01200-y` | Review |
| Protein folding and proteostasis | `10.1038/s41392-025-02439-w` | Review |
| Non-CG DNA methylation | `10.1038/s41588-025-02303-1` | Review |
| Antibacterial preclinical pipeline | `10.1038/s41579-025-01167-w` | Review |
| African bioeconomy genomics | `10.1038/s44185-025-00102-9` | Perspective |
| Seven technologies to watch in 2025 | `10.1038/d41586-025-00075-6` | News feature |
| ESHG 2025 ePoster abstracts | `10.1038/s41431-025-01934-6` | Conference abstracts |

## On the search itself

Dropping the organism clause was worth doing: 20 articles became 481 hits and five new
Tier A candidates, which says the first two queries were narrow rather than the year being
thin. Two gaps remain. Both sweeps cover Springer Nature journals only, so *Science*,
*JACS*, *ACS Catalysis* and bioRxiv are still invisible; and "enzyme engineering" still
misses directed-evolution and deep-mutational-scanning papers that never use the phrase —
Duan 2025 was found through the organism query rather than by describing itself as enzyme
engineering at all.

One practical note for the next sweep: nature.com rate-limits on bursts and answers with
a 3 KB `Client Challenge` page that returns HTTP 200 and parses as valid HTML. Check the
byte count on every fetch; a tiny response is a block, not an empty result.
