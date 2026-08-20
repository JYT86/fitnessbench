# Example workflow: adding a paper

A worked example of turning one publication's supplementary data into FitnessBench
datasets, using Jiang et al. 2024 (PRIME) as the case.

One paper often yields **several** datasets — that paper measured five proteins across
three different properties, and became six CSVs in three categories. Work one
`(protein, readout)` pair at a time.

---

## 1. Stage the source

```
papers/{FirstAuthor} {Year}-{Model}-{Journal}.pdf
original_datasets/{FirstAuthor} {Year}-{Model}-{Journal}-data_s1.xlsx
```

Keep the supplementary file byte-identical to what the publisher shipped. Everything
downstream is regenerated from it, so it must stay the untouched ground truth.

## 2. Decide what each sheet actually measures

Read the methods, not the column headers. For each `(protein, readout)` pair settle
four things before writing any code:

| Question | Example answer | Determines |
|---|---|---|
| What property? | thermal stability | `Stability/ThermalStability/` |
| What readout, what unit? | Tm, °C | `readout` column |
| Which direction is better? | higher | whether to invert |
| How was it measured? | nanoDSF, Prometheus NT.48 | `assay_method` |

One trap worth naming: a paper's abstract may bundle unrelated goals into one
sentence — PRIME's "polymerize nonnatural nucleic acid **or** resilience to extreme
alkaline conditions" is two proteins, two properties, two categories.

## 3. Establish the wild-type sequence

In order of preference: a sequence the source states outright, a fetched accession,
a reconstruction. Whichever you take, run the same check on it — every mutation names
the wild-type residue it expects, so this is hundreds of independent checks at once:

```python
bad = [m for m in all_mutations if seq[int(m[1:-1]) - 1] != m[0]]
```

**If the source gives the sequence** — in the supplementary text, a FASTA, or a
methods section — use it. It is the construct they assayed. Still run the check, since
it also catches the numbering being stated against a different reference.

**Otherwise fetch.** PRIME's T7 RNA polymerase is the clean case: `P00573` fetches at
883 aa, all 70 distinct substitutions verify, `bad` is empty. Done.

**If `bad` is non-empty**, scan for a constant offset before discarding anything — an
initiator Met or a leading tag shifts every position alike:

```python
for off in range(-40, 41):
    ok = sum(seq[int(m[1:-1]) - 1 + off] == m[0] for m in all_mutations)
```

| Diagnosis | Action |
|---|---|
| Clean hit at some offset | Right sequence, different numbering. Renumber and use it. |
| Only one or two mismatches | Likely a typo in the paper. If the source data is self-consistent, follow the data and note it in `remark`. |
| Scattered mismatches, source ranks all substitutions | Wrong sequence. Reconstruct, below. |
| Scattered mismatches, no exhaustive ranking | Cannot reconstruct — mutation labels only constrain tested positions. Keep the fetched sequence, drop the mismatching variants, note it in `remark`; or reject the dataset. |

The construct that was actually on the bench is ground truth. Mutation labels are
direct evidence of it; an accession is a database entry that may be a different
isolate, an untagged native sequence, or a pre-engineering parent.

**Reconstruction.** When the source ranks every possible substitution, position `i`
appears 19 times with the same wild-type residue, so the sequence falls out:

```python
import re
pos_aa = {}
for m in ranking_column:                       # e.g. "H370K"
    g = re.fullmatch(r'([A-Z])(\d+)([A-Z])', m)
    pos_aa.setdefault(int(g.group(2)), set()).add(g.group(1))

assert all(len(v) == 1 for v in pos_aa.values())          # WT residue consistent
L = max(pos_aa)
assert set(pos_aa) == set(range(1, L + 1))                # no gaps
assert len(ranking_column) == L * 19 == len(set(ranking_column))
WT = ''.join(next(iter(pos_aa[p])) for p in range(1, L + 1))
```

Pass those and the sequence is not a guess — and it is the assayed construct, tags and
engineered background included. LbCas12a needed this (its one plausible UniProt entry
missed at every offset). So did VHH, whose construct carries a C-terminal
`DDDDK-SGGGGS-His6` tag with one tested variant sitting in the linker.

## 4. Assemble the variants

Common cleanups, in the order they usually bite:

- **Several blocks per sheet.** Papers often list one ranking per competing method,
  with the same variant showing up in more than one. Merge them and average the
  duplicates — but assert first that they agree, so a real disagreement surfaces
  instead of being averaged away:

  ```python
  vals = collections.defaultdict(list)          # mutant -> [values]
  ...
  for m, v in vals.items():
      assert max(v) - min(v) < tol, f'{m}: values disagree {v}'
  readout = {m: statistics.fmean(v) for m, v in vals.items()}
  ```

  Set `tol` to the rounding of the reported values. PRIME's T7 duplicates were exactly
  equal, so the same measurement was clearly reprinted; its Tgo-D4K sheet listed Q93A
  twice differing by 7e-5, which is rounding, not a second experiment.
- **Non-numeric cells.** `"no expression"` is not a measurement. Drop the row and
  record it in `remark`.
- **Multi-site rounds.** Join with `:`, keep them; they are the only epistasis signal
  in the file.

Then apply every mutation against `WT` with the checks that matter:

```python
for m in mutations:
    wt, p, mt = m[0], int(m[1:-1]), m[-1]
    assert 1 <= p <= L
    assert seq[p - 1] == wt          # catches numbering offsets
    assert wt != mt                  # catches synonymous entries
    seq[p - 1] = mt

assert sum(a != b for a, b in zip(WT, ''.join(seq))) == len(mutations)
```

That last line is the one that earns its keep: it is computed from the *output*, so it
catches a position mutated twice or a substitution that silently never landed.

## 5. Construct the readout, then normalize

**The readout does not have to be a column in the source.** Be willing to derive it.
The question to answer is what the experiment is actually comparing, and a source
column often answers a narrower or different one.

PRIME's VHH is the case to imitate. The sheet gives two columns: EC50 untreated, and
EC50 after 24 h in 0.3 M NaOH. Neither alone measures alkali resistance — the treated
column confounds it with how good the variant's binding was to begin with, so a
variant that binds poorly throughout looks alkali-sensitive, and a strong binder that
degrades badly can still beat the wild type. The ratio isolates what the experiment is
about:

```python
readout = ec50_untreated / ec50_treated       # how much binding survived
```

And because the untreated column answers a real question of its own, it becomes a
second dataset under `Binding/` rather than being discarded.

The cost is that derived readouts will not reproduce the paper's own statistics — the
PRIME text counts 11 of 29 variants as improved, using absolute treated EC50; the ratio
gives 26 of 29. Neither is wrong, they answer different questions. Record the
derivation in `remark` so nobody assumes the numbers should match.

**Then orient**, so `readout` always increases with fitness:

```python
readout = 1 / ec50            # EC50, IC50, Kd, error rate
readout = tm                  # Tm, rate, yield — already higher-is-better
```

**Then z-score** the readout as-is:

```python
mean, sd = statistics.fmean(x), statistics.pstdev(x)
score = [(v - mean) / sd for v in x]      # sd == 0 -> all zeros
```

## 6. Write the files

The CSV, four columns, WT row first when the source measured it:

```
datasets/{Category}/{Property}/{Source}/{Author} {Year}-{Model}-{Protein}-{property}-{readout}.csv
```

And one row appended to `datasets/{Category}/reference.csv`. Derive `seq_len`,
`wt_readout` and `n_variants` from the finished CSV rather than typing them, so they
cannot drift.

`remark` records **only what this version does differently from the source** — rows
dropped and why, duplicates merged, data deliberately excluded, a place where the
paper's text contradicts its own supplementary file. Things inherited unchanged from
the source do not belong there: that four variants are dead is the experiment's
result, not a curation decision.

---

## Before committing

```python
x = [float(r['readout']) for r in rows]
s = [float(r['normalized-score']) for r in rows]
m, sd = statistics.fmean(x), statistics.pstdev(x)
assert all(abs((xi - m) / sd - si) < 1e-6 for xi, si in zip(x, s))
assert len({r['mutant'] for r in rows}) == len(rows)
assert len({len(r['sequence']) for r in rows}) == 1
assert os.path.exists(os.path.join(category_dir, reference_row['filename']))
```

Plus one thing no assertion covers: re-derive a number the paper states in prose — a
count of improved variants, a fold-change — and check you land on it. When you cannot,
say so rather than reverse-engineering a formula that hits the published figure.
