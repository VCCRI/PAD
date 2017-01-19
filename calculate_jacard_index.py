import os
import itertools
import math

from multiprocessing import Pool
from pybedtools import BedTool as bt


def calculate_jaccard_pairs(base_dir):
    cutoff_folders = [d for d in os.listdir(base_dir) if (not d.startswith(".") and
                                                          os.path.isdir(os.path.join(base_dir, d)))]

    all_jaccard_pair_index = []
    for cutoff_folder in cutoff_folders:
        print("processing", cutoff_folder)
        cutoff_folder_path = os.path.join(base_dir, cutoff_folder)
        bed_files = [f for f in os.listdir(cutoff_folder_path) if ".bed." in f]
        distal_bed_files = [os.path.join(cutoff_folder_path, b) for b in bed_files if "_distal_" in b]
        proximal_bed_files = [os.path.join(cutoff_folder_path, b) for b in bed_files if "_proximal_" in b]

        all_pairs = list(itertools.combinations(distal_bed_files, 2)) + \
                    list(itertools.combinations(proximal_bed_files, 2))

        pool = Pool()
        result_pool = pool.map_async(calculate_jaccard_index, all_pairs)
        result_pool.wait()
        results = result_pool.get()
        pool.close()

        all_jaccard_pair_index.extend(results)

    return all_jaccard_pair_index


def calculate_jaccard_index(file_paths):
    file_one, file_two = sorted(file_paths)
    bed_file_one = bt(file_one)
    bed_file_two = bt(file_two)
    jaccard = bed_file_one.jaccard(bed_file_two)
    jaccard_index = jaccard['jaccard']
    if math.isnan(jaccard_index):
        jaccard_index = -1 # Jaccard index values range between 0 and 1 (inclusive), so NaN will be represented by -1

    proxdis = file_one.split("_")[-2]
    cutoff = file_one.split("_")[-1]

    return file_one.split("/")[-1], file_two.split("/")[-1], proxdis, cutoff, str(jaccard_index)

if __name__ == "__main__":
    base_dir = "test"
    all_jaccard_pairs = calculate_jaccard_pairs(base_dir)
    with open("all_jaccard_pairs.csv", "w") as f:
        f.write("file_one,file_two,proxdis,cutoff,jaccard_index\n")
        f.write("\n".join([",".join(p) for p in all_jaccard_pairs]))
