# 2025 candidate papers

Screening notes for the `2025` branch — papers published in 2025 that may yield
FitnessBench datasets. Nothing here is curated yet; this is the shortlist that
step 1 of `example_workflow.md` should start from.

## Scope — enzymes and enzyme-adjacent

Set on 2026-08-31 on the `2022` and `2023` branches, and **propagated here on 2026-09-06**, late:
it should have arrived with the other branches, and its absence cost this branch two curations
before anyone noticed.

FitnessBench is in practice an enzyme benchmark and always has been: this branch is around 112 of
144 datasets on catalytic activity, about twenty enzymes out of twenty-three proteins. Nothing in
`README.md` or `example_workflow.md` ever said so — the focus lived in the 2025 sweep queries,
which were phrased around *machine learning guided enzyme engineering*, and not in the
documentation. Broader DMS-vocabulary sweeps therefore drifted off it without anything pushing
back.

**In scope**: catalysts, and proteins whose measured phenotype is catalytic machinery —
nucleases, polymerases, helicases, ATP-driven transporters.

**Out of scope**: fluorescent proteins, binding domains, ion channels, structural and scaffold
proteins, viral surface glycoproteins.

### What this cost on this branch

The eighth to tenth sweeps ran without the scope in view and two of their curations failed it,
both now reverted and recorded on the tracker's Rejected tab:

| Paper | Why it failed | Recovered |
|---|---|---|
| Jansen 2026, CymR | a TetR-family transcriptional repressor — a DNA-binding regulatory protein, not a catalyst | 3 datasets, 9,557 variants each |
| Kung 2025, human myoglobin | an oxygen-binding heme protein, and the readout is surface display level, which reports folding and abundance rather than catalysis | 1 dataset, 2,350 variants |

Myoglobin is close to the GFP case the scope note singles out — fluorescence "reports chromophore
maturation and folding rather than catalysis" — and display level reports the same thing. Neither
was a quality failure: the CymR extraction verified against the source's own `mutation_codes`
column, and the myoglobin sequence matched `P02144` exactly with the paper's own statistics
re-deriving. They are scope rejections, and worth revisiting only if the scope widens.

**The lesson is where the scope lives.** It was recorded in the sibling branches' candidate files
and nowhere else — not in `README.md`, not in `CLAUDE.md`, not in the skill. A curator working
only from this branch had no way to see it, which is exactly the failure mode the scope note
itself diagnoses. It is now also a Phase 1 gate in `skill/fitnessbench-digger/SKILL.md`, so it is
checked per work item rather than depending on how a sweep query happened to be phrased.

### A deliberate exception: three 2026 papers on the 2025 branch

The branches are one per publication year — `2022`, `2023`, `2024`, `2025`, each cut from `main` —
and this file's own first line says *papers published in 2025*. The eighth sweep deliberately went
past that, because by 2026-09 the 2025 literature was a year stale and no branch existed for the
current year. Three 2026 papers were curated here as a result, and **they stay here by decision
rather than by oversight**:

| Paper | Datasets | Status |
|---|---|---|
| Vanella 2026, DAOx | 5 | in scope, kept |
| Jiang 2026, T7 RNA polymerase | 2 | in scope, kept |
| Jansen 2026, CymR | 3 | reverted, out of scope |

Anyone cutting a `2026` branch later should take Vanella and Jiang from here rather than
re-curating them, and should read the eighth, ninth and tenth sweeps below, which cover 2026 as
well as 2025.

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
- **Wong 2025**, PglB glycosylation, `10.1038/s41467-025-60526-6` — **curated.** The
  earlier search limit was real but wrong about where to stop: "Source Data 1.xlsx" ->
  sheet "Figure 5" holds the per-variant AlphaLISA table the first pass missed (the
  ~345,000-row sheets are unrelated sequencing/MS output from the paper's separate RiPP
  section). 285 single substitutions across 15 site-saturated positions of CjPglB
  (UniProt Q0P9C8), all 15 verified against it exactly. Readout is AlphaLISA signal
  (RLU) for CPS4 glycan transfer, mean of two replicates; the wild-type row is a
  genuine same-plate control measurement, not synthesized. As a check, the ten
  highest-signal variants the paper names in prose (S80V, S80T, Q287K, N311I, N311V,
  N311M, L480A, L480F, L480W, L480R) are exactly this file's top ten by readout. The
  paper's separate 328-construct PD-sequon-insertion library (Fig. 6) is a different
  kind of variant — insertion position in a different carrier protein, not a
  substitution of CjPglB itself — and stays out of scope.

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

## Seventh sweep — ACS, redone systematically

The fourth sweep was the one sweep with no recorded boolean query: it was a manual browse
of each journal's 2025 issue listings plus a title/abstract read. Redone here with the
same method as the third, fifth and sixth sweeps so it sits on the same footing:

`(JOURNAL:"ACS Catal" OR "ACS Cent Sci" OR "ACS Synth Biol" OR "J Am Chem Soc" OR
"Biochemistry") AND PUB_YEAR:2025 AND SRC:MED AND ("deep mutational scanning" OR
"site-saturation mutagenesis" OR "directed evolution" OR "variant effect map" OR
"massively parallel mutagenesis" OR "enzyme engineering" OR "protein engineering")`
— **237 hits, 234 not seen in any earlier sweep.** All 234 abstracts were pulled and
keyword-scored for signals of a per-variant quantitative table (deep sequencing, FACS,
site-saturation, explicit variant counts, sequence-function), and the top of that ranking
was chased to full text and supplement.

**The re-sweep was worth running: it found a paper the manual pass missed.**

### Curated from this sweep

**Somvilla 2025**, *Ultrahigh-Throughput Activity Engineering of Promiscuous Amidases
through a Fluorescence-Activated Cell Sorting Assay*, ACS Catalysis,
`10.1021/acscatal.5c01903` — 8 datasets, 20 variants each, on SaAmd, an amidase-signature
family amidase from *Sphingomonas alpina*. Combinatorial libraries at active-site loop L3
(positions 207-210) and distal loop positions 123 and 364 were sorted by FACS, using a
coumarin hydrolysis product retained in the cell by glutathione conjugation for the
genotype-phenotype link; the curated numbers are the follow-up purified-enzyme specific
activities in Supplementary Table S3, one dataset per substrate across 8 amide, ester and
carbamate substrates. Reference sequence is UniProt A0A7H0LPJ3, 436 residues; the paper's
construct appends a C-terminal `LELEHHHHHH` tag, dropped here as a purification artefact
that cannot shift any residue number. Wild type is a real same-panel measurement. Three of
the paper's own prose fold-changes re-derive exactly: 16.4x vs "up to 16-fold", 4.7x vs
"almost 5-fold", 5.6x vs "up to 6-fold".

**Why the manual pass missed it.** Its abstract says "directed evolution",
"high-throughput screening" and "flow cytometry" and never uses "enzyme engineering" or
"deep mutational scanning" — the exact blind spot the directed-evolution sweep was meant
to cover, in a venue that sweep did not weight heavily. It is also a PDF-only supplement,
the property that got four ACS candidates written off in the fourth sweep without
extraction being attempted. Here extraction *was* attempted and the table came out clean.
That earlier note — "worth revisiting with actual extraction if the floor-check-from-
abstract heuristic turns out to be wrong" — turned out to be the right worry.

### Rejected from this sweep

| Paper | DOI | Why not |
|---|---|---|
| A cyanobacterial screening platform for Rubisco mutant variants | `10.1021/acssynbio.5c00065` | 16 variants, under the floor -- the authors' own GitHub repository is named `CbbM_16variants`. Deep-sequenced competitive growth, so the shape is right and only the size is wrong. |
| Ultrahigh-throughput multiplexed screening from cell-free expression | `10.1021/jacs.5c04962` | Not open access, no PMC record; a droplet-microfluidics methods paper rather than a variant dataset |
| Directed evolution of a genetically encoded chloride indicator | `10.1021/acssynbio.4c00818` | `fullTextXML` empty; abstract describes a lineage to a named improved indicator |
| Stereoselective photoenzymatic hydroarylation | `10.1021/jacs.5c12440` | `fullTextXML` empty; biocatalysis paper, evolution to a named champion variant |

The rest of the 234 fall into the categories already established elsewhere in this file:
biocatalysis papers evolving to one named champion, de novo design papers, reviews, and
metabolic-engineering papers with no protein-variant table at all.

### What this says about the other sweeps

Two lessons worth carrying, both of which argue for redoing rather than trusting an
earlier pass:

- **A manual browse is not equivalent to a query, and should not be recorded as if it
  were.** The fourth sweep's row in the tracker said "title/abstract screen", which read
  like the others but was not comparable to them.
- **"PDF-only supplement" is a reason to try extraction, not a reason to reject.** Four
  fourth-sweep candidates were rejected on that basis without opening the PDF. Somvilla
  is a PDF-only supplement whose Table S3 extracted cleanly with PyMuPDF in one pass. The
  four earlier ones are worth re-opening on the same basis before they stay rejected.

## Fourth sweep — directed evolution, avoiding "DMS" and "enzyme engineering" phrasing

Requested explicitly: sweep directed-evolution literature that describes itself with
neither phrase, restricted to 2025 and to real journals (`SRC:MED` on Europe PMC, which
excludes the bioRxiv/PPR source and therefore excludes preprints without a separate
filter). Two query axes — `"directed evolution"` and `"site-saturation mutagenesis"`,
each `NOT "deep mutational scanning" NOT "enzyme engineering"` — plus a narrower
`"laboratory evolution"` pass and a `"yeast surface display" AND "deep sequencing"` pass.

**The headline finding is about the vocabulary itself, not any one paper.** Papers that
describe their own work as "directed evolution" overwhelmingly turn out to be classic
low-throughput campaigns: randomize, select, sequence a handful of survivors, name one
champion. That shape is structurally incompatible with this format regardless of how the
paper reads — there is no systematic per-variant table to recover, because one was never
generated. This is close to the inverse of the DMS/enzyme-engineering sweeps, where the
phrase itself was a reasonable proxy for "a library was scored systematically." Here the
phrase is closer to a proxy for the opposite. Twenty-plus abstracts and a dozen full-text
fetches this round, and every single one that reached full text turned out to name only
its final winner(s):

| Paper | DOI | Why not |
|---|---|---|
| Wong (chitosanase signal peptide) | `10.1021/acs.jafc.5c13730` | Iterative rounds to one named winner (M8); paywalled, not opened past the abstract |
| PROTEUS mammalian evolution platform | `10.1038/s41467-025-59438-2` | Methods/tool paper; the "N variants" figures are allele-frequency spectra from continuous passaging, not an isolated-clone table, and the two characterized Nb139 mutations are far under floor |
| Golden Gate continuous-evolution toolkit | `10.1093/synbio/ysaf014` | Pure toolkit demonstration; no target-protein dataset, just proof the mutator works |
| Maize HPPD via TADR | `10.1111/pbi.70160` | 3-page technical advance; 9 point mutants individually tested, qualitative colony-color readout for most |
| MerR Hg2+ biosensor | `10.1016/j.bios.2025.117687` | Selection funnel (98% eliminated, then top 0.2%) ending in one named variant (V124E); not open access |
| Oncolytic Sindbis virus (osteosarcoma) | `10.1016/j.omton.2025.201096` | Adaptive passaging to a consensus lineage, not a mapped substitution landscape; "variant" appears 6 times in the whole paper |
| Rubisco laboratory-evolution screen (Nat Plants) | `10.1038/s41477-025-02093-8` | Screen narrows to exactly two named point mutations (M116L, A242V), deeply characterized but not a library table |
| Nonheme iron BsQueD (alkene amination) | `10.1021/jacsau.5c00817` | "An optimized variant" — lineage evolution to one champion |
| PchB to chorismate mutase (reverse evolution) | `10.1021/acs.biochem.5c00157` | Functional-complementation selection from a 7-position, 38,000-variant library down to a handful of named sequenced clones (5-1, 2-43, 10-37...); no per-variant table, just individually characterized survivors |
| PHL7 PET hydrolase (4 rounds) | `10.1016/j.checat.2025.101399` | Four named final variants (Jemez, Santa Fe, Taos, Tusas); no deposited dataset, "available upon reasonable request" |
| Q-body immunosensor quenching prediction | `10.1021/jacsau.4c01189` | The large NGS-scored library is a synthetic nanobody repertoire, not point mutants of one wild type; the validated point-mutant sets (Trp scans) are single digits per antibody |
| Curr Protoc SELIS walkthrough | `10.1002/cpz1.70218` | Protocol demonstration, not a dataset paper |
| Ebola VP40 patient mutations | `10.1016/j.jbc.2025.110489` | "40 mutations" is epidemiological surveillance across outbreak lineages, not an experimental library; only 2 mutations (R204H, H269R) are lab-characterized |
| Affibody stability (DR5 / TNFR1) | `10.1002/bit.28954` | Deep sequencing used only to triage candidates for individual validation; reported data is a handful of purified variants, not library-wide |

**Two papers came closer than anything above and are worth a dedicated pass rather than a
quick verdict:**

- **A class A β-lactamase gatekeeper-residue screen**, `10.1016/j.jbc.2025.110347` — site
  saturation of Ambler position 105 in five different β-lactamases (BlaC, CTX-M-14,
  KPC-2, NmcA, TEM-1), each screened by deep sequencing against 7 substrates/inhibitors
  with 3 replicates. The Supporting Data (`mmc2.xls`, a genuine legacy `.xls`, needs
  `xlrd`) really does hold raw counts and per-replicate fitness values, not just a
  figure. The catch: this is one saturated position, so each enzyme's dataset would be
  19 substitutions plus WT — one row under this branch's usual floor, and thin compared
  to everything else on it. Worth a second look if the bar is "genuine deep-sequencing
  fitness data" rather than "library-scale."
- **A tryptophan decarboxylase (TDC) active-site recombination study**, `10.1002/pro.70356`
  — substrate-multiplexed screening (SUMS) across five active-site positions, combining a
  clean prior single-site-saturation sub-library (96 unique single mutants, referenced
  but not obviously deposited) with iterative combinatorial recombination libraries
  (~250 variants total, up to triple mutants, LC-MS-quantified activity against multiple
  substrates). Multi-site labels are within the format's scope, but the data availability
  statement is "upon reasonable request" — nothing machine-readable was found in the
  supplement, so this would need an email to the authors before it goes further.
- **A yeast-display Aβ-fibril conformational antibody campaign**, `10.3389/fimmu.2025.1655893`
  — unlike the Frontiers antibody paper found in an earlier round (heatmap-only, no
  export), this one deposited raw NGS data on GitHub
  (`Tessier-Lab-UMich/druglike-abeta-antibodies`, `data/ngs_data/Rep_{1,2}/DMD_data/`):
  per-sort-round CDR-sequence frequency tables covering a 10-site NNK library (5 in
  HCDR1: H27/H31/H32/H33/H34, 5 in LCDR2: L50/L51/L52/L53/L55) built off a named parent
  antibody ("clone 97"). This is genuinely promising — real sequencing counts, a defined
  wild type, a defined mutated region — but turning sort-round frequencies into an
  enrichment score means first finding clone 97's parent CDR sequence (a different,
  earlier paper) and working out which of the five numbered files per replicate is
  "before" and which is "after" selection, none of which is safe to guess at. Left for a
  session that can read the cited parent paper's methods in full.

Not yet run: `"phage display"`, `"PACE"` / `"phage-assisted continuous evolution"`,
`"ancestral sequence reconstruction"`, and `"combinatorial active-site saturation
test"` / `"iterative saturation mutagenesis"` as their own query axes. Given how lopsided
this round's hit rate was, the phage/PACE axis is the more promising one to try next —
PACE campaigns are more likely than manual "directed evolution" write-ups to carry a
deep-sequencing-scored population, closer in spirit to the β-lactamase and Aβ-antibody
leads above than to the one-champion pattern that dominated everything else this round.

## Audit of within-paper rejections — 2026-08-27

Every curated paper's `remark` ends with a clause naming what was *not* extracted from it.
That clause is the only record of those decisions, and until now nothing had ever re-read
one. This round did: all 36 exclusions across the 17 curated papers are now enumerated in
the **Partial rejections** tab of `FitnessBench_2025_literature_search.xlsx`, each with a
verdict. Twenty-nine hold up. Four do not, and one is imprecise.

**Singh 2025 — the YmPhytase campaign. Wrong, now fixed.** The remark said "no sequence is
given in the paper and no reference accession could be found". The *Description of
Additional Supplementary Files* lists Supplementary Data 5 as
`SupplementaryDataFile_5_DNA_sequencing_files.zip` — "The DNA sequences for wild-type AtHMT
and YmPhytase" — and the Fig. 3 caption repeats the pointer in the caption of the very
figure whose data was curated. The zip holds a plasmid map whose CDS at 2413..3714
translates to a 434-residue ORF against which all 180 mutation labels verify at offset 0.
Shipped as `Singh 2025-ML-YmPhytase-catalyticactivity-relative_activity.csv`, 181 variants.

The failure was searching for an accession and treating its absence as the absence of a
sequence. **A construct sequence in a supplementary plasmid map is a Phase 3 source like
any other** — 0a's attachment listing is where to look for it, before any accession search.

**Singh 2025 — rounds 2 to 4, both enzymes. Wrong, now fixed.** The remark said the rounds
are "built on several different improved parents per round with no per-well template
assignment shipped, so a variant's full genotype cannot be reconstructed". The `Mutations`
column of every round-2/3/4 sheet writes the full genotype, not the new substitution:
`V141M / K226G / I15V / Q295D`. No template assignment is needed to read it.

Both datasets now pool all four rounds, since every round normalizes to wild type on its own
plate and they therefore share a scale: **AtHMT 176 → 482 variants** and **YmPhytase 181 →
449**, singles through quadruples. Both reconcile against the paper's own arithmetic — the
AtHMT Overview sheet states 482 new mutants and the YmPhytase Summary sheet 448, the latter
plus the T44V/K45E benchmark giving 449. Two carried-forward parents are named by round and
well rather than by genotype (`R2C12`, `R3 B3`) and resolve against those sheets. The cost of
pooling is that the positive controls drift across plates — V140T spans 1.78 to 3.09 over six
rounds, M16 2.90 to 3.87 over five — and that spread is now the recorded statement of
plate-to-plate reproducibility in each `remark`.

**Singh 2025 — AtHMT round-1 variant identity. Wrong, harmless.** Found while rebuilding: the
remark claimed identity "is not in the screening file, whose rows are plate wells" and had to
be recovered by joining to the primer plate map of Supplementary Data 1. The round-1 sheets
carry their own `Mutation` column holding all 176 labels — identical to the set the join
produced, so the data was never affected, but the file was described as something it is not.
Three wrong claims about one paper's supplement is not three mistakes; it is one file that
was skimmed rather than inventoried.

**Landwehr 2025 — the GitHub combinatorial libraries. Not a rejection reason.** "Measure a
different library on the same enzyme" describes a *separate dataset*, which is exactly what
this format curates one row at a time. `data/ML_validation/*.xlsx` and `data/HSS/*.xlsx` in
`github.com/grantlandwehr/accelerated-enzyme-engineering` hold per-variant measured
activity keyed by a four-letter code over the four randomized sites — 77 to 243 variants
per file across 9 substrates, all above the floor, and the same shape as the ALDE ParLQ
dataset already shipped. Open.

**Estevam 2025 — the exon-14-deleted MET background. A deferral written as a rejection.**
"A different construct, and would be its own set of datasets" is a reason to curate it, not
to drop it; it would roughly double this paper's yield to ~24 datasets. Availability is
unconfirmed — the eLife PMC package carries figures only and the data repository was not
located — so chase the Data availability statement before committing to it.

**Huber 2025 — Fig. 3a. Imprecise.** Grouped with four other panels as "fewer than twenty
distinct protease genotypes". The other four are 6, 12, 5 and 5 and the claim holds; Fig. 3a
is 2 positions × 20 amino acids = 40. It is almost certainly redundant with the shipped
library, which already covers positions 171 and 176, but the stated reason is not the true
one.

**What generalizes.** Three of the four wrong calls share a shape: a clause that reads like
a finding but is really an unfinished search — *no sequence could be found*, *the genotype
cannot be reconstructed*, *it would be its own set of datasets*. None of them names the file
that was opened and found wanting. A clause-5 rejection should say what was looked at, so
that re-reading it later is cheaper than redoing the search — "Supplementary Data 5 holds
only the AtHMT map" would have been checkable in seconds; "no sequence is given in the
paper" was not.

## Eighth sweep — 2026, the year nobody had looked at

Every sweep above is `PUB_YEAR:2025`. The branch is named for that year and so is this
file, but the calendar moved: this sweep was run on **2026-09-04**, so roughly eight
months of literature had accumulated that no query in this file could have reached. That
is a larger gap than any of the vocabulary axes the earlier sweeps worried about, and it
costs nothing to close — the sweeps that worked need only their year changed.

Two queries, both Europe PMC, both `SRC:MED AND OPEN_ACCESS:Y AND PUB_YEAR:2026`:

| Query | Hits |
|---|---|
| `ABSTRACT:("deep mutational scanning" OR "site-saturation mutagenesis" OR "variant effect map")` | **66** |
| `ABSTRACT:("enzyme engineering" OR "protein engineering" OR "machine learning-guided") AND ABSTRACT:"variants"` | **45** |

Both are relevance-ordered and were read to a `pageSize` of 40, so the lists below are the
top slice rather than an enumeration — the third, sixth and seventh sweeps are worth
re-running verbatim against 2026 before this year is called done.

### Chased to a data-availability statement

| Paper | DOI | Verdict |
|---|---|---|
| **Vanella 2026**, *Decoding the substrate specificity landscape of a promiscuous enzyme through multi-substrate mutational scanning*, Nat Commun | `10.1038/s41467-026-69913-z` | **Curated — 5 datasets, 5,800 variants each.** See below |
| **Jansen 2026**, *Mapping the phenotypic landscape of a transcriptional repressor using deep mutational scanning and growth-based quantitative sequencing*, NAR | `10.1093/nar/gkag206` | **Curated, then reverted as out of the enzyme scope.** See below |
| Echinocandin resistance in *S. cerevisiae*, Genetics | `10.1093/genetics/iyag055` | **Open.** Fks1 (beta-1,3-glucan synthase), 465 single substitutions across three hotspots confidently classified, bulk-competition DMS against anidulafungin, caspofungin and micafungin plus a no-drug control — four conditions on one WT. No formal data-availability statement in the full text; the selection coefficients are presumably in the eleven supplementary tables, which is a Phase 0 chase rather than a decided fact |
| Urease functional and catalytic landscape, *H. pylori*, Gut Microbes | `10.1080/19490976.2026.2653575` | **Deprioritized.** UreB, 58 alanine-scan point mutants — over the floor — but the readouts are a spread of expression, growth, colonization and binding assays rather than one quantity across the panel, and there is no data-availability statement at all |

### Curated from this sweep

**Vanella 2026**, *Decoding the substrate specificity landscape of a promiscuous enzyme through
multi-substrate mutational scanning*, Nature Communications, `10.1038/s41467-026-69913-z` —
**5 datasets, 5,800 variants each**, on D-amino acid oxidase (DAOx) from *Rhodotorula gracilis*,
365 aa. One EP-Seq library — yeast surface display on *S. cerevisiae* EBY100, single-cell
tyramide proximity labeling of the H2O2 the enzyme releases, FACS into four bins, barcode
sequencing — scored against five D-amino acid substrates each at its own Km, giving one dataset
per substrate under `Activity/CatalyticActivity/DMS/`. Readout is the source's
expression-normalized activity fitness, with wild type at 1.0 by the definition of the score;
there is no wild-type row.

**Three things about this paper worth carrying forward.**

*The Zenodo deposit is the source, and the article's own Source Data is the one that is wrong.*
Source Data sheet `Fig. 2B` holds 5,821 missense rows and Supplementary Table 3 states that same
5,821 as the set shared by all five substrate screens — but **26 of its labels put a substitution
at a position whose wild-type residue does not match** (`A144N` where 144 is Q, `H129C` where 129
is G, and 24 more), and the Zenodo `Fitness_scores_dataset.xlsx` carries 5,800 rows of which all
5,800 verify. The two files also differ by 20 further labels that verify but appear only in
Source Data. This is the inverse of the Jiang 2025 lesson: there, Source Data held the real table
and the files labelled "Supplementary Data" did not. **Run the label check against every candidate
source before choosing between them** — it is the only thing that distinguishes them, and it is
cheap.

*The sequence question was settled by the previous paper's deposit, not this one's.* The scan
covers positions 2-365 and UniProt `P80324` is 368 aa, so whether the construct carries the native
C-terminal `SKL` decides `seq_len`. This paper's SI has no construct sequence at all. Ref 19 —
Vanella 2024, `10.1038/s41467-024-45630-3`, the EP-Seq paper whose plasmid and library this work
reuses — says the library targeted "codons 2 to 365" and deposits `DAOx_ref.fa` at Zenodo
`10.5281/zenodo.8388902`. Translating it gives a 396-aa ORF: DAOx 1-365, then
`LESRGPFEGKPIPNPLLGLDSTRTGHHHHHH` — an XhoI scar, a V5 tag and a 6xHis. So `SKL` (the PTS1
peroxisomal targeting signal) is genuinely absent from the displayed construct, and `seq_len` is
365. **When a paper reuses a previous paper's plasmid, that paper's deposit is a Phase 3 source**,
and it is often the only place the construct is actually written down. The article's own prose
corroborates it arithmetically: stop codons "beyond position 356" are said to lose "only the last
~10 amino acids", which is true of a 365-residue construct and not of a 368-residue one.

*Do not fetch a Zenodo record blindly.* Both deposits list their files through
`https://zenodo.org/api/records/<id>`, and record `8388902` includes a 2 GB PacBio FASTQ and a
14 GB Illumina zip beside the 2 KB `DAOx_ref.fa` that was actually wanted. Filter the `files`
array by size and extension before downloading anything.

**Not extracted, and why.** The ten Sp-score columns are the authors' own z-scores of fitness
differences between substrate pairs — curatable, a new `Selectivity/SubstrateSpecificity/`
property, and left for a later decision rather than shipped unasked. The expression fitness
column is a measurement from ref 19, not from this paper, so Phase 1 excludes it under this
paper's name. Synonymous (432) and nonsense (330) variants are not amino acid substitutions. The
single-clone Amplex Red validation (18 variants), the purified-enzyme kinetics (5 to 6) and the
Fig. 7C combinatorial set (15) are all under the floor — the first of those is instead what
Phase 7 used.

**Phase 7 re-derivation.** Supplementary Table 3 states the between-replicate Pearson r per
substrate as 0.93 (D-Ala), 0.96 (D-Phe), 0.96 (D-Met), 0.93 (D-Asn), 0.94 (D-Gln). Recomputing
from the shipped rows gives 0.939, 0.969, 0.968, 0.943, 0.950 — agreeing to within 0.01 on a
slightly smaller variant set than the paper used. The stated median log2 fitness per substrate
(-0.33, -0.28, -0.28, -0.34, -0.35) likewise re-derives to -0.326, -0.290, -0.305, -0.355, -0.362.

**Jansen 2026**, *Mapping the phenotypic landscape of a transcriptional repressor using deep
mutational scanning and growth-based quantitative sequencing*, Nucleic Acids Research,
`10.1093/nar/gkag206` — **curated, then reverted on 2026-09-06 as out of the enzyme scope.** CymR is
a TetR-family transcriptional repressor: a DNA-binding regulatory protein, not a catalyst and not
catalytic machinery. Nothing below is a quality objection — the extraction verified against the
source's own `mutation_codes` column throughout — and the work is recorded here in full so that it
can be recovered cheaply if the scope ever widens to regulatory proteins.

What it would have been: **3 datasets, 9,557 variants each**, on CymR from
*Pseudomonas putida*, 203 aa. One GROQ-Seq library — barcoded variants in *E. coli* whose
CymR-controlled promoter drives a `tetA`-mScarlet-I fusion, so tetracycline selection turns
repressor function into growth — scored against three inducers, giving one dataset per ligand
under the new `Activity/TranscriptionalRegulation/DMS/`. Readout is log10 fold induction
(Ginf/G0) from the paper's own Hill fit; higher is better and no inversion was needed.

**The supplement is far richer than the abstract implies.** `cymr_variant_table.csv`, inside
`gkag206_supplemental_files.zip`, has 54 columns: for each of three ligands a Hill fit gives
basal output, saturating output, EC50 and a Hill coefficient, plus Gaussian-process-smoothed
restatements and inversion probabilities. Thirteen of those are curatable measurements; three
were taken. It also ships a full amino-acid sequence per variant *and* a `mutation_codes` column,
so Phase 3 and Phase 4 verify against each other for free — all 9,557 derived labels agree with
the source's own codes.

**Multi-site variants are the bulk of the yield here.** Singles are 3,662 of the 9,557; the rest
are 5,310 doubles, 525 triples and 58 higher. The paper frames its library as single-mutant
coverage and analyses it that way, so taking the multis is a departure from its framing — but
they are the same measurement on the same parent, which is what the format calls more rows, and
they are the only epistasis signal available.

**Two findings worth carrying.**

*The wild type is not the wild type.* The assayed repressor carries S110G and A171V relative to
UniProt `O33453`, which the paper notes were "previously reported to improve the dynamic range".
The construct is a known engineered parent, so `wt_readout` describes that parent and a positive
`normalized-score` says nothing about natural CymR. The two differences were found by alignment
before the paper's sentence was located, which is the order the check is supposed to run in.

*The paper and its own supplement disagree on the protein's length.* The text says the CDS "spans
202 amino acids, including the initiating methionine" and designs "201 positions × 19
substitutions" for 3,819 variants; the sequences the same supplement ships are 203 residues, and
so is `O33453`. The datasets follow the sequences. The discrepancy does not change any residue
number, and the coverage re-derives either way: 3,662 singles is 95.4% of 202 × 19 and 95.9% of
the paper's own 3,819, against its stated "more than 95% of all possible substitutions".

Not extracted: the 11,671 insertion and deletion variants, which cannot be written as
`{WT}{position}{MUT}` at all; the other ten Hill-fit readouts; the Gaussian-process columns; and
the inversion probabilities, which are posterior probabilities from a model rather than
measurements.

### Also in the 2026 lists, by tree

Human and viral scans are as abundant in 2026 as the third sweep found them in 2025, and
drop below cellular non-human work by the same rule. Noted here so a later pass can see
they were found: TYK2 DMS (`10.7554/eLife.110149`), IAPP amyloid formation
(`10.1038/s41467-026-70611-z`), tapasin (`10.1016/j.jbc.2026.111400`) for `datasets_human/`;
HIV-1 Vif x APOBEC3G epistasis (`10.1126/sciadv.aed4872`), influenza HA subtype constraints
(`10.1093/ve/veag018`) and the Omicron JN.1/XEC RBD scan
(`10.1080/22221751.2026.2686472`) for `datasets_virus/`.

Worth a look on a later pass, not chased here: substrate-selective Hsp104 variants from a
high-throughput screen (Mol Cell, `10.1016/j.molcel.2026.04.015`), *Fast analysis and
engineering of protein function by microbe-independent deep assembly and screening* (Mol
Syst Biol, `10.1038/s44320-026-00210-z`), and phage-assisted evolution of allosteric
protein switches (Nat Commun, `10.1038/s41467-026-71717-0`).

One hit is not a candidate but is already familiar: the EnzEngDB paper
(`10.1093/nar/gkaf1142`) is the publication behind the `EnzymeEngineeringDB/` clone named
in `CLAUDE.md`. It is a compilation of other people's measurements, so Phase 1 excludes it
under its own name — its value here is the bulk-conversion route already recorded there.

## Ninth sweep — the display axis, and a verdict on it

The directed-evolution sweep listed `"phage display"`, `"PACE"`, `"ancestral sequence
reconstruction"` and `"iterative saturation mutagenesis"` as not yet run, and guessed the
phage/PACE axis was the more promising. Run here for 2025 and 2026 together:

`ABSTRACT:("phage-assisted continuous evolution" OR "phage display" OR "yeast surface
display") AND ABSTRACT:("deep sequencing" OR "next-generation sequencing" OR "enrichment")
AND (PUB_YEAR:2025 OR PUB_YEAR:2026) AND SRC:MED AND OPEN_ACCESS:Y` — **38 hits.**

**The guess was wrong, and the axis is close to dead for this format.** Essentially all 38
are antibody, nanobody or peptide *discovery* from naive or synthetic repertoires: the
sequences that come out are not substitutions of a shared wild type, so they fail the same
half of the work-item definition that sank the Cas12a orthologs and the PET-hydrolase
panel. Deep sequencing is present and quantitative in many of them, which is what made the
axis look promising, but a library with no parent has nothing to write in the `mutant`
column. The one paper here already known to be different — the Abeta conformational
antibody campaign, `10.3389/fimmu.2025.1655893` — is different precisely because it mutates
a named parent clone, and it is already on the Open (maybes) tab.

### An attempted query that must not be recorded as a sweep

`("iterative saturation mutagenesis" OR "combinatorial active-site saturation" OR
"CASTing" OR "ancestral sequence reconstruction")` was run **unscoped** and returned 9,406
hits of tundish flow, investment casting and denture clasps — Europe PMC matched `CASTing`
as free text. An earlier attempt at the PACE axis failed the same way, matching `PACE`
against prime-editing papers. Both were discarded.

So the ASR and ISM/CASTing axes are **still not swept**, and the fourth sweep's lesson
applies to my own work: an unrecorded or malformed query should not be entered in the
tracker as if it were one of the others. What the polluted results did show in passing is
that ASR papers mostly resurrect a handful of ancestors and compare them — a homolog panel
under another name — so the axis is worth scoping properly but not worth much optimism.

## Preprints — sized, not swept

`ABSTRACT:("deep mutational scanning" OR "site-saturation mutagenesis" OR "machine
learning-guided") AND SRC:PPR AND (PUB_YEAR:2025 OR PUB_YEAR:2026)` — **230 hits**, of
which the first 25 were read. Visible already: ML-guided olivetolic acid cyclase
engineering in yeast, ML dual optimization of yeast alcohol dehydrogenase substrate
specificity and thermostability, directed evolution of Fe-nitrogenase for CO2 reduction,
and continuous site-directed mutagenesis and selection in *E. coli*.

This is a sizing probe, not a sweep. Every earlier sweep used `SRC:MED` deliberately, which
excludes the bioRxiv/Research Square source, so **whether preprints are in scope is a
policy question that has never been asked** — not a gap in anyone's querying. The number is
recorded here so the question can be answered against a real quantity.

## Leads re-verified rather than re-searched — 2026-09-04

The 2026-08-27 audit left two follow-ups open, and one of them was confirmed live this
session rather than re-argued:

**Landwehr's GitHub files — opened, and the audit's reading of them was wrong.** The
2026-08-27 audit recorded them as "a separate dataset rather than a rejection reason" and this
file called them the cheapest yield available. Both claims were made from the *file listing*.
Opening the files says otherwise.

`data/HSS/` holds seven `{drug}_train.xlsx` and `data/ML_validation/` two more, and every one of
the nine is **77 rows of single mutants, not a combinatorial library**: 4 sites x 19
substitutions plus the parent, the parent being wild-type McbA in every case. The four sites are
per substrate, from that substrate's own hot-spot screen — moclobemide V177/I220/A323/R430,
metoclopramide V177/T319/A323/A424, cinchocaine V177/A205/C232/R430, itopride E228/N316/A323/A424,
declopramide T103/V177/A295/A424, and by value-matching against the shipped data procainamide
C201/A266/A323/A424, sulpiride I220/A266/A323/R430, trimethobenzamide L225/E228/A323/R430,
troxipide V177/A323/A424/R430.

All four of those sites are inside the 64 the shipped hot-spot datasets already cover, and every
label overlaps: 76/76 for each of the five substrates whose sites the SI states, and 19/19 exact
value matches at every inferred site for the other four. For cinchocaine, itopride and
declopramide the numbers are identical to rounding. **These files are ML training exports of data
already in the repo.** Nothing to curate.

The two `*_test.xlsx` files are the exception and are genuinely new: 243 multi-site moclobemide
variants and 169 metoclopramide ones — doubles, triples and quadruples over those same four sites,
with no overlap with anything shipped.

**But not from GitHub.** The two ML_validation files are also the only two whose train values do
*not* match the shipped data: the shipped/GitHub ratio runs 1.2 to 15.8 for moclobemide and 14.3
to 25.0 for metoclopramide, so they sit on some processed scale that no single factor recovers,
and the test sets inherit it. Phase 2 rejects that — a ratio with an unknown denominator is not a
measurement.

The paper's own **Source Data carries the same variants with a stated denominator**: sheet
`Fig 4a` is moclobemide (245 rows, 243 distinct codes, mutation profile 59/146/38 matching the
GitHub file exactly) and `Fig4b` is metoclopramide (243 rows, a *superset* of GitHub's 169). Both
give `Actual` min-max normalized with the best variant in the set at 1. That is a different
quantity from the shipped datasets' fold-change against wild type, so they ship as two new
datasets rather than extra rows on the existing nine.

**Shipped 2026-09-05**, 243 variants each, taking this paper to 11 datasets. Two Phase 7 checks
land on the paper's own prose. The top-ranked moclobemide variant decodes to
`V177S:I220S:A323F:R430L`, a quadruple carrying V177S and A323F — the first two mutations the
paper names from its ISM rounds, which independently confirms the site order the four-letter code
is read in. And the paper states its model was "trained on single mutant data (n = 77) from the
HSS" and tested on "the withheld higher-order mutants ... (n ≈ 200)", which is exactly the split
found on disk: 77-row train files that duplicate the curated hot-spot screen, and 243- and
169-row test files of higher-order mutants that do not.

One consequence worth knowing: neither dataset has a wild-type row, because the wild type was
not measured in this set, so both carry an empty `wt_readout`. `validate.py` calls that an error,
so the branch now reports three of them — the Alamos row and these two — all the same false
positive.

**What generalizes.** The audit was right that "measures a different library on the same enzyme"
describes a dataset — but it never checked whether the library *was* different. A file listing
plus a plausible sentence is not evidence about contents; four column reads would have settled it.
That is the same failure the audit itself diagnosed in the Singh remarks, committed one level up.

**Estevam's exon-14-deleted MET background is unchanged** — still a deferral written as a
rejection, still needs the Data availability statement chased before it can be committed to.

## Tenth sweep — the never-swept journals, weighted to enzymes

The venue audit behind the ninth sweep showed that every journal-specific sweep so far had been
Nature-family, ACS, PNAS or Cell Press, and that several venues carrying enzyme work had never
been queried at all. This sweep takes those, 2025 and 2026 together, and weights the query toward
enzymes rather than proteins in general:

`JOURNAL:"<J>" AND (PUB_YEAR:2025 OR PUB_YEAR:2026) AND SRC:MED AND (ABSTRACT:"enzyme" OR
"enzymatic" OR "biocatalyst" OR "catalytic" OR "substrate specificity" OR "thermostability" OR
"polymerase" OR "protease" OR "hydrolase" OR "oxidase") AND (ABSTRACT:"deep mutational scanning"
OR "site-saturation mutagenesis" OR "saturation mutagenesis" OR "directed evolution" OR
"variant library" OR "protein engineering" OR "enzyme engineering" OR "machine learning")`

**289 hits across 20 journals**, every title screened, five chased to their data-availability
statements and three of those opened further.

| Journal | Hits | Verdict on the venue |
|---|---|---|
| Angew Chem Int Ed | 62 | the one-champion biocatalysis pattern, wall to wall |
| Chem Sci | 32 | computational catalysis and ML method papers; almost no wet variant tables |
| Protein Sci | 28 | **productive** — two real candidates, and its data lives on Zenodo |
| Nucleic Acids Res | 21 | **productive** — enzyme evolution papers, but data often only in the SI PDF |
| Chembiochem | 21 | reviews and small biocatalysis; nothing at library scale |
| Biotechnol Bioeng | 21 | metabolic engineering; titles are pathway yields, not variant tables |
| Enzyme Microb Technol | 19 | same |
| Synth Syst Biotechnol | 18 | same — almost every hit is strain or pathway engineering |
| Chem Commun, J Biotechnol, AEM, Microb Biotechnol, Metab Eng, Biotechnol Biofuels | 4-13 each | thin; nothing above the floor |
| Sci Adv | 7 | **one strong candidate, unreachable** |
| Protein Eng Des Sel | 5 | small |
| Nat Chem Biol | 4 | two directed-evolution papers, neither with a PMC record |
| Science | 3 | one candidate, rejected on inspection |
| Nat Catal | 1 | already rejected in an earlier sweep |
| Green Chem | 0 | — |

**The venue lesson.** Weighting a query toward enzymes does not make the biotechnology journals
productive. `Biotechnol Bioeng`, `Synth Syst Biotechnol`, `Enzyme Microb Technol` and `Metab Eng`
together returned 64 hits and not one candidate: their subject is pathway and strain engineering,
where the reported number is a titre and the protein work is a handful of rational mutants. That
is a property of the field, not of the query, and those four are not worth re-sweeping.
`Angew Chem` is the same story in a different register — 62 hits of elegant biocatalysis, each
evolving to one named champion, exactly what the directed-evolution sweep predicted.

### Rejected on inspection

**Science 2025**, *Evolutionary-scale enzymology enables exploration of a rugged catalytic
landscape*, `10.1126/science.adu1058` — **rejected, homolog panel.** The headline is attractive:
kcat, KM and kcat/KM measured by microfluidics for hundreds of adenylate kinase variants, with all
kinetics deposited at Zenodo `10.5281/zenodo.15022270`. But the library is **193 orthologs** with
"an average pairwise sequence identity of 42%", and the only true mutants are LID-domain swap
chimeras and a short cysteine series. No shared wild type, so no `mutant` column can be written —
the same shape that sank the Cas12a orthologs and the PET-hydrolase panel. Worth recording because
the abstract reads like the single best enzyme dataset of the year.

**Protein Sci 2026**, *High-throughput mutational analysis of F1-ATPase*, `10.1002/pro.70699` —
**rejected.** Data availability is "available from the corresponding author upon reasonable
request", and the saturation covers two residues (βE190, βY307).

### Open, and why each is stuck

**Sci Adv 2026**, *The fitness landscape of a form II rubisco in a photosynthetic bacterium guides
engineering of oxygen tolerance*, `10.1126/sciadv.aee9222` — **the best candidate this sweep found,
and unreachable from here.** A barcoded library of **15,000 single-site and multi-site variants** of
a *Gallionella* form II rubisco, scored by growth-coupled selection in *Synechocystis* sp. PCC 6803
— one wild type, bacterial, well above the floor, and a second rubisco to sit beside Wysocki's
RbcL. Europe PMC has the record but `inEPMC:"N"`, `hasSuppl:"N"`, subscription only; there is no
route to the supplement from here at all. This one needs a hand-off.

**NAR 2026**, *Deep learning-guided dual-fitness evolution of T7 RNA polymerase*,
`10.1093/nar/gkag259` — **curated, 2 datasets, 164 variants each**, into
`datasets_virus/Stability/ThermalStability/ML/` and
`datasets_virus/Activity/CatalyticActivity/ML/`. The Somvilla lesson held: the data availability
statement says only "All data described are contained within the article", the supplemental zip
holds three PDFs and no spreadsheet, and the numbers came out of the SI PDF cleanly anyway.

**The table is split across two tables and joined on an index.** `Table S3` maps an index
(`R2-1` … `R5-40`) to a genotype; `Table S4` gives Tm and 52 °C activity against the same index.
Neither is usable alone — which is why the mutation-density scan found labels on pages 25-29 and
none on 30-33, and why a first glance suggests the results table has no genotypes.

**Plain text extraction was not good enough, twice.** Reading the PDF as lines and pairing each
index with the following line silently dropped `R5-30` to `R5-39` — the 12- to 14-site mutants,
whose long genotype strings wrap. Widening to "accumulate until the next index" then over-collected,
inventing variants with 30 substitutions. Only the appendix's method — words with coordinates,
columns cut at fixed `x` ranges, wrapped cells reattached as orphans — produced a table whose row
index is contiguous within every round in *both* tables. **The contiguity assert is what caught
both failures**; without it the first pass looked perfectly plausible and was missing a sixth of the
data.

One genuine gap survives the extraction: `Table S3` defines `R4-30` and `Table S4` reports no result
for it, so 165 defined mutants give 164 rows. Page 32 runs `R4-29` straight into `R5-1`.

**Two Phase 7 findings.** The paper reports **two different wild-type melting temperatures** — 46.9 °C
by CD and calorimetry, 42.1 °C by the incubation assay — and puts neither in Table S4, which is why
`wt_readout` is empty rather than typed. Against the 46.9 °C figure the best variant here, 57.7 °C,
is 10.8 °C above wild type, matching the paper's stated ">10 °C". The sequence needed no work at
all: T7 RNAP is already in this repo from Jiang 2024, and all 26 distinct substitutions verify
against that 883-residue sequence.

**Protein Sci 2025**, *Deep mutational scanning reveals a de novo disulfide bond and combinatorial
mutations for engineering thermostable myoglobin*, `10.1002/pro.70112` — **curated, then reverted on
2026-09-06 as out of the enzyme scope.** Myoglobin is an oxygen-binding heme protein rather than a
catalyst, and the readout compounds it: surface display level reports folding and abundance, which
is the same objection the scope note makes to GFP. The `Expression/SurfaceDisplay/` category created
for it was removed with it. Again not a quality objection — the sequence matched `P02144` exactly
and the paper's own statistics re-derived — so the detail below stands if the scope widens.

What it would have been: **1 dataset, 2,350
variants**, at `datasets_human/Expression/SurfaceDisplay/DMS/`. Over 10,000 human myoglobin variants
were screened by yeast surface display and FACS; the Zenodo deposit `10658344` holds
`Figure_2_data.xlsx`, whose `Figure_2B` sheet classifies 2,578 scored variants as 2,350 missense,
119 nonsense and 109 synonymous.

**A new category, `Expression/`, and why not `Stability/`.** What was measured is surface display
level. What the paper claims is a thermostability proxy, validated against eleven NanoDSF melting
temperatures. The skill's rule is to name a level for what was measured, so the directory says
`SurfaceDisplay` and the `readout` string carries the proxy claim. Vanella 2024's expression scores,
the same assay from the same lab, belong here when that lead is worked.

**Three things worth carrying.**

*The labels are numbered against the fusion, not the protein.* `AA_Mutation` runs from 137 to 290,
because the construct is an Aga2p fusion; the `Figure_2E` sheet gives the myoglobin numbering (1 to
155) for the same rows, and the offset is exactly **136**. It is uniquely determined — no other
offset in ±300 makes all the labels verify — and it was confirmed independently against the
`Figure_4E` NanoDSF labels, which use the same convention. Renumbered, the sequence is identical to
UniProt `P02144` at all 154 residues and all 2,350 labels verify with zero failures, every position
carrying at least three substitutions.

*The synonymous variants are the wild type.* All 109 encode wild-type myoglobin through alternate
codons, so they are repeat measurements of one protein and collapse into a single WT row rather than
being dropped. That gives a real `wt_readout` of 0.0225 instead of an empty field, and their spread
of 0.29 log units is the assay's own reproducibility statement.

*Phase 7 re-derives twice.* The paper states nonsense variants at "0.52 ± 0.13" and synonymous at
"0.03 ± 0.07"; recomputing from the deposited file gives **−0.525 ± 0.121** and **+0.023 ± 0.056**.
The sign on the first is missing from the paper's PDF text, not from the data.

Not extracted: the `Figure_4E` NanoDSF melting temperatures (ten variants plus wild type) and the
`Figure_6C` combinatorial set (sixteen, identified only as `Var1`–`Var16` with no genotype in the
deposited file) — both under the twenty-variant floor.

Also noted, not chased: *Promiscuity-Guided Enzyme Evolution via Substrate Multiplexed Screening*,
`10.1002/anie.202600007`, which is the same SUMS method as the tryptophan-decarboxylase paper
already on the Open tab and may share its "upon reasonable request" problem.

### What this sweep taught the skill file

Three venues file their data somewhere `0b` did not predict, and the rows have been added:

- **Nucleic Acids Res** ships one `{articleid}_supplemental_files.zip` holding everything at once —
  the per-variant CSV, the plasmid maps and the SI PDF together. The Data availability statement
  names a "Supplementary file 1" that is a *member of that zip*, so the file it names cannot be
  found until the archive is unpacked. Both NAR papers seen so far behave this way.
- **Protein Science** puts the numbers in the Zenodo record named in Data availability, as small
  `Figure_N_data.xlsx` workbooks sitting beside multi-gigabyte raw-sequencing archives — 6 GB of
  Illumina reads next to a 293 KB spreadsheet in the myoglobin deposit. Filter by size first.
- **Cell Press** already had this failure recorded in prose from Teo 2025 but not in the table; the
  row now says to check a STAR-Methods Zenodo deposit before the article's own supplement.

And one retrieval row: **`fullTextXML` can 404 for an article that does have a PMCID**, when a
subscription paper is deposited without its XML released. `europepmc.org/articles/<pmcid>?pdf=render`
recovered the full text of both the Science and the Protein Science papers above, including their
data-availability statements. The complementary case — no PMCID at all and `inEPMC:"N"`, as for the
Sci Adv rubisco — has no route and should go straight to 0d.


## Eleventh sweep — 2025 only, enzymes, everything not already ruled on

The first sweep run with the enzyme scope in view rather than implied by query phrasing, and the
first to exclude prior verdicts programmatically: every DOI already on the Curated, Rejected or
Open tabs, and every DOI in a shipped `reference.csv`, was filtered out before ranking, so the 82
papers already decided could not be re-offered.

`(enzyme nouns) AND (library-scale method) AND PUB_YEAR:2025 AND SRC:MED AND OPEN_ACCESS:Y` —
**188 hits, 174 new after filtering**, ranked by signals of a large per-variant enzyme dataset
(assay vocabulary, plus any variant count the abstract states).

### Curated

**Prywes 2025**, *A map of the rubisco biochemical landscape*, Nature 638,
`10.1038/s41586-024-08455-0` — **2 datasets, 8,760 variants each**, on the Form II rubisco large
subunit of *Rhodospirillum rubrum*, 466 aa, in `Activity/CatalyticActivity/DMS/`. A growth-coupled
selection in engineered *E. coli*, where rubisco carboxylation rescues a phosphoribulokinase-
dependent strain, scored **8,760 of the 8,835 possible single amino acid substitutions — 99% of
the protein**. Readouts are carboxylation fitness and relative Vmax, both normalized so wild type
is 1 and catalytically dead mutants are 0.

**Watch the year.** The DOI reads `s41586-`**`024`**`-08455-0` and the version of record is Nature
638 (2025). This is the preprint-year trap the 2022 branch documents, in the DOI rather than in a
ProteinGym field, and it belongs on this branch.

**Phase 3 needed no reconstruction.** The supplement ships `position` and `WTresidue` columns
beside every label, so the sequence falls out of the file, and it matches NCBI `WP_011390153.1` at
all 462 covered positions with no offset. Positions 1, 2, 465 and 466 carry no mutation, so
`sequence` is the full 466-residue protein rather than truncated at the library's edge — the
question Vanella's `SKL` tail made worth asking every time. The library is contiguous over
positions 3-464 with 447 of 462 positions carrying all 19 substitutions.

**Two sources disagree, and the smaller one is right.** The data availability statement names
`github.com/SavageLab/rubiscodms`, but the publisher's Supplementary Data 2 carries the same
readouts and is the version of record. They are not identical: GitHub holds nine mutants the
supplement lacks (A77T, A179T, A179V, F126D, G110P, K310A, N111V, S368G, V24Q) plus a wild-type
row. The supplement's 8,760 is the number the paper itself reports, so this follows the supplement
and records the difference.

**Phase 7, twice, exactly.** 8,760 of 8,835 is 99.15%, against the paper's "more than 99%". And
the nine replicate enrichment columns give 36 pairwise Pearson coefficients averaging **0.9815**,
against the paper's "an average pairwise Pearson coefficient of 0.98".

**The third readout, shipped 2026-09-07.** Apparent CO2 affinity `K_C` is the quantity the paper is
really about and a different measurement from velocity, so it got its own directory —
`Activity/SubstrateAffinity/DMS/`, **5,667 variants**, expressed as `1/K_C` in mM^-1 so higher is
better. Michaelis constants live here rather than under `datasets/Binding/` on purpose: `K_C` is a
kinetic parameter of the catalytic cycle, and `Binding/` holds equilibrium affinities of binding
domains.

**It could not be shipped unfiltered, and the filter is the paper's own.** The full text does not
merely report a coverage figure, it states the cut: it focuses "on the 65% of the mutants (5,687)
that had a coefficient of variation under 1". That is `Km_qbcov`, and `< 1` and `<= 1` select the
same rows — there are no exact ones. An unfiltered `Km_median` column would pass every validator in
this repository and be wrong, because 2,921 of its values are ones the paper itself declines to
interpret.

**Where 5,667 differs from the paper's 5,687, and why that is not an error.** The GitHub deposit
reproduces 5,687 exactly, as 5,686 mutants plus its wild-type row; the publisher's supplement gives
5,667. Chasing the 20 rows down turned up something the earlier write-up on this page got wrong.
**The two files are separate runs of the paper's 1,100-fold bootstrap, not copies of one table.**
On the 8,760 rows they share, *every* `Km_median`, `Vmax_median` and coefficient-of-variation value
differs slightly — median relative difference 0.9% and 0.7% for the two medians — and 72 labels sit
close enough to the cut that the resampling puts them on opposite sides of it. So the gap decomposes
cleanly: 4 rows are GitHub-only and pass (A77T, A179T, A179V, and the wild type), and the other 16
are net bootstrap noise across the threshold, 44 passing only on GitHub against 28 passing only on
the supplement. All three readouts here come from the one supplement file so that a variant's
fitness, velocity and affinity are the same bootstrap run — which is worth more than matching a
headline count from a file the other two did not come from. The shipped remarks on the two sibling
datasets were corrected in the same commit; they had described the difference as nine mutants and a
wild-type row, which was true but incomplete.

**`wt_readout` here is an assumption, not a measurement,** and the remark says so. The Methods fit
each mutant's affinity ratiometrically "with the wild-type KC set to the literature value of 149
μM", so 6.711409 mM^-1 is 1/0.149 mM — the value the fit was built on. It is also what pins the
column to **mM CO2** rather than to a ratio, since the deposit's wild-type `Km_median` is 0.149
against a literature K_C of 149 uM.

**A sanity check the format makes easy to state.** The wild type sits at the 87th percentile of the
shipped column, and 731 of 5,667 variants bind CO2 more tightly than it — a distribution where most
substitutions hurt and a minority help, which is what a saturation library of a highly optimized
enzyme should look like.

### Housekeeping from the same round

The Abeta conformational-antibody lead (`10.3389/fimmu.2025.1655893`) was retired from the Open tab
to Rejected: an antibody is a binding domain, so the enzyme scope excludes it and the NGS-parsing
problem that was blocking it no longer matters.


## Parked: three leads that are not 2025 papers

Worked through on 2026-09-07. Six leads stood on the Open tab; checking each against its Europe PMC
record before spending any more time on it turned up that **half of them are not 2025 papers**, and
that two of the three "blocked" notes were stale. They move to a new **Parked (other years)** tab in
the tracker rather than to Rejected — nothing is wrong with these papers except the branch.

| Lead | DOI | Record says | Was recorded as |
|---|---|---|---|
| Vanella 2024, DAOx EP-Seq | `10.1038/s41467-024-45630-3` | Nat Commun **2024**, reachable | "belongs on the 2024 branch" — correct |
| Fks1 echinocandin DMS | `10.1093/genetics/iyag055` | Genetics **2026**, `inEPMC:Y`, `hasSuppl:Y` | "a Phase 0 data-availability chase" — **stale**, it fetches cleanly |
| Form II rubisco, Gallionella | `10.1126/sciadv.aee9222` | Sci Adv **2026**, `inEPMC:N`, paywalled | "needs the article dropped in by hand" — true, but moot |

Two lessons worth keeping.

**Check the year before checking the paywall.** The Gallionella rubisco was on the list as the one
item needing a human to fetch a PDF. It is a 2026 paper, so fetching it would have repeated on this
branch exactly the mistake the eighth sweep already made — and this time knowingly. The publication
year is one field of the same Europe PMC call that reports `inEPMC`, and it costs nothing to read.

**A blocking note decays faster than the finding it summarizes.** Fks1 was recorded as needing a
data-availability chase; by the time anyone came back to it the article was in PMC, open access,
supplement and all. The note was right when written and wrong when read. This is the same failure
mode the 2026-08-27 audit found in the `remark` fields — a recorded conclusion outliving the state
of the world it described — and the cheap defence is the same: re-run the one query that produced
the note before acting on it.

Fks1 in particular is now the strongest single lead on the whole list — 465 single substitutions
across three hotspots, four conditions on one wild type, in scope and well above the floor. It is
waiting on a `2026` branch, not on any technical problem.


## Rejected on shape: the class A beta-lactamase gatekeeper screen

`10.1016/j.jbc.2025.110347`, *A glycine at position 105 leads to clavulanic acid and avibactam
resistance in class A β-lactamases*, J Biol Chem 2025. This one sat on the Open tab for weeks with
the note "19 substitutions + WT, one row under the floor — worth a second look if the bar is
'genuine deep-sequencing data' rather than 'library-scale'". Worked up properly on 2026-09-07, and
rejected.

**The data is real, and better than the note suggested.** Supplementary Data 2 is a 256 KB legacy
`.xls` (needs `xlrd`, which reads BIFF where `openpyxl` will not), five sheets, one per enzyme. Each
sheet is seven condition blocks — ampicillin, carbenicillin, meropenem, ceftriaxone, clavulanic
acid, sulbactam, avibactam — each block three replicates of raw unselected and selected counts with
per-replicate fitness, then an averaged fitness with an error and a significance call. Nothing about
it is a figure scraped back into numbers.

**It is the shape that fails.** Counting rather than estimating: 35 datasets, 651 variant rows,
mean 18.6, and not one reaches 20.

| Enzyme | WT at 105 | Usable substitutions, per condition |
|---|---|---|
| BlaC | Ile | 19, 17, 19, 19, 19, 19, 19 |
| CTX-M-14 | Tyr | 19 × 7 |
| KPC-2 | Trp | 16, 17, 19, 19, 19, 16, 15 |
| NmcA | His | 19 × 7 |
| TEM-1 | Tyr | 19 × 7 |

The shortfalls are not gaps in the file. Fitness is undefined wherever the selected count is zero,
so KPC-2 under avibactam genuinely has 15 measurable substitutions — the enzyme is killed by the
drug, which is the experiment working.

Three reasons past the count, and the count is the weakest of them.

**A one-position scan is not a landscape.** Every file would hold 19 sequences differing at a single
residue, and the `sequence` column would render that identically to a 5,000-variant DMS. A model
scoring it is ranking 20 amino acids at one site.

**It would distort the repository more than it fills it.** 35 files against the current 156 is 22%
of the dataset count, for 651 of 599,881 variants — 0.11%. Every per-dataset average on the Summary
tab moves, in exchange for almost no data.

**Phase 3 would be five alignments, not one lookup.** Ambler 105 is a structural-alignment number,
not a sequence index; BlaC, CTX-M-14, KPC-2, NmcA and TEM-1 each need their own mapping, and each is
an opportunity to place the substitution on the wrong residue with nothing downstream able to catch
it.

Revisit only if the floor is ever redefined as "genuine deep-sequencing data" rather than
library-scale coverage. That is a defensible bar, and this paper would be the first thing through it.


## Curated: McDonald 2025, tryptophan decarboxylase (RgnTDC)

`10.1002/pro.70356`, *Active site diversification of a non-canonical amino acid decarboxylase by
merging substrate multiplexed screening with computationally guided recombination*, Protein Science
2025. **6 datasets, 27 variants each**, in `Activity/CatalyticActivity/SUMS/`. The last item on the
Open tab, and it came off it because the blocking note was wrong.

**"Upon reasonable request" was true and irrelevant.** The data availability statement does put the
per-variant numbers for the screening libraries behind an email. But the supporting-information PDF
carries a complete, quantified 27-variant validation panel that nobody had opened — Supplementary
Table 2 for the mutation profiles, Supplementary Table 3 for fold activities against twelve
tryptophan analogues. The lesson is the one the Protein Science row in the skill file already half
records: **read the supplement before believing the availability statement**, in either direction.

**Two tables that only work together.** Table 2 is a well-plate manifest — one column per mutated
site (`F98 V99 L339 W349 L355 I343`, note the order, `I343` last) with a letter where a substitution
landed and a blank where it did not. Table 3 is fold activity keyed by the same `V01`-`V27` names.
Neither is a dataset alone. Both were extracted from the PDF by word coordinates with every letter
and number required to land within a few points of a known column centre, the same discipline that
caught the two silent failures in the T7 RNA polymerase tables.

**Phase 3 was unusually clean, and worth the paragraph.** The supplement prints the protein sequence
outright — but the first regex to look for it returned the *DNA*, because `ACGT` is a subset of the
amino-acid alphabet and the nucleotide string was longer. Splitting on the "DNA Sequence" heading
first fixes it. What comes back is the 498-residue C-His construct, and its **first 490 residues are
UniProt A7B1V0 exactly**, with the remainder the `LEHHHHHH` tag. All six mutated positions sit well
inside the native part, so the tagged construct was kept — it is what was on the bench — and the
choice moves no label. Every one of the six positions carries the residue its column header claims.

**Six of twelve substrate columns shipped.** Fold activity is reported to one decimal place, and in
half the columns that is not enough resolution to separate 27 variants:

| Shipped | distinct values | | Dropped | distinct values |
|---|---|---|---|---|
| 5-OEt | 19 | | 4-CN | 5 (19 rows at 0.1) |
| 5-NO2 | 18 | | 4-Br | 5 |
| 6-COOMe | 11 | | β-Me | 5 (20 rows share one) |
| 5-CONH2 | 9 | | 7-I | 5 (21 rows share one) |
| Trp | 9 | | Phe | 2 |
| 4-OMe | 7 | | Tyr | **2** — 26 zeros and a single 0.1 |

The cut is **seven or more distinct values**, i.e. more than a quarter of the panel resolving.
Dropping 4-CN is the uncomfortable one, because V04's 41-fold on 4-cyanotryptophan is a headline
result — but 19 of its 27 rows sit at 0.1, and one outlier would carry the entire z-score. A Tyr
dataset would have passed every check in this repository while containing no information at all,
which is the same failure the rubisco `K_C` filter guards against, in a different disguise.

**Phase 7, four times.** The paper says it "curated a set of 27 diverse, activated variants" — 27.
It says V04 gave "41-fold and 3.5-fold improvements in 4-CN- and 4-OMe-tryptamine production" —
the extracted table gives 40.6 and 3.5. It says "the best 5-NO2-Trp is V05 (23-fold), while the best
5-OEt-Trp is V01 (22-fold)" — the two shipped columns peak at 23.4 on V05 and 22.4 on V01. And it
says those two variants "contain 3 active site mutations, with only the L339M mutation in common":
V05 is `L339M:I343K:W349M`-shaped with three, V01 carries four substitutions of which three are at
active-site positions, and `L339M` is in both. That last one initially read as a contradiction
until the supplement's own annotation — "active site in bold, **I343 underlined**" — made clear that
`F98` is counted outside the active site.

**What is deliberately left behind**, recorded in the remark: the six unresolved substrate columns;
the single-site saturation sub-library and the recombination libraries, whose per-variant numbers
really are only available on request; and the steady-state kinetics, which cover the wild type and a
few variants rather than this panel. Also recorded there, because it matters for how the
distribution should be read: **these 27 are a curated panel, not a library** — chosen across three
library styles to span a range of predicted activity, so they are not a random sample of sequence
space.


## The five validator errors were one bug in the validator

Carried on this page for weeks as "known false positives the skill permits" — five `wt_readout is
empty` errors across three trees, on the Alamos ENTRAPseq dataset, the two Landwehr McbA
combinatorial datasets and the two Jiang T7 RNA polymerase datasets. They were not false positives
and they were not tolerable. They were `validate.py` contradicting itself.

`REFERENCE_REQUIRED` demanded every column except `remark` be non-empty. The check at the bottom of
`check_reference` handles an empty `wt_readout` explicitly, for the case where a dataset has no
wild-type row and the readout is defined against the parent by the paper's own normalization:

```python
elif printed:          # <- only reached when wt_readout is non-empty
```

The blanket rule made that branch unreachable, so the shape it was written to permit could never
occur. `wt_readout` now joins `remark` outside `REFERENCE_REQUIRED`, and the narrower check governs
it alone — matching the WT row when there is one, numeric wherever printed, empty only when there is
no WT row to derive it from. **0 errors and 0 warnings across all three trees, with no dataset
touched.** Fixed on `add-validation` as `849935f`, where the validator lives; nothing on this branch
changed.

**The test that mattered did not fit the harness.** Every existing case in `test_validate.py` has
the shape *corrupt the data, assert the validator rejects it*. The regression test for this fix is
the opposite: *present legitimate data, assert the validator accepts it*. That needed a new
`ACCEPTED` list — because a validator that rejects good data is exactly as broken as one that
accepts bad data, and the suite had no way to say so. Two further cases guard the exemption from
becoming a hole: `wt_readout` must still be present when a WT row exists to check it against, and
must still be a number wherever it is printed.

The new case was watched fail. Against the unpatched `validate.py` the suite reports 25 checks and 1
failure, on exactly that case; against the patched one, 25 and 0. Per the repository's own standard,
a check nobody has watched fail is not evidence of anything — and that cuts both ways for a check
that can only ever pass.

**Worth noting how long this sat.** The errors were recorded, counted, re-counted as they grew from
3 to 5, and written into the skill file as permitted. Nobody opened the validator. The cost of
labelling something a known false positive is that it stops being looked at.


## Audit: what `OPEN_ACCESS:Y` actually cost — 2026-09-07

Six of the eleven sweeps above carried an open-access filter: the third, fourth, fifth, sixth,
eighth, ninth and eleventh all restrict to `OPEN_ACCESS:Y` or say "open access" in their recorded
method. Only the seventh, tenth and the preprint probe ran without it. That is a systematic blind
spot nobody had sized, so this sizes it.

**A caveat that has to come first.** The exact boolean of several earlier sweeps was not recorded
verbatim — the eleventh, for instance, is written down as "(enzyme nouns) AND (library-scale
method)". The queries below are *reconstructions*, and they are broader than the originals: the
eleventh-sweep reconstruction returns 915 open-access hits against the 188 actually recorded. So
the **rates** are indicative of what this filter does to this kind of query, not an audit of what
each historical sweep missed. The reachability counts underneath them are exact.

| Reconstructed family, `PUB_YEAR:2025 AND SRC:MED` | all | `OPEN_ACCESS:Y` | `OPEN_ACCESS:N` | hidden |
|---|---|---|---|---|
| DMS phrasing, all publishers | 644 | 498 | 146 | 23% |
| enzyme × library-scale method | 1,819 | 915 | 904 | 50% |
| PNAS | 103 | 101 | 2 | **2%** |
| ACS five journals | 207 | 76 | 131 | **63%** |
| Cell Press | 144 | 101 | 43 | 30% |

**The filter was mostly excluding papers that are readable anyway.** This is the finding that
matters, and it is exact rather than reconstructed. Of the 146 closed-access hits in the DMS family,
**104 have a PMCID and `inEPMC:"Y"`** — Europe PMC holds the full text right now — and 66 have
supplementary files. Only 42 are genuinely dark. `OPEN_ACCESS:Y` is a licence flag, not a
reachability flag, and treating the two as the same thing is what caused the blind spot. In the
broader enzyme family the ratio inverts (61 reachable of 904), because that query drags in a long
tail of subscription-only reviews from journals no sweep should be reading anyway.

**Of the genuinely dark papers, the best two have open preprints.**

| Paper | Route |
|---|---|
| *Engineering highly active nuclease enzymes with machine learning and high-throughput screening*, Cell Syst, `10.1016/j.cels.2025.101236` | bioRxiv `10.1101/2024.03.21.585615` — **open** |
| *Evaluation of machine learning-assisted directed evolution across diverse combinatorial landscapes*, Cell Syst, `10.1016/j.cels.2025.101387` | bioRxiv `10.1101/2024.10.24.619774` — **open** |

Both are Cell Systems, both 2025, both `inEPMC:"N"` — so the sixth sweep's open-access filter is
exactly what hid them. The nuclease paper (TeleProt) is in scope on its face and worth a Phase 0.
The second is an *analysis over 16 existing* fitness landscapes rather than a new measurement, so
it is more likely a source of already-published data than a candidate, but it should be read before
that is asserted.

Two more from the dark set are worth a look and neither needs anyone's library card, only time:
`10.1002/bit.70041`, a DMS of the AAV *rep* gene covering all single codon substitutions at ~300
sites — library-scale, and Rep is a helicase/endonuclease so it clears the enzyme scope, though its
readout is virion packaging rather than catalysis; and `10.1093/protein/gzaf011`, TEV protease
engineered by enzyme-substrate co-display on yeast. The remainder of the ranked dark list is
semi-rational design of a handful of mutants, strain engineering, or reviews that scored well only
because review abstracts are dense in the vocabulary the ranker rewards.

**What to change.** Drop `OPEN_ACCESS:Y` from the sweep template and filter on `inEPMC` instead,
which is what the queries were trying to express. When a paper really is dark, check for a bioRxiv
version before recording it as unreachable — `TITLE:"..." AND SRC:PPR` finds them, and two of the
two best candidates here had one.


## Twelfth sweep — sweeps 3, 6 and 11 re-run without the open-access filter

The audit above said the filter was worth removing; this removes it. Each family was re-queried
with `OPEN_ACCESS:N` — precisely the population the original sweep could not see — every record
paged out in full, prior verdicts excluded, and the remainder scored for enzyme scope and
library scale with reviews screened out by `pubType`.

Sweeps 4/7 and 5 were not re-run and did not need to be: the seventh sweep's recorded query
already carries no open-access clause, so ACS was covered, and PNAS hides two papers in total.

| Sweep | closed-access hits | new | screened out | scored |
|---|---|---|---|---|
| 3 — DMS phrasing, all publishers | 146 | 142 | 47 no enzyme noun, 41 reviews | 54 |
| 6 — Cell Press | 44 | 44 | 31 no enzyme noun, 4 reviews | 9 |
| 11 — enzyme × library-scale | 904 | 901 | 223 reviews | 678 |

**The yield is two papers, and the tail is as thin as the tenth sweep predicted.** Nearly
everything scoring above the noise is semi-rational design of a handful of mutants, one-champion
biocatalysis, or a *Methods in Enzymology* chapter. Representative of the rest: nattokinase
residue 131, a single position; a glucose oxidase paper whose "single-point saturation mutation"
is a shortlist from computational screening; a penicillin G acylase study whose 1,130 "variants"
are 4D-QSAR *predictions* rather than measurements. The engineered-Mannichase chapter
(`10.1016/bs.mie.2025.08.007`) is readable and in scope but ends at one champion, LolT-V4, at
60-fold — the pattern the directed-evolution sweep named.

### The two that matter

**`10.1016/j.cels.2025.101236`** — *Engineering highly active nuclease enzymes with machine
learning and high-throughput screening*, Cell Systems 2025. The abstract states it outright:
**"We have released a dataset of 55,000 nuclease variants, one of the most extensive
genotype-phenotype enzyme activity landscapes to date."** A nuclease is squarely in the enzyme
scope, the readout is catalytic activity, and 55,000 would make it among the largest single
datasets in this repository. Authors are Google Research (Thomas, Belanger, Colwell) with a
droplet-microfluidics screen.

**`10.1016/j.celrep.2025.116446`** — *Multi-environment deep mutational scanning reveals the
distribution of temperature-sensitive variants in a bacterial kinase*, Cell Reports 2025. A real
DMS of an enzyme across **multiple temperatures** — several conditions on one wild type, which
is several datasets — and the paper's own point is that single-condition landscapes hide
condition-dependent effects. It appeared in both the sweep 3 and sweep 6 re-runs.

### The finding that outlasts these two papers

**Europe PMC's `OPEN_ACCESS` flag misclassified both of them.** Each is recorded as
`OPEN_ACCESS:"N"`, `inEPMC:"N"`, `pmcid=None`. Crossref lists both as carrying
`creativecommons.org/licenses/by/4.0/` on the version of record, and Unpaywall confirms it:
the Cell Reports paper is `oa_status: gold` with a direct PDF URL, the Cell Systems paper
`oa_status: hybrid`. Neither is behind a paywall at all. The flag describes *Europe PMC's
holdings*, not the article's licence, and six sweeps treated the two as the same thing.

`api.unpaywall.org/v2/<doi>?email=<addr>` is the authoritative check and costs one request. It
is now a row in the skill file's 0c table, together with the second half of the lesson: both PDFs
return **403** to an automated fetch, because `cell.com` and `biorxiv.org` block agents
irrespective of licence. That is the rare case that is genuinely a hand-off — the file is free to
a person with a browser, so the right move is to hand over the exact URL rather than grind
through mirrors.

Three others were checked the same way and are **not** worth a hand-off: `10.1093/protein/gzaf011`
(TEV protease, PEDS) has `PMC13010152` already assigned but `live: False`, so it will free itself
on embargo expiry and only needs re-checking; `10.1002/bit.70041` (AAV *rep* DMS) and
`10.1016/j.cels.2025.101387` (an evaluation across 16 *existing* landscapes, so more likely a
pointer to published data than a new measurement) are genuinely closed.


## Curated: Ghose 2025, EnvZ histidine kinase across temperatures

`10.1016/j.celrep.2025.116446`, Cell Reports 2025 — the stronger of the two papers the twelfth
sweep recovered. **2 datasets, 1,140 variants each**, in `Activity/CatalyticActivity/DMS/`.

**Curated from the deposit, not the article.** The paper is CC-BY and `cell.com` still refuses it to
an automated fetch, so the article was never read. What made this curatable anyway is that its data
availability statement names a MaveDB accession, `urn:mavedb:00001240-a`, and MaveDB carries the
authors' own method text alongside the numbers. Every claim in the remarks rests on that deposit;
the remarks say so, because it is a weaker provenance than a paper read end to end.

**Phase 3 fell out of the deposit.** MaveDB's target is the 60-residue EnvZ DHp domain with labels
numbered 1–60 inside it. Those 60 residues occur exactly once in UniProt P0AEJ4, the 450-residue
*E. coli* K-12 EnvZ, at **residues 230–289** — the very positions the deposit names. So the offset
is +229, every label was rewritten into full-length numbering, and the shipped `sequence` is the
whole 450-residue protein rather than the mutated domain, following the Prywes precedent. All 1,200
wild-type residues checked against that sequence with no mismatch.

**The scope call.** EnvZ activity is read as GFP expression downstream of its cognate regulator
OmpR. That is a transcriptional output, and the Jansen CymR curation was reverted on scope for
being transcriptional — but the distinction holds: CymR *is* a transcriptional regulator, a
DNA-binding protein, while EnvZ is a kinase and the reporter is how its catalysis is observed. The
protein decides the scope, not the instrument. Filed under catalytic activity, with the indirect,
non-baseline-subtracted readout stated in the remark.

### One of the three temperatures was dropped, and this is why

The experiment ran at 30 °C, 37 °C and 42 °C, and the obvious move was three datasets. The
experiment ships its own control against that: **59 nonsense variants**, which truncate the kinase
and must be dead.

| | wild-type `score` | median nonsense `score` | substitutions on the dead side |
|---|---|---|---|
| 30 °C | 3.73 | 2.26 | 13% |
| 42 °C | 3.73 | 2.15 | 10% |
| **37 °C** | **3.639** | **3.754** | **50%** |

At 37 °C a truncated EnvZ scores *higher* than the intact one, and half the substitutions fall on
the dead side of the nonsense median — the signature of a column carrying no signal.
`fold_induction` does not rescue it: there it does separate wild type (73.3) from nonsense (1.18),
but puts the median substitution at 1.16, indistinguishable from dead, which would make nearly every
mutation lethal at 37 °C and contradict the paper's own headline of high mutational tolerance. The
37 °C file is also the only one of the three carrying full float precision rather than values
rounded to two decimals, so it looks to have been processed differently. Without the methods that
cannot be resolved, so it is left out.

**What flagged it was not the control, it was a correlation that made no sense.** The paper says
temperature-associated changes in activity are rare, which should mean the three arms agree closely.
They did not: Pearson *r* was 0.21 between 30 °C and 37 °C. Chasing that discrepancy rather than
recording it as noise is what turned up the inverted control. The two surviving arms correlate at
0.49 (Spearman 0.60), which is unremarkable for a DMS with this dynamic range.

**A second thing the arithmetic caught.** `score` never leaves 0.8–4.7 in any arm, and 10 rows at
30 °C and 41 at 42 °C sit at exactly 0.8. Those are the ends of the sorting range, not measurements,
and the remark says a variant at the floor should be read as "at or below it".

**Recorded but not used**, because it cannot be pinned down without the paper: `fold_induction`.
It is the baseline-controlled quantity and would arguably be the better readout, but it is not the
deposit's designated score and it does not equal `10**(score - mean_off)` across the file — 112 of
1,201 rows at 30 °C, 631 of 1,200 at 42 °C. What it is exactly is unknown, so it stays unshipped
rather than guessed at.

Worth noting for anyone re-checking: the MaveDB record's linked publication is
`10.1073/pnas.2221163120`, an earlier paper from the same laboratory, not the Cell Reports paper.
The DOI recorded in `reference.csv` is the Cell Reports one, since that is the paper whose data
availability statement names the accession.


## Curated: Thomas 2025, the NucB nuclease campaign — the largest paper on this branch

`10.1016/j.cels.2025.101236`, Cell Systems 2025, the other paper the twelfth sweep recovered.
**4 datasets, 58,137 variants**, in a new `Activity/CatalyticActivity/TeleProt/`. NucB, the
biofilm-dispersing nuclease of *Bacillus licheniformis*, 142 residues, **byte-identical to UniProt
F1BV52** — the cleanest Phase 3 on this branch, no tag, no truncation, no reconstruction.

**The article was never opened, and it did not need to be.** cell.com refuses the CC-BY PDF to an
automated fetch. But the trail from the paper's own pointer — `github.com/google-deepmind/
nuclease_design`, Apache-2.0 — led through `constants.py` to a public bucket,
`storage.googleapis.com/nuclease_design`, holding the whole campaign.

**The advertised dataset is not the best dataset in the deposit.** The abstract headlines "a dataset
of 55,000 nuclease variants, one of the most extensive genotype-phenotype enzyme activity landscapes
to date", and `landscape.csv` duly has 55,760 rows. Its activity column is a **four-level ordinal** —
`non-functional` (33,890), `activity > 0` (11,099), `activity > WT` (10,572), `activity > A73R`
(199). Z-scoring that would have produced 55,760 rows carrying four distinct values, the same
degeneracy that disqualified TDC's Tyr column at 1/2000th the scale. The bucket's
`processed_data/g1–g4.csv` hold the **continuous enrichment factors** the ordinal was thresholded
from, and those are what shipped.

**Phase 7, exactly.** The union of genotypes across the four generation files is **55,759 distinct
mutants** — precisely `landscape.csv`'s 55,759 mutants plus its one wild type, 100% overlap, none
missing in either direction. The four files reconstruct the paper's headline set and improve its
resolution at the same time.

### The gate choice, and a recommendation that was wrong

Each generation was sorted at several stringencies, and the plan was one dataset per generation at
the most stringent gate, on the reasoning that it would give the widest dynamic range. **The data
says the opposite.**

| Generation | most stringent gate | zeros | separates the deposit's own "beats WT" labels? |
|---|---|---|---|
| g3 | `ef_2_99` | 16,530 / 18,618 (89%) | **no** |
| g4 | `ef_4_99.5` | 14,027 / 15,404 (91%) | **no** |

A stringent gate recovers almost nothing, so most variants are simply absent from the output and
their enrichment factor collapses to zero. The gate actually shipped for each generation is the one
with the fewest zeros and the most distinct values that still separates those labels: `ef_3_high_g1`,
`ef_1_86_g2`, `ef_1_59_g3`, `ef_1_70_g4`. The others are left unshipped rather than averaged,
because a mean across stringencies is not a quantity the experiment measured.

**Zeros are censored, not measured**, and this is the thing to read before using these files. Even
at the best gate, 58% of g1, 55% of g2, 23% of g3 and 29% of g4 are exactly zero — the variant was
never seen in the sorted output, rather than measured as having no activity. They are kept, because
dropping them would bias each file toward what survived selection, but a zero means "at or below
detection". Wysocki's rubisco is the precedent, at up to 79%.

**Model token.** `TeleProt` is the paper's own named platform, which outranks `DMS` and `ML` under
the skill file's rule, so it takes the directory and the filename slot.


## A note on this file's name

`candidates_2025.md` now holds a 2026 sweep, and the tracker beside it is
`FitnessBench_2025_literature_search.xlsx` on a branch called `2025`. The year in all three
names has stopped describing the contents. Renaming touches the tracker's own pointer back
to this file and the branch both, so it is left as it stands and flagged here.
