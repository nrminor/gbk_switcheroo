# Genbank File Data Switch-a-roo
[![Open Source Starter Files](https://github.com/nrminor/gbk_switcheroo/actions/workflows/open-source-starter.yaml/badge.svg)](https://github.com/nrminor/gbk_switcheroo/actions/workflows/open-source-starter.yaml)

Bespoke Python script for slotting information into an Genbank file (for submission to IPD or wherever else)

## Overview
This simple Python module finds lines with features you'd like to replace with new information and (you guessed it) replaces them. It uses Poetry to manage the project environment, streamline installation, and provide a simpler interface to the module. To set it up, [install Poetry](https://python-poetry.org/), and then:
1. Clone this repository with `git clone https://github.com/nrminor/filter_vcf_and_cadd_scores.git .`
2. Run `poetry install` to make sure all the required Python libraries are present in an isolated environment.
3. Run `poetry shell`
4. Run your replacement with:

```
gbk_switcheroo \
--key_file /path/to/key_file.tsv \
--key_col 1 \
--val_col 2 \
--feature "ACCESSION" \
--gbk_file /path/to/input.gbk
```

The full usage of the module is:

```
usage: gbk_switcheroo [-h] --key_file KEY_FILE [--key_col KEY_COL] [--val_col VAL_COL] --feature FEATURE --gbk_file GBK_FILE

options:
  -h, --help            show this help message and exit
  --key_file KEY_FILE, -f KEY_FILE
                        Path to a tab-delimited key file.
  --key_col KEY_COL, -k KEY_COL
                        The (zero-based) column index with information that you'd like to replace.
  --val_col VAL_COL, -v VAL_COL
                        The (zero-based) column index with information that you'd like to replace with.
  --feature FEATURE, -q FEATURE
                        The Genbank feature to search for when updating the file (e.g., 'ACESSION').
  --gbk_file GBK_FILE, -g GBK_FILE
                        Path to the genbank file to query.
```
