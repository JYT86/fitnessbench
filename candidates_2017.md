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

## Shipped — 2 datasets, 4,808 variants

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

## Not done

- **The article is not staged in `papers/`.** It is open access as `PMC5715146` but neither Europe PMC's
  `fullTextPDF` route nor the publisher's PDF link returns a PDF to an automated request. Recorded in
  both remarks.
- **Phase 7 has no re-derived prose number.** The abstract's figure is the library size, 1.9 × 10⁷
  variants, which is the number of *molecules screened* rather than the number scored, so it cannot be
  re-derived from a 2,470-row deposit. If the PDF is fetched, the count of positions identified as
  functionally important is the number to check.
- The positive and negative arms together define a **specificity** measure — on-target activity against
  off-target cleavage — which under Phase 1 would be a third work item with its own property, and a
  derived readout. Not constructed, because the two arms' scores are not obviously on a common scale.

## Other 2017 items seen and not taken

From the MaveDB enumeration on the `2015` branch:

- **`10.15252/msb.20177908`** — the Weile framework, 5 experiments. Mixed targets: UBE2I and TPK1 are
  enzymes, SUMO1 and CALM1 are not, so it must be split by target before anything is curated.
- **`10.7554/elife.27810`** — Ras switching cycle, 4 experiments. A GTPase, so in scope by the
  hydrolysis reading, but the scope's transporter clause is about ATP-driven transport and the
  catalyst reading should be settled deliberately rather than assumed.
- **`10.1093/nar/gkx183`** — a platform paper for assessing large variant libraries; likely a method
  paper whose data belongs to others.
