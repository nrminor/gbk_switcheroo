#!/usr/bin/env python3


import sys
import argparse
from typing import Tuple
from result import Result, Ok, Err  # type: ignore
import polars as pl


def parse_command_line_args() -> Result[Tuple[str, int, int, str, str], str]:
    """
    Parses command line arguments.

    Returns:
        Result[Tuple, str]: Returns Ok(Tuple) if args could
        be parsed, else returns Err(str).
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--key_file",
        "-f",
        type=str,
        required=True,
        help="Path to a tab-delimited key file.",
    )
    parser.add_argument(
        "--key_col",
        "-k",
        type=int,
        default=0,
        help="The (zero-based) column index with information that you'd like to replace.",
    )
    parser.add_argument(
        "--val_col",
        "-v",
        type=int,
        default=1,
        help="The (zero-based) column index with information that you'd like to replace with.",
    )
    parser.add_argument(
        "--feature",
        "-q",
        type=str,
        required=True,
        help="The Genbank feature to search for when updating the file (e.g., 'ACESSION').",
    )
    parser.add_argument(
        "--gbk_file",
        "-g",
        type=str,
        required=True,
        help="Path to the genbank file to query.",
    )
    args = parser.parse_args()

    return Ok((args.key_file, args.key_col, args.val_col, args.feature, args.gbk_file))


def gbk_switcheroo(gbk_file: str, key_dict: dict, feature: str) -> Result[None, str]:
    """
        Function `gbk_switcheroo()` goes through each line in the input, finds the
        feature that should be replaced, replaces it, and then writes it to a new
        output Genbank file. Minimal parsing is performed.

    args:
        - `gbk_file: str`: A string specifying the path to the genbank file.
        - `key_dict: dict`: A dictionary of the old strings and the new strings
        you intend to replace them with.
        - `feature: str`: A string specifying the feature to replace, e.g.,
        "ACCESSION"
    """
    with open(gbk_file, "r", encoding="utf-8") as input, open(
        "replacement.gbk", "w", encoding="utf-8"
    ) as output:
        for line in input:
            if not line.startswith(feature):
                output.write(line)
                continue
            elements = line.split()
            replacement = key_dict.get(elements[1])
            output.write(f"{elements[0]}   {replacement}")

    return Ok(None)


def main() -> None:
    """
    Main coordinates the flow of data through the above-defined functions.
    """

    # parse command line arguments while handling any errors
    args_result = parse_command_line_args()
    if isinstance(args_result, Err):
        sys.exit(
            f"Command line parsing encountered an error:\n{args_result.unwrap_err()}"
        )
    key_file, key_col, val_col, feature, gbk_file = args_result.unwrap()

    # read the key file
    key_dicts = (
        pl.read_csv(key_file, separator="\t", has_header=True)
        .select([key_col, val_col])
        .to_dicts()
    )

    # create dictionary of query and replacement strings
    key_dict = {old_string: replacement for old_string, replacement in key_dicts}

    # feed the key dictionary into a function that will read, modify, and write
    # the new genbank file
    gbk_result = gbk_switcheroo(gbk_file, key_dict, feature)
    if isinstance(gbk_result, Err):
        sys.exit(
            f"Genbank file could not be properly updated:\n{gbk_result.unwrap_err()}"
        )


if __name__ == "__main__":
    main()
