# 2022 candidate papers

Screening notes for the `2022` branch — papers published in 2022 that may yield
FitnessBench datasets. Nothing here is curated yet; this is the shortlist that
step 1 of `example_workflow.md` should start from.

Cut from `main`, as `2023`, `2024` and `2025` were, so it starts from the six Jiang 2024
PRIME datasets and nothing else.

## What 2022 looks like

**ProteinGym overlaps, but far less than 2023.** The benchmark holds 22 assays carrying
`year = 2022` against 87 for 2023. After the version-of-record correction below that becomes
**17 assays across 10 publications** — a fifth of the 2023 collision. The decision taken on the
`2023` branch stands here: curate regardless of overlap, and record it per row.

**The preprint-year trap applies again, and in both directions.** ProteinGym's `year` is the
preprint year. Four of the fifteen 2022-labelled publications are cited by bioRxiv DOI, and
chasing each to its version of record moves five assays out of this branch:

| ProteinGym cites | Version of record | Goes to |
|---|---|---|
| `10.1101/2022.05.04.490571` Gersing, glucokinase activity map | `10.1186/s13059-023-02935-8` Genome Biol | **2023** |
| `10.1002/pro.4656` Nguyen, Hsp90 dependence of Src | Protein Sci, published 2023 | **2023** |
| `10.1101/2022.12.06.519122` + `...519127` Weng, KRAS landscape (two halves) | `10.1038/s41586-023-06954-0` Nature | **2024** |
| `10.1101/2021.12.05.471322` Chakraborty, Src drug resistance | `10.1016/j.chembiol.2023.08.005` Cell Chem Biol | **2024** |

Note the Gersing case in particular: the `2023` branch already records a *different* Gersing
paper, the 2024 multiplexed abundance assay. These are two separate glucokinase studies, and
only the 2023 activity map belongs on the 2023 branch.

**The year's character is SARS-CoV-2.** Where 2023's additive seam was viral and 2025's was
enzyme engineering, 2022's is overwhelmingly coronavirus: RBD antibody escape, ACE2 binding,
Omicron antigenic characterisation, Mpro and 3CL protease maps. Most of it belongs in
`datasets_virus/`.

## Where these came from

Europe PMC REST, `PUB_YEAR:2022 AND SRC:MED`, reusing the axes that proved productive on the
2023 branch. The 2023 calibration carries over: the first 100 hits hold nearly all the
experimental signal, and publisher-restricted sweeps find what the vocabulary sweeps miss.

| Sweep | Hits |
|---|---|
| ProteinGym cross-reference, `year = 2022` | 22 assays / 15 publications |
| DMS vocabulary, open access, with supplements | 377, top 100 screened |
| Nature family, eight titles | 143, top 100 screened |
| Cell Press, seven titles | 22, all screened |

## Tier A — ProteinGym-confirmed, 2022 version of record

Ten publications, 17 assays. Counts are ProteinGym's and are a floor.

| # | Paper | DOI | Assays | Mutants | OA | Notes |
|---|---|---|---|---|---|---|
| 1 | Somermeyer, *Heterogeneity of the GFP fitness landscape* | `10.7554/eLife.75842` | 3 | 89,426 | yes | eLife. Three GFP homologues, the largest item here and open |
| 2 | Faure, *Mapping the energetic and allosteric landscapes of protein binding domains* | `10.1038/s41586-022-04586-4` | 2 | 70,342 | no | Nature. Doubles as well as singles, so it carries a scope question |
| 3 | Seuma, *An atlas of amyloid aggregation* | `10.1038/s41467-022-34742-3` | 1 | 14,811 | yes | Nat Commun. Substitutions, insertions and deletions — only the substitutions convert |
| 4 | Coyote-Maestas, *Determinants of trafficking, conduction and disease in a K+ channel* | `10.7554/eLife.76903` | 2 | 13,880 | yes | eLife. Two readouts on one library, the shape that gave Weeks three datasets |
| 5 | Kwon, *Structure-function analysis of the SHOC2-MRAS-PP1C holophosphatase* | `10.1038/s41586-022-04928-2` | 1 | 10,972 | no | Nature |
| 6 | Miller, *Allosteric inhibition of PPM1D phosphatase* | `10.1038/s41467-022-30463-9` | 1 | 7,889 | yes | Nat Commun |
| 7 | Flynn, *Comprehensive fitness landscape of SARS-CoV-2 Mpro* | `10.7554/eLife.77433` | 1 | 5,725 | yes | eLife. `datasets_virus` |
| 8 | Hobbs, *Saturation mutagenesis of a predicted ancestral Syk-family kinase* | `10.1002/pro.4411` | 1 | 4,670 | yes | Protein Sci |
| 9 | Roychowdhury, *Microfluidic deep mutational scanning of the human executioner caspases* | `10.1038/s41420-021-00799-0` | 2 | 3,247 | yes | Cell Death Discov. Two caspases |
| 10 | Erwood, *Saturation variant interpretation using CRISPR prime editing* | `10.1038/s41587-021-01201-1` | 3 | 965 | no | Nat Biotechnol. Smallest, and three genes, so each may sit near the 20-variant floor |

Seven of the ten are open access, which is a better starting position than the Cell Press group
that stalled the 2023 queue.

## Tier B — additive, not in ProteinGym

From the DMS, Nature-family and Cell Press sweeps. Heavily viral, as expected for the year.

- `10.1016/j.cell.2022.08.010` — *Deep mutational scanning identifies SARS-CoV-2 Nucleocapsid
  escape mutations*, Cell.
- `10.1016/j.cell.2022.08.024` — *Deep mutational learning predicts ACE2 binding and antibody
  escape to combinatorial RBD mutations*, Cell. Combinatorial, so check the genotype encoding.
- `10.1016/j.chom.2022.08.003` — *Functional map of SARS-CoV-2 3CL protease*, Cell Host Microbe.
- `10.1016/j.chom.2022.09.003` — *The evolutionary potential of influenza A hemagglutinin is
  highly constrained*, Cell Host Microbe.
- `10.1371/journal.ppat.1010951` — *Deep mutational scans for ACE2 binding, RBD expression and
  antibody escape*, PLoS Pathog.
- `10.1126/sciadv.add7221` — *Biophysical constraints of the SARS-CoV-2 spike N-terminal domain*,
  Sci Adv.
- `10.1038/s41467-022-34506-z` — *Compensatory epistasis maintains ACE2 affinity in Omicron
  BA.1*, Nat Commun.
- `10.1038/s41586-022-04464-z` — *ACE2 binding is an ancestral and evolvable trait of
  sarbecoviruses*, Nature.
- `10.7554/elife.75555` — *Comprehensive interrogation of the ADAR2 deaminase domain*, eLife.
- `10.7554/elife.72482` — *Functional and structural segregation of overlapping helices in
  HIV-1*, eLife.
- `10.1016/j.jbc.2022.102608` — *Deep mutational scanning and massively parallel kinetics of
  plasminogen activator*, JBC.
- `10.1186/s12915-022-01304-4` — *Optimization of the antimicrobial peptide Bac7 by deep
  mutational scanning*, BMC Biology.
- `10.1093/molbev/msac187` — *High mutational sensitivity of the ccdA antitoxin*, Mol Biol Evol.
- `10.1073/pnas.2122676119` — *Stability determinants of a challenging de novo protein fold*,
  PNAS.
- `10.1186/s13059-022-02839-z` — *Saturation-scale functional evidence for clinical variant
  interpretation*, Genome Biol. Human.

## Rejected on sight

Tooling and prediction papers, the Phase 1 exclusion: `VaLiAnT`, `MAVE-NN`, `Resistor`,
`GigaAssay` as a platform description, protein language-model embedding papers, and the
AlphaFold2 community assessment. Antibody and antigenic-characterisation papers that report
neutralisation titres against named variants rather than a scored variant library are excluded
on the same grounds that removed the 2025 branch's serum-mapping candidates.
