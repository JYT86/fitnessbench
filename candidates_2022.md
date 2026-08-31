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

## Scope — enzymes and enzyme-adjacent

Set on 2026-08-31, and it changes this shortlist substantially, so it comes before the tiers.

FitnessBench is in practice an enzyme benchmark and always has been: the `2025` branch is
**112 of 144 datasets on catalytic activity**, about twenty enzymes out of twenty-three
proteins. Nothing in `README.md` or `example_workflow.md` ever said so — the focus lived in the
2025 sweep queries, which were phrased around *machine learning guided enzyme engineering*, and
not in the documentation. Broader DMS-vocabulary sweeps therefore drifted off it without
anything pushing back.

**In scope**: catalysts, and proteins whose measured phenotype is catalytic machinery —
nucleases, polymerases, helicases, ATP-driven transporters.

**Out of scope**: fluorescent proteins, binding domains, ion channels, structural and scaffold
proteins, viral surface glycoproteins.

Green fluorescent protein is the clearest casualty and it is a deliberate one. Somermeyer's
three-homologue landscape is the largest and most accessible item ProteinGym holds for 2022,
but fluorescence reports chromophore maturation and folding rather than catalysis, the protein
is the most thoroughly covered in this entire literature, and the same data already sits in the
project's own `EvoAI/me12_features/` set alongside Sarkisyan's avGFP. Curating it would add a
format, not a measurement.

## Tier A — ProteinGym-confirmed, 2022 version of record, in scope

Five publications, six assays, roughly 32,500 mutants. Four of the five are open access.

| # | Paper | DOI | Protein | Mutants | OA |
|---|---|---|---|---|---|
| 1 | Kwon, *Structure-function analysis of the SHOC2-MRAS-PP1C holophosphatase* | `10.1038/s41586-022-04928-2` | PP1C holophosphatase complex | 10,972 | no |
| 2 | Miller, *Allosteric inhibition of PPM1D phosphatase* | `10.1038/s41467-022-30463-9` | PPM1D serine/threonine phosphatase | 7,889 | yes |
| 3 | Flynn, *Comprehensive fitness landscape of SARS-CoV-2 Mpro* | `10.7554/eLife.77433` | main protease | 5,725 | yes |
| 4 | Hobbs, *Saturation mutagenesis of a predicted ancestral Syk-family kinase* | `10.1002/pro.4411` | ancestral Syk kinase | 4,670 | yes |
| 5 | Roychowdhury, *Microfluidic deep mutational scanning of the human executioner caspases* | `10.1038/s41420-021-00799-0` | CASP3 and CASP7, two assays | 3,247 | yes |

## Tier A — out of scope under the enzyme rule

Recorded rather than deleted, so the decision is visible and reversible.

| Paper | DOI | Why out |
|---|---|---|
| Somermeyer, GFP fitness landscape, 3 assays, 89,426 mutants | `10.7554/eLife.75842` | Fluorescent proteins. See the scope note above |
| Faure, energetic and allosteric landscapes of protein binding domains | `10.1038/s41586-022-04586-4` | PSD95-PDZ3 and GRB2-SH3 are binding domains, not catalysts |
| Coyote-Maestas, trafficking and conduction in a K+ channel | `10.7554/eLife.76903` | Kir2.1 is an ion channel; conduction is not catalysis and it is not ATP-driven |
| Seuma, atlas of amyloid aggregation | `10.1038/s41467-022-34742-3` | Amyloid-beta aggregation, a structural phenotype |
| Erwood, saturation variant interpretation by prime editing | `10.1038/s41587-021-01201-1` | BRCA2 and NPC1 — a recombination mediator and a cholesterol transporter, neither catalytic |

## Tier B — additive, in scope

The enzyme rule cuts hard here too: most of 2022's additive seam is coronavirus surface and
antibody work, which is out. What survives is worth having.

- `10.1016/j.chom.2022.08.003` — *Functional map of SARS-CoV-2 3CL protease*, Cell Host Microbe.
  Note this is the **same enzyme** as Flynn's Mpro in Tier A, measured independently — two
  papers on one protein, which is useful rather than duplicative.
- `10.7554/elife.75555` — *Comprehensive interrogation of the ADAR2 deaminase domain*, eLife.
- `10.1016/j.jbc.2022.102608` — *Deep mutational scanning and massively parallel kinetics of
  plasminogen activator*, JBC. A protease, and the kinetics make it unusually rich.
- `10.1093/molbev/msac187` — *High mutational sensitivity of the ccdA antitoxin*, Mol Biol Evol.
  Borderline: an antitoxin is not a catalyst, but it acts on a gyrase-poisoning toxin. Check
  before committing.

### Out of scope from Tier B

Everything coronavirus-surface: nucleocapsid escape, combinatorial RBD binding, ACE2 affinity
and evolvability, spike NTD constraints, hemagglutinin evolutionary potential. Also the de novo
fold stability study, the Bac7 antimicrobial peptide, the HIV-1 overlapping-helix study and the
clinical variant interpretation set, none of which measures catalysis.

## Original Tier B listing, before the scope rule

Kept for the record.

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
