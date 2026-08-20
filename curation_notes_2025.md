# Curation notes: how the Zhang 2025 datasets were made

A companion to `example_workflow.md`, not a replacement — that document is the protocol
and is unchanged. This one records how one paper was taken from a search result to two
validated CSVs, in the order it happened, and the judgment calls the protocol does not
yet cover. The paper is Zhang et al. 2025, *Machine learning-guided evolution of
pyrrolysyl-tRNA synthetase*, Nature Communications, `10.1038/s41467-025-61952-2`.

Everything below is publisher-open. No subscription, no manual downloads, and no
hand-editing of a spreadsheet at any point.

---

## The run, end to end

| Stage | What it produced |
|---|---|
| Screen the search hits | 20 unique 2025 articles → 3 with variant-level data (`candidates_2025.md`) |
| Pull the files | article PDF, Supplementary Data XLSX, Source Data XLSX, SI PDF |
| Inventory the workbooks | 4 sheets + 35 sheets, of which 11 hold measurements |
| Establish the references | 2 sequences, translated from supplementary DNA, verified three ways |
| Map the panels | 7 panels for one readout, 2 parents, 18 shared labels |
| Merge and write | 101 + 407 variants, 2 CSVs, 2 `reference.csv` rows |
| Verify | validator clean, 3 prose numbers re-derived, 1 discrepancy found |

---

## 0. Screen before you download

A publisher search restricted to one year returns mostly reviews, and it sees only that
publisher's journals. Two fields decide whether a paper is worth staging:

- **the abstract** — does it measure many variants of *one* protein, or compare
  unrelated proteins? "24 Cas12a orthologs" is not a mutational landscape.
- **the data-availability statement** — "all data are available within the paper" with
  no XLSX and no named repository usually means there is nothing to curate.

Zhang 2025 passed both: a named ML framework, an explicit fold-change, and a statement
pointing at Supplementary Data, Source Data, GitHub and Zenodo.

## 1. Pull the files

`nature.com` answers a plain HTTP fetcher with `303 See Other` to
`idp.nature.com/authorize`, so a fetch-and-summarize tool returns the redirect rather
than the page. `curl -sL` with a browser user-agent follows it:

```bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0"
ID=s41467-025-61952-2
curl -sL -A "$UA" "https://www.nature.com/articles/${ID}"     -o article.html -w '%{http_code} %{size_download}\n'
curl -sL -A "$UA" "https://www.nature.com/articles/${ID}.pdf" -o paper.pdf
grep -oE 'https://media[^"]*MOESM[0-9]+_ESM\.[a-z]+' article.html | sort -u
```

**One request at a time.** A burst trips the bot challenge, and every response becomes a
~3 KB `Client Challenge` page instead of the ~130 KB article. It is not an error, and it
parses into zero rows without complaining — so print `%{size_download}` on every fetch
and actually look at it.

**The MOESM number is not the Supplementary Data number.** Read the caption text sitting
next to each link before deciding what a file is. Zhang 2025 ran: `MOESM1` SI PDF,
`MOESM2` description, `MOESM3` Supplementary Data XLSX, `MOESM4` reporting summary,
`MOESM5` peer review, `MOESM6` Source Data XLSX. The reporting summary and the
peer-review file are never wanted.

**Staging names.** `papers/` takes the article, `original_datasets/` takes the data,
both under the `{FirstAuthor} {Year}-{Model}` prefix that links them to the dataset.
Two things about `{Model}`:

- it **cannot contain a hyphen** — `validate.py` reads that field as `[^-]+`, so
  `FFT-PLSR` breaks the filename check and became `FFTPLSR`
- when the paper brands no framework, name the model that actually does the work. Here
  the deep-learning models only nominate positions; FFT-PLSR drives every round.

Stage a supplementary PDF only if you took something from it that is not in the
spreadsheets. Zhang 2025's Supplementary Table 8 is the only place the `Z7-n`
abbreviations expand into mutation sets, so the table is needed — but the 26 MB of
figures wrapped around it are a permanent cost to everyone who clones the repo. That
file is deliberately left out of the commit and named in `remark` instead.

## 2. Inventory the workbooks before reading any of them

```python
wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
for ws in wb.worksheets:
    print(ws.title, ws.calculate_dimension())
```

This is what showed where the work was. The Supplementary Data workbook held only DNA
and primers — no measurements at all — while the Source Data workbook held 35 sheets,
one per figure panel, of which 11 carried variant measurements. A file called
"Supplementary Data" is not reliably the data.

## 3. Establish the reference sequences

### Prefer the supplement's DNA over an accession

Zhang 2025 ships the coding sequence of every construct, so the protein came from a
codon table rather than from UniProt — and it is the assayed construct by definition,
with no isolate or tagging question to resolve. Translate to the first stop, and check
the length against the paper.

### Then verify it three ways

```python
MmPylRS = translate(dna["MmPylRS"])                   # 454 aa, as the paper states
assert MmPylRS[345] == "N" and MmPylRS[347] == "C"    # the paper calls IFRS "N346I/C348S"
assert apply(apply(MmPylRS, COM1_MUTS), Z7_3_MUTS) == translate(dna["Com2-MmPylRS"])
```

The third line is the one to look for in any paper: when the supplement ships a **final
engineered sequence**, applying the paper's own mutation labels to the parent must
reproduce it exactly. That single assertion confirms the parent, the numbering, the
label parsing and the substitution code all at once — a check no accession can give you.

### One paper, two reference sequences

The campaign ran two rounds, the first normalized to IFRS and the second to Com1-IFRS,
which is IFRS plus seven substitutions. **A round that improves on the previous round's
winner is a different dataset**, even though it is the same protein, the same assay and
the same units: a CSV has one reference sequence and one z-score population, and a
reader who pooled them would be comparing fold-changes measured against different
denominators.

Watch for this whenever a paper reports "relative to the parent" and also reports that
it improved the parent.

## 4. Map the panels before curating anything

Source Data is organised **by figure panel, not by experiment**, so one readout is
spread across as many sheets as the authors drew figures — seven, here — and the same
variant can appear in several of them. Enumerate labels per panel and print the
overlaps:

```python
panels = {t: set(labels_of(wb[t])) for t in wb.sheetnames}
for a, b in itertools.combinations(panels, 2):
    if panels[a] & panels[b]:
        print(a, b, len(panels[a] & panels[b]))
```

What comes back falls into three kinds:

| Overlap | What it is | What to do |
|---|---|---|
| Same labels, same values | one measurement, re-plotted | take either, they are one panel |
| A "predicted vs experimental" sheet matching another sheet's replicate mean | the model-accuracy scatter | use the replicates, keep the scatter as a check |
| Same labels, different values | two experiments, or an inconsistency | rank them, below |

Two shapes worth naming:

- **A matrix, not a list.** A mutability landscape ships as 20 amino-acid rows by N site
  columns. Melt it to labels, and drop the cell where the substituted residue equals the
  site's own residue — it reads 1.0 because it is the parent, not because a variant was
  measured.
- **Data the text never counts.** Fig. 2b is described only as a scatter of "single
  variants designed", but the sheet behind it carries 115 measured single mutants across
  85 positions — more than a quarter of that dataset, and no sentence in the paper
  mentions it. Panel-mapping is how you find this; reading the paper is not.

## 5. Merge: rank, do not average

`example_workflow.md` says to assert that duplicates agree before averaging them. When
that assertion fires, **do not widen the tolerance.** Rank the panels once, take the
best-ranked value for every shared label, and put the disagreement in `remark`:

1. a panel measured in triplicate and drawn with error bars
2. a systematic screen — a saturation landscape, a designed library
3. a scatter or summary that re-plots either of the above

Averaging is right for a reprint and wrong for a disagreement. Fig. 2b and 2d share 18
labels, 13 identical to the last digit and 3 more within 0.03 — which says the two
panels draw on one set of measurements. The remaining two do not: N7D reads 0.634
against 0.472, K67R 0.527 against 0.801. Their mean would be a number neither sheet
reports. Take the ranked panel, name both values in `remark`, and let a reader who cares
go to the source.

### Labels you derived need their own check

Fig. 2b is keyed `residue index | residue type | method | activity` — no wild-type
letter. That forces you to fill the letter in from your own reference sequence, which
makes the label agree with that sequence **by construction**. An off-by-one in the
sheet's indexing would be invisible: every label would apply cleanly, and every one
would be wrong.

The check is external agreement. Those 18 derived labels coincide with labels printed in
full elsewhere in the same workbook, and 13 carry identical values — which an offset
could not produce. Find that overlap before trusting a derived label; if there is none,
say so in `remark` rather than presenting the labels as read.

### Units, when one panel disagrees with the others

Fig. 2h reports raw normalized fluorescence while every other round-2 panel reports
fold-change against the parent. It was converted by dividing by the Com1-IFRS mean
*within that panel*, which is what the paper does implicitly — see the 30.8-fold check
below. Its `Z7-n` labels were resolved through Supplementary Table 8, and its wild-type
sfGFP control row dropped, since that row is not a synthetase variant.

## 6. Write

Two things learned by tripping the validator:

- **Round the readout before z-scoring it, not after.** The two columns must agree to
  1e-6, and they will not if `readout` is written rounded while `normalized-score` came
  from the full-precision value. `x = [float(f"{v:.6g}") for v in x]` first, then
  mean/sd/score from those.
- **A parent-normalized readout needs no `WT` row.** It is 1.0 by definition rather than
  by measurement, and adding it drags the z-score population toward a number nobody
  measured. Put 1.0 in `wt_readout`, leave the row out, and say so in `remark`.
  `validate.py` accepts this and still checks every other row's substitutions against
  the reference sequence. PRIME's Tgo-D4K is the precedent.

## 7. Verify

```bash
python validate.py       # 8 datasets, 861 variants, 0 errors, 0 warnings
python test_validate.py
```

Then the half no assertion covers: re-derive numbers the paper states in prose. Pick the
statements that touch the most of the pipeline.

| Stated | Re-derived | What it covers |
|---|---|---|
| Z7 is 11-fold over IFRS | 11.12 | the round-1 merge, and that the parent really is the denominator |
| Com2-IFRS is 30.8-fold over IFRS | 30.6 | the Fig. 2h unit conversion, the `Z7-n` lookup, **and** that the two rounds compose |
| 3, 7, 5, 1, 2, 9 mutations improve on Com1-IFRS by >10% at six sites | 3, 7, 5, 1, 2, 9 | the landscape melt, the dropped parent diagonal, the threshold |

The third is the kind worth hunting for: an exact integer sequence that only comes out
right if several independent decisions are all correct. It also earned its keep. The
counts reproduce at **V74 and D76**, while the sentence stating them names **V73 and
D75**. The source data columns say 74 and 76, so the data numbering wins and the
discrepancy goes in `remark`.

A re-derivation that *disagrees* is worth more than one that agrees — but only if you
write down which side you followed, and why.

---

## Checklist for the next paper

1. Screen on the abstract **and** the data-availability statement.
2. `curl` one request at a time; check the byte count on every fetch.
3. Map MOESM numbers to captions before naming files.
4. List every sheet and its dimensions before reading any of them.
5. Build the reference sequence from the supplement's own DNA where it exists.
6. Find one assertion that reproduces a shipped engineered sequence from labels.
7. Count the parents. One dataset per parent.
8. Enumerate panel labels and print every overlap.
9. Rank overlapping panels; never average a real disagreement.
10. Corroborate any label whose wild-type letter you supplied yourself.
11. Round, then z-score.
12. Run the validator, then re-derive three numbers from the prose.

---

## What this branch touches

Nothing carried over from `main` is modified except `datasets/Activity/reference.csv`,
which gains two rows. That file is the registry every dataset must appear in, and
`.gitattributes` sets `merge=union` on it precisely so parallel contributions
concatenate rather than conflict. `README.md` and `example_workflow.md` are byte-identical
to `main`.

The script that produced the Zhang 2025 datasets was kept out of the repository, matching
how the other hand-curated papers were done — no per-paper scripts in the tree. Ask if
you would rather it shipped alongside the datasets.
