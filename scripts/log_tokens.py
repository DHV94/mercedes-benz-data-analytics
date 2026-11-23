"""Claude Code "Stop" hook: appends the token usage of the last turn to logs/token_log.csv.

Claude Code passes a JSON on stdin with `transcript_path` and `session_id`.
The transcript (JSONL) repeats the same API message once per content block,
so usage is de-duplicated by message id. The last cumulative totals per
session are kept in logs/.token_state.json (ignored by git) so each CSV row
only holds the tokens spent since the previous row.
"""
import csv
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "logs" / "token_log.csv"
STATE_PATH = ROOT / "logs" / ".token_state.json"
FIELDS = ["date", "time", "session_id", "model", "input_tokens",
          "cache_write_tokens", "cache_read_tokens", "output_tokens"]
KEYS = ["input_tokens", "cache_creation_input_tokens",
        "cache_read_input_tokens", "output_tokens"]


def read_totals(transcript):
    """Return ({key: total}, last_model) for a transcript, de-duplicated by message id."""
    by_id = {}
    model = ""
    with open(transcript, encoding="utf-8") as fh:
        for line in fh:
            try:
                d = json.loads(line)
            except ValueError:
                continue
            msg = d.get("message") or {}
            usage = msg.get("usage")
            if d.get("type") != "assistant" or not usage:
                continue
            by_id[msg.get("id") or d.get("uuid")] = usage
            model = msg.get("model") or model
    totals = {k: sum(u.get(k, 0) or 0 for u in by_id.values()) for k in KEYS}
    return totals, model


def main():
    try:
        payload = json.load(sys.stdin)
        transcript = payload["transcript_path"]
        session = payload.get("session_id", "unknown")
        totals, model = read_totals(transcript)
    except Exception as exc:  # never break the Claude session
        print(f"log_tokens: skipped ({exc})", file=sys.stderr)
        return 0

    try:
        state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        state = {}
    prev = state.get(session, {k: 0 for k in KEYS})
    delta = {k: totals[k] - prev.get(k, 0) for k in KEYS}
    if not any(delta.values()):
        return 0

    CSV_PATH.parent.mkdir(exist_ok=True)
    new_file = not CSV_PATH.exists()
    now = datetime.now()
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        if new_file:
            writer.writerow(FIELDS)
        writer.writerow([now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"), session, model,
                         delta["input_tokens"], delta["cache_creation_input_tokens"],
                         delta["cache_read_input_tokens"], delta["output_tokens"]])
    state[session] = totals
    STATE_PATH.write_text(json.dumps(state), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
