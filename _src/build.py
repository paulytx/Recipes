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
    img = f'<meta property="og:image" content="{e(site + r["image"])}"><meta name="twitter:card" content="summary_large_image">' if r.get("image") else ""
    target = f'../../#s/{r["id"]}'
    d = os.path.join(root, "r", r["id"]); os.makedirs(d)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow">
<title>{e(r["title"])}</title><meta name="description" content="{e(r.get("description",""))}">
<meta property="og:type" content="article"><meta property="og:site_name" content="Pauly's Recipe Book">
<meta property="og:title" content="{e(r["title"])}"><meta property="og:description" content="{e(r.get("description",""))}">
<meta property="og:url" content="{e(site + "r/" + r["id"] + "/")}">{img}
<meta http-equiv="refresh" content="0; url={target}"><script>location.replace("{target}")</script>
</head><body><p><a href="{target}">Open {e(r["title"])}</a></p></body></html>''')
print(f"Built {len(recipes)} recipes for {site}")
