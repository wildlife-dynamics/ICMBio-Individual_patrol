# Individual Patrol Report

**Relatório Patrulha** — a lightweight, single-patrol record for ICMBio, following the partner's Relatório Individual por patrulha template. Implemented as a configuration of the unified patrol reporting workflow (see [`ICMBio-patrol_analysis`](../ICMBio-patrol_analysis)), scoped to one patrol at a time, rather than a separate build. It pulls one patrol's track and events from EarthRanger and produces both an interactive dashboard and a Word (`.docx`) report.

## Dashboard

**Stat cards** — patrol metadata for the selected patrol

| Card | Shows |
|---|---|
| ID da patrulha | The patrol's serial number |
| Tipo de patrulha | Patrol type |
| Líder da patrulha | Patrol leader/subject |
| Participantes | Same value as Líder da patrulha (see [Known limitations](#known-limitations)) |
| Distância percorrida | Total distance covered by the patrol track, in km |
| Data e hora de início | Patrol start time |
| Data e hora do fim | Patrol end time |

**Map**

| Map | Shows |
|---|---|
| Mapa da patrulha | The single patrol track with its events overlaid, legend by event type. Optionally overlays an EarthRanger spatial feature layer and/or a locally-uploaded GeoJSON/GeoPackage/GeoParquet file (**Spatial Features** / **Local Spatial Features**). |

**Tables** — sortable, filterable, downloadable

| Table | Contents |
|---|---|
| Eventos | ID do evento, Tipo de evento, Detalhes do evento (situação do local; tempo estimado da atividade; estruturas observadas; ação tomada) |
| Registros Fotográficos | ID do evento, data e hora, coordenadas geográficas, tipo de evento — metadata only; the docx report embeds the actual photos |

## Scoping to a patrol

The **Patrol ID** parameter (`patrol_id`) is matched against the patrol's serial number (the human-facing ID shown in EarthRanger, e.g. what's displayed as "ID da patrulha"). Every patrol in the selected **Time Range** is fetched, then narrowed down to the one matching this ID — everything downstream (stat cards, map, tables, report) is scoped to that single patrol.

## Report (.docx)

`Patrol Report` renders the dashboard's content into the Relatório Patrulha template (`resources/templates/relatorio_individual_patrulha_template.docx`, built by `scripts/build_relatorio_individual_patrulha_template.py`). A patrol with zero events renders the Eventos/Registros Fotográficos sections empty rather than failing the whole report. Photo attachments can be skipped entirely via **Skip Photo Attachments**, if a faster run without images is preferred.

## Known limitations

- **Participantes** currently duplicates **Líder da patrulha** — EarthRanger has no separate support-crew ("equipe de apoio") list, matching the same open PRD question already flagged in `ICMBio-patrol_analysis`.
- The **Patrol ID → patrol row** column match (`serial_number` on the pre-observations patrols dataframe) needs to be confirmed against a real compile+run — see `spec.yaml`'s comment on the `selected_patrol` task.

## Status

This repo is scaffolded but not yet runnable end-to-end:

- [x] `spec.yaml` / `param.yaml` / `metadata.yaml` / `layout.json` / `test-cases.yaml` / `Makefile` / `dev/`
- [ ] New tasks in `wd-partner-tasks`'s `ecoscope-workflows-ext-icmbio`: `extract_formatted_datetime`, `format_individual_patrol_event_details`, `prepare_individual_patrol_report_context`, `generate_individual_patrol_report`
- [ ] `resources/templates/relatorio_individual_patrulha_template.docx` (built from the partner's mockup via `scripts/build_relatorio_individual_patrulha_template.py`)
- [ ] A real patrol serial number from the test data source, to replace the `TBD` placeholder in `param.yaml` / `test-cases.yaml`
- [ ] `make compile && make run` verified against real EarthRanger data

## Requirements

[pixi](https://pixi.sh) is required for environment and dependency management. You will also need an EarthRanger connection configured for the `parnaiguacu` data source (or another ICMBio account of your choosing).

## Getting started

```bash
make compile   # builds the ecoscope-workflows-ext-icmbio task package and compiles spec.yaml
make run       # runs the workflow against param.yaml (real EarthRanger data, no mock IO)
make open      # opens the generated HTML outputs in your browser
```

Run `make help` to see every available target (`recompile`, `refresh`, `clean`, `all`).

Results (dashboard HTML/PNG, the `.docx` report, and `result.json`) are written to `/tmp/icmbio-individual-patrol/output` by default — override with `OUTPUT_DIR=...`.

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
| `ecoscope-workflows-individual-patrol-workflow/` | Compiled workflow package (generated — never hand-edit) |
