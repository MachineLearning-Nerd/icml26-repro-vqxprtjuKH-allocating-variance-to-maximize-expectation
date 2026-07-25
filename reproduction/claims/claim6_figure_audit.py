"""Four-route audit of the empirical Figures 1--2 claim."""

from __future__ import annotations

import hashlib
import io
import itertools
import statistics
import tarfile
import urllib.request

import numpy as np
from PIL import Image


SOURCE_URL = "https://export.arxiv.org/e-print/2502.18463"
SOURCE_SHA256 = "459cf66ee46d8c78ca931343dbf1d13729d3e4ce62ab1179c93aa34212b7f2af"
USER_AGENT = "OpenResearch-Reproduction/1.0 (figure-source verifier)"
PAYOFF_X = (172, 389, 607, 824, 1042, 1259, 1477, 1694)


def source_bundle() -> tuple[bytes, list[str]]:
    request = urllib.request.Request(
        SOURCE_URL, headers={"User-Agent": USER_AGENT}
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = response.read()
    digest = hashlib.sha256(payload).hexdigest()
    if digest != SOURCE_SHA256:
        raise AssertionError(f"paper source hash changed: {digest}")
    with tarfile.open(fileobj=io.BytesIO(payload), mode="r:*") as archive:
        members = archive.getnames()
    return payload, members


def member_image(payload: bytes, name: str) -> np.ndarray:
    with tarfile.open(fileobj=io.BytesIO(payload), mode="r:*") as archive:
        handle = archive.extractfile(name)
        if handle is None:
            raise AssertionError(f"missing source image {name}")
        return np.asarray(Image.open(handle).convert("RGB"))


def color_y_at_x(
    image: np.ndarray, color: tuple[int, int, int], x: int
) -> float:
    mask = np.all(image == np.asarray(color, dtype=np.uint8), axis=2)
    ys = np.where(mask[:, x])[0]
    if len(ys) == 0:
        raise AssertionError(f"no exact-color pixels at x={x}, color={color}")
    return float(statistics.median(int(y) for y in ys))


def payoff_curves(payload: bytes) -> dict[str, list[float]]:
    image = member_image(payload, "payoff.png")
    green = [color_y_at_x(image, (42, 160, 43), x) for x in PAYOFF_X]
    # At p=1/8 all three curves coincide and green is drawn last. The orange
    # curve has exact-color vertices for every later p.
    orange = [green[0]] + [
        color_y_at_x(image, (255, 127, 15), x) for x in PAYOFF_X[1:]
    ]
    return {"independent_orange_y": orange, "negative_green_y": green}


def dominant_horizontal_levels(
    image: np.ndarray, color: tuple[int, int, int]
) -> list[dict[str, int]]:
    mask = np.all(image == np.asarray(color, dtype=np.uint8), axis=2)
    counts = np.sum(mask, axis=1)
    return [
        {"pixel_y": int(y), "exact_color_pixel_count": int(count)}
        for y, count in enumerate(counts)
        if count >= 500
    ]


def lemma_b3_grid_audit() -> dict[str, object]:
    def inequality(a: int, b: int, c: int, d: int) -> bool:
        left = (
            3 * max(a, b, c, d)
            + max(a, d)
            + max(b, d)
            + max(c, d)
        )
        right = (
            2 * max(a, b, d)
            + 2 * max(a, c, d)
            + 2 * max(b, c, d)
        )
        return left <= right

    domain = range(-3, 4)
    checked = 0
    passed = True
    for values in itertools.product(domain, repeat=4):
        checked += 1
        passed &= inequality(*values)
    return {
        "passed": passed,
        "finite_sanity_cases": checked,
        "exact_derivation": (
            "Apply max(u,b)+max(u,c)>=max(u,b,c)+u with "
            "u=max(a,d), then repeat with u=max(b,d), max(c,d), and sum."
        ),
        "scope": (
            "This certifies the max inequality used by the independent "
            "concavity proof, not the unspecified correlated simulations."
        ),
    }


def verify_figure_claim() -> dict[str, object]:
    payload, members = source_bundle()
    suffixes = {name.rsplit(".", 1)[-1].lower() for name in members if "." in name}
    scripts = [
        name
        for name in members
        if name.endswith((".py", ".ipynb", ".r", ".R", ".jl"))
    ]
    raw_data = [
        name
        for name in members
        if name.endswith((".csv", ".json", ".npy", ".npz", ".tsv"))
    ]
    missing_parameters = [
        "number of sets m",
        "random seeds",
        "Monte Carlo sample count",
        "optimizer and stopping rule",
        "raw numerical values",
    ]

    curves = payoff_curves(payload)
    orange_second = np.diff(curves["independent_orange_y"], n=2).tolist()
    green_second = np.diff(curves["negative_green_y"], n=2).tolist()
    allocation = member_image(payload, "independent.png")
    uniform_levels = dominant_horizontal_levels(
        allocation, (31, 119, 180)
    )
    concentrated_levels = dominant_horizontal_levels(
        allocation, (227, 119, 193)
    )

    route1 = {
        "route": "source-bundle completeness audit",
        "source_url": SOURCE_URL,
        "source_sha256": SOURCE_SHA256,
        "member_count": len(members),
        "suffixes": sorted(suffixes),
        "simulation_scripts": scripts,
        "raw_data_files": raw_data,
        "missing_parameters": missing_parameters,
        "conclusion": "exact regeneration is under-specified",
        "completed": not scripts and not raw_data,
    }
    route2 = {
        "route": "deterministic pixel extraction from the hashed paper figures",
        "payoff_pixel_y": curves,
        "independent_pixel_second_differences": orange_second,
        "independent_display_concave": all(value >= 0 for value in orange_second),
        "p_0.25_independent_dominant_levels": uniform_levels,
        "p_1.0_independent_dominant_levels": concentrated_levels,
        "displayed_concentration": (
            len(uniform_levels) == 1 and len(concentrated_levels) == 2
        ),
        "completed": True,
    }
    route3 = {
        "route": "independent theorem-proof reconstruction",
        **lemma_b3_grid_audit(),
        "completed": True,
    }
    route4 = {
        "route": "mandatory falsification attempt on displayed correlated concavity",
        "negative_correlation_pixel_second_differences": green_second,
        "candidate_violation_pixels": min(green_second),
        "valid_falsification": False,
        "reason": (
            "The final second difference is -3 pixels, comparable to line "
            "width; without raw values, seeds, or uncertainty it cannot be "
            "promoted to an assumption-satisfying numerical counterexample."
        ),
        "completed": True,
    }
    routes = [route1, route2, route3, route4]
    all_complete = all(bool(route["completed"]) for route in routes)
    return {
        "claim": "Figures 1-2 Monte Carlo illustration",
        "status": "BLOCKED",
        "routes": routes,
        "all_four_routes_complete": all_complete and len(routes) == 4,
        "blocker": (
            "The public paper omits m, seeds, sample count, optimizer, stopping "
            "rule, and raw values, so its exact Monte Carlo experiment cannot "
            "be regenerated or statistically compared."
        ),
        "what_would_unblock": (
            "Authors' simulation code/configuration and raw per-seed outputs, "
            "or a complete statement fixing all omitted parameters."
        ),
    }


def verify_negative_control() -> dict[str, object]:
    artificial_pixel_y = [1000.0, 800.0, 650.0, 530.0, 400.0]
    second = np.diff(artificial_pixel_y, n=2).tolist()
    # Data y increases upward, while pixel y decreases upward. Concavity in
    # data therefore requires non-negative pixel second differences.
    rejected = any(value < 0.0 for value in second)
    return {
        "control": "artificial visibly non-concave pixel series",
        "pixel_y": artificial_pixel_y,
        "second_differences": second,
        "status": "REJECTED_NONCONCAVE_SERIES" if rejected else "UNEXPECTED",
    }
