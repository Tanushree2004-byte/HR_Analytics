"""Run full data pipeline: cleaning → EDA → ML training."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.data_processing.clean_data import run_cleaning_pipeline
from src.data_processing.eda import run_eda
from src.ml.train import run_training


def main():
    print("=" * 60)
    print("HR Intelligence Platform — Data Pipeline")
    print("=" * 60)
    run_cleaning_pipeline()
    print()
    run_eda()
    print()
    run_training()
    print()
    print("Pipeline completed successfully.")


if __name__ == "__main__":
    main()
