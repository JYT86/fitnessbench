# 2017 candidate papers

Screening notes for the `2017` branch. Cut from `main`, so it starts from the six Jiang 2024 PRIME
datasets and nothing else.

Part of the **2009–2020 MaveDB enzyme cohort**. The discovery work and the backlog files live on the
`2015` branch (`candidates_2015.md`, `backlog_pre2022.tsv`); this file records only what 2017 yielded.

## Scope — enzymes and enzyme-adjacent

Set on 2026-08-31 on the `2022` branch. Carried here verbatim.

**In scope**: catalysts, and proteins whose measured phenotype is catalytic machinery — nucleases,
polymerases, helicases, ATP-driven transporters.

**Out of scope**: fluorescent proteins, binding domains, ion channels, structural and scaffold
proteins, viral surface glycoproteins.

SpCas9 is an RNA-guided DNA endonuclease, so it is in scope on both halves: a nuclease by protein, and
DNA cleavage by readout.

## Shipped — 5 datasets, 15,052 variants

### Spencer 2017, SpCas9 — 2 datasets, 2,404 variants each

`10.1038/s41598-017-17081-y`, *Deep mutational scanning of S. pyogenes Cas9 reveals important
functional domains*, Sci Rep 2017. From `urn:mavedb:00000071` (CC0), in
`Activity/CatalyticActivity/DMS/`.

Two arms of a ccdB selection in *E. coli*, and they are separate work items because the condition
differs:

| Dataset | Selection | What survival means |
|---|---|---|
| `…-selection_positive_selection` | positive, on-target | the variant **did** cleave the target |
| `…-selection_negative_selection` | negative, off-target | the variant **did not** cleave a near-match |

**Phase 3.** The deposit's 4,173-nt target translates to 1,390 aa, which is UniProt **Q99ZW2 verbatim
at positions 1–1368** followed by a 22-residue C-terminal tag, `SRADPKKKRKVCTYPYDVPDYA` — an SV40
nuclear localisation signal (`PKKKRKV`) and an HA epitope (`YPYDVPDYA`). The tag is part of the
molecule that was assayed and **53 variants per arm fall inside it**, so it stays in `sequence`; the
remarks name the residues. Dropping the tag would have meant dropping those 53 measurements or
mis-numbering everything after 1368.

**One row per arm is dropped** for naming a terminator rather than an amino acid: a readthrough of the
stop at position 1391.

**63 duplicate groups per arm collapse by averaging, and these do not agree exactly** — worst spread
3.12 on the positive arm, 2.66 on the negative. Unlike the CBS sets on `2020`, where every duplicate
group had spread exactly zero, here the same protein variant was measured independently via different
codons in a DNA-level library, so the spread is data and is recorded per row rather than passed over.

No wild-type row exists in the deposit, so `wt_readout` is empty and the zero point of
`normalized-score` is the dataset mean.

### Weile 2017, UBE2I and TPK1 — 3 datasets, 10,244 variants → `datasets_human/`

`10.15252/msb.20177908`, *A framework for exhaustively mapping functional missense variants*, Mol Syst
Biol 2017. From `urn:mavedb:00000001` and `urn:mavedb:00001251` (CC0), in
`datasets_human/Fitness/GrowthFitness/DMS/`. Opens `datasets_human/` on this branch.

**Split by target first.** The paper covers four proteins across six genes. **UBE2I** (SUMO E2
conjugase) and **TPK1** (thiamin pyrophosphokinase) are enzymes; **SUMO1** is a modifier protein and
**calmodulin** a calcium-binding regulator, so both fail the scope. Only the first two are taken, and
the remarks say so — curating the deposit whole would have shipped two non-enzymes.

| Dataset | Assay | `n_variants` | Shape |
|---|---|---|---|
| `…-UBE2I-…-complementation_barseq` | DMS-BarSeq | 3,239 | **1–11 substitutions per genotype** |
| `…-UBE2I-…-complementation_tileseq` | DMS-TileSeq | 2,870 | single substitutions |
| `…-TPK1-…-complementation_tileseq` | DMS-TileSeq | 4,135 | single substitutions |

**Only the raw score sets are used.** The deposit's machine-learning *imputed and refined* sets are
excluded because imputed values are computed rather than measured, and UBE2I's *joint data* set is
skipped because it merges the two raw assays that ship separately here.

**BarSeq and TileSeq are two experiments, not two analyses.** BarSeq is a multi-site library —
1,164 doubles, 815 triples, on up to 11 sites — while TileSeq is singles only. A first pass that
matched single substitutions alone silently dropped 78% of the BarSeq file; the multi-site genotypes
are joined with `:` and kept, and they are the only epistasis on this branch.

**TPK1's deposit metadata is wrong about its own sequence.** MaveDB gives it a 194-residue TPK1
isoform, which its labels do not verify against. The labels span positions 2–243 and match canonical
**Q9H3S4 at 241 of 242** covered positions. The one exception is position 193, where 22 independent
rows all assert `S` and Q9H3S4 has `M`, with nothing contradicting them — so the construct is taken as
Q9H3S4 with **M193S**, on the repo's rule that mutation labels outrank the accession. The build asserts
Q9H3S4 still has `M` there, so a future reference update cannot silently invalidate the patch.

## Not done

- **Neither article is staged in `papers/`.** For SpCas9, `PMC5715146` is open access but neither Europe
  PMC's `fullTextPDF` route nor the publisher's PDF link returns a PDF to an automated request; recorded
  in both remarks.
- **Phase 7 has no re-derived prose number.** The abstract's figure is the library size, 1.9 × 10⁷
  variants, which is the number of *molecules screened* rather than the number scored, so it cannot be
  re-derived from a 2,470-row deposit. If the PDF is fetched, the count of positions identified as
  functionally important is the number to check.
- The positive and negative arms together define a **specificity** measure — on-target activity against
  off-target cleavage — which under Phase 1 would be a third work item with its own property, and a
  derived readout. Not constructed, because the two arms' scores are not obviously on a common scale.

## Other 2017 items seen and not taken

From the MaveDB enumeration on the `2015` branch:

- **`10.15252/msb.20177908`** — the Weile framework. **Now curated, see above.**
- **`10.7554/elife.27810`** — Ras, 4 score sets of 3,300 each (Unregulated, Attenuated, Regulated, and a
  G12V background), UniProt P01112, CC0. **Rejected: outside the enzyme scope, on the readout half.**
  Ras is a GTPase and so catalytic by protein, but these variants were selected by a **bacterial
  two-hybrid**, which reports Ras–effector *binding* rather than GTP hydrolysis. The scope test asks what
  the readout reports, not only what the protein is — the same reasoning that excludes a yeast
  surface-display level. Reopen only if a hydrolysis-based readout for the same library turns up.
- **`10.1093/nar/gkx183`** — a platform paper for assessing large variant libraries; likely a method
  paper whose data belongs to others.
