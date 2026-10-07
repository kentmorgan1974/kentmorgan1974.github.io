# kentmorgan1974.github.io

Static site (GitHub Pages) with a home page, a software list, and one page per program.
Live at https://kentmorgan1974.github.io/

The pages are generated from `products.json` by `build.py` and the output is committed.

## Add a program

1. Add an entry to `products.json` (copy the `litwell` one). `repo` is the public GitHub
   repo whose latest release holds the downloads; `windows_asset` and `mac_asset` are the
   fixed file names in that release.
2. Put its icon in `assets/` and point `icon` at it.
3. Run `python3 build.py`, check the pages locally (`python3 -m http.server`), commit, push.

The home page, the Software list and the program's own page update together, and each page
reads the latest version number from the program's GitHub release.

## Change the site name or headline

Edit the `site` block at the top of `products.json` and run `python3 build.py`.
Colours and type are in `assets/style.css` (palette variables at the top; the dark theme is the
second block). The header has a light/dark toggle (`assets/site.js`) that remembers the choice
in the visitor's browser.
