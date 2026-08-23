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

### Shortlisted, not yet worked

| Paper | DOI | Why |
|---|---|---|
| Deep mutational scanning of the multi-domain phosphatase SHP2 | `10.1038/s41467-025-60641-4` | full DMS of a multi-domain signalling enzyme |
| Deep Mutational Scanning of FDX1 | `10.1038/s41467-025-67869-0` | ferredoxin, lipoylation and cuproptosis |
| EGFR resistance to 4th-generation TKIs | `10.1038/s41698-025-01086-2` | the EGFR analogue of the MET study; human, so `datasets_human/` and lower priority |
| Reshaping a glycoside hydrolase active site | `10.1021/acscentsci.5c01227` | ACS, a genuine carbohydrate-active enzyme |
| DMS in *E. coli* | `10.1073/pnas.2516165122` | PNAS |
| Glucokinase variant characterization | `10.3390/ijms27010156` | clinical variant panel |

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
