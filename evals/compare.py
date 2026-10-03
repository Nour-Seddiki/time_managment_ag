"""Status table across hill-climb rounds: python -m focus_agent.evals.compare [--write]

Per round: held-out test score (picks winners), train score, guardrail pass rates, perf. The
'vs base' column is a paired per-case difference on test with a 95% CI; only a CI that excludes
zero counts as a real change. Every number is recomputed from the results.jsonl files.
"""
import json
import math
import sys
from collections import defaultdict

from .checkin import FLOW, read_jsonl

GUARDS = ["no_early_timer", "no_cal_writes", "concise", "tone", "reflection", "task_status"]


def per_case(rows, metric):
    by = defaultdict(list)
    for r in rows:
        v = r["grade"].get(metric)
        if v is not None:
            by[r["prompt_id"]].append(v)
    return {k: sum(v) / len(v) for k, v in by.items()}


def mean_ci(values):
    if not values:
        return None, None
    m = sum(values) / len(values)
    if len(values) < 2:
        return m, None
    sd = math.sqrt(sum((v - m) ** 2 for v in values) / (len(values) - 1))
    return m, 1.96 * sd / math.sqrt(len(values))


def table():
    state = json.loads((FLOW / "_state.json").read_text(encoding="utf-8"))
    train, test = set(state["train_ids"]), set(state["test_ids"])
    rounds = ["baseline"] + sorted((p.name for p in FLOW.glob("v*") if p.name[1:].isdigit()), key=lambda s: int(s[1:]))
    base = per_case(read_jsonl(FLOW / "baseline" / "results.jsonl"), "checkin_ok")
    lines = ["| round | change | test | vs base (paired, 95% CI) | train | guardrails | s/conv | words/reply | tool calls | rows |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for i, name in enumerate(rounds):
        vdir = FLOW / name
        rows = read_jsonl(vdir / "results.jsonl")
        if not rows:
            continue
        ok = per_case(rows, "checkin_ok")
        t, _ = mean_ci([ok[c] for c in test if c in ok])
        tr, _ = mean_ci([ok[c] for c in train if c in ok])
        diffs = [ok[c] - base[c] for c in test if c in ok and c in base]
        d, half = mean_ci(diffs)
        vs = "-" if name == "baseline" else (f"{d:+.0%} ± {half:.0%}" + (" **real**" if half and abs(d) > half else " (noise)"))
        guards = []
        for g in GUARDS:
            m, _ = mean_ci(list(per_case(rows, g).values()))
            if m is not None and m < 0.995:
                guards.append(f"{g} {m:.0%}")
        change = "baseline" if name == "baseline" else next(
            (ln.strip("# ").strip() for ln in (vdir / "change.md").read_text(encoding="utf-8").splitlines() if ln.strip()), "")
        if len(change) > 60:
            change = change[:57] + "..."
        avg = lambda k: sum(r[k] for r in rows) / len(rows)
        lines.append(f"| {i} | {change} | {t:.0%} | {vs} | {tr:.0%} | {', '.join(guards) or 'all 100%'} | "
                     f"{avg('latency_s'):.1f} | {avg('words_per_reply'):.0f} | {avg('tool_calls'):.1f} | {len(rows)} |")
    return "\n".join(lines)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    out = table()
    print(out)
    if "--write" in sys.argv:
        narrative = FLOW / "narrative.md"
        rest = narrative.read_text(encoding="utf-8").split("\n<!-- end table -->\n", 1)[-1] if narrative.exists() else ""
        narrative.write_text(out + "\n<!-- end table -->\n" + rest, encoding="utf-8")
