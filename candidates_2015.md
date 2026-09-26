# 2015 candidate papers

Screening notes for the `2015` branch. Cut from `main`, as `2022` through `2026` were, so it
starts from the six Jiang 2024 PRIME datasets and nothing else.

This branch exists because the **2009–2020 window is covered by no branch at all**, and that is
where MaveDB's enzyme back catalogue lives. The `2025` branch parked it as a single
"2009–2020: 26 publications / 87 score sets" tracker entry and never worked it. The
publication-year convention gives each of those papers its own branch; this is the first.

## Open task — needs a person, not a sweep

**Fetch the Cell 2015 article PDF.** `10.1016/j.cell.2015.01.035`,
<https://www.cell.com/cell/fulltext/S0092-8674(15)00078-1>

Unpaywall reports it **bronze OA**, so it is free in a browser, but `cell.com` returns HTTP 403 to
automated requests — both the PDF and the fulltext URL, confirmed, not assumed. Drop it into
`papers/` under the publisher's own filename and the rename is mine to do.

What it unblocks: the seven shipped rows carry an **empty `wt_readout`** because the MaveDB deposit
has no wild-type row and never states what the fitness score is relative to. If the article defines
the metric against wild type, `wt_readout` becomes `0.0 by definition` and the remark says so — the
`Jiang 2024-PRIME-TgoD4K` precedent. It would change **only `wt_readout` and `remark`**; `readout`
and `normalized-score` are unaffected either way, which is why the datasets shipped without it
rather than waiting.

## Scope — enzymes and enzyme-adjacent

Set on 2026-08-31 on the `2022` branch. Carried here verbatim.

**In scope**: catalysts, and proteins whose measured phenotype is catalytic machinery — nucleases,
polymerases, helicases, ATP-driven transporters.

**Out of scope**: fluorescent proteins, binding domains, ion channels, structural and scaffold
proteins, viral surface glycoproteins.

## Shipped

### Stiffler 2015, TEM-1 β-lactamase — CURATED, 7 datasets, 34,827 variants

`10.1016/j.cell.2015.01.035`, *Evolvability as a function of purifying selection in TEM-1
β-lactamase*, Cell 2015. Curated from the authors' MaveDB deposit `urn:mavedb:00000086` (CC0), not
from the article.

TEM-1 is the most-scanned enzyme in MaveDB and this benchmark had none of it, purely because every
TEM-1 paper predates 2022.

Seven conditions on one wild type, all in `Activity/DrugResistance/DMS/`: ampicillin at 10, 39,
156, 625 and 2500 µg/mL, cefotaxime at 0.15 µg/mL, and the unselected control. Every source row is
a single substitution — no nonsense, no synonymous, no indels — so the only rows dropped are the
133 (10 µg/mL) and 19 (cefotaxime) that carry no score.

**The unselected arm is the weakest of the seven** and was curated because the Fks1 precedent
curates a no-drug control as a dataset. Its sd is 0.061 against 0.711 at 156 µg/mL and it
correlates at r = 0.035 with the selected arms, so it ranks noise rather than resistance. Anyone
benchmarking on this branch should know that before using it.

**Positions are sequential, not Ambler.** Ambler = sequential + 2 up to 236, + 3 for 237–249, + 4
for 250–287. Established twice: the STFK and SDN motifs sit at sequential 68 and 128 against Ambler
70 and 130, and the same group's deposit `urn:mavedb:00000070` ships an explicit `ambler` column
that agrees. This is in all seven remarks because the β-lactamase literature numbers this enzyme
the other way, so `E104K` here is not the literature's Ambler E104K.

That mapping also removes the blocker on the `2025` branch's parked β-lactamase item
(`10.1016/j.jbc.2025.110347`), which was held up partly by needing "5 separate Ambler→sequence
alignments".

## The rest of the pre-2022 cohort — enumerated, verified reachable, unclaimed

Every one of these downloads from MaveDB with the same schema
(`accession, hgvs_nt, hgvs_splice, hgvs_pro, score, …`), all **CC0**, all per-variant, HGVS protein
notation that converts directly to `{WT}{position}{MUT}`. None needs a publisher.

| Publication | Protein | Organism | Score sets | Variants/set | Belongs on |
|---|---|---|---|---|---|
| `10.7554/elife.56707` (2020) | **VIM-2 metallo-β-lactamase** | *P. aeruginosa* | 9 | 5,549 | a `2020` branch |
| `10.1093/molbev/msu081` (2014) | **TEM-1 β-lactamase** | *E. coli* | 2 (aa-level) | 5,740 | a `2014` branch |
| `urn:mavedb:00000004-a` | **E4B ubiquitin E3 ligase** | *M. musculus* | 1 (aa-level) | 96,991 | year TBD |
| `10.1186/s13073-020-0711-1` (2020) | **CBS**, cystathionine β-synthase | human | 2 **raw** | 11,478 / 10,802 | `datasets_human/`, 2020 |
| `10.7554/elife.53476` (2020) | **DHFR** | *E. coli* BL21(DE3) | 2 | 3,171 / 3,132 | a `2020` branch |
| `10.1038/s41598-017-17081-y` (2017) | **SpCas9** | *S. pyogenes* | 2 | 2,470 | a `2017` branch |
| `urn:mavedb:00000085-a…d` | **TEM-15 / TEM-17 / TEM-19** | *E. coli* | 4 | — | `10.1073/pnas.0901246106`, 2009 |
| `10.1093/nar/gku689` (2014) | **AID**, activation-induced deaminase | human | 3 exp | — | a `2014` branch |
| `10.7554/elife.27810` (2017) | **Ras** (GTPase switching cycle) | human | 4 exp | — | check scope: GTP hydrolysis |
| `10.1016/j.ajhg.2018.03.018` (2018) | **PTEN** lipid phosphatase | human | 1 | — | `datasets_human/`, 2018 |
| `10.1016/j.molcel.2019.02.003` (2019) | **Src** kinase | human | 2 | — | `datasets_human/`, 2019 |
| `10.7554/elife.58026` (2020) | **VKOR**, vitamin K epoxide reductase | human | 1 | — | `datasets_human/`, 2020 |
| `10.1002/jimd.12227` (2020) | human enzyme, 200 missense variants | human | 1 | ~200 | `datasets_human/`, 2020 |
| `10.15252/msb.20177908` (2017) | UBE2I, TPK1 (+ SUMO1, CALM1 — mixed) | human | 5 exp | — | split by target first |

DHFR and SpCas9 resolve to exactly **6,303 over 2 sets** and **4,940 over 2 sets**, matching the
counts the `2025` branch's parked tracker recorded for them — an independent check that this
enumeration agrees with that one.

**Rejected on the format, not on merit:** `10.1016/j.jmb.2019.04.030`, *Fitness Effects of Single
Amino Acid Insertions and Deletions in TEM-1 β-Lactamase* (2019, 2 sets). Insertions and deletions
cannot be written as `{WT}{position}{MUT}`, so the four-column format has no way to express them.
Worth reopening only if the format ever grows an indel notation.

**Out of scope, and numerous:** the `FYN SH3 domain` series (`urn:mavedb:00000116`–`00000120` and
onwards, one experiment per background) is a binding domain scored by proteolytic digestion, so it
fails the scope on both halves. The same applies to `10.1038/s41467-026-70341-2`, *The genetic
architecture of an allosteric hormone receptor*, whose 14 experiments make it look large.

## Recent years, from the same enumeration

Enzyme-matching MaveDB experiments at 2024 and 2026 that no branch has recorded:

- **`10.1101/2024.02.13.579700`** — a missense variant effect map for **CHK2**, a serine/threonine
  kinase. Belongs to `2024`.
- **`10.64898/2026.02.09.704817`** — a functional genetic atlas of **Parkin**, a ubiquitin E3 ligase
  acting downstream of PINK1. Belongs to `2026`.
- **`10.1038/s41588-024-01800-z`** — saturation genome editing of **VHL**. VHL is the substrate
  recognition component of an E3 ligase complex rather than the catalytic subunit, and the readout is
  a cellular function score; scope needs deciding before any work.

Notes per row:

- **VIM-2** is the highest-value item here. Nine conditions on one wild type — ampicillin at 2/16/128
  µg/mL × 25/37 °C, cefotaxime at 0.5/4, meropenem at 0.031 — so nine work items. It is also the
  table the `2024` branch recorded as unobtainable: the Chen J remark says the VIM-2 scan "was
  published previously (refs 5 and 50) and [its] per-variant table this paper does not carry". This
  is that table. Composition is 5,035 single substitutions + 247 synonymous + 267 nonsense.
  The signal peptide **was included in the assay**, so Phase 3 must settle the construct boundary.
- **TEM-1 MBE 2014** ships the `ambler` column described above. Its nucleotide-level sets (18,081
  each) are not directly usable; take the amino-acid sets.
- **CBS** ships both "imputed and refined" sets and **raw** ones. Take the raw pair — imputed scores
  are computed, not measured, and Phase 1 excludes computed columns.
- **HMGCR** (`urn:mavedb:00000035-a`, 3 × 18,448, human, statin conditions) is listed nowhere above
  because **all three of its sets are "imputed and refined"**. Find raw versions or reject it.

## Two items elsewhere that this sweep unblocked

- **Dengue NS5** — `urn:mavedb:00001276-a`, 2 sets × **16,897** variants, CC0. The `2023` branch
  parked `10.1101/2023.03.07.531617` as preprint-only and therefore uncuratable; the count matches
  exactly and the table is now deposited. NS5 is a methyltransferase and RNA polymerase, not a
  surface glycoprotein, so it goes to `datasets_virus/`. **Check the readout half of the scope test
  first**: it is measured "under type-I IFN", which reports immune antagonism rather than catalysis.
- **HMBS** — `10.1016/j.ajhg.2023.08.012`, 19,120 variants. The `2023` branch filed this under "fail
  the scope", but HMBS is hydroxymethylbilane synthase, an enzyme. It may have been rejected for
  being human before `datasets_human/` existed. Worth re-reading.

## The 2009–2020 Europe PMC sweep — run, and mostly empty

No branch had ever queried this window. Five date-chunked queries over the enzyme × library-scale
vocabulary at `SRC:MED`, 2009 through 2020, returned **898 records, 893 of them unseen**. All 893 are
in `backlog_pre2022.tsv` with a verdict each, so this is resumable rather than a one-off.

| Verdict | Count |
|---|---|
| unopened | 412 |
| rejected: no library-scale technique named | 249 |
| rejected: computational | 99 |
| rejected: outside the enzyme scope | 70 |
| rejected: no enzyme term | 35 |
| rejected: landscape in the cancer/theory sense | 28 |

**The yield rate here is low, and the reason is the era, not the query.** Deep mutational scanning
dates from about 2010 and only became common mid-decade, so the 2009–2020 enzyme literature is
overwhelmingly champion-shaped: a handful of rationally chosen or site-saturated positions, screened
to one improved clone. Titles in the unopened pile run "Engineering the substrate binding site of…",
"Improving thermostability and catalytic activity of…", "Site-saturation mutagenesis of tryptophan
116 of…". Under the 20-variant floor most of these are rejections waiting to be confirmed.

**MaveDB is the better index for this window**, and by a wide margin — it holds only deposited
per-variant data, so everything in it has already passed the test that most of these 893 will fail.
Every confirmed pre-2022 lead in the table above came from MaveDB, not from here.

Two survivors are worth opening first:

- **`10.1093/nar/gku511`** (2014) — *Comprehensive mutational scanning of a kinase in vivo reveals
  substrate-dependent fitness landscapes*. `inEPMC:Y`, `hasSuppl:Y`, and a genuine library-scale scan
  of an aminoglycoside kinase against multiple substrates, so several work items on one wild type.
- **`10.1371/journal.pone.0073727`** (2013) — *Systematic mutational analysis of the putative
  hydrolase PqsE*. Open access, in EPMC, with supplements. Scale needs checking.

### Two vocabulary traps this sweep walked into

**"Mutational landscape" and "fitness landscape" have senses that are not ours, and in this window
they dominate.** Cancer genomics uses "the mutational landscape of adenoid cystic carcinoma";
evolutionary theory uses "predictability of evolutionary trajectories in fitness landscapes". A first
triage keying on those phrases surfaced 136 candidates of which the large majority were exome studies,
reviews and off-lattice folding models. This is the same failure the `2026` branch recorded for
"high-throughput screening" meaning small-molecule screening: the word carries two unrelated meanings
and only one of them is ours.

**"Saturation mutagenesis" is a weak signal before about 2020.** In this era it nearly always means
site-saturation at one to three chosen positions — at most 57 variants, and usually reported as a few
improved clones — rather than a library-scale scan. Post-2020 the same phrase reliably means the
scan. The `2026` backlog already carries two rejections of exactly this shape, "saturation at one
residue, Arg121" and "Gly374".

## Method notes

**MaveDB's API will not page, and its text search caps at 100.** `POST /api/v1/score-sets/search`
returns at most 100 score sets and ignores `limit`/`offset` (HTTP 422). There are **2,819 published
score sets**; a keyword sweep over ~50 enzyme terms found 502, and `DHFR`, `kinase`, `APH` and
`enzyme` each hit the cap, so that 502 is a floor rather than an enumeration. Enumerating properly
means walking all 2,063 records from `GET /api/v1/experiments` and resolving their score sets.

**`.gitattributes` needed the `-text` rule before anything was staged.** `main` carries only the
`merge=union` line; the `original_datasets/** -text` and `papers/** -text` rules were added on `2025`
after a MaveDB CSV lost 1,202 bytes to `core.autocrlf`, which is `true` on this machine. These
sources are MaveDB CSVs. With the rule in place all seven stage byte-identically; without it they
would not have.

**Round `readout` before computing `normalized-score`.** Phase 5 says so, and 19 datasets on the
`2024` branches did it the other way — computing the z-score from full-precision values, then
rounding both columns — which fails `validate.py`'s 1e-6 assertion on ~155,000 rows. Rounding first
lands the worst deviation at 5.0e-07, exactly half a unit in the last place.
