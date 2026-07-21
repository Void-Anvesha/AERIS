from __future__ import annotations

import pandas as pd
from ml.train import run_training
from ml.utils import save_json
from ml.config import REPORTS_DIR


def evaluate_models() -> dict[str, object]:
    training_result = run_training(demo_mode=True)
    save_json(REPORTS_DIR / "metrics.json", training_result)
    return training_result


if __name__ == "__main__":
    evaluate_models()
