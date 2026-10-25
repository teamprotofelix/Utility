# UTILITY NEXUS

A futuristic, lightweight, dependency-free utility directory for **https://util.moip.ai.kr/**.

## Included

- Cybernetic responsive design with locally generated & compressed WebP artwork
- Accessible navigation, keyboard `/` search shortcut and working category filters
- `Imgcomp` directory entry, service and GitHub source links
- Two honest, non-clickable future extension slots
- Static files only; no CDN, analytics, external API, cookie or account required by this hub
- SEO/OG metadata, CNAME, .nojekyll and smoke tests

## Add a new utility

Edit only `tools.js`, adding an object inside `window.UTILITY_TOOLS`. Required: a unique `id`, `name`, `subtitle`, `description`, `category` array, `tags` array, `url` (HTTPS), `image`, `status: 'live'`. Optional: `repository` (HTTPS) and `imageAlt`. Add the referenced optimized `.webp` under `assets/`. `app.js` will automatically update the listing, search, filters and live count. Supported filter categories in the current UI: `media`, `file`; when introducing a new category, also add a filter button in `index.html`.

**Important:** The directory does not inspect or upload user files. Individual apps have their own security, data handling and browser support caveats.

## Preview

Open `index.html` directly in a modern browser, or use a local server:

```sh
python -m http.server 8080
# http://localhost:8080
```

Test with Node.js 20+ (no npm install needed):

```sh
npm run check
```

Rebuild deterministic vector-inspired art as compressed WebP using Pillow + numpy:

```sh
python scripts/generate_art.py
```

## GitHub Pages and domain

1. `teamprotofelix/Utility` → **Settings → Pages** → `Deploy from a branch`, `main`, `/(root)`.
2. Add DNS CNAME `util` → `teamprotofelix.github.io` at the DNS provider; do not replace existing `imgcomp` record.
3. Repository `CNAME` already specifies `util.moip.ai.kr`. Confirm GitHub Pages custom domain and DNS verification, then enable `Enforce HTTPS` when available.
4. A GitHub push **alone** does not guarantee that Pages or custom DNS is configured.

All paths are relative for both root and `/Utility/` preview.
