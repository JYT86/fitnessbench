# 2016 candidate papers

Screening notes for the `2016` branch. Cut from `main`, so it starts from the six Jiang 2024 PRIME
datasets and nothing else.

Part of the **2009–2020 MaveDB enzyme cohort**. The discovery work and the backlog files live on the
`2015` branch (`candidates_2015.md`, `backlog_pre2022.tsv`); this file records only what 2016 yielded.

## Scope — enzymes and enzyme-adjacent

Set on 2026-08-31 on the `2022` branch. Carried here verbatim.

**In scope**: catalysts, and proteins whose measured phenotype is catalytic machinery — nucleases,
polymerases, helicases, ATP-driven transporters.

**Out of scope**: fluorescent proteins, binding domains, ion channels, structural and scaffold
proteins, viral surface glycoproteins.

## Shipped — 4 datasets, 10,582 variants

### Steinberg 2016, the TEM-1 → TEM-15 adaptive pathway — 4 datasets

`10.1016/j.jmb.2016.04.033`, *Shifting Fitness and Epistatic Landscapes Reflect Trade-offs along an
Evolutionary Pathway*, J Mol Biol 2016. From `urn:mavedb:00000085` (CC0), in
`Activity/DrugResistance/DMS/`.

| Dataset | Wild type | Selection | `n_variants` |
|---|---|---|---|
| `…-TEM19-…-fitness_amp` | TEM-1 + G236S | ampicillin | 2,751 |
| `…-TEM17-…-fitness_amp` | TEM-1 + E102K | ampicillin | 2,139 |
| `…-TEM15-…-fitness_amp` | TEM-1 + E102K + G236S | ampicillin | 2,466 |
| `…-TEM15-…-fitness_cefotaxime` | TEM-1 + E102K + G236S | cefotaxime | 3,226 |

**Four score sets are four datasets, not one**, because three of them have different wild-type
sequences. Pooling would z-score incomparable series and write `mutant` labels against the wrong
parent.

**The allele identities are a chemistry check, not an alignment.** In Ambler numbering the background
substitutions are **G238S** and **E104K** — the two canonical extended-spectrum β-lactamase positions.
That is a third independent confirmation of this cohort's Ambler offset (+2 up to 236, +3 for
237–249, +4 for 250–286), after the motif positions on `2015` and the explicit `ambler` column on
`2014`. `bad = 0` against each background separately.

Between 872 and 1,178 rows per set carry no score and are dropped; the remarks give the count per
dataset. No set has a wild-type row, so `wt_readout` is empty throughout.

**Phase 7 re-derives the paper's headline across two branches.** The abstract claims "~12,500 unique
single amino acid mutants of the TEM-1, TEM-17, TEM-19, and TEM-15 β-lactamase alleles". The scored
variants come to 2,751 + 2,139 + 2,466 = **7,356** here, plus the **5,199** of the TEM-1 arm on the
`2014` branch, giving **12,555**. The TEM-1 arm is deposited separately as `urn:mavedb:00000070` and
belongs to the earlier Firnberg paper, which is why it is not duplicated here.

The two TEM-15 conditions share a wild type and correlate at **r = 0.831** over 2,306 shared variants,
with cefotaxime the wider spread (sd 0.448 against 0.160) — the expected direction, cefotaxime being
the selective condition for the resistant end of the pathway.

## A correction to the record

MaveDB carries **no publication identifier** for `urn:mavedb:00000085`, and the `2025` branch's
parked tracker attributed it to `10.1073/pnas.0901246106`. That is **Sohka 2009, "An externally
tunable bacterial band-pass filter"** — the method these experiments use, not the source of the
measurements, and a 2009 paper rather than a 2016 one. Acting on it would have put these datasets on
the wrong branch under the wrong authors.

The real source was found by searching Europe PMC for `AUTH:"Ostermeier M" AND (TEM-15 OR TEM-17 OR
TEM-19)`, whose abstract names the allele series outright. It had **already been surfaced** by the
2009–2020 sweep recorded on the `2015` branch, without anyone connecting it to the deposit — which is
the argument for keeping the sweep's backlog file rather than only its conclusions.

Every remark on this branch names the correct DOI and says why the other one is wrong, so the
misattribution does not propagate.

## Not done

- **The article is not staged in `papers/`.** J Mol Biol 2016 has no PMC deposit and Europe PMC reports
  it as not open access.
- Whether the **TEM-1 ampicillin arm of this same series** is better placed beside these three, rather
  than on `2014` under Firnberg, is a judgement the merge can revisit. It is measured on the same
  band-pass system but reported in the earlier paper.
