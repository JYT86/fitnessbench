# Proposed amendments to `fitnessbench-digger`

From curating Zhang et al. 2025 (PylRS, `10.1038/s41467-025-61952-2`) on the `2025`
branch — done before the skill landed on `main`, then checked back against it. Six
suggestions, each with the case that produced it. Two of them are places where the skill
as written led me to the wrong answer; the rest are gaps I hit that it does not cover.

These come from **one paper**, so they are accumulated experience rather than a
specification — the same standing the skill gives its own journal tables. Take what is
useful.

> **Target file:** `skill/fitnessbench-digger/SKILL.md` on `main`.
> **This file is a proposal, not documentation.** It is carried on the `2025` branch only
> so the amendments can be read next to the datasets that motivated them. Delete it once
> each item has been accepted or declined — a proposal left lying around reads as a second
> protocol, which is exactly what retiring `curation_notes_2025.md` was meant to avoid.

| # | Target | What | Priority |
|---|---|---|---|
| A1 | Phase 1, *What does not justify a split* | Say **how** to merge rounds against a moving parent, and when you cannot | high — changed our output |
| A2 | Repo shape, `{Model}` | A named method from prior literature is "merely used" | high — changed our filenames |
| A3 | Phase 0b / 0c | Direct Nature-family retrieval route, and a third failure signature | high — converts hand-offs into retrievals |
| A4 | Phase 1 | Per-figure Source Data: map panel overlaps before writing the work list | medium |
| A5 | Phase 4 | Labels whose wild-type residue you supplied are unverified by 3b | medium |
| A6 | Phase 4, duplicates table | A precedence ladder for "investigate" | low |

Plus one cross-document inconsistency at the end, which is not a skill change.

---

## A1 — Phase 1: merging rounds against a moving parent

**Target.** The *What does not justify a split* table, row:

> | a second round or generation of engineering on the same protein | one work item; the later round is more rows, and its multi-site variants are the only epistasis signal in the file |

**Why.** I read this rule the other way and shipped two CSVs. In fairness to the reading:
Zhang 2025's round 2 is normalised to Com1-IFRS, which is round 1's winner and a
*different sequence* — seven substitutions from round 1's parent. The skill's own
definition of a work item is "one wild-type sequence × one measurement", and by that
line the two rounds have two wild types. The rule and the definition point opposite ways
and the row does not say which wins, or what the merge would even look like.

It is worth resolving because the merged file is the better artifact: 508 variants in one
z-score population instead of 101 and 407 in two, with Com1-IFRS itself becoming an
ordinary 7-mutation row and the round-2 winners becoming 11-mutation rows. That is
exactly the epistasis signal the row already says it cares about.

**Proposed replacement row plus a following paragraph:**

> | a second round or generation of engineering on the same protein | one work item — see *Rebasing a later round* |

> ### Rebasing a later round
>
> A campaign that improves its own parent reports each round against the parent of that
> round, so the later rounds arrive in a different scale **and** in different labels. Both
> are convertible, and the conversion is what makes it one work item rather than several:
>
> - **Scale.** Multiply the later round's values by the parent's own value on the first
>   round's scale. Zhang 2025's Com1-IFRS reads 11.12 in round 1, so round 2's
>   parent-relative values are multiplied by 11.12.
> - **Labels.** Re-express every later-round label against the *first* wild type, by
>   prepending the parent's own substitutions. Round 2's `N7Y:H63L:K67N:V74W` becomes an
>   11-substitution label once Com1-IFRS's seven are folded in.
>
> The rounds then share exactly one genotype — the later parent, which is a measured row
> in the earlier round and the definitional 1.0 in the later one. That single point is the
> whole join, so `remark` must say so, per Phase 4's rule on blocks sharing only a control.
>
> **Check the composition against the paper.** A campaign that quotes a cumulative
> fold-change is handing you the test: Zhang 2025 states 30.8-fold for its final variant
> over the original parent, and 11.12 × 2.75 = 30.6 confirms both the rebasing and the
> label chain in one number. If no such statement exists, say so — the merge then rests on
> the control alone.
>
> **When you cannot rebase, it is two work items after all.** If the later parent was
> never measured on the earlier scale, or its own substitutions are not stated, there is no
> conversion and no join. Split, and record in each `remark` which parent its readout is
> against.

---

## A2 — Repo shape: a named method from prior literature is still "merely used"

**Target.** In *Repo shape*, the sentence after the `{Model}` fallback table:

> Software the paper merely *used* is not its method: Rosetta, AlphaFold and FoldX never fill this slot, however prominently they appear.

**Why.** I filled the slot with `FFTPLSR` and was wrong. FFT-PLSR is named 17 times in
Zhang 2025 including the abstract, which reads like a paper naming its own method — but it
is Innov'SAR, from the paper's refs 17–18, applied here rather than contributed. The
correct token under the existing table is `ML`: a learned model ranked the variants and
the paper gives *its own* framework no name.

The current sentence lists three tools, all of them software packages. A named
*statistical method* from prior work does not read as belonging to that list, which is how
the mistake happened. One clause fixes it.

**Proposed replacement:**

> Software or a method the paper merely *used* is not its method: Rosetta, AlphaFold and
> FoldX never fill this slot, and neither does a named modelling method taken from prior
> literature — Innov'SAR / FFT-PLSR, ProteinMPNN, ESM — however prominently it appears, and
> however much the abstract reads as though it were the paper's own. The test is
> contribution, not prominence: if the method has a citation, it is not this paper's name.
> A paper that applies a published regressor and names no framework of its own is `ML`.

---

## A3 — Phase 0b / 0c: the Nature-family direct route

**Why.** Zhang 2025's four files were all retrievable directly from the publisher, with no
PMC lookup and no hand-off. The skill's Nature row says where the links sit on the page,
which is what 0d quotes to the user — but there is a programmatic route that makes 0d
unnecessary for this family, and one failure signature whose current remedy is wrong.

**A3a — add to 0b, under the Nature-family row:**

> **Nature family, direct route.** `nature.com` answers a plain fetcher with `303 See
> Other` to `idp.nature.com/authorize`, so a fetch-and-summarise tool returns the redirect
> instead of the page. `curl -sL` with a browser user-agent follows it and gets the
> article; the supplementary links are then in the HTML, on `media.springernature.com`:
>
> ```bash
> UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0"
> curl -sL -A "$UA" "https://www.nature.com/articles/${ID}" -o article.html -w '%{http_code} %{size_download}\n'
> curl -sL -A "$UA" "https://www.nature.com/articles/${ID}.pdf" -o paper.pdf
> grep -oE 'https://media[^"]*MOESM[0-9]+_ESM\.[a-z]+' article.html | sort -u
> ```
>
> **`MOESM<n>` is positional, not the paper's own numbering** — `MOESM3` is not
> Supplementary Data 3. Read the caption text adjacent to each link, which is the listing
> 0a told you to trust. Zhang 2025 ran: `MOESM1` Supplementary Information PDF, `MOESM2`
> Description, `MOESM3` Supplementary Data xlsx, `MOESM4` Reporting Summary, `MOESM5` Peer
> Review, `MOESM6` Source Data xlsx.

**A3b — add a row to the 0c failure table:**

> | HTTP **200** with a ~3 KB body containing `Client Challenge` | rate limit, from issuing requests in parallel or in quick succession | serialise and retry — this one is **not** a mirror problem, and another mirror will not help |

This is a distinct signature from the two size-based rows already there: the status is 200,
`file` says HTML for an HTML request, and nothing is wrong with the host. Six parallel
fetches tripped it for me; the same six issued one at a time all succeeded. The existing
rows would send you to another mirror, which does not fix it.

Worth pairing with a line under the table:

> Print `%{size_download}` on every fetch and read it. A challenge page is not an error —
> it returns 200, parses as valid HTML, and yields zero rows without raising anything.

---

## A4 — Phase 1: map panel overlaps before writing the work list

**Why.** Nature Source Data is one sheet **per figure panel**, so a single work item's rows
are scattered across sheets and the same variant recurs in several. Zhang 2025 had 35
sheets, 11 with measurements, 7 of them feeding one readout. Three consequences the current
Phase 1 does not anticipate:

- `Where it lives` expects `file › locator`. With seven panels the locator is a list, and
  a single cell cannot hold it honestly.
- `Rows` is defined as what the source holds before merging — but summed naively across
  panels it double-counts every shared variant. For Zhang 2025 the naive sum was 341 and
  the true figure 407.
- **A panel can hold data the paper never counts.** Fig. 2b is described only as a scatter
  of "single variants designed"; the sheet behind it carries 115 measured single mutants
  across 85 positions, a quarter of that dataset. Nothing in the prose reaches it.

**Proposed insert, in Phase 1 before *Present the table*:**

> ### Per-figure Source Data: map the panels first
>
> When the inventory shows one sheet per figure panel, one work item is spread across
> several of them and the same variant appears in more than one. Enumerate labels per
> sheet and print the pairwise overlaps before writing a single row of the work list:
>
> ```python
> panels = {t: set(labels_of(wb[t])) for t in wb.sheetnames}
> for a, b in itertools.combinations(panels, 2):
>     if panels[a] & panels[b]:
>         print(a, b, len(panels[a] & panels[b]))
> ```
>
> | Overlap | What it is |
> |---|---|
> | same labels, same values | one measurement re-plotted — one panel, not two |
> | a *predicted vs experimental* sheet whose experimental column matches another sheet's replicate mean | the model-accuracy scatter; use the replicates, keep the scatter as a check |
> | same labels, different values | two experiments, or an inconsistency — Phase 4 |
>
> Then: `Rows` is the size of the **union**, never the sum. `Where it lives` names the sheets
> as a list, and if there are more than three, names the workbook and the count and puts the
> full list under the table.
>
> **A panel may also be a matrix rather than a list.** A mutability landscape ships as 20
> amino-acid rows by N site columns. Melt it to labels, and drop the cell where the
> substituted residue equals the site's own residue — it reads 1.0 (or 100%) because it is
> the parent, not because a variant was measured.
>
> **Count from the sheets, not the prose.** A panel routinely holds more than the text
> describes; the figure needed a scatter, not a number in a sentence.

---

## A5 — Phase 4: labels whose wild-type residue you supplied are unverified

**Why.** This one has teeth, and the skill already has the hazard without naming it.

Zhang 2025's Fig. 2b is keyed `residue index | residue type | method | activity` — position
and *substituted* residue, no wild-type letter. To build `{WT}{pos}{MUT}` you take the
letter from your own reference sequence, at which point the label agrees with that sequence
**by construction**. 3b's `bad` is empty for those rows no matter what: an off-by-one in the
sheet's indexing would produce 115 labels that all apply cleanly and are all wrong.

The same hazard sits in Phase 4's existing `to_mutant`, which reads `WT[p-1]` for
combinatorial codes — so the note belongs right there rather than as a new concept.

**Proposed insert, immediately after the `to_mutant` code block:**

> **A label you completed is not a label you read.** Both this converter and any sheet keyed
> by position-plus-substituted-residue take the wild-type letter from `WT` itself, so the
> resulting label agrees with the sequence by construction and **3b cannot see it**. An
> off-by-one in the source's own indexing yields labels that every downstream assert
> accepts.
>
> The only check is external agreement. Before trusting completed labels:
>
> - find labels printed in full — with their wild-type letter — anywhere else in the same
>   bundle, and intersect. In Zhang 2025, 18 of the 115 completed labels also appear in the
>   mutability landscape, and 13 carry identical values, which an offset could not produce.
> - state the overlap as a number in the report, and if the overlap is **empty**, say in
>   `remark` that the labels are completed rather than read, and from which sequence.
>
> This is clause 1 of the `remark` shape — the sequence clause — not clause 2.

---

## A6 — Phase 4: a precedence ladder for "investigate"

**Target.** The duplicates table row:

> | Large, rows from the same well | contradiction in the source | investigate; do not average silently |

**Why.** Correct, and the only row that does not say what to *do*. The Zhang 2025 case:
Fig. 2b and 2d share 18 labels, 13 identical to the last digit and 3 more within 0.03 — so
they are one measurement set re-plotted — while N7D reads 0.634 against 0.472 and K67R
0.527 against 0.801. Averaging those two produces a number neither sheet prints.

**Proposed addition under the table:**

> When two blocks are one measurement re-plotted and a few pairs still disagree, do not
> widen `tol` and do not average — rank the blocks once and take the better-ranked value
> throughout, so the file is internally consistent about its source:
>
> 1. measured in triplicate and drawn with error bars
> 2. a systematic screen — a saturation landscape, a designed library
> 3. a scatter or summary that re-plots either of the above
>
> Then record, in one sentence: how many labels overlap, how many agree, and the
> disagreeing pairs with **both** values. A reader who cares can go to the source; a reader
> who does not is not misled by a mean.

---

## Not proposed — checked and left alone

- **`wt_readout` 1.0 with no WT row.** Phase 7 already covers this precisely, by name,
  citing `Jiang 2024-PRIME-TgoD4K`. Our two datasets follow it, remark and all.
- **Prose re-derivation.** Already Phase 7, and already the strongest thing in the skill.
  Our run bears it out: re-deriving the mutability-landscape counts reproduced the paper's
  3/7/5/1/2/9 exactly *and* surfaced that the sentence stating them names positions V73 and
  D75 while the source columns are V74 and D76.
- **Staging supplements only when a shipped row draws on them.** We diverged — the 26 MB SI
  PDF is used, for the `Z7-n` expansions in Supplementary Table 8, and we left it out of the
  commit on size grounds. The skill's rule is the better one and we were wrong; noting it
  here only so the gap in our branch is not mistaken for a disagreement.

## One inconsistency to resolve — not a skill change

Phase 4 says that with no WT row, `wt_readout` "stays empty", and Phase 7 asserts
`ref['wt_readout'].strip() == '' or ref['remark'].strip()`. But `validate.py` on the
unpushed `add-validation` branch builds `REFERENCE_REQUIRED` as every column except
`remark`, so an empty `wt_readout` is a hard error there. One of the two has to move.

Suggestion: `validate.py` drops `wt_readout` from `REFERENCE_REQUIRED` and instead enforces
Phase 7's rule — empty is fine, non-empty must be numeric, and non-empty with no WT row
requires a non-empty `remark`. That keeps the skill's wording and makes the validator agree
with it. Worth settling before `add-validation` merges, since three branches now append to
`datasets/Activity/reference.csv`.

## Out of scope, offered separately

The skill starts from a known paper and says so explicitly — an empty argument means ask
and stop. The step before it, **finding candidate papers at all**, is what
`candidates_2025.md` on the `2025` branch does: screen a year's publisher search on the
abstract *plus* the data-availability statement, shortlist, and record the rejects with
reasons so the next sweep does not re-offer them. If that is wanted it should be a sibling
skill rather than a phase here, since it ends where this one begins.
