# A pre-registered field test of SFRT targeting for orogenic gold — Lac Courville Property (Abitibi, Québec)

**Part I (pre-registration):** targets, drill-hole geometry and explicit pass/fail criteria
filed **before** drilling, so the test of whether Seismic Frequency Resonance (SFRT) adds value
for gold targeting is *falsifiable*. Part II will report the drilling and adjudicate these
criteria without modification.


**Repository:** https://github.com/Ruqing1963/lac-courville-sfrt-gold-test

**Authors:** Aimin Xue (Beijing Petrosound Geoservices Corp.; `aiminx@126.com`) ·
Ruqing Chen (Minesound Ltd., Montreal; `ruqing@hotmail.com`)

---

## What this repository is
This is the time-stamped pre-registration of a drill test. The moment it is released with a
Zenodo DOI (see below), the predictions in `predictions/predrill_predictions.csv` and in the
manuscript are fixed in the public record. The drill results are **not** in this repository;
they will be added in a Part II release.

## Repository layout
```
paper/        main.tex, references.bib, compiled main.pdf, figures/ (PDF)
code/         reproducible Python (analysis, georeferencing, drill design, figures)
data/raw/     Line-1 P- and S-wave impedance (Valdor-Zp-f0.txt, Valdor-Zs.txt)
data/processed/  proc.npz (Zp/Zs fields), georef4.npz, mann.npz
data/         property_polygon.csv, targets.csv, drill_plan.csv, references_ledger.csv
predictions/  predrill_predictions.csv  <-- the falsifiable core
figures/      fig01–fig03 (PDF + PNG)
```

## Reproduce
```bash
pip install -r code/requirements.txt
cd code
python 01_zpzs_analysis.py            # raw impedance -> data/processed/proc.npz
python 02_georeference_manneville.py  # GM-49463 graticule -> UTM; digitized Manneville fit
python 03_drill_design.py             # collars, azimuth, dip, target intersections
python make_figures.py                # regenerate figures (PDF + PNG)
cd ../paper && pdflatex main && bibtex main && pdflatex main && pdflatex main
```

## Pre-registered criteria (summary)
- **Gold threshold (mineralization hit):** Au ≥ 0.3 g/t over ≥ 1 m, in or ≤10 m from the structural zone.
- **Structural hit:** a shear/altered/veined zone within ±50 m (TVD) of the predicted depth window.
- **Program-level:** ≥2/3 holes structural-hit ⇒ SFRT effective for *structural* targeting;
  ≥1/3 holes mineralization-hit ⇒ *direct vectoring*; 0/3 structural-hit ⇒ recorded failure.

## Drill program
Three NQ holes, 600 m each, azimuth 225° (grid), dips −58° to −65° (see `data/drill_plan.csv`,
`figures/fig03_drill_section.pdf`). Collar elevations to be fixed by RTK.

## Third-party verification
Independent Québec-registered QP (NI 43-101) core logging; assays at Activation Laboratories
(Actlabs, ISO/IEC 17025) by fire assay with standards/blanks/duplicates; RTK collar/trace survey;
core photographed and archived.

## Method basis (SFRT)
Passive-source seismic frequency resonance: Xue (2020, AGU Fall Meeting abstract T033-0013);
U.S. Patent 11,650,342 B2 (priority CN201811587566.3, 2018). Treated here as a hypothesis under
test, not as established.

## Minting the DOI (GitHub → Zenodo)
1. Push this repository to GitHub (https://github.com/Ruqing1963/lac-courville-sfrt-gold-test).
2. Enable the repository in your Zenodo account (Zenodo ↔ GitHub integration).
3. Create a GitHub **Release** (e.g. `v1.0-prereg`). Zenodo automatically archives the release
   and issues a DOI. Put that DOI in the manuscript "Data and code availability" section before
   journal submission, and (optionally) post the PDF to a preprint server (e.g. EarthArXiv).

## Honest limitations (see manuscript §9)
Relative (uncalibrated) impedances → anomalies indicate rock state, not grade; single 2-D line →
no across-strike control; historical georeferencing ~±100–150 m (does not affect on-line targets).
The authors hold the property and provide the method; the pre-registration and third-party
verification are designed to mitigate this. **Regional peer-reviewed citations should be expanded
before journal submission** (the bibliography currently leans on the assessment-report archive and
company disclosures for property-specific facts).

## Licence
Content, data and figures: CC BY 4.0. Code: MIT (see `LICENSE`).
