# Pauly's Recipe Book

Live at https://paulytx.github.io/Recipes/

- Recipe data: `_src/recipes.json` (one entry per recipe, same template as Focaccia Buns)
- Page design and features: `_src/template.html`
- Photos: `img/<recipe-id>.jpg`
- Rebuild after any change: `python3 _src/build.py https://paulytx.github.io/Recipes/`
  (writes `index.html` and `r/<recipe-id>/index.html`, one shareable page per recipe)
