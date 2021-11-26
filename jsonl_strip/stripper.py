import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Union

from tqdm.auto import tqdm

path_like = Union[Path, str]
json_dict = Dict[str, Any]

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument(
    "-i", "--input", help="The .jsonl file to clean", type=str, required=True
)
parser.add_argument(
    "-o", "--output", help="The output .jsonl file", type=str, required=True
)
parser.add_argument(
    "-k",
    "--keys",
    help="The keys to remove from the file",
    nargs="+",
    default=["unigramCount", "bigramCount", "trigramCount"],
    type=str,
    required=False,
)


def get_number_of_records(jsonl_file: path_like):
    with open(jsonl_file, "r") as jsonl_file:
        count = sum(1 for _ in jsonl_file)
    return count


def read_jsonl(json_file: path_like):
    with open(json_file, "r") as json_file:
        for line in json_file.readlines():
            yield json.loads(line)


def remove_keys(json_dict: json_dict, key_blacklist: List[str]):
    return {key: val for key, val in json_dict.items() if key not in key_blacklist}


def append_to_jsonl(json_dict: json_dict, json_file: path_like):
    with open(json_file, "a") as json_file:
        json_file.write(json.dumps(json_dict) + "\n")


def strip_keys(jsonl_in: path_like, jsonl_out: path_like, key_blacklist: List[str]):
    print(f"Removing the following keys: {key_blacklist}")
    print(f"Reading data from {jsonl_in}")
    print(f"Saving output to {jsonl_out}")
    ask_append_replace(Path(jsonl_out))
    total_lines = get_number_of_records(jsonl_in)
    for line in tqdm(read_jsonl(jsonl_in), desc="Removing keys", total=total_lines):
        json_cleaned = remove_keys(line, key_blacklist=key_blacklist)
        append_to_jsonl(json_cleaned, jsonl_out)
    print(f"Done.")


def ask_append_replace(jsonl_out: Path):
    if jsonl_out.exists():
        ask = f"Output file {jsonl_out} already exists, replace (r), append (a) or cancel (c)?: "
        response = input(ask)
        while response.lower() not in ["r", "a", "c"]:
            response = input(ask)
        if response.lower() == "r":
            print(f"Replacing output file {jsonl_out}")
            jsonl_out.unlink()
        elif response.lower() == "a":
            print(f"Appending to output file {jsonl_out}")
        elif response.lower() == "c":
            print("Cleaning cancelled, exiting.")
            sys.exit()


if __name__ == "__main__":

    args = parser.parse_args()

    strip_keys(jsonl_in=args.input, jsonl_out=args.output, key_blacklist=args.keys)
