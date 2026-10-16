# Homepage build

`index.html` and `es/index.html` are generated. Edit these scripts, then run from the repo root:

    python3 tools/site-build/build.py && python3 tools/site-build/build_es.py

- `build.py` builds the English homepage from `year_end_src.html` (hero scene, form, styles and script)
  plus the original site's copy in `original_index.html`.
- `build_es.py` builds `/es/` from the English page with a string-for-string translation table. It prints
  `missing: [...]` for any English string it could not find; fix those before committing. Values sent to
  GHL stay in English.
