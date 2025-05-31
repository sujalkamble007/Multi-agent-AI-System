import argparse
from agents.classifier_agent import classify_and_route
from memory.memory_store import log_to_memory


def main():
    parser = argparse.ArgumentParser(description="Multi-Agent AI System CLI")
    parser.add_argument("file", type=str, help="Path to input file (.txt, .json, .pdf)")
    parser.add_argument(
        "--thread-id",
        type=str,
        default=None,
        help="Optional thread ID for tracking/log chaining"
    )
    args = parser.parse_args()

    format_, intent, result = classify_and_route(args.file)

    print("\n=== Final Output ===")
    print("Format:", format_)
    print("Intent:", intent)
    print("Agent Result:", result)

    # Log the result to outputs/logs.json with unique and thread IDs
    log_to_memory({
        "source": args.file,
        "format": format_,
        "intent": intent,
        "extracted": result
    }, thread_id=args.thread_id)


if __name__ == "__main__":
    main()
