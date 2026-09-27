# 2013 candidate papers

Screening notes for the `2013` branch. Cut from `main`, so it starts from the six Jiang 2024 PRIME
datasets and nothing else.

Part of the **2009–2020 MaveDB enzyme cohort**. The discovery work, the full enumeration of MaveDB
and the two backlog files live on the `2015` branch (`candidates_2015.md`, `backlog_pre2022.tsv`);
this file records only what 2013 yielded.

Note that a `2023` branch already exists and is unrelated — it holds 2023 publications. Do not
confuse the two when merging.

## Scope — enzymes and enzyme-adjacent

Set on 2026-08-31 on the `2022` branch. Carried here verbatim.

**In scope**: catalysts, and proteins whose measured phenotype is catalytic machinery — nucleases,
polymerases, helicases, ATP-driven transporters.

**Out of scope**: fluorescent proteins, binding domains, ion channels, structural and scaffold
proteins, viral surface glycoproteins.

An E3 ubiquitin ligase is in scope: the `2023` branch records Hrd1, a ligase, as explicitly passing.
The readout here is the domain's own auto-ubiquitination, which is catalysis rather than binding.

## Shipped — 1 dataset, 88,375 variants

### Starita 2013, E4B / Ube4b U-box domain — 88,375 variants

`10.1073/pnas.1303309110`, *Activity-enhancing mutations in an E3 ubiquitin ligase identified by
high-throughput mutagenesis*, PNAS 2013. From `urn:mavedb:00000004` (CC0), in
`Activity/CatalyticActivity/DMS/`.

**The largest single dataset in the benchmark**, and the only one so far that is not a saturation
scan. The library came from doped oligo synthesis at a 2 % per-position error rate, so genotypes
carry between 1 and 10 substitutions:

| substitutions | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| genotypes | 940 | 52,131 | 26,572 | 6,977 | 1,454 | 256 | 35 | 8 | 1 | 1 |

99 % of the file is multi-site, on a 102-residue domain. That makes it almost entirely epistasis,
which is what this benchmark has least of — worth knowing before anyone uses it as a single-mutant
set, because it is not one.

The target is the **U-box domain alone**, 102 aa, not full-length E4B. Every label verifies against
it and there are no duplicate genotypes: 88,375 groups from 88,375 rows, worst spread 0.

8,614 rows are dropped for a premature stop, a readthrough of the terminator at position 103, or
being synonymous at the protein level once the codon changes are applied. The wild-type row is the
deposit's own `_wt` entry and reads 0.

**Which score set, and why.** The deposit carries three. `a-3`, the amino-acid Enrich2 set, is the one
shipped, because it has both the wild-type row and per-replicate scores. `a-1` is the Enrich analysis
as published in 2013 over the *same measurements* and is deliberately not shipped, so the experiment
is not curated twice under two pipelines. `a-2` is nucleotide-level, which the four-column format
cannot express.

## Not done

- **The article is not staged in `papers/`.** `10.1073/pnas.1303309110` is `PMC3619334` but Europe PMC
  reports it as not open access. Worth one attempt by hand.
- **Phase 7 has no re-derived prose number.** The paper's headline is qualitative — activity-enhancing
  mutations exist — and the numeric claims are in figures. The checks that were run are internal: the
  label check, the zero duplicate spread, and the row arithmetic closing exactly. If the PDF is
  fetched, the count of activity-enhancing variants is the number to check against.
- `a-1` could be shipped as a second dataset **only** if the project decides two analysis pipelines
  over one experiment are two datasets. They are not, under the current reading of Phase 1, since
  "what was done" and "what was counted" are both identical.
