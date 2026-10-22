"""Build Pauly's Recipe Book site.
Usage: python3 _src/build.py https://paulytx.github.io/recipes/
Writes index.html plus r/<id>/index.html (one share page per recipe, with its own
title and photo preview, that opens the recipe in the book)."""
import json, sys, html, os, shutil
site = sys.argv[1] if len(sys.argv) > 1 else "https://paulytx.github.io/recipes/"
if not site.endswith("/"): site += "/"
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
recipes = json.load(open(os.path.join(root, "_src/recipes.json"), encoding="utf-8"))
tpl = open(os.path.join(root, "_src/template.html"), encoding="utf-8").read()
data = json.dumps(recipes, ensure_ascii=False).replace("</", "<\\/")
page = tpl.replace("/*RECIPES*/", data, 1).replace("/*SITE*/", site, 1)
open(os.path.join(root, "index.html"), "w", encoding="utf-8").write(page)
shutil.rmtree(os.path.join(root, "r"), ignore_errors=True)
for r in recipes:
    e = lambda s: html.escape(s, quote=True)
    url = site + "r/" + r["id"] + "/"
    meta = (f'<base href="../../"><title>{e(r["title"])}</title>'
            f'<meta name="description" content="{e(r.get("description",""))}">'
            f'<meta property="og:type" content="article"><meta property="og:site_name" content="Pauly\'s Recipe Book">'
            f'<meta property="og:title" content="{e(r["title"])}"><meta property="og:description" content="{e(r.get("description",""))}">'
            f'<meta property="og:url" content="{e(url)}">')
    if r.get("image"):
        meta += (f'<meta property="og:image" content="{e(site + r["image"])}"><meta property="og:image:width" content="1000">'
                 f'<meta name="twitter:card" content="summary_large_image">')
    meta += f'<script>if(!location.hash)history.replaceState(null,"",location.pathname+"#s/{r["id"]}")</script>'
    rp = page.replace("<title>Pauly's Recipe Book</title>", "", 1).replace("<meta charset=utf8>", "<meta charset=utf8>" + meta, 1)
    d = os.path.join(root, "r", r["id"]); os.makedirs(d)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(rp)
print(f"Built {len(recipes)} recipes for {site}")
