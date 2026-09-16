"""Debug/verification script — NOT part of the compiled workflow.

Replicates spec.yaml's Event Style task-group exactly, step by step,
against real parnaiguacu data for one real patrol, using the
already-compiled workflow's own installed functions — without a full
`make compile && make run` cycle. Point of this: confirm the pipeline is
correct *before* touching spec.yaml again, since each compile+run cycle
costs real minutes.

Run with the compiled workflow's own python:
    ecoscope-workflows-individual-patrol-workflow/.pixi/envs/default/bin/python .scripts/debug_events_pipeline.py
"""

import os

import pandas as pd
from ecoscope.io.earthranger import EarthRangerIO
from ecoscope.io.earthranger_utils import unpack_events_from_patrols_df
from ecoscope.platform.tasks.io._earthranger import process_events_details
from ecoscope_workflows_ext_icmbio.tasks._individual_patrol import format_individual_patrol_event_details

PATROL_SERIAL = 262


def get_client() -> EarthRangerIO:
    return EarthRangerIO(
        server=os.environ["ECOSCOPE_WORKFLOWS__CONNECTIONS__EARTHRANGER__parnaiguacu__SERVER"],
        username=os.environ["ECOSCOPE_WORKFLOWS__CONNECTIONS__EARTHRANGER__parnaiguacu__USERNAME"],
        password=os.environ["ECOSCOPE_WORKFLOWS__CONNECTIONS__EARTHRANGER__parnaiguacu__PASSWORD"],
    )


def main() -> None:
    client = get_client()

    # --- selected_patrol / selected_patrol_serial_as_int (spec.yaml) ---
    patrols = client.get_patrols(since="2025-09-01", until="2026-09-01", patrol_type_value=[], status=["done"])
    single_row_patrols_df = patrols[patrols["serial_number"] == PATROL_SERIAL]
    assert len(single_row_patrols_df) == 1, "patrol not found"

    # --- patrol_events (unpack_events_from_patrols_df_and_combined_params) ---
    convert_events_tz = unpack_events_from_patrols_df(
        patrols_df=single_row_patrols_df, event_type=[], drop_null_geometry=False, event_state=None
    )
    print(f"convert_events_tz: {len(convert_events_tz)} rows, columns: {list(convert_events_tz.columns)}")

    # --- events_with_type_display (get_event_type_display_names_from_events) ---
    events_with_type_display = client.get_event_type_display_names_from_events(convert_events_tz, append_category_names="duplicates")
    assert "event_type_display" in events_with_type_display.columns
    print("event_type_display:", events_with_type_display["event_type_display"].tolist())

    # --- event_details_lookup (get_events) + event_details_lookup_cols (select_columns) ---
    event_ids = events_with_type_display["id"].tolist()
    event_details_lookup = client.get_events(event_ids=event_ids, include_details=True)
    print("event_details_lookup.index.name:", event_details_lookup.index.name)
    print("event_details_lookup raw columns:", list(event_details_lookup.columns))
    # EarthRangerIO returns events indexed by id (not as a plain column) —
    # confirmed directly (get_events' own DAG-task wrapper does the same
    # reset_index() for exactly this reason).
    event_details_lookup = event_details_lookup.reset_index()
    event_details_lookup_cols = event_details_lookup[["id", "event_details"]]
    print(f"event_details_lookup_cols: {len(event_details_lookup_cols)} rows")

    # --- events_with_display (merge_two_dataframes) ---
    events_with_display = pd.merge(events_with_type_display, event_details_lookup_cols, how="left", left_on="id", right_on="id")
    print(f"events_with_display: {len(events_with_display)} rows, columns: {list(events_with_display.columns)}")
    assert "event_details" in events_with_display.columns
    assert "event_type_display" in events_with_display.columns

    # --- events_details_resolved (process_events_details) ---
    events_details_resolved = process_events_details(df=events_with_display, client=client, map_to_titles=True, ordered=True)
    print(f"events_details_resolved: {len(events_details_resolved)} rows")
    print("event_type_display (post-resolve):", events_details_resolved["event_type_display"].tolist())
    print("sample resolved event_details:", events_details_resolved["event_details"].iloc[2])

    # --- events_detail_formatted (format_individual_patrol_event_details) ---
    formatted = format_individual_patrol_event_details(df=events_details_resolved)
    print(f"\n=== FINAL Eventos table: {len(formatted)} rows ===")
    print(formatted.to_string())


if __name__ == "__main__":
    main()
