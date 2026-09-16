# Individual Patrol Report

**Relatório Patrulha** — a lightweight, single-patrol record for ICMBio, following the partner's Relatório Individual por patrulha template. Implemented as a configuration of the unified patrol reporting workflow (see [`ICMBio-patrol_analysis`](../ICMBio-patrol_analysis)), scoped to one patrol at a time, rather than a separate build. It pulls one patrol's track and events from EarthRanger and produces both an interactive dashboard and a Word (`.docx`) report.

## Dashboard

**Stat cards** — numeric only, matching every sibling workflow's convention (text/categorical fields go in tables, not cards)

| Card | Shows |
|---|---|
| Número de eventos | Count of events recorded on the patrol |
| Distância percorrida (km) | Total distance covered by the patrol track |
| Tempo total (h) | Total elapsed patrol time |

**Map**

| Map | Shows |
|---|---|
| Mapa da patrulha | The single patrol track with its events overlaid, legend by event type. Both the track and the events have their own colormap (Palette / Custom Colors), matching every sibling workflow's Patrol Style / Event Style sections. Optionally overlays an EarthRanger spatial feature layer and/or a locally-uploaded GeoJSON/GeoPackage/GeoParquet file (**Spatial Features** / **Local Spatial Features**). |

**Table** — sortable, filterable, downloadable

| Table | Contents |
|---|---|
| Eventos | ID do evento, Tipo de evento, Detalhes do evento (situação do local; tempo estimado da atividade; estruturas observadas; ação tomada) |

## Scoping to a patrol

The **Patrol** parameter (`patrol_id`, labeled "Patrol ID") is matched against the patrol's serial number (the human-facing ID shown in EarthRanger, e.g. what's displayed as "ID da patrulha"). Every patrol in the selected **Time Range** is fetched, then narrowed down to the one matching this ID — everything downstream (stat cards, map, table, report) is scoped to that single patrol.

## Report (.docx)

`Patrol Report` renders the same underlying data into the Relatório Patrulha template (`resources/templates/relatorio_individual_patrulha_template.docx`, built by `scripts/build_relatorio_individual_patrulha_template.py`). Unlike the dashboard, the docx report includes the full patrol metadata table (ID da patrulha, Tipo de patrulha, Líder da patrulha, Distância percorrida, Data e hora de início/fim, Participantes) — matching the PRD's stat-card list literally, since that's the template's own layout — plus the Eventos table and a **Registros Fotográficos** table with the actual embedded photos (dashboard-only metadata table for this was intentionally dropped; photos live in the docx only). A patrol with zero events renders those sections empty rather than failing the whole report. Photo attachments can be skipped entirely via **Skip Photo Attachments**, if a faster run without images is preferred.

## Known limitations

- **Participantes** (docx only) currently duplicates **Líder da patrulha** — EarthRanger has no separate support-crew ("equipe de apoio") list, matching the same open PRD question already flagged in `ICMBio-patrol_analysis`.

## Requirements

[pixi](https://pixi.sh) is required for environment and dependency management. You will also need an EarthRanger connection configured for the `parnaiguacu` data source (or another ICMBio account of your choosing).

## Getting started

```bash
make compile   # compiles spec.yaml against the published ecoscope-workflows-ext-icmbio
make run       # runs the workflow against param.yaml (real EarthRanger data, no mock IO)
make open      # opens the generated HTML outputs in your browser
```

Run `make help` to see every available target (`recompile`, `refresh`, `clean`, `all`).

Results (dashboard HTML/PNG, the `.docx` report, and `result.json`) are written to `/tmp/icmbio-individual-patrol/output` by default — override with `OUTPUT_DIR=...`.

`param.yaml`/`test-cases.yaml` are set up against a real, verified patrol (serial number `262`) at `parnaiguacu`, over its actual real date range — verified end-to-end (`error: None`), including real photo-attachment downloads.

## Repo layout

| Path | Purpose |
|---|---|
| `spec.yaml` | The DAG — hand-authored, compiled via `wt-compiler` |
| `param.yaml` | Default run configuration (real EarthRanger data source, time range, patrol ID) |
| `layout.json` | Dashboard widget grid |
| `metadata.yaml` | Workflow name/author/description |
| `test-cases.yaml` | Named test case(s) against real ICMBio park data |
| `dev/` | `recompile.sh` (full compile) and `regenerate_rjsf.sh` (fast, schema-only regen) |
| `resources/templates/` | The `.docx` report template |
| `scripts/` | `build_relatorio_individual_patrulha_template.py` — builds the template from the original mockup |
| `.scripts/` | Ad-hoc, gitignored debug/verification scripts used during development (not part of the compiled workflow) |
| `ecoscope-workflows-individual-patrol-workflow/` | Compiled workflow package (generated — never hand-edit) |
