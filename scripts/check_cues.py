#!/usr/bin/env python3
"""Audit phrase-cued visual events against measured narration durations.

Input JSON:
{
  "lines": [
    {"id": "n26", "say": "...", "duration": 13.35}
  ],
  "cues": [
    {"id": "n26", "phrase": "mean Attack Success Rate", "lead": 0.5}
  ]
}
"""

import argparse
import json
import sys


def cue_time(text, duration, phrase, lead):
    index = text.casefold().find(phrase.casefold())
    if index < 0:
        return None
    return max(0.0, index / max(1, len(text)) * duration - lead)


def main():
    parser = argparse.ArgumentParser(
        description="Estimate and validate narration phrase cue times.")
    parser.add_argument("input", help="JSON file containing lines and cues")
    parser.add_argument(
        "--json", action="store_true", help="Print machine-readable output")
    args = parser.parse_args()

    with open(args.input, encoding="utf-8") as handle:
        data = json.load(handle)

    lines = {item["id"]: item for item in data.get("lines", [])}
    results = []
    last_by_line = {}
    failed = False

    for cue in data.get("cues", []):
        line_id = cue["id"]
        line = lines.get(line_id)
        result = {
            "id": line_id,
            "phrase": cue["phrase"],
            "ok": False,
        }

        if not line:
            result["error"] = "missing line"
            failed = True
        else:
            duration = float(line["duration"])
            lead = float(cue.get("lead", 0.5))
            seconds = cue_time(
                line["say"], duration, cue["phrase"], lead)
            if seconds is None:
                result["error"] = "phrase not found"
                failed = True
            elif seconds >= duration:
                result["error"] = "cue falls outside narration"
                result["seconds"] = round(seconds, 3)
                failed = True
            elif seconds < last_by_line.get(line_id, -1):
                result["error"] = "cue is out of order"
                result["seconds"] = round(seconds, 3)
                failed = True
            else:
                result["ok"] = True
                result["seconds"] = round(seconds, 3)
                last_by_line[line_id] = seconds

        results.append(result)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for result in results:
            if result["ok"]:
                print(
                    f'{result["id"]} {result["seconds"]:6.2f}s  '
                    f'{result["phrase"]}')
            else:
                print(
                    f'ERROR {result["id"]}: {result.get("error")} - '
                    f'{result["phrase"]}',
                    file=sys.stderr,
                )

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

