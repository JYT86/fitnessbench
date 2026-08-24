---
name: fitnessbench-digger
description: ⛏ Curate a publication's experimentally measured protein variant data into FitnessBench format — locate and download the real source data, extract tables out of supplementary PDFs, establish the wild-type sequence and its residue numbering, assemble variants, orient and normalize the readout, then write the dataset CSV and its reference.csv row under gated validation checks. Use whenever adding a paper or dataset to FitnessBench, pulling variant readouts out of a supplementary PDF or spreadsheet, deciding which category a measurement belongs in, or auditing an existing FitnessBench dataset.
---

# ⛏ Adding a paper to FitnessBench

## Start here — resolve the input, before anything else

Arguments are free text and may be empty. Decide which case you are in and act; do not begin any
phase until the target is fixed.

| What you were given | Do |
|---|---|
| A DOI or article URL | resolve it, then Phase 0 |
| A path to a PDF, or one named in `papers/` | read its front matter for the DOI and journal, confirm the match in one line, then Phase 0 |
| A paper already discussed in this conversation | use it; restate which one in one line, then Phase 0 |
| A request to audit or fix an existing dataset | skip to Phase 7 against the named CSVs; report, do not silently rewrite |
| **Nothing, or too vague to identify one paper** | **Ask, and stop.** |

When you must ask, ask exactly this and wait:

> Which paper? Give a DOI, a path under `papers/`, or a title.
> If you already know which `(protein, readout)` pairs you want, say so — otherwise I will
> enumerate the candidates in Phase 1 and you pick.

**Do not** fill an empty argument by listing what is already in `datasets/`, by picking the most
recent paper in `papers/`, by surveying the repo, or by explaining the workflow instead of running
it. An empty invocation is a request to start work, not a request for a description of the work.

## Already curated? — check before Phase 0

Once the target is fixed, and before enumerating anything, check whether this paper has been
through here already:

```bash
DOI=10.1038/s41467-024-50698-y
grep -lF "$DOI" datasets/*/reference.csv
ls papers/ original_datasets/ | grep -i "<FirstAuthor> <Year>"
```

| Found | Do |
|---|---|
| no row carries the DOI, nothing staged | new paper — go to Phase 0 |
| files staged under `papers/`, still no row anywhere | staged and never shipped, or every item was rejected and nothing survived to record it. Say which you cannot tell apart, then Phase 0 |
| one or more `reference.csv` rows carry the DOI | **stop and ask**, after building the table below |

### Build the table before you ask

`remark` is the only place an earlier pass's decisions survive. Read the `remark` of **every** row
carrying that DOI, across all categories — exclusions live there, e.g. `the NNK control library is
excluded, its members having no genotype` or `Activity at 50 degC is reported for only WT and 5
variants, so it is not included`. The shipped rows and those remarks together are the candidate list.

| Candidate | Status | Where / why |
|---|---|---|
| RmaCytC, C–B yield | extracted | `CatalyticActivity/MODIFY/Ding 2024-…-CB_yield.csv`, 149 variants |
| RmaCytC, C–Si yield | extracted | `CatalyticActivity/MODIFY/Ding 2024-…-CSi_yield.csv`, 149 variants |
| NNK control library | not extracted | no genotype, only plate and well |
| enantiomeric ratio | not extracted | `remark` says excluded, gives no reason |

Two rules:

- **A reason that is not in a `remark` is not a reason.** Write `no reason recorded` and leave it
  there. Do not re-read the paper to reconstruct why the earlier pass skipped something — a
  plausible reason invented now is indistinguishable from one the earlier pass actually had, and
  the gaps in what the repo knows are part of the answer you owe the user.
- The candidate list comes from the repo, so it can only be as complete as the remarks are. Say so.
  Phase 1 re-enumerates from the paper and may surface candidates no remark ever mentioned.

Present the table, then ask exactly this and wait:

> This paper is already curated. Do you want to (1) double-check the shipped datasets,
> (2) work the un-extracted candidates, or (3) stop?

| Answer | Do |
|---|---|
| double-check | Phase 7 against each shipped CSV, re-deriving a stated number for each. Report; do not silently rewrite |
| work the un-extracted | Phases 0–1 on the full paper, then drop the already-shipped items from the work list |
| stop | stop |

## Done means

A shipped work item is one `(protein, readout)` pair that has:

1. a CSV at `datasets/{Category}/{Property}/{Source}/` with exactly the four columns,
2. one appended row in `datasets/{Category}/reference.csv` whose derived fields were computed from
   that CSV, not typed,
3. every Phase 7 assertion passing, **and**
4. at least one number the paper states in prose re-derived from the finished data.

Anything short of all four is not shipped. A work item may also end **rejected** — that is a
legitimate outcome, not a failure. It must be reported, and **recorded where the next run will
find it** (Phase 6), never silently dropped.

## The loop

```
Phase 0  acquire the paper and all it ships         -> files in hand + an inventory, or REJECT
Phase 1  enumerate work items                       -> work list, confirmed with the user
for each work item:
    Phase 2  read the methods                      -> basis, direction, assay_method, or REJECT
    Phase 3  establish WT sequence + numbering      -> sequence shown and approved, or REJECT
    Phase 4  assemble variants                      -> mutant/sequence pairs
    Phase 5  construct + orient + normalize readout -> readout, normalized-score
    Phase 6  write CSV and reference.csv row
    Phase 7  verify                                 -> SHIP, or back to the failing phase
```

Phases 0 and 1 are **paper-level and run once**: one paper has one attachment listing and one
supplementary bundle, and what those files actually contain is the most reliable source for the
work list. Enumerating from the abstract first and discovering the data later gets the order
backwards — half the list turns out to be figure-only.

Then finish one work item end to end before starting the next. Phases 0–3 are gated: a failed gate
sends you to a named branch or rejects the item — never to "proceed anyway and note it later".

## Repo shape

```
papers/{FirstAuthor} {Year}-{Model}-{Journal}.pdf
original_datasets/{FirstAuthor} {Year}-{Model}-{Journal}-{what it is}.{pdf,xlsx}
datasets/{Category}/{Property}/{Source}/{Author} {Year}-{Model}-{Protein}-{property}-{readout}.csv
datasets/{Category}/reference.csv
```

Directory levels describe **what was measured**, never the protein family. The shared filename
prefix is what links a dataset back to its source.

`{Model}` is the paper's own named method or platform — `PRIME`, `FSFP`, `MODIFY`. **Many papers
name none**, and a slot you cannot fill is a step that gets silently skipped, so it has a fallback:
take the first row that matches, top down.

| Token | The paper's variants came from |
|---|---|
| *its own name* | a method or platform **the paper itself contributes** and names — always wins |
| `DMS` | a systematic scan or saturation, not a chosen set |
| `ML` | a learned model ranked them, but the paper gives it no name |
| `MD` | simulation or large-scale computation chose the positions |
| `RD` | structure or mechanism reasoning, without a simulation campaign |
| `DE` | random mutagenesis plus screening |
| `HT` | a designed combinatorial library screened at scale, none of the above |

Software the paper merely *used* is not its method: Rosetta, AlphaFold and FoldX never fill this
slot, however prominently they appear. A paper whose variants Rosetta designed from positions found
by large-scale simulation is `MD`.

First match wins, so the choice is deterministic and two runs on the same paper agree. A mechanism
paper that engineers positions found by large-scale computation is `MD`, whatever else it also did.
It describes **the paper**, not how any individual variant was picked, and it stays the same across
`papers/`, `original_datasets/` and every dataset from that paper.

Dataset CSV, exactly four columns: `mutant`, `sequence`, `readout`, `normalized-score`.
`mutant` is `{WT}{position}{MUT}`, 1-indexed against `sequence`, multi-site joined with `:`, the
unmutated reference is `WT`. `normalized-score` is a z-score of `readout` over the dataset using
the population standard deviation, oriented so higher is always better.

`reference.csv`, 11 columns: `filename`, `protein`, `source_organism`, `seq_len`, `property`,
`readout`, `wt_readout`, `assay_method`, `n_variants`, `doi`, `remark`.

---

## Phase 0 — Acquire the paper and everything it ships

Stage the article itself first, as `papers/{FirstAuthor} {Year}-{Model}-{Journal}.pdf`. That shared
filename prefix is what links every dataset back to its source, and it is the second thing the
duplicate check reads. A paper you only ever read through a URL leaves no trace in the repo.

Look in `papers/` before fetching anything: if the user pointed at a local PDF, or one is already
sitting there under this paper's prefix, that is the copy to use and there is nothing to retrieve.

**It still gets renamed at 0e.** A PDF the user handed over arrives under the publisher's own name —
`s41467-024-53018-6.pdf` — and leaving it that way is the most common way this phase fails: nothing
downstream errors, the file simply never joins the prefix that links it to its datasets. Having
skipped retrieval is not having skipped 0e.

Otherwise try to get it — and **bound the attempt to these two routes, once each**:

| Route | |
|---|---|
| PMC / Europe PMC | `.../PMC<id>/fullTextXML`, or the PDF the OA service advertises |
| the DOI | `curl -sSLI https://doi.org/<DOI>` and follow where it lands |

**A preprint is not a third route.** Do not fall back to bioRxiv, arXiv, or any other preprint of
the same work — not for the article, not for its supplements. Only the version of record counts
here: its supplement numbering routinely differs from the preprint's, so a locator taken from a
preprint sends the user to the wrong file, and a `remark` citing one records a table that the
published paper does not have. If the version of record cannot be retrieved, go to 0d and ask.

| Outcome | Do |
|---|---|
| a real PDF arrives | confirm with `file`, stage it, go to 0a |
| paywall, 403, captcha interstitial, or an HTML page where a PDF was promised | **stop and ask** |

Stop means stop. Do not work down a list of mirrors, do not try another search phrasing, do not
reconstruct the article from whatever fragments are readable. Ask, naming what you tried, so the
user knows exactly which file is missing:

> I can't retrieve the article PDF for `<DOI>` — <paywalled at the publisher / not deposited in PMC
> / captcha interstitial>. The supplementary files <are / are not> reachable.
> Drop the PDF into `papers/` and tell me when it's there, and I'll pick up at 0a. Keep whatever
> filename the publisher gave it — renaming is mine to do.

A paywalled article is **not** grounds to reject the paper. Supplements are frequently open when the
article is not, so this costs one file and a wait, nothing more.

### 0a. Read the paper's own attachment listing — it is authoritative

Every paper enumerates its own attachments, and that list beats any general rule. Find it in two
places and reconcile them:

- the **Data availability** statement — says *whether* the data exists and where in principle.
  "Available in the main text and the Supplementary Information" means the numbers are inside a PDF.
- the **supplementary file listing** — Science prints `Other Supplementary Material for this
  manuscript includes the following:` in the main text; Nature-family articles list theirs on the
  article page and in the *Description of Additional Supplementary Files*.

**Then let the body text pin it down.** A paper almost always says where its own numbers are, at the
point where it discusses them: *"screening results are listed in Supplementary Table 5"*, *"Source
Data Fig. 3b"*, *"the full library is provided as Supplementary Data 3"*. Follow each candidate
readout back to the sentence that cites it, and write down the **exact label** — `Supplementary
Table 5`, not "the SI".

That label is the unit of work from here on. It is what you download, what you extract from, and —
if you cannot download it — the words you hand the user so they click the right link.

The journal table below tells you which **slots to expect**. The listing tells you which slots this
particular paper actually filled. Two papers in the same journal routinely differ: of the two
Nature Communications papers already in this repo, one declares a Source Data file and the other
has no Source Data statement at all, with its screening tables living inside the SI PDF.

### 0b. Journal-keyed slots, in the order to check

| Journal family | Check in this order | Never data |
|---|---|---|
| Nature, Nat Commun, Nat Methods, Nat Biotechnol | **Source Data** (per-figure numbers behind each plot — only when the paper says "Source data are provided as a Source Data file") → **Supplementary Data N** (xlsx/csv, standalone) → **Supplementary Information** (one PDF: Supplementary Figs/Tables/Notes) | Peer Review File, Reporting Summary, Description of Additional Supplementary Files |
| Science, Sci Adv, Sci Transl Med | **Data SN** (standalone xlsx/zip, enumerated by the "Other Supplementary Material" line) → **Supplementary Materials** PDF (Materials and Methods, Figs SN, Tables SN) | — |
| Cell Press | **Data SN / Table SN** (standalone) → supplemental PDF; methods are in STAR Methods in the main text | — |
| PNAS | **Dataset SN** (xlsx) → **SI Appendix** (one PDF holding everything else) | — |
| eLife | per-figure **source data** files → **Supplementary file N** | — |
| ACS (JACS, ACS Catal., Biochemistry) | a single **Supporting Information** PDF; standalone xlsx only sometimes | — |

Rule of thumb behind the ordering: prefer the slot that is *machine-readable and per-variant*.
Source Data and Dataset/Data SN files are the numbers behind a figure; an SI PDF is the same
numbers typeset, and costs you an extraction step and an extraction risk.

Where each family puts the links on its own article page — this is what you quote to the user when
they have to fetch it by hand:

| Journal family | Where on the page |
|---|---|
| Nature family | a **Supplementary information** section low on the article page; Source Data links also hang under the individual figure captions |
| Science family | a **Supplementary Materials** link in the article body; the SM PDF also sits at `science.org/doi/suppl/<DOI>` |
| Cell Press | a **Supplemental information** section at the foot of the article page |
| PNAS | **Supporting Information** on the article page — SI Appendix and each Dataset SN listed separately |
| eLife | an **Additional files** section near the foot, alongside **Data availability** |
| ACS | a **Supporting Information** box linking the SI PDF; also at `pubs.acs.org/doi/suppl/<DOI>` |

**Both tables are accumulated experience, not a specification.** When a paper turns out to file its
data somewhere these rows do not predict, amend the row or add one, in the same session — that is
the whole reason this table beats guessing next time.

### 0c. Retrieve

Route that survives blocked publisher hosts:

```bash
# DOI -> PMCID
curl -sSL "https://pmc.ncbi.nlm.nih.gov/tools/idconv/api/v1/articles/?ids=<DOI>&format=json"
# every supplementary file, as one zip
curl -sSL -o suppl.zip "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC<id>/supplementaryFiles"
unzip -l suppl.zip
```

Known failure modes, each with a distinct signature:

| Symptom | Cause | Do |
|---|---|---|
| `file` says `HTML document` for a `.pdf` | proof-of-work / captcha interstitial | use another mirror |
| 4 KB file for a 4.1 MB supplement | same | check size against the publisher's stated size |
| HTTP 404 on `ftp.ncbi.nlm.nih.gov/pub/pmc/oa_package/` | retired, still advertised by the OA service | use the Europe PMC route |
| curl exit 35, `Connection reset by peer` | host unreachable from here | another mirror, not another flag |
| `idconv` returns no record for the DOI | not deposited in PMC — common for subscription journals | go to the publisher's own supplementary URL |
| HTTP 500 from `.../supplementaryFiles`, body is the EBI error page | the bundler cannot build the zip — often a very large member | fetch each file by name, per the row below |

When the bundle refuses, the **per-file** Europe PMC route still works, and it survives hosts that
block everything else. The filenames come from 0a — they are the `xlink:href` of each
`<supplementary-material>` in `.../PMC<id>/fullTextXML`, which also carries each file's byte size in
a `<?size N?>` processing instruction; that size is the check the publisher's page would otherwise
have given you.

```bash
B="https://europepmc.org/api/fulltextRepo?pprId=PMC<id>&type=FILE"
curl -sSL -o data.csv  "$B&fileName=41467_2024_50712_MOESM4_ESM.csv&mimeType=text/plain"
curl -sSL -o data.zip  "$B&fileName=41467_2024_50712_MOESM6_ESM.zip&mimeType=application/octet-stream"
```

| Symptom | Cause | Do |
|---|---|---|
| `{"error": "Please input a valid fileName and mimeType"}` | `mimeType` omitted | it is required, not optional |
| times out, or 500, on a `.zip` or `.xlsx` | `application/zip` is refused for large members | retry once as `application/octet-stream` |
| `{"error":"PDF link has expired or is invalid"}` | **this endpoint serves no PDFs at all** | the article and SI PDF must come from elsewhere — usually 0d |

The last row is the one that decides the phase: a paper whose data is machine-readable can be fully
retrieved here while its **PDFs** stay out of reach, so 0d gets asked for the PDFs only, and Phase 1
is not blocked meanwhile.

The zip holds what PMC happens to hold. **Diff its contents against the listing from 0a**: if a
file the paper names is missing, do not assume it does not exist — fetch that one from the
publisher.

**That table is the whole budget.** Each symptom names one alternative; take it once. Grinding on a
host that has already refused you twice is not persistence — go to 0d instead.

### 0d. When you cannot download it yourself

Paywalls and captchas are not a failure of the workflow and not grounds to reject anything. Hand the
job over, then wait.

What you hand over must be **navigation, not an apology**. You have already done the work that makes
it easy: 0a gave you the exact label, 0b gives you where that family's site puts it. Say all of it:

> According to the Data availability statement, the per-variant screening data for this paper is in
> **Supplementary Data 3** (xlsx). On a Nature-family article page that is in the **Supplementary
> information** section, low on the page at
> `https://www.nature.com/articles/s41467-024-50698-y#Sec26`.
> I get a captcha interstitial fetching it directly.
>
> Please download it and drop it in `original_datasets/`. **Keep the publisher's filename** — I'll
> rename it to the repo convention when I stage it. Tell me when it's there and I'll continue at 0e.

Rules for this handoff:

| | |
|---|---|
| Name the file the way the **paper** names it | `Supplementary Data 3`, not "the supplement" — that string is what the user will look for on the page |
| Give the section, not just the URL | a bare DOI link makes the user hunt; `0b` already tells you which section to name |
| Say what failed | paywalled / captcha / 404 — otherwise the user cannot tell whether their institution's access would even help |
| Ask for **one named file at a time**, or a short list of them | a request to "get the supplements" hands your job back untriaged |
| **Do not rename anything for the user** | they drop the publisher's file as-is; renaming is yours to do at Phase 2 |

Then stop and wait. When the file lands, run the same checks retrieval would have had to pass —
`file` against the declared type, size against the publisher's stated size — before continuing. A
file arriving by hand gets no exemption from the gate.

### 0e. Rename the article — the supplements wait

Rename the article now and put it in `papers/`. Everything downstream refers to it by name, and it
is what the duplicate check reads.

```
papers/{FirstAuthor} {Year}-{Model}-{Journal}.pdf
```

`{Model}` comes from the table in **Repo shape** — if the paper names no method, take the fallback
row rather than leaving the rename undone. A slot you cannot fill is not a reason to skip the step.

```bash
find papers -type f -printf '%f\n' \
  | grep -vE '^[A-Z][a-z]+ [0-9]{4}-' && echo "UNRENAMED — 0e is not done"
```

**The supplements stay in scratch.** Every one of them, including the ones 0a's labels name. At this
point nobody knows which will be drawn on: 0a read a listing, Phase 1 has not run, and a file's
presence in `original_datasets/` is a claim that a shipped dataset came out of it. Staging the whole
bundle here makes that claim about files that will turn out to serve nothing — and once they are all
renamed alike, there is no longer any signal telling the unused ones apart.

A supplement moves in later, when something in a shipped row actually comes from it — see
**Staging a supplement** below.

### Staging a supplement

Move a file from scratch into `original_datasets/`, renamed, at the moment a shipped row draws on it:

```
original_datasets/{FirstAuthor} {Year}-{Model}-{Journal}-{what it is}.{ext}
```

`{what it is}` describes the **file**, not a work item — one workbook routinely serves four datasets.
Follow the publisher's own label, lowercased: `-data_s1.xlsx`, `-supplementary_information.pdf`,
`-data_table1.pdf`. Renaming is not modifying: the bytes must stay identical, which is the only
thing `original_datasets/` guarantees.

| Drawn on for | When | Example |
|---|---|---|
| the `readout` values | Phase 2 / Phase 4 | the workbook the numbers were read out of |
| the wild-type sequence | Phase 3 | a supplement carrying the construct or an alignment |
| a definition you quote | Phase 2 / Phase 6 | the footnote fixing what the number is relative to |

**The test is that you can name the field and the sentence.** *"`readout` says `% of WT` because this
file's footnote says `RA denotes the relative activity (fold) to that of the WT RpBE`"* is a use.
"I read it for background" is not — otherwise every file qualifies and the directory means nothing.

**Redundant sources are common and only one of them is the source.** The same table is often printed
in an SI PDF and shipped as a workbook; extract from the machine-readable one, which usually also
carries the replicates the PDF dropped. The PDF earns a place only if it supplies something the
workbook does not — and a footnote defining the basis is exactly such a thing.

**Reconcile before the paper is finished.** For every file carrying this paper's prefix, name the
field it fed. Anything you cannot account for was never used: say so, and ask before removing it.

### 0f. Open it, by type

Read every retrieved file and write down what is in it — they are all still in scratch, and this is
what decides which of them ever earns a place in `original_datasets/`. That inventory, not the
abstract, is the input
to Phase 1: a workbook with six sheets states the paper's candidate list more reliably than its
prose does, and it is the only thing that says which candidates have per-variant numbers at all.

**`.xlsx` / `.xls`** — list the sheets before reading any of them; the sheet you want is often not
the first, and several sheets are legends rather than data.

```python
import openpyxl
wb = openpyxl.load_workbook(path, data_only=True)   # cached VALUES, not "=B2/C2" strings
for ws in wb:
    print(ws.title, ws.max_row, ws.max_column, [c.value for c in ws[1]])
```

| Trap | Sign | Do |
|---|---|---|
| `data_only` left off | cells come back as formula strings | reload with `data_only=True`; if values are `None`, the file was written without a cached result — open it once in a spreadsheet app, or reconstruct the formula |
| header spans two rows | row 1 is mostly `None`, units sit in row 2 | join the two rows into one header before anything else |
| merged cells | one value, then `None` across the span | forward-fill the group label |
| numbers stored as text | `'12.3'`, or a stray `'<0.1'` | coerce explicitly and count what fails to coerce — that count is a Phase 4 decision, not a nuisance |
| footnote rows | trailing rows where only column 1 is filled | drop by shape, and assert how many you dropped |

**`.csv` / `.tsv`** — check the encoding (`utf-8-sig` if a BOM leads column 1) and the delimiter,
then treat it as above.

**`.pdf`** — table text extraction interleaves multi-column tables into nonsense; work from word
coordinates, per the appendix at the end of this file.

> **PDF-extracted tables never go into `original_datasets/`.** Write them to scratch, outside the
> repo. That directory holds the publisher's bytes and nothing else; an extracted CSV is a *derived*
> artifact whose correctness is precisely what the appendix's contiguity and orphan asserts exist to
> establish. A file sitting in `original_datasets/` claims to be source. An extraction is not source,
> and if it were kept there, a later audit could no longer tell what the publisher actually shipped.

The extracted CSV is scratch throughout — Phase 4 reads it, Phase 6 never copies it anywhere. What
ships is the dataset CSV under `datasets/`; the PDF it came from is staged as the source when
Phase 2 draws on it.

**`.docx`** — `python-docx`, `doc.tables`; each `table.rows[i].cells[j].text`.
**`.zip`** — unzip into scratch and recurse; a supplement is often a zip of the real files.

**Gate — do not continue until:** every slot named in 0a is accounted for (retrieved, or shown not to
exist), each retrieved file passes `file` as its declared type and matches the publisher's stated
size, the article is renamed into `papers/`, and the inventory is written down.

If the paper deposited nothing per-variant anywhere — every number is in a figure — stop here and
reject the paper as a whole. There is no work list to build.

## Phase 1 — Enumerate work items

One paper usually yields several datasets. Work from the Phase 0 inventory and the paper together —
the inventory says what has per-variant numbers, the paper says what they mean.

**Enumerate the paper's own case studies, and nothing else.** A dataset the paper merely *evaluates
on* — ProteinGym, a published DMS landscape, someone else's fitness data reused as a benchmark — is
not a candidate here at all. It belongs to the publication that measured it, and curating it under
this paper's name would attribute an experiment to authors who did not run it. Method papers are
full of such data and it is often the largest thing in the supplement; size is not relevance.

Mention what you skipped in one line under the table, never as a row: *also present, out of scope:
evaluated on ProteinGym and two published DMS landscapes.* That is enough for a reader to see it was
noticed, without offering it as something to pick.

### What one work item is

**One wild-type sequence × one measurement.** Both halves are load-bearing: each row's `sequence` is
that WT with substitutions applied, `mutant` is written against that WT, and `normalized-score` is a
z-score *within that one series*. A candidate that cannot supply both cannot be written in the
four-column format at all.

**And at least 20 variants carry it.** Below that a z-score has no distribution to speak of and a
rank correlation has no power, so the file cannot do the one job a FitnessBench dataset exists for.
Three enzyme-kinetics points across WT and two variants are a real measurement and still not a
dataset. Count *distinct genotypes carrying this readout*, excluding the WT row — merging two tables
of the same measurement is exactly how a candidate legitimately clears the bar.

A **measurement** is itself two things, and they split independently:

- **what was done** — which reaction, which substrate, which condition, treated or untreated
- **what was counted** — which quantity, in which unit

Two candidates are the same work item only when *both* halves match. So one protein routinely yields
several work items, and drawing the grid is how you see how many. Ding 2024 engineered a single
Rma cyt c library, screened in one set of wells, and reported two quantities across two reactions:

| | product yield (%) | enantiomeric ratio |
|---|---|---|
| **C–B bond formation** | work item → `Activity/CatalyticActivity/` | work item → a selectivity, its own property |
| **C–Si bond formation** | work item → `Activity/CatalyticActivity/` | work item → a selectivity, its own property |

Four work items, one protein, one library. Nothing about that is over-splitting: every cell is a
different number answering a different question, each needs its own orientation, and each gets its
own z-score — pooling any two of them would normalize incomparable quantities against each other.

**What does not justify a split** — the measurement is the same, so these are more rows, not more
work items:

| Looks like | Actually |
|---|---|
| a second round or generation of engineering on the same protein | one work item; the later round is more rows, and its multi-site variants are the only epistasis signal in the file |
| the same measurement printed in two tables, or across two plates | one work item; join them, and reconcile any overlap per Phase 4 |
| a variant series plus a benchmark protein it is compared against | one work item; the benchmark is a single point, not a series |

**What is not a work item at all** — it fails the *one WT sequence* half, so no amount of splitting
rescues it:

**A panel of homologs.** A paper may screen twelve natural orthologs — `AaBE`, `BfBE`, … `RpBE` —
and then engineer one of them. Twelve names in the results is twelve *proteins*, but one measurement
each on twelve unrelated sequences: no shared WT, no `{WT}{position}{MUT}` to write, and a z-score
across unrelated proteins would mean nothing. Mark it `no` with that reason, and take the variant
series on the one protein they went on to engineer.

Before presenting anything, say the shape out loud: *N distinct wild-type sequences that carry a
variant series, and for each, the reaction × quantity grid.* Two numbers that should agree — the
work-item count and the number of filled cells across those grids — and if they do not, you have
either split by table or split by protein, and neither is the axis.

**Enumerate everything in scope; decide nothing.** Which of them become datasets is the user's call,
not yours — you are here to lay out the options accurately, with the facts attached that the choice
depends on. Three kinds of candidate are `no` on their face:

- **not an experimental measurement.** Predicted ΔΔG, docking scores, simulation output — anything a
  computation produced rather than an assay. FitnessBench holds measurements; a prediction column is
  not a weak dataset, it is a different kind of thing. Mark it `no` whatever its row count.
- **no per-variant numbers in any retrieved file.** This one is a fact about the data, not an opinion:
  digitizing a scatter plot is not curation, and there is nothing to select. Mark it `no`, give the
  reason, and offer it as information rather than as an option.
- **fewer than 20 variants.** Also a fact, once counted. Mark it `no — N variants`.

**Do not confuse "too small" with "needs a new directory".** They are unrelated, and only the first
is ever a reason to mark `no`. A two-variant candidate is out because it is two variants; that it
would also have been the first of its property is beside the point, and naming the new directory as
though it were the objection puts a cost on precisely the thing the hierarchy exists to do.

**Gate — do not continue until:** each item has a name, an intended category/property directory, the
file and sheet-or-table its numbers live in, and a stated reason it is (or is not) the authors' own
experimental data.

### Present the table, then let the user pick

**Present the work list and stop.** This is the last point at which redirecting costs nothing —
everything after it is per-item work that a wrong list wastes in full. One table, built so that a
reader with the paper open can check every row without having to ask you anything:

| # | Protein | Property → directory | Readout | Where it lives | Rows | Curatable |
|---|---|---|---|---|---|---|
| 1 | Rma cyt c | Catalytic activity → `Activity/CatalyticActivity/` | product yield %, C–B | `Ding 2024-…-supplementary_information.pdf` › Supplementary Table 3 | 160 | yes |
| 2 | Rma cyt c | Catalytic activity → `Activity/CatalyticActivity/` | product yield %, C–Si | same file › Supplementary Table 4 | 160 | yes |
| 3 | Rma cyt c | Selectivity → `Activity/Selectivity/` (new) | enantiomeric ratio | same tables › `e.r.` column | 160 | yes |
| 4 | NNK control library | Catalytic activity | product yield % | same file › Supplementary Table 6 | 88 | **no** — wells only, no genotype |

`Curatable` is a **fact about the data**, and it is the only column you are entitled to fill in. It
answers "could this become a dataset at all", never "should it". There are exactly four ways to say
`no`, and each is checkable rather than felt:

| `no` because | |
|---|---|
| not an experimental measurement | a predicted or simulated column |
| no per-variant numbers anywhere | nothing to extract |
| fewer than 20 variants | `no — N variants` |
| no single wild-type sequence | a homolog panel |

Everything else is `yes`, however marginal you privately think it is. A readout you would not have
picked is still the user's to pick, and a property with no directory yet is not a caveat — the
`Property → directory` cell simply names the one to create.

**`Where it lives` is the column the user actually checks**, and a vague one wastes the whole
exercise:

- write it as **`file › locator`**, always both, in that order. The file is the one on disk; the
  locator is the string *inside* it. Keeping them separated matters more than it looks: a Nature
  Source Data workbook names its sheets after the SI's figures, so
  `…-source_data.xlsx › sheet "Supplementary Table 10"` and the SI PDF's own *Supplementary Table 10*
  are two different files printing the same label — and only one of them has the replicates
- give the locator *in the publisher's own words*, the string actually printed there:
  `sheet "Tm data"`, `Data S1, sheet 2`, `Supplementary Table 3`. Never "the SI", never "the third
  table" — the user is going to search for that string
- for a workbook, name the sheet **and** the columns
- `Rows` is what the source holds **before** any merging or dropping. It is what the user compares
  against a library size the paper states in prose, and what Phase 7 compares against `n_variants` —
  where the difference must equal exactly what your `remark` claims you dropped or merged

Then **ask with `AskUserQuestion`, `multiSelect: true`** — the user clicks the items to work. Do not
substitute a prose question; the point is that picking is one click per item, against a table they
have just read.

| Curatable candidates | How to ask |
|---|---|
| **0** | do not ask anything. Present the table, say why each row is `no`, and stop — a question with no workable answer is not a question |
| **1** | `AskUserQuestion` takes 2–4 options, so one candidate cannot be one option each. Ask **work it / stop** |
| **2–4** | one option per candidate, labelled `#N {protein} — {readout}`, with the source location in `description` |
| **more than 4** | the option cap is 4, so the table above is the enumeration and the options become groupings — by property, by protein, plus "all of them". The user can always type an arbitrary set through **Other** |

Rows marked `no` are **not options** — selecting one cannot produce anything. They stay in the table
so the user can see they were found and why they are unusable. A candidate omitted from the table
entirely looks like one you never noticed, and an absence is the one thing a reader cannot check.

Work only what was selected, in the order selected. If the user picks a row you marked `no`, do not
silently skip it: say which gate blocks it and what would have to be true to pass — a table
elsewhere, a genotype list, a deposited file — and let them answer that.

## Phase 2 — Read the methods

Phase 1 fixed where this item lives, an intended property directory, and a name for the readout — it
read those off table headers and captions. **Do not ask any of them again.** Extract per the appendix
if the source is a PDF, then open the Methods and answer the three questions a table header cannot:

| Question | Determines | If you cannot answer |
|---|---|---|
| Relative to what? | the unit, and whether merged sources need rebasing | REJECT — a ratio with an unknown denominator is not a measurement |
| Which direction is better? | whether to invert in Phase 5 | REJECT — an unoriented score is worse than none |
| How was it measured? | `assay_method` | proceed, but say so |

The Methods are also the first thing entitled to **overturn** Phase 1. What Phase 1 wrote down was an
intent taken from a header; this is where it gets checked against how the number was actually
produced:

| What the Methods show | Do |
|---|---|
| they confirm the property and readout | adopt Phase 1's directory; create it if new — see below |
| the measurement is not what the header implied | correct it here, say what changed and why, and re-check the property |
| there is no table behind it at all | a Phase 1 miss — reject, and say which row was wrong |
| the sources were run under different conditions | they are separate work items — back to Phase 1, and re-check each against the 20-variant floor |

### One item, several sources — settle the scale here

A work item Phase 1 assembled from more than one table arrives in more than one scale. Decide it
now, in writing; Phase 5 only executes what this phase decides.

| Symptom | Do |
|---|---|
| one source in `fold`, another in `%` | pick one unit, state the conversion |
| each source normalized against its own control | rebase every block on its own control, so the control reads exactly 1 — or 100 — in all of them |
| a caption claims a basis the numbers contradict — *"the WT is regarded to possess 100%"* while the WT row reads `100.73` | the caption states the intent, the number states the measurement. Rebase to the caption, and record both figures |

Then ask what actually joins the blocks. **If the only value they share is the control, the merge
rests entirely on that control meaning the same thing in each** — there is no overlapping variant
available to check it against. That is often true and still worth doing, but it is an assumption
rather than a verification, so it belongs in `remark`.

Two traps:

- An abstract may bundle unrelated goals into one sentence. Two proteins, two properties, two
  categories — split them into separate work items and go back to Phase 1.
- **The protein need not natively be what the assay implies.** A cytochrome c is an electron
  carrier, not an enzyme; its engineered carbene-transfer activity still belongs under
  `Activity/CatalyticActivity/`, because the hierarchy describes the measurement. Put the native
  function in `protein` so the category is not read as a claim about it.

**A property with no existing directory is a new directory, not a rejection.** The hierarchy
describes what was measured, and papers keep measuring new things, so it is meant to grow. Creating
a level is cheap and reversible:

| What is new | Do |
|---|---|
| the property, under an existing category | `mkdir datasets/{Category}/{NewProperty}/` — the category's `reference.csv` already exists and needs nothing |
| the category itself | `mkdir datasets/{NewCategory}/`, then write `reference.csv` holding the 11-column header and nothing else; `.gitattributes` already matches `datasets/*/reference.csv` |

Name it the way the existing levels are named: CamelCase, a noun phrase for **what was measured** —
`ThermalStability`, `AlkalineStability`, `CatalyticActivity`, `BindingAffinity`. Never a protein
family, never the instrument.

The rejection is for a property you cannot *state*, not one you have not seen before. "I cannot say
what this number means" has no home; "this number means something not measured here before" gets a
directory and a row.

**Gate — do not continue until:** the basis, the direction and the assay are fixed in writing, and
Phase 1's property and readout have each been either confirmed against the Methods or corrected.

## Phase 3 — Establish the WT sequence and its numbering

The whole dataset rests on this. Everything downstream silently inherits an error here.

### 3a. Get a candidate sequence — and the reference, always

Preference order for the sequence you will *use*: one the source states outright > a fetched
accession > a reconstruction. A stated sequence is the construct they assayed.

**Fetch the reference accession anyway**, even when the source states its own sequence, and even
when you are certain. It is the only external check Phase 3 has, and the differences are the
interesting part: an engineered parent, a purification tag, a different isoform, a numbering
convention stated against something else. Report the comparison at 3h whatever it shows — an exact
match is worth as much as a mismatch, and neither is worth anything if nobody looked.

If no accession exists, say that at 3h. "There is none" and "I did not look" are indistinguishable
downstream, so only one of them may be left unsaid.

### 3b. Run the label check — always

Every mutation names the wild-type residue it expects, so this is hundreds of independent checks:

```python
bad = [m for m in all_mutations if seq[int(m[1:-1]) - 1] != m[0]]
```

**That line is the whole of 3b.** It diagnoses nothing and repairs nothing — it only reports. What
follows are five repairs and a gate, and the *shape* of `bad` chooses between them. So look at the
shape before reaching for anything:

```python
hits = sorted((int(m[1:-1]), seq[int(m[1:-1]) - 1] == m[0]) for m in all_mutations)
print("".join("." if ok else "X" for _, ok in hits))     # positions in order
```

| Shape | Reading | Repair | Re-run 3b after |
|---|---|---|---|
| `bad` empty | — | none | — go to **3h** |
| every position wrong, one constant `off` fixes all | an initiator Met, a signal peptide, a leading tag | **3c** | yes |
| one or two `X` in a sea of `.` | a typo, in the paper or in the table | **3d** | yes, if you changed anything |
| clean `.` up to some position, then `X` from there on | an insertion or deletion between the construct and the reference | **3e** | yes, if 3e or 3f yields a sequence |
| `X` scattered with no structure at all | wrong protein, or a construct unrelated to the reference | **3f** if the scan is saturated, else REJECT | no — see 3f |
| too few positions for any shape to be distinguishable | — | **3g** | yes |

Keeping the check separate from the repairs is what makes re-running it mean something. Four of the
five repairs end in a fresh 3b; **3f cannot**, and that is the most important thing to know about it.

**A sequence the source states outright, passing 3b, goes straight to 3h.** No repair is owed: the
construct is quoted and the check confirms it. The repairs exist for cases where something has to
change — running one because the phase has letters in it is not rigour.

### 3c. A constant offset — the whole sequence is shifted

The cheapest and commonest repair, so try it first. Scan for the offset **before discarding
anything**:

```python
for off in range(-40, 41):
    ok = sum(seq[int(m[1:-1]) - 1 + off] == m[0] for m in all_mutations)
```

A clean hit means the sequence is right and only the numbering was stated against a different
reference. Renumber, re-run 3b, and record the convention you adopted — the offset itself belongs in
`remark` whenever it was not the source's own numbering.

### 3d. One or two mismatches — go back to the paper's own text

A handful of `X` against a clean background is almost never a wrong sequence; it is a typo. Find
which side made it, by reading the paper's prose for that specific variant and comparing it against
the supplementary table.

The repo already holds a worked instance: for Jiang 2024, position 659 carries `Y` in the source
data, which lists the variant as `Y659E`, while **the paper's own text calls it `H659E`**. The two
disagree and only one can be right.

| Which side is self-consistent | Do |
|---|---|
| the source data agrees with the sequence, prose does not | follow the data, record the discrepancy in `remark` |
| the prose agrees with the sequence, the table does not | correct the table entry, record it |
| neither agrees | this is not a typo — go back to 3b and read the shape again |

Never silently drop the variant. A typo you fixed and a variant you deleted look identical in the
finished CSV, and only one of them is honest.

### 3e. Drift from one position onward — an insertion or deletion

`.........XXXXXXXXX` is a signature, not noise. Everything before the breakpoint verifies, so the
sequence is the right protein; everything after it fails, so the construct and the reference differ
in *length* somewhere near that breakpoint. Locate it, and measure it:

```python
k = next(p for p, ok in hits if not ok)                  # first failing position
for off in range(-30, 31):                               # offset applied only from k onward
    ok = sum(seq[p - 1 + off] == m[0] for p, m in tail_mutations)
```

| Outcome | Reading | Do |
|---|---|---|
| one `off` fixes everything from `k` onward | a clean indel of `off` residues before `k` | you know its size and roughly where, but **not which residues** |
| no single `off` works | more than one indel, or not an indel at all | back to 3b — read the shape again |

An indel is not repairable by renumbering. A constant offset leaves the sequence intact, so 3c can
simply renumber; here the assayed construct genuinely has residues the reference does not, or lacks
residues it has, and `sequence` must be the construct. You now need the true residues from
somewhere:

| Where they can come from | Go to |
|---|---|
| the scan itself, if it is saturated enough to state them | **3f** |
| a construct the source states outright, or another accession that matches without an indel | back to **3a** with that as the candidate |
| nowhere | REJECT — do not paper over an indel by trimming the variants that fall past it |

### 3f. Derive the sequence from a saturated scan

**This repair always stops at 3h for approval — it never proceeds on its own.** It is the one path
that destroys its own check: the sequence is *derived* to satisfy the label check, so `bad` is empty
by construction and 3b can no longer catch anything. The asserts below are strong, but every one of
them is internal.

When every possible substitution is ranked, position `i` appears 19 times with the same wild-type
residue, so the sequence falls out:

```python
pos_aa = {}
for m in ranking_column:
    g = re.fullmatch(r'([A-Z])(\d+)([A-Z])', m)
    pos_aa.setdefault(int(g.group(2)), set()).add(g.group(1))
assert all(len(v) == 1 for v in pos_aa.values())        # WT residue consistent
L = max(pos_aa)
assert set(pos_aa) == set(range(1, L + 1))              # no gaps
assert len(ranking_column) == L * 19 == len(set(ranking_column))
WT = ''.join(next(iter(pos_aa[p])) for p in range(1, L + 1))
```

**Partial coverage is the normal case, not a failure.** Real saturation data drops variants, and
scans often cover one domain rather than a whole chain, so the last two asserts fail routinely. That
is not a reason to fall through to REJECT — it is a reason to derive less:

| Coverage | Do |
|---|---|
| every position, all 19, no duplicates | all four asserts hold — derive the whole sequence |
| most positions, ≥2 agreeing rows each, gaps or an offset window | derive only the positions the scan covers; take the rest from the reference, and record in `remark` exactly which residues came from which |
| fewer than 2 rows at most positions | no redundancy, so nothing is being verified — REJECT |

At 3h, say plainly that this sequence came out of the data it is about to be used to curate, and
align it against whatever accession exists anyway, so the difference is on the record even when
nothing matches exactly.

### 3g. Too few positions — the numbering convention is the unknown

A 6-site combinatorial library constrains 6 residues; no shape above is distinguishable at that
size. Here a deposited structure of the same protein is the authority:

```bash
curl -sSL -o entry.ent "https://www.ebi.ac.uk/pdbe/entry-files/download/pdb<id>.ent"
```

`DBREF` maps PDB residue numbers to UniProt numbers; `SEQADV` labels every expression tag and
engineered mutation explicitly. Enumerate the candidate conventions and let the data choose:

```python
for name, s in [("mature", mature), ("uniprot", full), ("pdb", full[OFFSET:])]:
    print(name, "".join(s[p-1] for p in SITES))     # exactly one should match the paper
```

| Outcome | Branch |
|---|---|
| Exactly one convention matches | adopt it, re-run 3b, then corroborate below |
| More than one matches | the sites are not discriminative — find more constraints or REJECT |
| None matches | wrong protein or wrong structure — REJECT |

Corroborate with everything else the paper asserts in prose: a named prior variant
(`V75R M100D M103T`), a cofactor-ligating residue, an active-site motif, a structure's own
`SEQADV` mutations. **Two independent corroborations minimum** — one is a coincidence.

**Padding is legitimate; pretending it is sourced is not.** If the structure's construct is
numbered from 2 (tag at 2–7, mature chain from 8), `sequence` must still be 1-indexed, so position
1 gets a placeholder. Record in `remark` exactly which residues are verbatim and which are padding.

**3f and 3g solve different unknowns**, and what sends you to 3g is *few distinct positions*, not
sparse coverage: 50 scattered sites across a 500-residue protein is sparse and still gives 3c all
the signal it needs.

| | 3f | 3g |
|---|---|---|
| unknown | **the sequence** — which residue sits at each position | **the numbering** — you have the residues, not the convention they were counted in |
| needs | thousands of rows: every position × every substitution | as few as six mutated positions, plus a deposited structure |
| evidence | the data's own redundancy — 19 rows per position agree | an external authority — `DBREF`, `SEQADV` |
| check left afterwards | **none**; `bad` is empty by construction | weak but real — six sites match by chance at 1/20⁶ — hence ≥2 corroborations |

Neither available — few positions, and no structure or accession to appeal to — is a REJECT.

### 3h. Re-check, then show, then stop

Phase 3 is where a silent error does the most damage: everything downstream inherits it, and every
downstream assert still passes. So it ends the way Phase 1 does — you present, the user decides.
Three things happen here, in order.

#### 1. Re-run 3b

Not the repair's own reasoning about why it worked — the check itself, against the exact sequence and
numbering you are about to write.

| Re-check | Do |
|---|---|
| `bad` empty | go to step 2 |
| `bad` still non-empty | back to 3b's shape table, repair again — **this counts as one loop** |
| the sequence came from 3f | `bad` is empty *by construction*. Say that, rather than reporting it as a pass |

#### 2. Count the loops — three is the limit

One loop is `shape → repair → re-check`. On the **third** failed re-check, stop and REJECT the work
item. Report, for each pass: the shape `bad` took, the repair it selected, and why the repair did not
hold.

Do not attempt a fourth. A sequence that has resisted three shape-directed repairs is not going to
yield to another guess, and by then the failures are more informative than any sequence you would
end up with. Rejecting here is a result; a fourth attempt is how a wrong sequence gets adopted
because it finally scored well.

#### 3. Present, then ask

**A sequence the source states outright, passing 3b, arrives here directly** — no repair is owed, and
the provenance line simply says where it was quoted from.

Report exactly this, then ask:

```
Sequence — <protein>, <L> aa

Provenance    quoted from <file> › <locator>  |  accession <id>  |  derived via 3f
              |  padded at positions <n>
Against <id>  exact match  |  differs at <positions>  |  indel of <k> residues before <p>
              -> category: numbering only | expression tag | engineered parent | isoform
                 or strain | indel | unrelated
Repairs       3c: offset +12; 3d: 1 typo, followed the source data
Label check   <N> mutations checked, bad = 0, positions <lo>-<hi> across <k> distinct sites
Not checked   <L-k> residues carry no mutation; they rest on provenance alone

<first 30 residues>...<last 30 residues>
```

Naming the **category** of the difference is the part that carries information. "Differs from
UniProt at 3 positions" is a fact the user still has to interpret; "an engineered parent carrying
`V75R M100D M103T`, so the reference is the wild type and this is not" is a finding. If you cannot
categorise a difference, say that too — an uncategorised difference is exactly the kind that turns
out to matter.

`Not checked` is the honest row. A label check verifies the positions the variants happen to name
and nothing else: 87 mutations across 50 sites verify 50 residues of a 500-residue protein, and the
other 450 rest entirely on provenance. That is precisely why 3a fetches the reference even when the
source states its own sequence.

Then **ask with `AskUserQuestion`** — accept this sequence, or reject the work item — and wait.

| The user says | Do |
|---|---|
| accept | Phase 4 |
| the disagreement with the reference matters | back to 3a with the reference as the candidate, re-run 3b, present again — this counts as a loop |
| reject | REJECT the work item, and record the reason per Phase 6 |

## Phase 4 — Assemble the variants

**Combinatorial libraries are named by an N-letter code**, one letter per mutated site. Convert
against WT; a site whose letter equals wild type contributes nothing — never emit `T101T`:

```python
def to_mutant(code):
    return ":".join(f"{WT[p-1]}{p}{a}" for p, a in zip(SITES, code) if WT[p-1] != a) or "WT"
```

**Duplicates.** `mutant` must be unique, so repeats must collapse. Diagnose before merging:

```python
for m, v in vals.items():
    assert max(v) - min(v) < tol, f'{m}: values disagree {v}'
```

| Spread | Meaning | Do |
|---|---|---|
| Exactly 0 | the same measurement reprinted | average, no note needed |
| At the rounding of the reported values | rounding | average, note briefly |
| Large, rows from **different wells or plates** | independent replicates of one genotype | average; the spread is data, not error — swap the tolerance for a check with teeth (group sizes match what the source says) and record the **worst spread** in `remark` |
| Large, rows from the same well | contradiction in the source | investigate; do not average silently |
| The same variant in **two sources Phase 1 merged** | two batches, each rebased in Phase 2 | compare *after* rebasing, and report the agreement — see below |

**Never widen `tol`, and never simply delete the assert.** They are the same move: both make the
check agree with the data instead of the other way round. When a tolerance is genuinely the wrong
instrument — real replicates have real spread — replace it with a check that can still fail, and put
the spread you actually saw in `remark`.

**Cross-source duplicates are the only empirical check a merge ever gets.** When Phase 1 assembled
one work item out of several tables, the variants appearing in more than one of them are the sole
evidence that the tables are commensurable; everything else rests on Phase 2's rebasing being right.
Report the agreement as a number — *ten variants overlap, agreeing to within 1%* is worth more than
any argument for the merge. And when the blocks share **no** variant at all, say that instead: the
merge then rests entirely on the control, which is an assumption, and `remark` is where assumptions
go.

**The wild-type row.** `mutant` is `WT`, it carries no substitution, and it is not a variant: it does
not count towards `n_variants` and the 20-variant floor does not see it. It is subject to everything
else — if the source measured the wild type more than once it collapses by the rules above, and if
Phase 2 rebased the sources it must come out at *exactly* the basis value in every one of them. A
wild type reading 100.0 in one block and 99.7 in another after rebasing means the rebasing did not do
what you thought it did; fix that before going on.

If the wild type was never assayed there is simply no row. **Do not synthesise one** at 1.0 or 100%
because the scale implies it — `wt_readout` stays empty and Phase 5 anchors on the dataset mean.

**Other cleanups.** Non-numeric cells (`"no expression"`) are not measurements — drop the row and
record it. Multi-site rounds join with `:` and stay; they are the only epistasis signal in the file.

Apply every mutation with the checks that matter:

```python
for m in mutations:
    wt, p, mt = m[0], int(m[1:-1]), m[-1]
    assert 1 <= p <= L
    assert seq[p - 1] == wt          # numbering offsets
    assert wt != mt                  # synonymous entries
    seq[p - 1] = mt

assert sum(a != b for a, b in zip(WT, ''.join(seq))) == len(mutations)
```

That last line is computed from the *output*, so it catches a position mutated twice or a
substitution that silently never landed.

**Gate — do not continue until:** every assert above passes as written, and you can state three
counts — rows read, rows dropped, groups merged — whose arithmetic lands exactly on the number of
variants you are about to write. Phase 4 has no user checkpoint because it needs none: unlike
Phases 1 and 3, nothing here rests on judgement that the asserts cannot see. That is only true while
the asserts run as written.

## Phase 5 — Construct, orient, normalize

### Construct — what is the readout?

**It need not be a column in the source.** Ask what the experiment actually compares. Where Phase 2
settled a unit or a rebasing, execute that here rather than reopening it.

| | Readout |
|---|---|
| a column already answers the question | use it |
| a treated measurement confounds the property with the starting level | use the ratio; the untreated column becomes a **second work item**, not a discard |

A derived readout will not reproduce the paper's own statistics. Record the derivation in `remark`
**in one sentence** — what you divided by what, and nothing more — so nobody assumes it should.

### Orient — is a higher raw value better?

One question, and if the answer is no, one choice:

| Higher is better? | |
|---|---|
| yes | use it as it stands |
| no | convert — **negate** by default; take the **reciprocal** only when the quantity is strictly positive *and* the reciprocal is itself the meaningful thing, as `1/EC50` is a potency |

State the conversion in the `readout` field — `-ddG (kcal/mol)`, `1/EC50 (nM^-1)` — never silently.

Negation is safe for anything. The reciprocal is not, which is why it is the exception rather than
the rule: it is undefined at zero and reverses order across it, so a `ddG` of `-0.1` and one of `+0.1`
would become `-10` and `+10` and the worse variant would outrank the better. It is also monotone but
not linear — ranks survive, the spacing the z-scores are computed from does not. And if a value you
are about to invert is zero, the assay usually could not measure that variant: drop the row and
record it, or use the source's own bound (`>2048`) and note in `remark` that those rows are censored.

### Normalize

**Fix the written precision before computing the score**, or averaged values get rounded on write
and the Phase 7 z-score assert fails:

```python
x = [round(v, 6) for v in x]              # and write THESE values, not the originals
mean, sd = statistics.fmean(x), statistics.pstdev(x)
assert sd > 0, "every readout identical — nothing to rank"
score = [(v - mean) / sd for v in x]
```

Write the rounded values, not the ones you rounded from. Phase 7 recomputes the z-score out of the
CSV, so the number on disk has to be the number the score was computed from.

`sd == 0` is not a normalization edge case to be handled quietly — it means every variant measured
the same, so the file can rank nothing and cannot do the job a FitnessBench dataset exists for.
REJECT it, the same way the 20-variant floor does.

The zero point is the dataset mean, not the wild type. If the wild type was never assayed, leave
`wt_readout` empty and say so — anchoring on the mean is what lets such a dataset normalize like
the rest.

## Phase 6 — Write the files

CSV first, WT row first when the source measured it. Then the `reference.csv` row, with `seq_len`,
`wt_readout` and `n_variants` **derived from the finished CSV**, never typed. `filename` is the
primary key: if a row for it already exists — a re-run, a correction — replace that row rather than
appending a second one.

### `remark` — five clauses, in this order, one sentence each

`remark` records **only what this version does differently from the source**. It is also the only
memory this repo has: the duplicate check at the top of this file reads nothing else, so a decision
that is not written here does not survive the session it was made in. That makes it collect
everything, which is why it needs a shape.

**A `remark` is a diff, not a description.** Every clause has a normal case, and the normal case is
written **nowhere**. A reader who knows this format already assumes it; repeating it buries the one
sentence that actually matters. The model to aim at is the `Creatinase` row already in this repo,
whose `remark` is empty — that dataset had nothing unusual about it, so it says nothing.

Write clauses joined by `. `, always in this order, and **only when the right-hand column applies**:

| # | Clause | Silent when — the normal case | Write only for |
|---|---|---|---|
| 1 | **sequence** | quoted from the paper, or an accession that `bad` = 0 verified first try | padding, a derivation via 3f, an adopted offset or convention, any repair 3c–3g, a construct that differs from the reference |
| 2 | **rows** | every source row became a variant, WT included | rows dropped and why, duplicate groups collapsed and their worst spread, no WT row |
| 3 | **readout** | a source column used as it stands | a derived value, a rebasing, rows censored at a bound, several sources merged — with their agreement, or the fact that they share only the control |
| 4 | **conflicts** | the paper agrees with its own supplement | it does not, plus which side this file followed |
| 5 | **scope** | nothing was rejected | every rejected candidate, one clause each |

So "fetched `P00573`, all 70 substitutions verify" is **not** a remark — that is the workflow working.
"the pET28a N-terminal His-tag of the assayed construct is not included, as its sequence is not
given" is, because the file departs from what was assayed. Name the accession when you name one at
all, since nothing else in the row records it.

**Clause 5 is the exception to terseness**: it is never optional when something was rejected, and it
is what the next run depends on. `the NNK control library is excluded, its members having no
genotype` is enough — but leaving it out means the next run re-offers a candidate you already ruled
out, with no reason attached.

**One sentence per clause.** A clause that wants a paragraph is not a remark — it is either a fact
that belongs in `assay_method` or `readout`, or a problem serious enough that the item should not
ship. Five sentences is a *full* `remark` and most should be shorter; ten means something is in the
wrong field.

**What does not belong in `remark` at all.** The field is for what *this curation* did, so anything
that is a property of the experiment goes elsewhere or nowhere:

| Fact | Field |
|---|---|
| the source's own normalization scheme | `assay_method` |
| a consequence of it that would otherwise look like an extraction bug (yields > 100%) | `readout` |
| a property inherited unchanged from the source | nowhere |
| that four variants are dead | nowhere — that is the experiment's result, not a curation decision |

The scheme has one gap, and it is not fixable from here: if **no** item from the paper shipped,
there is no row to write into and nothing persists. Say that plainly in the final report.


## Phase 7 — Verify

Everything here is read back **off the disk**. That is the whole point of the phase: Phase 4 and
Phase 5 checked what was in memory, and this checks what actually got written.

**The file itself:**

```python
assert list(rows[0]) == ['mutant', 'sequence', 'readout', 'normalized-score']
x  = [float(r['readout']) for r in rows]
z  = [float(r['normalized-score']) for r in rows]
m, sd = statistics.fmean(x), statistics.pstdev(x)
assert sd > 0
assert all(abs((xi - m) / sd - zi) < 1e-6 for xi, zi in zip(x, z))
assert len({r['mutant'] for r in rows}) == len(rows)
assert len({len(r['sequence']) for r in rows}) == 1
```

**`mutant` against `sequence` — the one that earns its keep.** Equal lengths prove nothing: a
mangled `sequence`, two rows written out of step, a substitution that never landed all leave the
length untouched. Reverting each row's own mutations must land every row on the same wild type:

```python
def revert(r):
    q = list(r['sequence'])
    if r['mutant'] != 'WT':
        for mut in r['mutant'].split(':'):
            wt, pos, mt = mut[0], int(mut[1:-1]), mut[-1]
            assert q[pos - 1] == mt          # the substitution is actually there
            q[pos - 1] = wt
    return ''.join(q)

assert len({revert(r) for r in rows}) == 1   # every row reverts to one WT
WT = revert(rows[0])
for r in rows:
    n = 0 if r['mutant'] == 'WT' else len(r['mutant'].split(':'))
    assert sum(a != b for a, b in zip(WT, r['sequence'])) == n
```

This works with or without a WT row, because the wild type is recovered from the variants
themselves rather than assumed.

**The `reference.csv` row against the CSV** — Phase 6 said these were derived, so prove it:

```python
var = [r for r in rows if r['mutant'] != 'WT']
assert int(ref['seq_len'])    == len(WT)
assert int(ref['n_variants']) == len(var)
assert len(var) >= 20
wt_rows = [r for r in rows if r['mutant'] == 'WT']
if wt_rows:
    assert float(ref['wt_readout']) == float(wt_rows[0]['readout'])
else:
    assert ref['wt_readout'].strip() == '' or ref['remark'].strip()
assert os.path.exists(os.path.join(category_dir, ref['filename']))
assert [r['filename'] for r in all_reference_rows].count(ref['filename']) == 1
```

**`wt_readout` without a WT row is legitimate, and only in one way.** Normally no WT row means an
empty `wt_readout` and Phase 5 anchoring on the dataset mean. But when the readout is *defined*
against the parent — a fold-change, a percent-of-WT — the parent's value is fixed by that definition
rather than measured, and recording it is what lets a reader ask "better than wild type?" at all.
`Jiang 2024-PRIME-TgoD4K` is the case in this repo: no WT row, `wt_readout` `1.0`, and a `remark`
saying `the readout is already normalized to the Tgo-D4K parent, which is 1.0 by definition`. A value
arrived at this way must say so in `remark`; one that appears with no row and no explanation is a
typed number, which Phase 6 forbids.

Add the domain checks the data itself offers: if the library excluded an amino acid at a site,
assert no variant carries it; if only certain sites were mutated, assert no mutation lands
elsewhere.

**Then re-derive a number the paper states in prose** — a count of improved variants, a
fold-change, a correlation coefficient. Nothing else catches a table extracted with rows missing.

The arm you *cannot* ship is often what makes this possible: a control library with no genotypes is
unusable as a dataset but perfectly good for reproducing "2.2-fold higher averaged yield". Keep it
in scratch, use it, drop it.

| Result | Branch |
|---|---|
| Reproduces | SHIP |
| Off by a margin your own `remark` already explains (averaging replicates lifts a correlation) | SHIP, stating both numbers |
| Off, unexplained | return to the phase that produced the input, usually the extraction in Phase 2 or the merge in Phase 4 |
| Cannot be made to reproduce | do not reverse-engineer a formula that hits the published figure — ship only with the discrepancy stated, or REJECT |

## Reject conditions, consolidated

Reject the work item, record it in the `remark` of a dataset shipped from the same paper
(Phase 6), report it, and move to the next:

- the data is only in a figure, or is not public (Phase 0–1)
- the property, units, or direction cannot be established (Phase 2)
- the sequence cannot be verified, or the numbering convention is ambiguous or absent (Phase 3)
- variants have no genotype — identified only by plate and well (Phase 4)
- a stated result cannot be reproduced and the gap has no explanation (Phase 7)

---

## Appendix — extracting tables from a supplementary PDF

Plain text extraction interleaves multi-column tables into nonsense. Work from word coordinates.

```python
import pymupdf, collections
rows = collections.defaultdict(list)
for x0, y0, x1, y1, txt, *_ in pymupdf.open(path)[pno].get_text("words"):
    rows[round(y0, 1)].append((x0, txt))          # cluster into visual lines

for y in sorted(rows):
    toks = sorted(rows[y])
    for lo, hi in COLUMN_BLOCKS:                  # e.g. ((100,300),(300,520))
        g = [t for x, t in toks if lo <= x < hi]
        ...
```

Find `COLUMN_BLOCKS` by printing the `x0` of the header row once. Then:

- **Filter structurally, not by page geometry.** Require the shape of a data row
  (`g[0].isdigit() and VARIANT_RE.match(g[2])`); captions and footnotes fall out on their own.
- **Assert the row index is contiguous** — `sorted(entries) == list(range(1, n+1))`. Cheapest
  possible guard against a silently dropped row, and it is not optional.
- **Handle wrapped cells.** A value too wide for its column (`>99.9:0.1`) lands on its own line and
  leaves a short group behind. Collect orphans, reattach by nearest `y` within the same column
  block, then assert none remain unattached.
- **Read the column header of every sibling table.** Two tables that look identical may key on
  `well` instead of `variant` — that arm was never sequenced. Reject it (Phase 4) no matter how
  good the numbers are.
- **Check the caption's sort order.** Row order is usually rank within a plate, not a clone ID, so
  `entry` numbers do **not** align across two tables of the same screen. Join on the variant.
