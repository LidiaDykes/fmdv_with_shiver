#!/usr/bin/env python3

# fix_fqs_templ.py will modify the fastq_screen.conf.template, 
# based on  contaminant / host species names and accession numbers 
# listed in the supplied csv file. 

# load required modules
import os
import re
import sys

# fetch absolute path of the script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# fastq_screen.conf.template file to be used as template
template_file =  "fastq_screen.conf.template"

# updated fastq_screen.conf.template file
new_template = "fastq_screen.conf.template.new"

# provide the csv file with the list of contaminants / host species and their accession numbers as an argument
# when running the script
contaminants_file = sys.argv[1]

# check if all arguments were provided:
if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} contaminants_file.csv")
    sys.exit(1)

with open(os.path.join(SCRIPT_DIR, new_template), 'w') as output:

    # obtain reusable part of a FastQ Screen configuration file template
    with open(os.path.join(SCRIPT_DIR, template_file), 'r') as input_template:
        for line in input_template.readlines():
            output.write(line)
            if re.search('DATABASE', line) and re.search('rRNA', line):
                break

    # read the contaminants list and add the relevant lines to the new template
    with open(contaminants_file, 'r') as cont_list:
        for line in cont_list.readlines():
            # skip empty lines
            if len(line.strip()) == 0 :
                continue
            line = line.rstrip()
            species = line.split(',')[0]
            accession = line.split(',')[1]
            output.write(f'##\n')
            output.write(f'## {species}\n')
            output.write(f'DATABASE\t{species}\t__DATA_DIR__/FastQ_Screen_Genomes/{species}/{species}_{accession}_genome\n')
        output.write(f'##')
