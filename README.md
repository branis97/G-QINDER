# G-QINDER
[![Build](https://github.com/branis97/G-QINDER/actions/workflows/build.yml/badge.svg)](https://github.com/branis97/G-QINDER/actions/workflows/build.yml)

Next generation G-quadruplex finder

## Usage
Executables are available as artifacts of release on GitHub.

G-QINDER is CLI tool which is accepting FASTA file and multiple parameters.

### Parameters

- `-h` (help) lists all available parameters and their order 
- `-i` (input) .FASTA file for reading 
- `-o` (output) destination folder for saving results 
- `-w` (window) reading window size 
- `-s/x` (scale/negative includes) G-score value (the minimum value to display, i.e. for example 2 and above, the system will generate a text file with the results. If the parameter `-x` is used instead of `-s`, negative scores (C-rich areas) will be taken into account, i.e. 2 and above and at the same time (-2) and below - the system will generate 2 separate text files with the results `-f` (offset) `-a` (angle)

To run this project for the first time you can use included test sequence in this repo.

Example how to run G-QINDER (Mac):

`./qinder -i ./test_sequences/Thermus_thermophilus_DNA.fasta -o ./ -w 25 -s 1.2 -f 25 -a 15`

## Development

G-QINDER welcomes contributions from the community.

### Requirements

- Python 3.9
- biopython 1.7

### Launch

`main.py -i ./test_sequences/Thermus_thermophilus_DNA.fasta -o ./ -w 25 -s 1.2 -f 25 -a 15`

