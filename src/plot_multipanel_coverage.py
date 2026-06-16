#!/usr/bin/env python3

# PART 3: PLOT COVERAGE FOR ALL SAMPLES
# plot_multipanel_coverage.py plots coverage for all samples in the project directory onto a single
# figure and saves that figure as PNG file.


# load required modules
import os
import math
import re
import datetime
import pandas as pd
from matplotlib.pyplot import subplots, show, savefig


print('Usage: python plot_multipanel_coverage.py\n') 

# get path to current working directory
dir_path = os.getcwd()

# visualise coverage for every file:

# estimate number of samples
sample_dirs = []

# find sample directories
for subdir in os.listdir(dir_path):
    if re.search(r"\.", subdir) or re.search(r"MyInitDir", subdir):
        continue
    else:
        print(f"Found sample directory: {subdir}")
        sample_dirs.append(subdir)


# estimate number of samples
n_samples = len(sample_dirs)

# define number of columns and rows
n_cols = 3
n_rows = math.ceil(n_samples / n_cols)

fig, axes = subplots(
    nrows=n_rows,
    ncols=n_cols,
    figsize=(17, 5 * n_rows) # scale height with number of rows
) # sharex=True, sharey=True

# flatten axes for easy indexing 
axes = axes.flatten()


# -----------------------------------

# interate over all samples
for idx, sample in enumerate(sample_dirs):
    file_path = os.path.join(dir_path, sample)
    sample_name = sample
    for file in os.listdir(file_path):
        if re.search(sample_name, file) and re.search(r"bwa_mapped_coverage_data_only.txt", file):
            cov_df = pd.read_csv(os.path.join(file_path, file), sep=r"\s+", header=None)


            ax = axes[idx]
            ax.plot(cov_df.iloc[:, 0], cov_df.iloc[:, 1], color="#9C0765")
            ax.set_yscale("log")
            ax.set_ylim(ymax=1e5)
            ax.tick_params(axis="both", labelsize=14)
            ax.set_xlabel("Genomic position", fontsize=16)
            ax.set_ylabel("Coverage", fontsize=16)
            ax.set_title(f"Coverage plot for {sample_name}", fontsize=18);
        


# hide any unused axes (if last row isn't full)
for j in range(n_samples, len(axes)):
    axes[j].set_visible(False)
    
fig.tight_layout()


# specify current date
c_date = datetime.datetime.now()

# export plot to PNG file
output_file = f"{c_date.strftime('%Y%m%d')}_bwa_remapped_coverage_multipanel.png"
fig.savefig(os.path.join(dir_path, output_file), bbox_inches="tight")

# confirm generation of plot
print(f"\nMultipanel coverage plot saved as {output_file} in {dir_path}")
