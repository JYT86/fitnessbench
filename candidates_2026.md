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


### 2. Form II rubisco fitness landscape (*Gallionella* sp.)

`10.1126/sciadv.aee9222`, *The fitness landscape of a form II rubisco in a photosynthetic bacterium
guides engineering of oxygen tolerance*, Science Advances 2026.

A barcoded library of **15,000 single-site and multi-site variants** scored by growth-coupled
selection in *Synechocystis* sp. PCC 6803. One wild type, bacterial, far above the floor, and a
third rubisco to sit beside Prywes and Wysocki.

Europe PMC has the record but `inEPMC:"N"`, `hasSuppl:"N"`, subscription only. **Check Unpaywall
before concluding it needs a hand-off** — see the method note below.

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
identified by ribonucleoprotein mutational scanning*, Nature Biotechnology 2026. The abstract is
unambiguous: "we mapped **comprehensive sequence-function landscapes** of a TnpB ribonucleoprotein
using **deep mutational scanning**", finding activating mutations in both the RNA and the protein,
then building a combinatorial library from them. TnpB is an RNA-guided endonuclease, so it is in
scope as catalytic machinery. Unpaywall: hybrid OA, publisher landing page only.

**`10.1016/j.jbc.2026.113212`** — *Noncatalytic surface electrostatic networks tune thermolability
in uracil-DNA glycosylase*, J Biol Chem 2026. A single-site variant library across **48
non-catalytic positions**, pooled thermal-shift assays resolving 16 hotspots, then **high-throughput
functional screening of 480 single mutants** yielding 114 clones and **54 unique characterised
variants**, nine of them with measured melting-temperature shifts. Two readouts on one wild type —
activity and thermolability. `PMC13316540`, `inEPMC:"Y"`, `hasSuppl:"Y"`, and a direct publisher PDF
at `jbc.org`. The most immediately workable of the four.

### Worth a look, but probably not

**`10.1002/cbic.70459`** — *Trylons*, ChemBioChem 2026. Four saturation libraries of NylC at
positions 146, 189, 192 and 305, "nearly 100 variants each", read by continuous light scattering.
Reachable (`PMC13343204`, supplement present, direct PMC PDF). The question is whether substitution
tolerance at four positions was reported per variant or only as summary tolerances; if pooled it
clears the floor, if reported per position it is four scans of nineteen.

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
