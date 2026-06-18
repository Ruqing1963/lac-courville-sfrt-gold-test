# Release v1.0-prereg — Part I: pre-registration (predictions filed before drilling)

**Repository:** https://github.com/Ruqing1963/lac-courville-sfrt-gold-test
**Status:** Pre-registration. Drill results are NOT in this release; they will be reported in Part II.

This release time-stamps the predictions, drill-hole geometry and pass/fail criteria for a
falsifiable field test of Seismic Frequency Resonance (SFRT) gold targeting on the Lac Courville
Property (eastern Abitibi greenstone belt, Québec). After this release is archived by Zenodo, the
criteria below are fixed in the public record and will be adjudicated, without modification, in Part II.

## What is being tested
Whether SFRT (passive seismic frequency resonance; Zp/Zs dual-impedance re-analysis of Line 1)
identifies drillable structure — and, secondarily, gold — beneath a single 2-D profile.

## Pre-registered criteria
- **Mineralization-hit:** Au ≥ 0.3 g/t over ≥ 1 m, within or ≤ 10 m of the structural zone.
- **Structural-hit:** a shear / altered / veined zone within ± 50 m (true vertical) of the predicted depth window.
- **Program-level:** ≥ 2/3 holes structural-hit ⇒ SFRT effective for *structural* targeting;
  ≥ 1/3 holes mineralization-hit ⇒ *direct vectoring*; 0/3 structural-hit ⇒ recorded failure.

## Drill program (three NQ holes, 600 m each; azimuth 225° grid)
| Hole | Target | Collar E | Collar N | Dip |
|------|--------|----------|----------|-----|
| DDH-LC-01 | T1 | 326,217 | 5,356,515 | −60° |
| DDH-LC-02 | T2 | 325,703 | 5,355,797 | −65° |
| DDH-LC-03 | T3 | 325,307 | 5,355,239 | −58° |

Collar elevations to be fixed by RTK survey. Grid convergence ≈ −1.7°; magnetic declination
≈ −14° (2026). DDH-LC-02 tests the upper-central part of T2 (to ~544 m); a ~730 m extension would
be needed to reach its base.

## Third-party verification
Independent Québec-registered QP (NI 43-101) core logging; assays at Activation Laboratories
(Actlabs, ISO/IEC 17025) by fire assay with certified standards/blanks/duplicates; RTK collar and
trace survey; core photographed and archived.

## Contents
`paper/` (main.tex + main.pdf, 9 pp) · `code/` (reproducible Python) · `data/` (raw + processed
impedance, polygon, targets, drill plan, reference ledger) · `predictions/predrill_predictions.csv`
· `figures/` (PDF + PNG).

## Reproduce
```bash
pip install -r code/requirements.txt
cd code && python 01_zpzs_analysis.py && python 02_georeference_manneville.py \
  && python 03_drill_design.py && python make_figures.py
cd ../paper && pdflatex main && bibtex main && pdflatex main && pdflatex main
```

## Before you publish this release
- Replace placeholder ORCID iDs (`0000-0000-0000-0000`) in `.zenodo.json` with the authors' real iDs.
- Confirm author contributions and affiliations.
- (Optional) post the compiled PDF to a preprint server (e.g. EarthArXiv) and cross-link the DOI.

## How the DOI is minted
Enable this repo in Zenodo (Zenodo ↔ GitHub), then publish this GitHub Release (`v1.0-prereg`).
Zenodo archives it and issues a DOI; insert that DOI into the manuscript's
"Data and code availability" section.

## Competing interests
R. Chen is affiliated with the property holder (Minesound Ltd.); A. Xue is affiliated with the
SFRT method provider. The pre-registration and third-party verification are designed to mitigate this.

## Citation
See `CITATION.cff`.
