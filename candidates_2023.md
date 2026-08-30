# 2023 candidate papers

Screening notes for the `2023` branch — papers published in 2023 that may yield
FitnessBench datasets. Nothing here is curated yet; this is the shortlist that
step 1 of `example_workflow.md` should start from.

The branch is cut from `main`, matching how `2024` and `2025` were cut, so it starts
from the six Jiang 2024 PRIME datasets and nothing else.

## What makes 2023 different from 2025

Two facts reshape the year, and both were established before any paper was opened.

**ProteinGym's newest assays are from 2023, and only from 2023.** The `2025` branch was
able to record that "a 2025 sweep cannot collide with the current release". The opposite
holds here: of ProteinGym's 217 DMS substitution assays, **87 carry `year = 2023`** — 40%
of the entire benchmark — drawn from 20 source publications. Sixty-four of the 87 come
from one paper, Tsuboyama's mega-scale folding stability study.

The decision taken for this branch is to **curate 2023 regardless of that overlap**.
ProteinGym is a compilation of other people's measurements, and the rule that a
compilation is never curatable under a compiler's name cuts the other way here: the
primary papers are the measurers, and they are curatable under their own names. The
formats also differ — FitnessBench carries a verified wild-type sequence, a stated
higher-is-better orientation, and a z-score, none of which ProteinGym's per-assay files
provide. Overlap is recorded per row in the tracker rather than used as an exclusion.

**ProteinGym's `year` is the preprint year, not the version of record.** Thirteen of the
twenty 2023 source publications are cited by their bioRxiv DOI. Chasing each to its
published version moves eight of them into 2024:

| ProteinGym cites | Version of record | Year |
|---|---|---|
| `10.1101/2023.05.28.542639` Nguyen, metabolic interaction | `10.1038/s41467-024-47671-0` Nat Commun | **2024** |
| `10.1101/2022.10.31.514613` Ding, structure-based residue preferences | `10.1038/s41467-024-45621-4` Nat Commun | **2024** |
| `10.1101/2023.04.28.538612` Muhammad, KCNE1 | `10.1186/s13073-024-01340-5` Genome Med | **2024** |
| `10.1101/2023.06.08.544160` Clausen, Parkin atlas | `10.1038/s41467-024-45829-4` Nat Commun | **2024** |
| `10.1101/2023.05.24.542036` Gersing, glucokinase abundance | `10.1186/s13059-024-03238-2` Genome Biol | **2024** |
| `10.1101/2023.08.03.551866` Estevam, MET juxtamembrane | `10.7554/eLife.91619` eLife | **2024** |
| `10.1101/2023.02.24.529916` Vanella, enzyme proximity sequencing | `10.1038/s41467-024-45630-3` Nat Commun | **2024** |
| `10.1101/2023.06.06.543963` Yee, OCT1 spectrum | `10.1016/j.molcel.2024.04.008` Mol Cell | **2024** |

Those eight belong to the `2024` branch, not this one. Phase 0 as hardened on 2026-08-24
forbids curating from a preprint at all — *"a locator taken from a preprint sends the user
to the wrong file"* — so there is no option to take them here under their bioRxiv numbering.

Two preprints could not be resolved to any journal version and are parked in **Maybes**:
Suphatrakul (dengue NS5) and Xie (compound heterozygous genotypes).

## Where these came from

All sweeps run against the Europe PMC REST API, `PUB_YEAR:2023 AND OPEN_ACCESS:Y AND
SRC:MED`, which is reproducible in a way the nature.com search box is not.

| Sweep | Query | Hits |
|---|---|---|
| ProteinGym cross-reference | `reference_files/DMS_substitutions.csv`, filtered to `year = 2023` | 87 assays / 20 papers |
| DMS | `"deep mutational scan(ning)" OR "variant effect map" OR "mutational scanning"`, `HAS_SUPPL:Y` | 200, top 100 screened |
| ML / engineering | `("machine learning" OR "deep learning" OR "language model") AND ("enzyme engineering" OR "protein engineering" OR "directed evolution")`, `HAS_SUPPL:Y` | 220, top 100 screened |
| Directed evolution | `"directed evolution"` | 876, not yet screened |

Screening is on title, abstract and data-availability statement. Supplementary files have
**not** been opened for anything still marked a candidate, so variant counts below are the
papers' own claims or ProteinGym's counts, not verified sheet contents.

## Tier A — 2023 version of record, per-variant data already confirmed by ProteinGym

Nine publications, after Tsuboyama was worked and skipped (below). Counts are ProteinGym's, and are a floor: they cover only the assays it
ingested, not necessarily everything the paper measured.

| # | Paper | DOI | Assays | Mutants | Notes |
|---|---|---|---|---|---|
| 1 | Chen 2023, *Deep Mutational Scanning of an Oxygen-Independent Fluorescent Protein CreiLOV* | `10.1021/acssynbio.2c00662` | 1 | 167,529 | ACS Synth Biol. Largest single assay in the cohort. ACS retrieval is the known-painful route |
| 2 | Li 2023, *Functional constraints and evolutionary potential of the influenza polymerase* | `10.1128/jvi.01329-23` | 1 | 12,003 | J Virol. `datasets_virus` |
| 3 | Gill 2023, *Self-association of chemokine receptors CXCR4 and CCR5* | `10.1016/j.jbc.2023.105229` | 1 | 6,137 | JBC. Human |
| 4 | van Loggerenberg 2023, *Systematically testing human HMBS missense variants* | `10.1016/j.ajhg.2023.08.012` | 1 | 5,689 | AJHG. Human |
| 5 | Weeks 2023, *Fitness and functional landscapes of the E. coli RNase III gene rnc* | `10.1093/molbev/msad047` | 1 | 4,277 | Mol Biol Evol. Growth fitness, one protein — the cleanest first item |
| 6 | MacRae 2023, *Protein–protein interactions in the Mla lipid transport system* | `10.1016/j.jbc.2023.104744` | 1 | 4,007 | JBC |
| 7 | Lo 2023, *Functional impact of 1,570 substitutions in human OTC* | `10.1016/j.ajhg.2023.03.019` | 1 | 1,570 | AJHG. Human |
| 8 | Meier 2023, *Deep mutational scan of a drug efflux pump* | `10.1038/s41589-022-01205-1` | 2 | 1,444 | Nat Chem Biol. 2022 DOI, 2023 issue |
| 9 | Ghose 2023, *Marginal specificity in protein interactions* | `10.1073/pnas.2221163120` | 1 | 1,121 | PNAS |

## Tier B — additive, not in ProteinGym

From the DMS sweep. 2023 is heavily viral, so most of these land in `datasets_virus/`.

- `10.1016/j.cell.2023.02.001` — *A pseudovirus system enables deep mutational scanning of
  the full SARS-CoV-2 spike*, Cell. The most-cited DMS of the year that ProteinGym does not
  hold; full-spike libraries, Bloom-lab deposits are consistently machine-readable.
- `10.1016/j.celrep.2022.111951` — *Mutational fitness landscape of human influenza H3N2
  neuraminidase*, Cell Rep.
- `10.1038/s41467-023-35940-3` — **CURATED** as Dewachter 2023, three datasets (FabZ, LpxC, MurA).
- `10.1038/s41467-023-37786-1` — **CURATED** as Tan 2023, two datasets (expression, membrane fusion).
- `10.1371/journal.ppat.1011901` — *Deep mutational scans of XBB.1.5 and BQ.1.1*, PLoS Pathog.
- `10.26508/lsa.202302043` — *Missense variant interaction scanning, FERM domain*, Life Sci Alliance.
- `10.1093/ve/vead055` — *Fitness effects of mutations to SARS-CoV-2 proteins*, Virus Evol.
- `10.1128/jvi.01414-23` — *Single mutations in Zika virus envelope and antibody escape*, J Virol.

## Rejected on sight — the Phase 1 exclusion, which dominates 2023

The ML/engineering sweep for 2023 returns overwhelmingly **prediction tools evaluated on
other people's data**, which Phase 1 excludes: a dataset a paper merely evaluates on belongs
to whoever measured it. From the top 100: `FireProt 2.0`, `SESNet`, `DeepTP`, `UniKP`,
`ASCARIS`, `Sequence UNET`, `MpbPPI`, `DG-Affinity`, `RNAdegformer`, `PredictONCO`,
`DEEPCYPs`, rapid stability prediction from deep learning representations, *Updated
benchmarking of variant effect predictors*, and *Zero-shot mutation effect prediction*.

Method and monitoring papers go the same way: `ACIDES` (online monitoring of forward genetic
screens), `SUNi mutagenesis` (library construction), `LibGENiE` (library design).

This is the clearest structural difference from 2025 after the ProteinGym collision — the
2023 ML-for-proteins literature is a tooling literature, and tooling papers do not measure.

## Tier C — 2023 engineering campaigns that do measure

The minority of the ML/engineering sweep that carries its own variants. Not yet chased.

- `10.1126/science.abn0966`-shaped: *Deploying synthetic coevolution and machine learning to
  engineer protein–protein interactions*, Science — DOI to confirm.
- *Machine learning optimization of candidate antibody yields highly diverse sub-nanomolar
  affinity antibody libraries*, Nat Commun.
- *Enhancing luciferase activity and stability through generative modeling of natural enzyme
  sequences*, PNAS.
- *Machine Learning-Supported Enzyme Engineering toward Improved CO₂-Fixation of
  glycolyl-CoA carboxylase*, ACS Synth Biol.
- *Repertoire of Computationally Designed Peroxygenases for Enantiodivergent C–H
  Oxyfunctionalization*, JACS.

## Maybes

- **Suphatrakul, dengue NS5 deep mutational scan**, `10.1101/2023.03.07.531617` — 16,897
  mutants in ProteinGym. No journal version found by title or by author-plus-keyword search.
  Under the hardened Phase 0 the preprint is not curatable; this needs either a version of
  record or a decision to make an exception.
- **Xie, compound heterozygous genotypes from variant effect maps**, `10.1101/2023.01.11.523651`
  — 1,914 mutants. Same position.

## Worked and skipped

**Tsuboyama 2023**, *Mega-scale experimental analysis of protein folding stability in biology
and design*, `10.1038/s41586-023-06328-6` — **taken through Phase 0 and Phase 1, then skipped
on scope.** Recorded here because nothing shipped, so there is no `remark` anywhere to hold it.

Everything needed is retrievable and the paper is in excellent shape. The article PDF comes
from the publisher with a browser user agent, and the Data availability statement points at
Zenodo `10.5281/zenodo.7992926`, whose `Processed_K50_dG_datasets.zip` carries
`Tsuboyama2023_Dataset2_Dataset3_20230416.csv` — one row per variant with `WT_name`,
`mut_type`, the variant `aa_seq` with the SAGG linkers already stripped, and `deltaG` in
kcal/mol with a 95% confidence interval. ΔG is a folding stability, so it is higher-is-better
as shipped and needs no inverting. Phase 2 and the orientation are settled; nothing was
blocking.

What stopped it is size. `Single_DMS_list.csv` enumerates **983 domains** carrying a complete
single-mutant scan, 26 to 74 residues each — **534 natural** (PDB-named) and **449 de novo
designed**. One domain is one protein, so one domain is one dataset, and the paper would
therefore land 983 rows and roughly 776,000 variants on this branch in a single PR. ProteinGym
takes 64 of them, all of which matched a row here by exact sequence.

The double mutants (210,118 across 559 site pairs in 190 domains), the single deletions and
the two insertions at every position are skipped with it. Deletions and insertions have no
representation in a `{WT}{pos}{MUT}` mutant column in any case.

**If it is picked up later**, the work is Phase 3 onward on a chosen subset, and the natural
domains are the obvious first cut. The Zenodo archive is 1 GB and takes about five minutes to
fetch; a copy of it and of the article PDF is in scratch at `C:/tmp/fbdl/tsu/`, which is
outside the repo and will not survive indefinitely.

**Ollikainen/Sievers 2023**, *Functional E3 ligase hotspots and resistance mechanisms to
small-molecule degraders*, `10.1038/s41589-022-01177-2` — **worked and rejected, no scored
variant table.** Recorded here because nothing shipped.

The saturation mutagenesis of VHL and CRBN under degrader selection is real and the raw data
is public, but the only per-variant deposit is `GSE198280`, which holds
`*.gatk.aaCounts.txt.gz` — a position-by-amino-acid **count** matrix per sample, 44 of them,
with no position labels and no score. The enrichment landscape the paper analyses exists only
as heat maps in Figs. 1–5. The publisher's single workbook is hybrid-capture MuTect2 allele
frequencies at genomic coordinates, a resistance-hit list rather than a landscape, and the
Supplementary Information carries only a gene-capture list, a degrader list, crystallography
statistics and oligo sequences.

Building a dataset would mean re-implementing the authors' normalization from raw counts,
choosing their filtering thresholds, and having no published per-variant table to check the
result against. That is the same shape as the FDX1 rejection already recorded on the `2025`
branch, and it falls under the consolidated reject condition for data that exists only in a
figure.

## Status

| | |
|---|---|
| Curated | Weeks (3 datasets), Meier (6), Dewachter (3), Tan (2) — **14 datasets** |
| Worked and skipped | Tsuboyama, on scope |
| Worked and rejected | E3 ligase degrader resistance, no scored variant table |
| Nature-family remaining | none — the family is exhausted for this shortlist |

Everything still open is outside the Nature family: Tier A's Chen (ACS Synth Biol), Li
(J Virol), Gill and MacRae (JBC), van Loggerenberg and Lo (AJHG), Ghose (PNAS); and Tier B's
Cell, Cell Reports, PLoS Pathogens, Life Science Alliance, Virus Evolution and J Virol items.
