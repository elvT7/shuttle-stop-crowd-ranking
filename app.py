import gradio as gr

# ── Default dataset ───────────────────────────────────────────────────────────
DEFAULT_STOPS = [
    ["Stauffer Library",        87],
    ["Douglas Library",          34],
    ["Mitchell Hall", 112],
    ["Chernoff Hall",    65],
    ["Bioscience",  143],
    ["Mac-Corry",   29],
    ["Queens General Hospital",     98],
    ["Theological Hall",    51],
    ["Ontario Hall",     76],
    ["Dunning Hall",    19],
]

# ── Emoji for step descriptions ───────────────────────────────────────────────
ACTION_EMOJI = {
    "start":       "🚌",
    "pivot":       "📍",
    "compare":     "🔍",
    "swap":        "🔄",
    "place_pivot": "📌",
    "recurse":     "↩️ ",
    "done":        "✅",
}

# ── Bar chart row tags — plain ASCII so spacing is predictable ────────────────
ROW_TAG = {
    "pivot":   "[PIV]",
    "swap":    "[SWP]",
    "compare": "[CMP]",
    "active":  "[   ]",
    "outside": "     ",
}

MAX_BAR_WIDTH = 30
NAME_COL_W    = 22
COUNT_COL_W   = 6

# ── Validation ────────────────────────────────────────────────────────────────
def parse_table(rows):
    result = []
    errors = []
    raw = rows.values.tolist() if hasattr(rows, "values") else list(rows)

    if not raw:
        return None, ["⚠️ No stops in the table. Add at least one stop."]

    for i, r in enumerate(raw):
        row_num = i + 1
        if not r or all(str(c).strip() == "" for c in r):
            continue
        name_raw = str(r[0]).strip() if len(r) > 0 else ""
        if not name_raw:
            errors.append(f"⚠️ Row {row_num}: missing stop name — row skipped.")
            continue
        if len(r) < 2 or str(r[1]).strip() == "":
            errors.append(f"⚠️ Row {row_num} ({name_raw}): crowd count is empty — row skipped.")
            continue
        try:
            count = int(float(str(r[1]).strip()))
        except (ValueError, TypeError):
            errors.append(f"❌ Row {row_num} ({name_raw}): '{r[1]}' is not a valid number — row skipped.")
            continue
        if count < 0:
            errors.append(f"❌ Row {row_num} ({name_raw}): crowd count cannot be negative ({count}) — row skipped.")
            continue
        result.append([name_raw, count])

    if not result:
        errors.append("❌ No valid stops found. Please fix the data above.")
        return None, errors
    if len(result) == 1:
        errors.append(f"ℹ️ Only 1 stop ({result[0][0]}). Nothing to sort — displaying as-is.")

    return result, errors

# ── Bar chart ─────────────────────────────────────────────────────────────────
def render_bar_chart(arr, pivot_idx=None, compare=None, swap=None, lo=None, hi=None):
    if not arr:
        return "  (no data to display)"
    max_val = max(r[1] for r in arr) if arr else 1
    legend  = "  Tags:  [PIV]=Pivot  [SWP]=Swap  [CMP]=Compare  [   ]=Active subarray"
    header  = "  TAG    " + "Name".ljust(NAME_COL_W) + "Count".rjust(COUNT_COL_W) + "  Bar"
    divider = "  " + "-" * (5 + 2 + NAME_COL_W + COUNT_COL_W + 2 + MAX_BAR_WIDTH)
    lines   = [legend, header, divider]
    for i, (name, count) in enumerate(arr):
        bar_len = max(1, round(count / max_val * MAX_BAR_WIDTH))
        bar = "█" * bar_len
        if i == pivot_idx:
            tag = ROW_TAG["pivot"]
        elif swap and i in swap:
            tag = ROW_TAG["swap"]
        elif compare and i in compare:
            tag = ROW_TAG["compare"]
        elif lo is not None and hi is not None and lo <= i <= hi:
            tag = ROW_TAG["active"]
        else:
            tag = ROW_TAG["outside"]
        name_col  = name[:NAME_COL_W].ljust(NAME_COL_W)
        count_col = str(count).rjust(COUNT_COL_W)
        lines.append(f"  {tag}  {name_col}{count_col}  {bar}")
    return "\n".join(lines)

# ── Step history ──────────────────────────────────────────────────────────────
def format_history(steps, current_idx):
    if not steps:
        return "No steps recorded yet."
    lines = []
    for i, s in enumerate(steps):
        marker = "▶ " if i == current_idx else "  "
        lines.append(f"{marker}Step {i+1:>3}: {s['description']}")
    return "\n".join(lines)

# ── Quick Sort ────────────────────────────────────────────────────────────────
def median_of_three(arr, lo, hi):
    mid = (lo + hi) // 2
    triple = sorted([(arr[lo][1], lo), (arr[mid][1], mid), (arr[hi][1], hi)])
    return triple[1][1]

def record_quicksort(data):
    arr   = [list(row) for row in data]
    steps = []

    def snap(action, description, pivot_idx=None, lo=None, hi=None, compare=None, swap=None):
        emoji = ACTION_EMOJI.get(action, "")
        steps.append({
            "arr": [list(r) for r in arr],
            "action": action,
            "description": f"{emoji}  {description}",
            "pivot_idx": pivot_idx,
            "lo": lo, "hi": hi,
            "compare": compare, "swap": swap,
        })

    def partition(lo, hi):
        pi         = median_of_three(arr, lo, hi)
        pivot_val  = arr[pi][1]
        pivot_name = arr[pi][0]
        arr[pi], arr[hi] = arr[hi], arr[pi]
        snap("pivot", f"Pivot: {pivot_name} (crowd={pivot_val})  |  subarray [{lo}..{hi}]",
             pivot_idx=hi, lo=lo, hi=hi)
        store = lo
        for j in range(lo, hi):
            snap("compare",
                 f"Compare {arr[j][0]} (={arr[j][1]}) vs pivot {pivot_name} (={pivot_val})",
                 pivot_idx=hi, lo=lo, hi=hi, compare=(j, hi))
            if arr[j][1] <= pivot_val:
                if store != j:
                    arr[store], arr[j] = arr[j], arr[store]
                    snap("swap", f"Swap  {arr[j][0]}  <->  {arr[store][0]}",
                         pivot_idx=hi, lo=lo, hi=hi, swap=(store, j))
                store += 1
        arr[store], arr[hi] = arr[hi], arr[store]
        snap("place_pivot", f"Placed pivot {pivot_name} at final position {store}",
             pivot_idx=store, lo=lo, hi=hi, swap=(store, hi))
        return store

    def quicksort(lo, hi):
        if lo < hi:
            p = partition(lo, hi)
            snap("recurse", f"Recurse  left [{lo}..{p-1}]  and  right [{p+1}..{hi}]",
                 pivot_idx=p, lo=lo, hi=hi)
            quicksort(lo, p - 1)
            quicksort(p + 1, hi)

    snap("start", "Initial order — ready to sort by crowd count.")
    if len(arr) > 1:
        quicksort(0, len(arr) - 1)
    snap("done", "Sorting complete!  Stops ranked from least to most crowded.")
    return steps

# ── Gradio UI ─────────────────────────────────────────────────────────────────
with gr.Blocks(title="🚌 Shuttle Stop Crowd Ranker") as demo:

    state_steps   = gr.State([])
    state_idx     = gr.State(0)
    state_playing = gr.State(False)

    gr.Markdown("# 🚌 Shuttle Stop Crowd Ranker")
    gr.Markdown("Quick Sort visualiser — rank stops by crowd size to decide where to send the next shuttle.")

    with gr.Row():
        # ── Left: data editor ────────────────────────────────────────────────
        with gr.Column(scale=1, min_width=300):
            gr.Markdown("### 📋 Stop Data")
            stop_table = gr.Dataframe(
                value=DEFAULT_STOPS,
                headers=["Stop Name", "Crowd Count"],
                datatype=["str", "number"],
                column_count=(2, "fixed"),
                row_count=(6, "fixed"),
                max_height=260,
                interactive=True,
                label=None,
            )
            with gr.Row():
                btn_add    = gr.Button("➕ Add Stop",    variant="secondary", size="sm")
                btn_remove = gr.Button("➖ Remove Last", variant="secondary", size="sm")
                btn_sample = gr.Button("📋 Sample Data", variant="secondary", size="sm")
            btn_run    = gr.Button("▶️ Run Quick Sort", variant="primary")
            status_msg = gr.Textbox(label="📢 Status", interactive=False, lines=3)

        # ── Right: visualisation ──────────────────────────────────────────────
        with gr.Column(scale=2, min_width=500):
            gr.Markdown("### 📊 Visualisation")
            chart_box = gr.Code(
                value=render_bar_chart(DEFAULT_STOPS),
                label="Bar Chart",
                interactive=False,
                lines=len(DEFAULT_STOPS) + 6,
            )
            step_desc = gr.Textbox(
                value="⏳  Press 'Run Quick Sort' to begin.",
                label="Current Step",
                interactive=False,
                lines=2,
            )
            step_label = gr.Markdown("**Step 0 / 0**")

            with gr.Row():
                btn_prev  = gr.Button("⬅️ Prev",      size="sm")
                btn_next  = gr.Button("➡️ Next",      size="sm")
                btn_play  = gr.Button("▶️ Autoplay",  variant="primary",   size="sm")
                btn_pause = gr.Button("⏸️ Pause",     variant="secondary", size="sm")
                btn_reset = gr.Button("🔁 Reset",                          size="sm")

            with gr.Accordion("📜 Full Step History", open=False):
                history_box = gr.Textbox(value="", label=None, interactive=False, lines=14)

    # ── Helper: build display tuple from a step index ─────────────────────────
    def step_to_display(steps, idx):
        if not steps:
            return render_bar_chart(DEFAULT_STOPS), "⏳  No sort run yet.", "**Step 0 / 0**", ""
        idx   = max(0, min(idx, len(steps) - 1))
        s     = steps[idx]
        chart = render_bar_chart(
            s["arr"],
            pivot_idx=s.get("pivot_idx"),
            compare=s.get("compare"),
            swap=s.get("swap"),
            lo=s.get("lo"),
            hi=s.get("hi"),
        )
        return chart, s["description"], f"**Step {idx + 1} / {len(steps)}**", format_history(steps, idx)

    # ── Live chart on table edit ──────────────────────────────────────────────
    def on_table_change(table_data):
        data, _ = parse_table(table_data)
        return render_bar_chart(data if data else [])

    stop_table.change(fn=on_table_change, inputs=[stop_table], outputs=[chart_box])

    # ── Sample data ───────────────────────────────────────────────────────────
    def load_sample():
        return DEFAULT_STOPS, "✅  Sample data loaded."

    btn_sample.click(fn=load_sample, outputs=[stop_table, status_msg])

    # ── Add / Remove ──────────────────────────────────────────────────────────
    def add_stop(table_data):
        rows = table_data.values.tolist() if hasattr(table_data, "values") else list(table_data)
        rows.append(["New Stop", 50])
        return rows

    def remove_stop(table_data):
        rows = table_data.values.tolist() if hasattr(table_data, "values") else list(table_data)
        if len(rows) > 1:
            rows = rows[:-1]
        return rows

    btn_add.click(fn=add_stop,       inputs=[stop_table], outputs=[stop_table])
    btn_remove.click(fn=remove_stop, inputs=[stop_table], outputs=[stop_table])

    # ── Run sort ──────────────────────────────────────────────────────────────
    def run_sort(table_data):
        data, errors = parse_table(table_data)
        status = "\n".join(errors) if errors else "✅  Sort complete."
        if data is None:
            return (render_bar_chart([]),
                    "❌  Fix the errors shown in Status before sorting.",
                    "**Step 0 / 0**", "", [], 0, False, status)
        if len(data) == 1:
            chart = render_bar_chart(data)
            msg   = f"ℹ️  Only 1 stop ({data[0][0]}, crowd={data[0][1]}). Nothing to sort."
            return chart, msg, "**Step 1 / 1**", msg, [], 0, False, status
        steps = record_quicksort(data)
        chart, desc, label, history = step_to_display(steps, 0)
        if not errors:
            status = f"✅  {len(steps)} steps recorded for {len(data)} stops."
        return chart, desc, label, history, steps, 0, False, status

    btn_run.click(
        fn=run_sort,
        inputs=[stop_table],
        outputs=[chart_box, step_desc, step_label, history_box,
                 state_steps, state_idx, state_playing, status_msg],
    )

    # ── Manual navigation ─────────────────────────────────────────────────────
    def go_next(steps, idx):
        if not steps:
            return render_bar_chart(DEFAULT_STOPS), "⚠️  Run Quick Sort first.", "**Step 0 / 0**", "", idx
        new_idx = min(idx + 1, len(steps) - 1)
        return (*step_to_display(steps, new_idx), new_idx)

    def go_prev(steps, idx):
        if not steps:
            return render_bar_chart(DEFAULT_STOPS), "⚠️  Run Quick Sort first.", "**Step 0 / 0**", "", idx
        new_idx = max(idx - 1, 0)
        return (*step_to_display(steps, new_idx), new_idx)

    btn_next.click(fn=go_next, inputs=[state_steps, state_idx],
                   outputs=[chart_box, step_desc, step_label, history_box, state_idx])
    btn_prev.click(fn=go_prev, inputs=[state_steps, state_idx],
                   outputs=[chart_box, step_desc, step_label, history_box, state_idx])

    # ── Reset ─────────────────────────────────────────────────────────────────
    def do_reset(steps):
        return (*step_to_display(steps, 0), 0, False)

    btn_reset.click(fn=do_reset, inputs=[state_steps],
                    outputs=[chart_box, step_desc, step_label, history_box, state_idx, state_playing])

    # ── Autoplay ──────────────────────────────────────────────────────────────
    autoplay_timer = gr.Timer(value=0.3, active=False)

    def start_play(steps, idx):
        return idx, True

    def stop_play(idx):
        return idx, False

    def tick(steps, idx, playing):
        if not playing or not steps:
            return gr.update(), gr.update(), gr.update(), gr.update(), idx, playing
        new_idx = idx + 1
        if new_idx >= len(steps):
            return (*step_to_display(steps, len(steps) - 1), len(steps) - 1, False)
        return (*step_to_display(steps, new_idx), new_idx, True)

    btn_play.click(fn=start_play, inputs=[state_steps, state_idx],
                   outputs=[state_idx, state_playing]).then(
        fn=lambda: gr.Timer(active=True), outputs=[autoplay_timer]
    )
    btn_pause.click(fn=stop_play, inputs=[state_idx],
                    outputs=[state_idx, state_playing]).then(
        fn=lambda: gr.Timer(active=False), outputs=[autoplay_timer]
    )

    autoplay_timer.tick(
        fn=tick,
        inputs=[state_steps, state_idx, state_playing],
        outputs=[chart_box, step_desc, step_label, history_box, state_idx, state_playing],
    )

    def maybe_deactivate(playing):
        return gr.Timer(active=playing)

    state_playing.change(fn=maybe_deactivate, inputs=[state_playing], outputs=[autoplay_timer])

if __name__ == "__main__":
    demo.launch()