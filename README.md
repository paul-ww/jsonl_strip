# JSONL Key Stripper

A small utility to remove specific top-level keys from `.jsonl` files.

## Installation

```
git clone https://github.com/paul-ww/jsonl_strip.git
pip install ./jsonl_strip
```

## Usage

Example usage is provided in the [notebook](example.ipynb).

You can also call the script from the command line:

```
python -m jsonl_strip.stripper -i input_file.jsonl -o output_file.jsonl -k unigramCount bigramCount trigramCount
```
