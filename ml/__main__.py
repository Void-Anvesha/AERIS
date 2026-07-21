from ml.inspect_data import main as inspect_main
from ml.merge_datasets import main as merge_main
from ml.train import main as train_main
from ml.predict import main as predict_main

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] in {"inspect_data", "inspect"}:
        inspect_main()
    elif len(sys.argv) > 1 and sys.argv[1] in {"merge_datasets", "merge"}:
        merge_main()
    elif len(sys.argv) > 1 and sys.argv[1] in {"train"}:
        train_main()
    elif len(sys.argv) > 1 and sys.argv[1] in {"predict"}:
        predict_main()
    else:
        print("Usage: python -m ml inspect_data|merge_datasets|train|predict")
