# ridni.app — instructions for Claude

Read `README.md` first: it is the full guide (rule, layout, writing, build, publish, what not to touch).

Short version:
1. The site follows the code. Every data claim is in `_build/CLAIMS.md` with the file that makes it true. Change the
   row and the text in all 7 languages together.
2. Edit only `_build/pages/<lang>/<slug>.html`, then `python3 _build/build.py`, commit, push to `main`, verify in a browser.
3. Same block order in every language; English is binding for privacy and terms; informal register (ти/ты/ty/du/tú/tu).
4. Do not touch DNS, `CNAME`, `.nojekyll`, repo visibility (must stay public), or Design's files without asking.
