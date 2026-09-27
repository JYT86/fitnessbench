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

## Shipped — 4 datasets, 5,826 variants

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

### Gajula 2014, AID cytidine deaminase — 3 datasets, 627 variants → `datasets_human/`

`10.1093/nar/gku689`, *High-throughput mutagenesis reveals functional determinants for DNA targeting
by activation-induced deaminase*, Nucleic Acids Res 2014. From `urn:mavedb:00000106` (CC0), in
`datasets_human/Activity/CatalyticActivity/Sat-Sel-Seq/`. Opens `datasets_human/` on this branch.

The model token is **`Sat-Sel-Seq`**, the method this paper contributes and names, which under the
Repo shape table always beats the `DMS` fallback.

Sequence is UniProt Q9GZX7 exactly, 198 aa, `bad = 0`. But **the library covers only positions
113–123**, eleven codons of the 198, so 187 residues carry no variant and rest on provenance alone.
209 variants per dataset — above the 20-variant floor, and narrow.

**Three generations of selection are three datasets, not one.** They are not reuploads: consecutive
generations correlate at r = 0.773 and 0.971, and selection visibly sharpens — the substitution median
falls 0.580 → 0.227 → 0.073 while the maximum rises 8.5 → 18.5 → 21.0. That is the same logic as the
ampicillin concentration series on `2015` and `2016`: a different amount of selection is a different
condition.

**The orientation was checked against the deposit's own dead-variant control.** The 11 nonsense rows
per generation sit *below* the substitutions in all three (0.141 vs 0.634, 0.039 vs 0.267, 0.021 vs
0.085), which is what a dead deaminase must do when the readout is rifampin resistance. So `score` is
used as it stands, and the build asserts that ordering rather than trusting it.

Each dataset keeps a wild-type row, collapsed from the 11 rows the deposit writes in substitution form
as `p.XnnX` rather than with `=`. The WT readout **rises with selection depth — 2.834, 6.716, 9.150** —
which is the expected direction for wild-type AID being enriched, and an independent sign the
generations are ordered as labelled.

The article is not staged in `papers/`: `PMC4150791` is open access but both the `fullTextPDF` route
and `?pdf=render` refuse an automated request.

## Other 2014 items seen and not taken

Nothing else from the MaveDB enumeration at 2014 remains unworked.
