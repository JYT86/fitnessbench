# Licences of the source data

Every dataset in this repository is *derived* from data someone else published. The derivation — the
four-column format, the verified wild-type sequence, the orientation and the z-score — is ours; the
measurements are not. This file records what terms the measurements came under, because that is not
recoverable from a CSV.

**Scope**: this file covers the 2009–2020 MaveDB enzyme cohort, curated on the `2013`–`2020` branches.
It should move to `main` when those branches merge, and be extended to cover the other branches.

## The short version

| Licence | Score sets | Datasets |
|---|---|---|
| **CC0 1.0** (public domain dedication) | 39 | 36 |
| **CC BY-NC-SA 4.0** | 2 | 1 |

All but one dataset carries **no restriction at all**. That is worth stating plainly, because it is a
strong position for a benchmark and nothing in the repository recorded it before.

## The exception, and what it requires

**`Sirr 2020-DMS-PSAT1-growthfitness-complementation.csv`** — on this branch, under
`datasets_human/Fitness/GrowthFitness/DMS/`.

Source: MaveDB `urn:mavedb:00000107` (score sets `a-1` and `b-1`), from Sirr A, Lo RS, Cromie GA,
Scott AC, Ashmead J, Heyesus M, Dudley AM, *A yeast-based complementation assay elucidates the
functional impact of 200 missense variants in human PSAT1*, J Inherit Metab Dis 2020,
`10.1002/jimd.12227`.

Licence: **CC BY-NC-SA 4.0** — <https://creativecommons.org/licenses/by-nc-sa/4.0/>

Three terms, all of which travel with the data:

- **BY — attribution.** Any redistribution must credit the authors above and MaveDB
  `urn:mavedb:00000107`. The `reference.csv` `remark` for this dataset carries both.
- **NC — non-commercial.** This dataset may not be used for commercial purposes. It is the only
  dataset in the cohort with that restriction, so a commercial user can take everything else and must
  exclude this one file.
- **SA — share-alike.** Any *adaptation* of this dataset must itself be released under CC BY-NC-SA 4.0.

**Why shipping it alongside CC0 data is acceptable.** This repository is a *collection*: each dataset
sits in its own file under its own terms, and the collection does not merge them into a single derived
work. Under CC BY-NC-SA 4.0 that is aggregation, not adaptation, so ShareAlike does not reach the other
datasets. What would change that is anything that *combines* them — a single merged table, or a model
trained across the whole corpus — where the NC and SA terms would attach to the result.

**If that is not a trade you want**, deleting the one file and its two staged sources removes the
restriction entirely, and the rest of the cohort is unaffected.

## CC0 sources, by paper

All of the following are CC0 1.0 in MaveDB — no attribution required, no restrictions. Citing the
original publication remains the right thing to do, and every `reference.csv` row carries its DOI.

| Branch | Paper | MaveDB | Score sets |
|---|---|---|---|
| `2013` | Starita 2013, E4B U-box | `urn:mavedb:00000004` | 1 |
| `2014` | Firnberg 2014, TEM-1 | `urn:mavedb:00000070` | 1 |
| `2014` | Gajula 2014, AID | `urn:mavedb:00000106` | 3 |
| `2015` | Stiffler 2015, TEM-1 | `urn:mavedb:00000086` | 7 |
| `2016` | Steinberg 2016, TEM-19/17/15 | `urn:mavedb:00000085` | 4 |
| `2017` | Spencer 2017, SpCas9 | `urn:mavedb:00000071` | 2 |
| `2017` | Weile 2017, UBE2I and TPK1 | `urn:mavedb:00000001`, `00001251` | 3 |
| `2018` | Mighell 2018, PTEN | `urn:mavedb:00000054` | 1 |
| `2019` | Ahler 2019, Src | `urn:mavedb:00000041` | 2 |
| `2020` | Chen 2020, VIM-2 | `urn:mavedb:00000073` | 9 |
| `2020` | Thompson 2020, DHFR | `urn:mavedb:00000063` | 2 |
| `2020` | Sun 2020, CBS | `urn:mavedb:00000005` | 2 |
| `2020` | Chiasson 2020, VKOR | `urn:mavedb:00000078` | 2 |

One dataset on the `2019` branch is not from MaveDB: **Gonzalez 2019, TEM-1 pairwise doubles**, taken
from the article's own supplementary workbook (`10.1016/j.jmb.2019.03.020`, Elsevier). Publisher
supplements carry the publisher's terms rather than a Creative Commons licence; it is curated on the
same footing as the rest of `original_datasets/`, which the README already describes as redistributed
under their publishers' terms.

## How to check this yourself

MaveDB reports the licence per score set:

```bash
curl -s https://api.mavedb.org/api/v1/score-sets/urn%3Amavedb%3A00000107-a-1 | \
  python -c "import json,sys; print(json.load(sys.stdin)['license'])"
```

## A note for whoever wires this up properly

`reference.csv` is fixed at eleven columns and `validate.py` enforces that, so the licence is recorded
in `remark` rather than in a column of its own. That is the right place under the repo's own rule —
a `remark` records what this version does differently, and CC0 is the norm here, so only the exception
is written. If the collection ever grows enough non-CC0 data that this stops being an exception, a
twelfth column and a matching corruption case in `test_validate.py` would be the better answer.
