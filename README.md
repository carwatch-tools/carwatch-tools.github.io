# CARWatch

CARWatch is an open-source framework to support **objective** and **low-cost** assessment of cortisol samples in real-world, unsupervised environments. It is especially suitable for **cortisol awakening response (CAR)** research, but not limited to this application.

For local authoring, the markdown files in [`docs/`](/Users/richer/Documents/PhD/Code_Repositories/HealthPsychology/CARWatch/carwatch/docs) remain normal UTF-8 source files. During the build, [`scripts/prepare_build_docs.py`](/Users/richer/Documents/PhD/Code_Repositories/HealthPsychology/CARWatch/carwatch/scripts/prepare_build_docs.py) creates a temporary normalized copy in `.build/docs` before MinimalDoc runs. This avoids a current MinimalDoc search-index issue with non-ASCII characters while keeping the editable source files clean.

## Project Website

The project overview, platform links, publication highlight, and privacy-policy page are hosted as a GitHub Pages site generated from the source files in [`docs/`](docs/).

This site uses [MinimalDoc](https://github.com/studiowebux/minimaldoc) as its static site generator and theme.

MinimalDoc also generates `llms.txt` and related machine-readable companion files. These can be useful for AI-assisted browsing or downstream tooling.

Once GitHub Pages is enabled to use GitHub Actions, the public site will be available at:

`https://carwatch-tools.github.io/`

For local editing, update the source files in [`docs/`](docs/), especially:

- [`docs/config.yaml`](docs/config.yaml)
- [`docs/index.md`](docs/index.md)
- [`docs/overview.md`](docs/overview.md)
- [`docs/components.md`](docs/components.md)
- [`docs/publications.md`](docs/publications.md)
- [`docs/privacy.md`](docs/privacy.md)
- [`docs/TOC.md`](docs/TOC.md)
- [`docs/brand/`](docs/brand) for site logo and favicon assets
- [`docs/site.webmanifest`](docs/site.webmanifest) for the web app/browser icon manifest
- [`scripts/postprocess_landing.py`](scripts/postprocess_landing.py) as the build-time entry point for HTML postprocessing
- [`scripts/postprocess_homepage.py`](scripts/postprocess_homepage.py) for homepage-specific layout and section rendering
- [`scripts/postprocess_shared.py`](scripts/postprocess_shared.py) for shared branding, content-page chrome, and common HTML helpers

The GitHub Pages deployment workflow is defined in [`.github/workflows/docs.yml`](.github/workflows/docs.yml).

## Local Preview

### Requirements

Local development requires:

- Go installed and available on `PATH`
- network access if MinimalDoc is not already available locally

The GitHub Actions deployment workflow does **not** depend on any local `/tmp` paths. It installs MinimalDoc during CI and builds the site independently of your machine.

### First-Time Setup

Bootstrap the MinimalDoc binary with:

```bash
make install
```

This installs MinimalDoc into the repo-local path `.tools/bin/minimaldoc`.

If `make install` fails, check your setup with:

```bash
make doctor
```

Build the site locally with:

```bash
make
```

Serve the built site and open it in your browser with:

```bash
make view
```

Build without serving with:

```bash
make build
```

If you want to run the server without opening the browser:

```bash
make serve
```

The server runs in the foreground until you stop it with `Ctrl+C`.

To use a different port temporarily:

```bash
make serve PORT=4321
make view PORT=4321
```

To remove local build output:

```bash
make clean
```

To remove both local build output and the repo-local MinimalDoc binary:

```bash
make clean-all
```

### Notes

- Local build output is written to `.build/site`.
- The local MinimalDoc binary is stored in `.tools/bin/minimaldoc`.
- The build pipeline applies a small post-processing step to generated HTML so the homepage and content pages can use the project-specific layout and branding that MinimalDoc does not expose through config alone.
- Brand assets from `docs/brand/` and `docs/site.webmanifest` are copied into the built site during local and CI builds.
- If `.tools/bin/minimaldoc` is missing, `make`, `make build`, `make serve`, and `make view` will install it automatically when Go is available.
- The first local install may take a moment because Go downloads the MinimalDoc module and its dependencies.
- If you are offline and do not already have a working `minimaldoc` binary, local installation will fail.
- In that case, reconnect to the network and run `make install`.
- `make` only builds the site. It does not start the server.
- `make view` starts a local server, opens the browser, and should stop the server again when you press `Ctrl+C` in that terminal.
- If `make serve` reports that the port is already in use, check for an existing listener with:

```bash
lsof -nP -iTCP:4173 -sTCP:LISTEN
```

Stop the old process and then run `make serve` again.

`make clean` removes only generated site output in `.build/`.

`make clean-all` removes both `.build/` and `.tools/`.

## Current Scope

The GitHub Pages site currently provides:

- a landing page for the CARWatch project
- links for the Android app, the Study Manager, project pages, publications, and related resources
- a structured news section ready for future updates
- a formal privacy-policy page with placeholder content for app-store compliance work

## Publication

If you use CARWatch in your work, please cite:

```text
Richer, R., Abel, L., Küderle, A., Eskofier, B. M., & Rohleder, N. (2023). CARWatch – A smartphone application for
improving the accuracy of cortisol awakening response sampling. Psychoneuroendocrinology, 151, 106073.
https://doi.org/10.1016/j.psyneuen.2023.106073
```

## License

This project is licensed under the MIT License. See [`LICENSE`](LICENSE) for details.
