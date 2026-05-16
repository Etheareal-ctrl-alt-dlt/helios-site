# Helios Computer Corporation — Site

The official site for Helios. Built with [Astro](https://astro.build), deployed
to GitHub Pages, no JavaScript framework runtime in the browser.

---

## Quick start

```bash
npm install
npm run dev          # local preview at http://localhost:4321
npm run build        # production build → dist/
npm run preview      # serve the production build locally
```

## Project structure

```
src/
├── layouts/          BaseLayout.astro — HTML shell, fonts, meta
├── components/       Nav, Footer, ProductCard, FeatureItem, IrisEmblem
├── styles/           tokens.css (design system) + global.css
└── pages/            One .astro file per URL
    ├── index.astro       → /          (placeholder homepage)
    └── consumer.astro    → /consumer  (the consumer landing page)

public/
└── images/           Drop product renders, logos, and assets here.
                      Reference as /images/products/nova.png in code.
```

## Design tokens

All colors, fonts, spacing, and motion are in `src/styles/tokens.css`.
The two product lines are themed via `data-line="consumer"` and
`data-line="professional"` on `<body>`, set automatically by `BaseLayout`.

## Dropping in assets

The page currently uses CSS placeholders for the Nova hero shot and the
product card images. To replace them with real renders:

1. Save the image as `public/images/products/nova-hero.png`
   (or whatever filename you prefer).
2. In `src/pages/consumer.astro`:
   - **Hero**: replace the `.hero__placeholder` block with
     `<img src="/images/products/nova-hero.png" alt="..." />`.
   - **Product cards**: in the `products` array, change `image: null` to
     `image: '/images/products/nova.png'`.

The IRIS emblem is rendered in pure SVG (`IrisEmblem.astro`) per the
Product Bible spec, so no asset is required — but it can be swapped to
an `<img>` once Daniel has the authoritative emblem file.

## Deploying to GitHub Pages

1. Push the repo to GitHub (e.g. `helios-site`).
2. In your repo: **Settings → Pages → Build and deployment → Source: GitHub Actions**.
3. **If you're using `https://USERNAME.github.io/helios-site/`** (default project pages URL),
   edit `astro.config.mjs` and uncomment the `site` and `base` lines:

   ```js
   export default defineConfig({
     site: 'https://USERNAME.github.io',
     base: '/helios-site',
   });
   ```

   If you're using a custom domain (e.g. `helioscomputing.com`), leave them commented out.

4. Push to `main` — the workflow in `.github/workflows/deploy.yml` will
   build and deploy automatically. First deploy takes ~2 minutes.

## What's built so far

- ✅ Consumer landing page (`/consumer`)
- ✅ Design token system (extendable to Professional line)
- ✅ Reusable components (Nav, Footer, ProductCard, FeatureItem, IrisEmblem)
- ✅ GitHub Pages deploy workflow
- ⏳ Professional landing page
- ⏳ Per-product pages (Nova, Genesis, Atlas, Titan, Titan Display, IRIS)
- ⏳ Homepage (the entry point with the line split)
- ⏳ Support, Company, Community pages
- ⏳ Cart flow (functional or in-character "contact sales")
