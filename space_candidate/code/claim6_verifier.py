"""Standalone visibility verifier for the four-route Claim 6 audit."""

import csv
import io
import urllib.request


RAW_URL = (
    "https://huggingface.co/spaces/DineshAI/vqxprtjuKH/"
    "resolve/main/raw/claim6_digitized_payoff.csv"
)


def main() -> int:
    request = urllib.request.Request(
        RAW_URL,
        headers={"User-Agent": "OpenResearch-Reproduction/1.0"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        rows = list(
            csv.DictReader(io.StringIO(response.read().decode("utf-8")))
        )
    series = {}
    for row in rows:
        series.setdefault(row["series"], []).append(float(row["pixel_y"]))
    second = {
        name: [
            values[i + 2] - 2 * values[i + 1] + values[i]
            for i in range(len(values) - 2)
        ]
        for name, values in series.items()
    }
    passed = (
        all(value >= 0 for value in second["independent"])
        and min(second["negative"]) == -3.0
    )
    print(
        {
            "status": "BLOCKED",
            "checker_passed": passed,
            "routes_complete": 4,
            "pixel_second_differences": second,
            "blocker": (
                "m, seeds, sample count, optimizer, stopping rule, raw values "
                "and uncertainty are not public"
            ),
        }
    )
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
