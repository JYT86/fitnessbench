# 2019 candidate papers

Screening notes for the `2019` branch. Cut from `main`, so it starts from the six Jiang 2024 PRIME
datasets and nothing else.

Part of the **2009–2020 MaveDB enzyme cohort**. The discovery work and the backlog files live on the
`2015` branch (`candidates_2015.md`, `backlog_pre2022.tsv`); this file records only what 2019 yielded.

## Scope — enzymes and enzyme-adjacent

Set on 2026-08-31 on the `2022` branch. Carried here verbatim.

**In scope**: catalysts, and proteins whose measured phenotype is catalytic machinery — nucleases,
polymerases, helicases, ATP-driven transporters.

**Out of scope**: fluorescent proteins, binding domains, ion channels, structural and scaffold
proteins, viral surface glycoproteins.

Src is a tyrosine kinase and the readout is its phosphotransferase activity, so it passes on both
halves. Human, so `datasets_human/`.

## Shipped — 1 dataset, 3,714 variants

### Ahler 2019, Src kinase — 3,714 variants

`10.1016/j.molcel.2019.02.003`, *A Combined Approach Reveals a Regulatory Mechanism Coupling Src's
Kinase Activity, Localization, and Phosphotransferase-Independent Functions*, Mol Cell 2019. From
`urn:mavedb:00000041` (CC0), in `datasets_human/Activity/CatalyticActivity/DMS/`.

This one needed three decisions, all of them caught by checks rather than noticed by eye.

**1. The deposit's target record is wrong for one of its two sets.** MaveDB labels both score sets
`Src catalytic domain`. A pooled label check against that 250-residue target gave `bad = 323`, and no
constant offset fixed it. Split per set, the picture resolves:

| set | region | positions | offset onto P12931 | bad after offset |
|---|---|---|---|---|
| `a-1` | catalytic domain | 1–250 | **+269** (the excerpt is P12931 270–519 verbatim) | 0 |
| `b-1` | SH4 domain | 1–18 | **+1** | 0 |

The SH4 offset is +1 because the initiator Met is cleaved for myristoylation, so the mature protein is
numbered from Gly. The labels imply `GSNKSKPKDASQRRRSLE`, which is P12931 2–19 exactly. Both sets are
renumbered onto **full-length P12931**, which is also the molecule actually assayed.

**2. The readout runs backwards, and the nonsense variants are what show it.** Under the deposit's
`score`, the 152 nonsense variants — a dead kinase — sat **above** the substitutions, median +1.61 and
+1.64 against +0.45 and −0.02. Active Src is growth-inhibitory in yeast, so a growth-derived score is
inverted with respect to activity. The deposit ships `activity_score`, which is exactly `-score` on
all 3,866 rows and puts the nonsense variants below. **`activity_score` is the readout.**

This is the check the `2025` branch's method notes demand after the EnvZ 37 °C arm, whose nonsense
variants also scored above wild type: *"When a source ships an internal control — nonsense variants, an
empty-vector lane, a wild-type row — check them before shipping."* Nothing mechanical would have caught
it; `validate.py` passes either way.

**3. Two sets, one work item.** Same protein, same assay, same quantity, two library regions — which
under Phase 1 is more rows, not more work items. They share **no variant**, so the merge rests entirely
on a control, and here the control holds: the dead-variant anchors agree to **0.033** (−1.606 against
−1.639). The build asserts that agreement rather than assuming it, and refuses to merge if the anchors
drift more than 0.2 apart.

No wild-type row exists in either set, so `wt_readout` is empty.

## Not done

- **The article is not staged in `papers/`.** `PMC6474823` exists but Europe PMC reports the paper as not
  open access.
- **Phase 7 has no re-derived prose number.** The internal checks are the offsets landing at bad = 0, the
  nonsense anchors agreeing across blocks, and the row arithmetic closing at 3,866 = 3,714 + 152.
- The paper's **phosphotransferase-independent** functions, which its title highlights, are not in this
  deposit. If they were measured per variant, they would be a second work item with a different
  property.

## Other 2019 items seen and not taken

From the MaveDB enumeration on the `2015` branch:

- **`10.1016/j.jmb.2019.04.030`** — TEM-1 single amino acid insertions and deletions. **Rejected on the
  format, not on merit**: an indel has no `{WT}{position}{MUT}` form. Recorded on `2015` too.
- **`10.1016/j.jmb.2019.03.020`** — *Pervasive Pairwise Intragenic Epistasis among Sequential Mutations
  in TEM-1*. Same lab and the same band-pass system as the `2014` and `2016` branches, and pairwise
  epistasis is exactly what this benchmark is short of. **Not opened** — no MaveDB deposit surfaced for
  it, so it needs a Phase 0 chase.
