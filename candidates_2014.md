# 2014 candidate papers

Screening notes for the `2014` branch. Cut from `main`, so it starts from the six Jiang 2024 PRIME
datasets and nothing else.

Part of the **2009–2020 MaveDB enzyme cohort**. The discovery work and the backlog files live on the
`2015` branch (`candidates_2015.md`, `backlog_pre2022.tsv`); this file records only what 2014 yielded.

## Scope — enzymes and enzyme-adjacent

Set on 2026-08-31 on the `2022` branch. Carried here verbatim.

**In scope**: catalysts, and proteins whose measured phenotype is catalytic machinery — nucleases,
polymerases, helicases, ATP-driven transporters.

**Out of scope**: fluorescent proteins, binding domains, ion channels, structural and scaffold
proteins, viral surface glycoproteins.

## Shipped — 1 dataset, 5,199 variants

### Firnberg 2014, TEM-1 β-lactamase — 5,199 variants

`10.1093/molbev/msu081`, *A comprehensive, high-resolution map of a gene's fitness landscape*, Mol
Biol Evol 2014. From `urn:mavedb:00000070` (CC0), in `Activity/DrugResistance/DMS/`.

The **second** TEM-1 scan in this cohort and a genuinely different experiment from the Cell 2015 one
on the `2015` branch: PFunkel comprehensive codon mutagenesis read out through the Sohka band-pass
selection system, where cells grow only when β-lactamase activity falls inside a window — too little
fails the ampicillin challenge, too much prevents the cell-wall damage that induces TetC. The 2015
paper instead selects directly at five ampicillin concentrations. Same protein, different assay, so
both are curated.

Sequence matches UniProt P62593 exactly, 286 aa, bad = 0.

**This deposit settles the Ambler question for the whole cohort.** It ships an explicit `ambler`
column, populated on every row, and it gives the offset as **+2 over sequential 1–236, +3 over
237–249, +4 over 250–286**. The `2015` branch claims exactly that from motif positions alone, and the
`2016` branch confirms it a third time from the TEM allele identities. Three routes, one
authoritative and two inferential, agreeing.

Three row classes were handled rather than assumed:

- **20 rows** are readthroughs of the stop at sequential 287 and are dropped — a terminator has no
  wild-type residue to write in `{WT}{position}{MUT}`.
- **251 rows** carry no score.
- **270 rows** are synonymous but written in substitution form as `p.XnnX` rather than with `=`. The
  `wt != mut` assert caught them; they are the wild-type protein and collapse to the single WT row at
  their mean. Had the assert been relaxed instead, 270 no-op "variants" would have shipped.

**Of the deposit's four score sets only one is curated.** `a-4` is byte-identical to the `a-2` used
here, checked score by score across all 5,740 rows, and the other two are nucleotide-level.

## Not done

- **The article is not staged in `papers/`.** It is open access as `PMC4032126` but neither the
  `fullTextPDF` route nor `?pdf=render` returns a PDF to an automated request. Recorded in the remark.
- **Phase 7 has no re-derived prose number** for this paper on its own. The related re-derivation lives
  on the `2016` branch, where the Steinberg abstract's "~12,500 unique single amino acid mutants of the
  TEM-1, TEM-17, TEM-19, and TEM-15 alleles" comes out at 12,555 — and **5,199 of those are this
  dataset**. So this branch supplies a term in a check completed elsewhere.

## Other 2014 items seen and not taken

From the MaveDB enumeration on the `2015` branch:

- **`10.1093/nar/gku689`** — AID, activation-induced deaminase, 3 experiments. A deaminase, so in
  scope by protein; not opened. Human, so it would go to `datasets_human/`.
