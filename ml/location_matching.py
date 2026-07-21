from __future__ import annotations

from typing import Any
import pandas as pd
from rapidfuzz import fuzz

ALIASES = {
    "bengaluru": "bangalore",
    "bombay": "mumbai",
    "madras": "chennai",
    "gurgaon": "gurugram",
}


def normalize_location(value: Any) -> str:
    text = str(value or "").strip().lower()
    return "".join(ch for ch in text if ch.isalnum())


def _canonical_location(value: Any) -> str:
    return ALIASES.get(normalize_location(value), normalize_location(value))


def match_locations(source_locations: list[str], target_locations: list[str]) -> list[dict[str, Any]]:
    matches = []
    normalized_targets = [normalize_location(item) for item in target_locations]
    for item in source_locations:
        normalized_source = normalize_location(item)
        if normalized_source in normalized_targets:
            match = target_locations[normalized_targets.index(normalized_source)]
        else:
            canonical_source = _canonical_location(item)
            best_score = 0
            best_match = None
            for candidate in target_locations:
                score = fuzz.ratio(canonical_source, _canonical_location(candidate))
                if score > best_score and score >= 85:
                    best_score = score
                    best_match = candidate
            match = best_match or item
        matches.append({"source": item, "match": match})
    return matches
