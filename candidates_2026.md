# 2026 candidate papers

Screening notes for the `2026_WJ` branch — papers published in 2026 that may yield FitnessBench
datasets. Nothing here is curated yet; this is the shortlist that step 1 of `example_workflow.md`
should start from.

Cut from `main`, as `2022`, `2023`, `2024` and `2025` were, so it starts from the six Jiang 2024
PRIME datasets and nothing else. The `skill/fitnessbench-digger/SKILL.md` and `.gitattributes`
carried over are the versions the `2025` branch ended with on 2026-09-08, which is where the
method notes below come from.

## Two 2026 papers are already curated, on the wrong branch

Do not curate these again. They were taken on the `2025` branch before a 2026 branch existed, and
they stay there by decision rather than by oversight:

| Paper | DOI | Datasets | Variants |
|---|---|---|---|
| Vanella, DAOx multi-substrate specificity landscape, Nat Commun | `10.1038/s41467-026-69913-z` | 5 | 29,000 |
| Jiang, T7 RNA polymerase dual-fitness evolution, Nucleic Acids Res | `10.1093/nar/gkag259` | 2 | 328 |

A third, Jansen's CymR repressor DMS (`10.1093/nar/gkag206`), was curated there and then reverted
because a transcriptional repressor is a DNA-binding protein and fails the enzyme scope. It does
not belong here either.

**Watch the publication year, and take it from the online date.** Two cases on the `2025` branch
show why. Wysocki's Form I rubisco paper (`10.1021/acssynbio.5c00591`) published online 2025-12-22
into a January **2026** print issue — Europe PMC reports `pubYear` 2026, but it is a 2025 paper and
is curated as one. Prywes's rubisco map carries an `s41586-`**`024`**`-08455-0` DOI and is a 2025
paper. Neither the DOI nor Europe PMC's `pubYear` settles it; Crossref's `published-online` does.

## Scope — enzymes and enzyme-adjacent

Set on 2026-08-31 on the `2022` branch and applied on `2023`, `2024` and `2025`. Carried here
verbatim.

**In scope**: catalysts, and proteins whose measured phenotype is catalytic machinery —
nucleases, polymerases, helicases, ATP-driven transporters.

**Out of scope**: fluorescent proteins, binding domains, ion channels, structural and scaffold
proteins, viral surface glycoproteins.

The scope is a Phase 1 gate in the skill file, checked per work item, because it is the cheapest
rejection available: it needs no counting and no file.

## Leads carried over from the 2025 sweeps

None of these were searched for. They fell out of sweeps aimed at 2025 and are recorded on that
branch's **Parked (other years)** tracker tab.

### 1. Fks1 echinocandin resistance DMS — CURATED 2026-09-08, 12 datasets

`10.1093/genetics/iyag055`, *Mutational landscape and molecular bases of echinocandin resistance
in Saccharomyces cerevisiae*, Genetics 2026.

**465 single substitutions across three Fks1 hotspots**, bulk-competition DMS with selection
coefficients, against anidulafungin, caspofungin and micafungin plus a no-drug control — four
conditions on one wild type, so four datasets. `PMC13147539`, `inEPMC:"Y"`, `isOpenAccess:"Y"`,
`hasSuppl:"Y"`: full text and supplement both fetch cleanly.

It was on the 2025 Open tab for weeks recorded as "a Phase 0 data-availability chase". That note
was **stale** — by the time anyone returned to it the article was in PMC, open, supplement and all.
Nothing blocks it but the branch.

**Curated.** Durand *et al.*, Genetics 2026, `10.1093/genetics/iyag055`, published online 2026-03-02
by Crossref, so a 2026 paper on the year rule. Twelve datasets under
`Fitness/GrowthFitness/DMS/`, 1,470 variant rows on one wild type — UniProt **P38631**, Fks1,
1,876 aa, whose three hotspot windows match the paper's positions exactly with no repair.

The numbers came from the **GitHub deposit the Data availability statement names**
(`Landrylab/Durand_et_al_2026` › `results/df/avg_scores.csv`), not from the article — the third
time on this project that following the deposit beat opening the PDF.

**Three hotspots could not be pooled.** gyōza centres each library on its own silent-mutant median,
and the paper says hotspot 2's coefficients are shifted by too few engineerable silent mutants. The
data shows it: wild type scores −0.11 in the hotspot 1 library and −0.81 in the hotspot 2 library
under the same drug. So the split is hotspot × condition, 3 × 4.

**The Phase 7 re-derivation reconciles exactly.** Figure 2d states 76 hotspot 1 single mutants
resistant to all three echinocandins; recomputing from the deposited classification table gives 76,
and the gap to the 72 in these files is fully accounted: one nonsense variant (`S643*`, dropped as
unwritable) and three substitutions absent from the pooled library that were measured individually
(`F639C`, `P647N`, `P647Q`).

Two things the check surfaced that no validator would have. `V641W` and `L642K` disagree between the
deposit's two tables, because `rescue_missing_mutants.py` replaces their pooled values with
individual validation estimates the authors judge less biased — these files keep the pooled values,
so the dataset stays one assay on one basis, and the divergence is in `remark`. And the paper's
prose count of **465** classified mutants recounts to **462**; the 3-variant gap is unexplained and
is recorded rather than reverse-engineered.

**Not curated, still available in the same file**: the same hotspot libraries in the R1158
background (*FKS2* repressible by doxycycline), 2 hotspots × 5 conditions, and two Fks2 hotspot
libraries (P40989, 1,895 aa), 2 × 5 — 20 further datasets on two more wild types, each a separately
normalized screen. The homolog hotspot libraries are excluded as a homolog panel.


### 2. Form II rubisco fitness landscape (*Gallionella* sp.) — CURATED, 3 datasets

`10.1126/sciadv.aee9222`, *The fitness landscape of a form II rubisco in a photosynthetic bacterium
guides engineering of oxygen tolerance*, Science Advances 2026.

A barcoded library of **15,000 single-site and multi-site variants** scored by growth-coupled
selection in *Synechocystis* sp. PCC 6803. One wild type, bacterial, far above the floor, and a
third rubisco to sit beside Prywes and Wysocki.

Chased on 2026-09-08 and **it is a hand-off, not a dead end**. Unpaywall reports it **gold OA**,
contradicting Europe PMC's `inEPMC:"N"`. But every automated route stops short of the per-variant
table: there is no Europe PMC deposit; the PMC id Unpaywall names (`PMC13544237`) 404s on
`fullTextXML` and 500s on `?pdf=render`; the bioRxiv preprint is `10.64898/2025.12.07.690893`
(Hoffmann *et al.*, KTH, deposited 2025-12-08, CC-BY-NC); and the Zenodo record
**`10.5281/zenodo.20308544`** holds *only* the 9.8 MB Supplementary Information PDF — no fitness
table.

**Superseded**: no hand-off is needed. The per-variant fitness table is public on GitHub at
`ute-hoffmann/CbbMLargeLibrary` — see *Two hand-offs dissolved* below.

**Curated 2026-09-08, three datasets, 41,799 variant rows** — the largest item on this branch.
`Fitness/GrowthFitness/DMS/`, one per growth condition, **13,933 variants each** on a single 484-residue
construct. Built entirely from `ute-hoffmann/CbbMLargeLibrary`; the article itself was never opened,
which is the third time on this project that the deposit beat the PDF.

The three conditions are defined in the deposit's own analysis notebook, not guessed:

| | |
|---|---|
| `CL_N2` | constant light 300 µE, 5% CO2, 95% N2, **0% O2** |
| `CL_O2` | constant light 300 µE, 5% CO2, 75% N2, **20% O2** |
| `LD` | light-dark cycles, 5% CO2, 75% N2, 20% O2 |

**Three things the notebook settled that no amount of staring at the table would have.**

*The sequence carries a Strep-tag, and the numbering is against it.* The deposited construct begins
`MWSHPQFEKGSGSG`, and the notebook says outright that "amino acid numbering ... are based on the
sequence including the N-Strep tag". The label check confirms it: **all 1,225 distinct substitution
labels verify against the 484-residue tagged construct at offset 0**, and 1,194 of them fail against
the untagged 470-residue form. The repo even ships a file pairing the two numberings, differing by 14.

*The row labelled `WT` is not the wild type.* It is the library's **pre-engineering parent, two
substitutions from wild-type Gallionella CbbM**, which the notebook calls WT "for reasons of
simplicity". This is exactly the case `CLAUDE.md` warns about, and it is only visible in the code.
Against UniProt **D9SHP6** (*G. capsiferriformans* ES-2, 470 aa) the untagged construct differs at
six positions — two being the engineered exchanges, the rest presumably isolate differences that
cannot be resolved from what is deposited.

*The zero point is not a non-growing control.* Fitness is normalized so the parent is 1.0 and **the
median K214 substitution is 0.0** — K214 being the carbamylated lysine required for catalysis, so
anything below zero is by the authors' own reading catalytically dead. A reader treating 0 as
"neutral" would misread the whole file.

**Phase 7 is honest rather than clean.** The parent lands at **exactly 1.000000** in all three
conditions. The K214 anchor does not: its median lands at **+0.011, −0.092 and −0.005** rather than
zero, a small residual the source does not explain, recorded in `remark` rather than smoothed away.
The library design reconciles — 72 mutated positions against the stated 67 saturated plus 7
combinatorial, sharing two.

Of the 39,386 rows in the supplementary table only **13,966 carry a measurement**; the rest are
variants the paper's models scored but which were never built, and dropping them is the single
biggest decision in this curation. A further 32 rows carry a `STOP` token and are dropped as
truncations. The article PDF is not redistributed — Science Advances blocks retrieval and the PMC
record its DOI advertises 404s.


### 3. LetA intermembrane lipid transporter

`10.1038/s41586-025-09990-0`, Nature 2026; preprint `10.1101/2025.03.21.644421`, 2025.

**8,967 variants already sitting in MaveDB** as `urn:mavedb:00001252-a`, machine-readable and
downloadable today through the MaveDB API — no chase needed at all.

Two cautions. **Scope**: LetA is a lipid transporter, and the scope admits transporters only when
they are ATP-driven; that needs establishing before any work. **Year**: a 2025 preprint with a 2026
version of record, so it falls between this branch and `2025` under the current convention. It is
the standing argument for settling the preprint question.

### 4. PqiC

`10.64898/2026.05.09.724024`, a 2026 preprint. `urn:mavedb:00001273-a`, **3,927 variants** of
*E. coli* PqiC. Part of the Pqi intermembrane transport system rather than an enzyme, so it
probably fails the scope — recorded because it is one of only three post-2023 in-scope-organism
deposits in the whole of MaveDB.

## What has already been swept for 2026, and what has not

The `2025` branch's **eighth sweep** ran two Europe PMC queries at `PUB_YEAR:2026`:

| Query | Hits |
|---|---|
| `ABSTRACT:("deep mutational scanning" OR "site-saturation mutagenesis" OR "variant effect map")` | 66 |
| `ABSTRACT:("enzyme engineering" OR "protein engineering" OR "machine learning-guided") AND ABSTRACT:"variants"` | 45 |

**Both carried `OPEN_ACCESS:Y`, and both were read only to a `pageSize` of 40.** So 2026 has been
sampled, not swept. Re-running these without the open-access clause is the first thing this branch
should do — on the `2025` branch that same removal, applied to three sweep families, surfaced two
papers that became 12 datasets and 58,533 variants.

Nothing else on this branch has been queried at all.

## First sweep — 2026-09-08, the eighth sweep redone without the filter

Four families, `PUB_YEAR:2026 AND SRC:MED`, **no open-access clause**, every hit paged out rather
than read to a `pageSize` of 40, and the 94 DOIs already decided on the `2025` branch or named
above excluded before ranking.

| Family | Hits | New | Enzyme-scoped, non-review |
|---|---|---|---|
| 8a. DMS phrasing (the eighth sweep's own query) | 122 | 118 | 38 |
| 8b. engineering + variants (the eighth sweep's own query) | 118 | 116 | 64 |
| 11'. enzyme × library-scale method | 1,949 | 1,943 | 1,466 |
| 14'. computational design vocabulary | 90 | 90 | 70 |

**1,529 distinct papers.** The eighth sweep saw 111. That is the cost of the two decisions it made —
the open-access clause and the 40-result cutoff — and it is the reason this branch starts with a
backlog rather than a blank page.

**Europe PMC's `isOpenAccess` was wrong on six of the eight papers checked.** Running each through
Unpaywall: seven of eight are open access, including four that Europe PMC reports as
`isOpenAccess:"N"`, `inEPMC:"N"`, `pmcid=None`. One of them, the human DNase I paper, has a PMC
record (`PMC12847522`) that Europe PMC does not know about. Only the ACS Synthetic Biology SMART
paper is genuinely closed. **Check Unpaywall before believing any reachability verdict.**

### Worth taking

**`10.1038/s41587-026-03059-7`** — *Engineered TnpB genome editors for plants and human cells
identified by ribonucleoprotein mutational scanning*, Nature Biotechnology 2026.
**CURATED 2026-09-08, five datasets, 30,229 variant rows.** The abstract is
unambiguous: "we mapped **comprehensive sequence-function landscapes** of a TnpB ribonucleoprotein
using **deep mutational scanning**", finding activating mutations in both the RNA and the protein,
then building a combinatorial library from them. TnpB is an RNA-guided endonuclease, so it is in
scope as catalytic machinery, and it is prokaryotic, so clear of the human and viral exclusion.
Unpaywall: **hybrid OA, publisher landing page only** — no PDF url, no PMC deposit, `hasSuppl:"N"`.
Crossref puts it online 2026-03-11. **Superseded**: the mutational landscape is public on GitHub at
`SavageLab/tnpb_dms` — see *Two hand-offs dissolved* below. Only the article PDF is still missing,
and it is not needed to start.

#### What the TnpB curation produced

Five datasets under `Activity/CatalyticActivity/DMS/` on one 408-residue wild type (Thornton *et
al.*, first author; Crossref puts it online 2026-03-11):

| Dataset | Variants | |
|---|---|---|
| `protein_scan` | **7,227** | the single-substitution scan across all 408 residues |
| `combinatorial_site1_4h` / `site2_4h` | 5,701 / 5,738 | two target sites, 4 h induction |
| `combinatorial_site1_8h` / `site2_8h` | 5,753 / 5,810 | the same two sites, 8 h |

The combinatorial arms carry **up to eleven substitutions per variant**, which is the deepest
epistasis anywhere in this repository.

**The sequence got an external check that a 3f derivation normally cannot have.** The scan's
`OriginalAA` column is consistent at all 406 positions it covers, which is enough to derive a
sequence — but a derived sequence satisfies the label check by construction, so nothing is tested.
Here the deposit also ships the reference plasmid, and translating it gives a 408-residue open
reading frame whose residues **2 to 407 reproduce the derived scan exactly**, with position 1 the
initiator methionine the library never mutates and position 408 lying past the scan's range. The
plasmid is the authority and the derivation merely agrees with it.

**Phase 7 reproduces the paper's design logic across two independent datasets.** The abstract says
the combinatorial library was built from activating mutations found in the protein landscape.
Taking the 33 constituent changes of the combinatorial library and looking each up in the
single-substitution scan: **all 33 have positive enrichment, all 33 sit in the top 5 percent of the
scan, and their median rank is the 99.6th percentile** — `E302K` is 4th of 7,227. Neither file knows
about the other, so this is a real check rather than an internal consistency one.

Dropped: **382 rows coded `X`**, the library's nonsense variant at each position, and one `dead` row
per sheet, a catalytically inactivated control rather than a genotype. The **reRNA sheet is out of
scope** — 576 guide-RNA variants, which cannot be written against a protein sequence.


### Worth a look, but probably not

**`10.1002/cbic.70459`** — *Trylons*, ChemBioChem 2026. Four saturation libraries of NylC at
positions 146, 189, 192 and 305, "nearly 100 variants each", read by continuous light scattering.
Reachable (`PMC13343204`, supplement present, direct PMC PDF). The question is whether substitution
tolerance at four positions was reported per variant or only as summary tolerances; if pooled it
clears the floor, if reported per position it is four scans of nineteen.

### Worked up, then skipped by decision — not a data defect

**`10.1016/j.jbc.2026.113212`** — Simões *et al.*, *Noncatalytic surface electrostatic networks
tune thermolability in uracil-DNA glycosylase*, J Biol Chem 2026. `PMC13316540`, CC-BY, article PDF
and supplement both fetch cleanly.

**Skipped on 2026-09-08 at the user's direction, with the curation already worked up to the point
of writing.** Nothing about the data disqualified it, so a later run can pick this up from here
rather than starting over. Nothing was staged and no files were written.

What is there, verified:

| | |
|---|---|
| Work item | UDG_7 melting temperature, one wild type, one measurement |
| Source | `mmc2.xlsx` › **Table S6**, in the Europe PMC supplementary bundle for `PMC13316540` |
| Rows | **54 unique single substitutions across 20 positions**, matching the abstract's count |
| Readout | average Tm from fluorescence-based unfolding of individually purified protein, 36.4–42.4 °C |
| Usable | 51 — three (`R201L`, `R201E`, `R201D` in the paper's numbering) are reported `ND`, no cooperative transition |
| Wild type | GenBank **`WP_135029980.1`**, *Micrococcus flavus*, 225 aa — bacterial, so clear of the human and viral exclusion |
| Numbering | the paper's native numbering begins at **residue 2** of the accession; a **+1 offset resolves all 20 positions at once**, the clean Phase 3c case |
| WT row | none — the wild type's Tm is given only in prose, as "approximately 42.5 °C", and is not tabulated |

**The orientation was decided and is worth keeping.** This campaign engineers thermo*lability* — a
lower Tm is the desired product, for sharper inactivation in PCR carryover control — so the readout
would be **`-Tm (degC)`**, negated, which is the reverse of every other dataset in
`Stability/ThermalStability/`. That reversal is the interesting thing about the paper and the
reason it is worth recording rather than forgetting.

**Not curatable from this paper, whatever happens to Table S6.** Table S3's melting temperatures are
per *position* — the pooled 19-member library at a site, not a genotype. Table S5's three-temperature
screen is binary (✔/✘) and keyed to clone number rather than to a substitution. The 24-member
natural UDG diversity panel is a homolog panel with no single wild type. And the article's Data
availability statement says only "available upon a reasonable request", which would have been a
dead end — the numbers are in the supplement regardless, which is the general lesson.


### Rejected on the abstract

**`10.1016/j.jbc.2026.113393`**, PlyC endolysin — "After screening **18,000 mutants**, the lead
candidate identified was the point mutant PlyCA N211H." A one-champion campaign wearing a large
number: 18,000 screened, one winner and one rational combination characterised. This is the exact
shape the `2025` branch rejected repeatedly, and the large screening figure is what makes it look
otherwise in a ranked list.

**`10.1007/s13205-026-04693-3`**, human DNase I — a library of 1,051 variants screened, one double
mutant (N78T, V90N) reported at 4.1-fold. Same shape. Worth reopening only if the deposit turns out
to hold the screen rather than the winner.

**`10.1200/po-25-00609`**, PIK3CA/AKT1/PTEN in breast cancer — ranked first by the scorer on 29,157
"variants" and 51,767 tumours. Clinical genomic profiling, not a variant library of one wild type.
A reminder that the ranker rewards large numbers regardless of what they count.


## Second sweep — 2026-09-08, deeper into the backlog, plus two axes never run at 2026

The first sweep found 1,529 papers and examined about eight of them. This one goes back to the same
population with a sharper triage, and adds the two axes the `2025` branch swept but never re-ran for
2026.

| Family | Hits | New | Enzyme-scoped |
|---|---|---|---|
| 8a, 8b, 11, 14 (as before) | 2,279 | 2,260 | 1,627 |
| **A. ancestral reconstruction / iterative saturation / CASTing** | **31** | 31 | 28 |
| **B. droplet microfluidics / ultrahigh-throughput / FADS** | **22** | 22 | 13 |

**2,170 distinct papers**, of which **1,541** are enzyme-scoped, undecided and not reviews. Every hit
is now kept with its abstract, so the population can be re-triaged without re-querying.

### The triage, and what it cost to get right

Filtering on *"the abstract states a library size of at least 20, with no one-champion phrasing and
no human or clinical vocabulary"* reduces 1,541 to **six**. All six were opened and all six are `no`:

| Paper | Count in context | Verdict |
|---|---|---|
| `10.1016/j.foodres.2026.119535`, methionine adenosyltransferase | "18 selected candidates from 209 mutants" | the 209 are **virtual** FoldX/Rosetta mutants; 18 were built. Predictions, and below the floor as measured |
| `10.1038/s41586-025-09746-w`, **computational design of metallohydrolases**, Nature | "from an initial set of 96 designs tested" | 96 **de novo** designs — unrelated sequences, no shared wild type. The same half of the work-item definition that sinks a homolog panel |
| `10.1002/anie.1402106`, ML photoenzyme evolution | "by screening only 40 variants" | 40 measured, but the paper's own point is a 4-mutation champion from a FRISM round. Genuinely closed |
| `10.1038/s41559-025-02804-6`, **KPC-2 carbapenemase**, Nat Ecol Evol | "we identified 40 different substitutions" | **the one worth chasing** — see below |
| `10.1371/journal.pone.0335829`, free-energy benchmarking | "for the 38 single mutants of" | computed FEP over *published* mutations of staphylococcal nuclease and T4 lysozyme. Not the authors' measurement |
| `10.1002/bit.70239`, *Bacillus subtilis* SDR | "four of the constructed 31 variants" | 31 built, four highlighted. Europe PMC advertises a PMCID and `hasSuppl:"Y"`, but `fullTextXML` 404s and the supplementary bundle is not a zip — the record is a stub |

A softer cut — library-scale vocabulary and reachable in PMC with a supplement, regardless of any
stated count — gives 118 candidates and 32 reachable. Reading them confirms the shape of the year:
2026 enzyme engineering is overwhelmingly semi-rational campaigns reporting one champion.

### `10.1021/acscatal.5c08164` — rejected, and the reason is a warning about the tooling

The GH42 β-galactosidase paper from *Bifidobacterium breve* reached the top of the first ranking on
an apparent **121 variants**. It has no such library. The scorer had matched **"Arg121 variants"** —
a *residue number* glued to the word that follows it. The paper is site-saturation at the single
residue Arg121, plus a handful of alanine-scan points in the water tunnel: **one position, and one
position is not a landscape**, which is the same ground the β-lactamase gatekeeper was rejected on.

**Any count regex over abstracts must reject a number with a letter glued to its left.**
`Arg121 variants`, `R121 variants` and `position 121 variants` all read as library sizes otherwise,
and protein papers are made of such strings. The first correction over-shot in the other direction —
excluding any count preceded by a letter *after* stripping whitespace kills `of 209 mutants` too,
and took the list to zero. The test has to be the character **immediately abutting the digits**,
with a separate check for a preceding residue or position word.

### The one lead worth a hand-off

**`10.1038/s41559-025-02804-6`** — *Cryptic phenotypic variation emerges rapidly during the adaptive
evolution of a carbapenemase*, Nature Ecology & Evolution 2026. Directed evolution of **Klebsiella
pneumoniae carbapenemase-2** toward ceftazidime: **40 different substitutions across 18 mutational
trajectories**, grouped into four classes by their first mutation, then compared across several
phenotypic dimensions. A bacterial enzyme, well clear of the human and viral exclusion, and the
epistasis structure is exactly what this benchmark is short of.

**CURATED 2026-09-08, four datasets.** Unpaywall was right that it is genuinely closed, with no PMC
deposit and no public repository — the Data availability statement says only "available in the
manuscript and its Supplementary Information", so the user supplied the article, the supplement and
the Source Data file by hand. This is the one paper this branch could not have reached on its own.

Four datasets under `Activity/AntibioticResistance/DE/`, one per antibiotic, on UniProt-equivalent
`WP_004199234.1` (KPC-2, 293 aa): ceftazidime with **39 variants** from all 18 evolutionary lines,
and cefotaxime, cefoxitin and imipenem with **34 each** from the 14 lines the Source Data covers.
Genotypes are cumulative trajectory points carrying one to six substitutions, so the file holds the
epistasis the paper is about. Readout is **log2 MIC**, because the assay is a twofold dilution
series and the raw values are spaced geometrically.

**The paper's residue numbering could not be used.** It is not a constant offset from the sequence
— the gap runs 0, +1, +2 and +3 at different positions — and it is internally inconsistent: the
single nucleotide change `c587a` is printed as **S196Y** in line H5 and **S197Y** in line L3. Every
mutation is however also given as a nucleotide change, so the labels were derived from the
*bla*KPC-2 coding sequence (GenBank `AY034847`, which translates exactly to the 293-residue
protein). **61 of the 62 printed nucleotide positions carry the stated wild-type base**, every
derived residue identity matches the paper's own, and the label check comes back empty. Both
apparent failures were transcription slips of mine off the image, and the coding sequence caught
both.

**Supplementary Table 2 is an image, not text.** It had to be rendered and read visually, which is
not a reading to trust on its own — so it was checked against the cumulative non-synonymous
mutation counts in the Source Data, which **agree for all 48 line-and-round combinations**, and
against the Source Data's own ceftazidime MICs, which agree in **47 of 48**.

The 48th is a genuine conflict between the paper's two files: **line S1, round 3, is 2048 in
Supplementary Table 2 and 1024 in the Source Data**. These files follow Supplementary Table 2
throughout, that being the only source covering all 18 lines, and the disagreement is in `remark`.

**Phase 7 reproduces exactly.** The paper reports that round one gave "consistently large MIC
increases (16- and 32-fold)"; recomputing every round-one founder from the shipped file gives fold
values of exactly {16, 32} and nothing else. The abstract's count of 40 distinct substitutions comes
out at **39**, which is recorded rather than reconciled.

### What this sweep did not cover

Preprints remain unswept for every year: all queries still use `SRC:MED`. Whether preprints are in
scope has never been decided, and the LetA lead is the standing cost of leaving it open.


## Two hand-offs dissolved — 2026-09-08, by searching GitHub for the author and the gene

Both papers that were about to be handed to the user for manual download turned out to have their
per-variant data public on GitHub. Neither article says so in a way any query would surface: the
rubisco paper is behind Science's paywall, and the TnpB paper is a Nature Biotechnology landing page
with no PMC deposit. **Neither needs a hand-off.**

### Form II rubisco — `ute-hoffmann/CbbMLargeLibrary`

`10.1126/sciadv.aee9222`. Found by searching GitHub for the **first author's surname and the gene
name** — Hoffmann, and *cbbM*, which is what a Form II rubisco gene is called. The repository README
carries the paper's exact title and a figure-by-figure index of which file backs which panel.

The table is **`EDA_output/SuppTable_all_fitness_values_wide.csv`** (7.3 MB, **39,386 variants**),
with a long form beside it:

| Column | |
|---|---|
| `sgRNA_target` | the variant label, e.g. `A164C`; higher-order variants carry several |
| `number_muts` | 1 for the single-site scan, higher for the combinatorial library |
| `norm_CL_N2`, `norm_CL_O2`, `norm_LD` | normalized weighted mean fitness in **three growth conditions** |
| `p_fit_adj_WT_*` | adjusted p-value against wild type, per condition |

So **three datasets on one wild type**, and far more than the 15,000 the abstract advertises, because
the deposit includes the combinatorial library and higher-order variants. The prediction columns
(`EVcoup_predict`, `DeepSeq_predict`, `MSA_Transform`, `proteinNPT_predict`, `additive_score`) are
computed, not measured, and are out of scope by the Phase 1 rule.

The Zenodo record `10.5281/zenodo.20308544` holds only the SI PDF and **403s to automated agents on
both its API and its normal download URL** — it was a dead end in both senses, and is not needed.

### TnpB — `SavageLab/tnpb_dms`

`10.1038/s41587-026-03059-7`. The README names the paper's exact title and its preprint
(`10.1101/2025.02.11.637750`). The data is one workbook,
**`notebooks/supptable/SupplementaryTables2_Enrichments_20251010.xlsx`** (2.6 MB, six sheets):

| Sheet | Rows | |
|---|---|---|
| `protein_DMS_library_enrichment` | **7,611** | the single-site protein scan — carries a `WT` row and `OriginalAA` / `NewAA` / `Position` columns, so labels need no reconstruction |
| `comboLib_strain1_4hrs`, `strain2_4hrs`, `strain1_8hrs`, `strain2_8hrs` | ~5,700 each | the combinatorial library, two strains × two timepoints, multi-mutants joined with `_` |
| `reRNA_library_enrichment` | 576 | **out of scope** — these are RNA variants of the reRNA guide, not protein substitutions, and cannot be written against a protein sequence |

Readout is `Avg_log2Enrich_Norm` with per-replicate medians and p-values. A `dead` row sits beside
`WT` as a negative control and is not a variant. Potentially **five datasets** on one wild type,
though whether the four combinatorial arms are one work item or four turns on whether the strains
and timepoints are separate selections — a Phase 2 question, not a Phase 1 one.

### The lesson, which is a sharpening of one already on the record

The 2025 branch learned to **follow the deposit, not the article**, but looked for deposits the
*paper* names. Both of these were found instead by **searching GitHub for the first author's surname
and the protein or gene name**, without reading either article — and in the rubisco case the gene
name that worked (*cbbM*) never appears in the title or abstract. When a paper is paywalled, that
search costs one request and should come **before** any hand-off is offered, not after.


## Method notes worth carrying, learned on the 2025 branch

**`OPEN_ACCESS` is a licence flag, not a reachability flag.** Europe PMC reports its own holdings.
Of 146 closed-access hits in one 2025 family, **104 had a PMCID and `inEPMC:"Y"`** — readable right
then. Ask **Unpaywall** instead: `api.unpaywall.org/v2/<doi>?email=<addr>` returns `is_oa`,
`oa_status` and a direct `url_for_pdf`, and it costs one request. Two Cell Press papers flagged
closed by Europe PMC were CC-BY gold and hybrid.

**When a page really is bot-blocked, that is a hand-off, not a mirror hunt.** `cell.com` and
`biorxiv.org` return 403 to automated agents regardless of licence. The file is free to a person
with a browser, so hand over the exact URL rather than grinding.

**Follow the deposit, not the article.** Three of the last four papers curated on `2025` were built
from a repository rather than a PDF: Harvard Dataverse (CC0), a Google Cloud bucket reached through
a GitHub repository's `constants.py`, and MaveDB. In two of those the article itself was never
opened. A data availability statement naming an accession is worth more than an open PDF.

**MaveDB is a source in its own right, and is exhausted for now.** Its `POST
/api/v1/score-sets/search` accepts `targetOrganismNames`, so the scope's organism half goes into
the query. All 608 published score sets on the 72 in-scope organisms were enumerated on 2026-09-07:
of 450 distinct publications, only LetA and PqiC are post-2023. Do not re-sweep it for 2026 without
a reason; do consult it per-paper, since it may hold a deposit the article does not advertise.

**Two tables that would have passed every validator failed a reproducibility test instead.** A
multi-temperature EnvZ DMS whose 37 °C arm scored nonsense variants *higher* than wild type, and an
ACE2 droplet screen whose three sorts correlated at 0.074, 0.006 and −0.029. Neither was catchable
mechanically. When a source ships replicates or an internal control — nonsense variants, an
empty-vector lane, a wild-type row — **check them before shipping**, and chase a correlation that
contradicts the paper's own claim rather than recording it as noise.

**Preprints are still unswept, for every year.** All sweeps to date used `SRC:MED`, which excludes
bioRxiv and Research Square. The 2025 population was sized at roughly 230 hits and never worked.
Whether preprints are in scope has never been decided, and LetA shows the cost of leaving it open.
