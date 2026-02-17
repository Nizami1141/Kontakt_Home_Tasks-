import argparse
import json
import os

from tqdm import tqdm

from src.core.evaluator import Evaluator, EvaluatorConfig, configure_logging


def main():
    parser = argparse.ArgumentParser(description="Run QA evaluation on a transcript dataset")
    parser.add_argument(
        "--dataset",
        default=os.getenv("DATASET_PATH", "Task_1_Eval_dataset.json"),
        help="Path to evaluation dataset JSON",
    )
    parser.add_argument(
        "--criteria",
        default=os.getenv("CRITERIA_PATH"),
        help="Path to criteria file (txt/yaml). Optional if provided per item in JSON.",
    )
    parser.add_argument(
        "--out",
        default=os.getenv("OUTPUT_PATH", "evaluation_results.json"),
        help="Where to write output JSON",
    )
    parser.add_argument("--no-llm", action="store_true", help="Run rule-only mode")
    parser.add_argument(
        "--log-level",
        default=os.getenv("LOG_LEVEL", "INFO"),
        help="Logging level (DEBUG, INFO, WARNING, ERROR)",
    )
    args = parser.parse_args()

    configure_logging(args.log_level)

    if not os.path.exists(args.dataset):
        raise FileNotFoundError(f"Dataset not found: {args.dataset}")

    with open(args.dataset, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    evaluator = Evaluator(EvaluatorConfig(criteria_path=args.criteria, use_llm=not args.no_llm))

    results = {}
    for item in tqdm(dataset):
        call_input = item.get("input", item)  # supports both formats
        out = evaluator.evaluate_json(call_input)
        results.update(out)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"Done. Saved: {args.out}")


if __name__ == "__main__":
    main()
