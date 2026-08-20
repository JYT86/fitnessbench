# 2025 candidate papers

Screening notes for the `2025` branch — papers published in 2025 that may yield
FitnessBench datasets. Nothing here is curated yet; this is the shortlist that
step 1 of `example_workflow.md` should start from.

## Where these came from

Two nature.com searches, both restricted to `date_range=2025-2025`, ordered by relevance:

- `machine learning guided enzyme engineering in prokaryotes` — **6 results**
- `machine learning guided enzyme engineering in eukaryotes` — **16 results**

20 unique articles, 22 hits (2 appear in both). Screened on title, abstract and
data-availability statement. Supplementary files have **not** been downloaded or
opened yet, so variant counts below come from the article text, not from the sheets.

## Shortlist

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

Twenty articles for a whole year is thin, and most of them are reviews — the query is a
natural-language sentence and nature.com matches it loosely. Two obvious gaps: it covers
Springer Nature journals only, so *Science*, *JACS*, *ACS Catalysis*, *Nature Catalysis*
preprints and bioRxiv are all invisible, and "enzyme engineering" misses directed-evolution
and deep-mutational-scanning papers that never use the phrase. If the 2025 set needs more
than three datasets, widen the net before curating.
