import argparse
from multiprocessing import Pool

import numpy
from pybedtools import BedTool as bt
import pybedtools
import pickle
import os

global file1, file2, genome_chrom_sizes


class Histogram:
    steps = 0
    counts = []
    count_sum = 0
    precision = 0

    def __init__(self, step, count):
        self.steps = step
        self.counts = count
        self.count_sum = sum(count)
        self.precision = len(str(step).split(".")[-1])

    def get_pvalue(self, value):
        rounded_value = round(value, self.precision)
        cdf_value = sum(self.counts[:int(rounded_value/self.steps)])
        return 1-(cdf_value/self.count_sum)


# Calculate jaccard index of all randoms in shuffledFile
def bootstrapRandom(num):
    #print(num)
    global file1, file2, genome_chrom_sizes
    shuffled_file1 = file1.shuffle(g=genome_chrom_sizes, chrom=True)
    shuffled_file2 = file2.shuffle(g=genome_chrom_sizes, chrom=True)
    f1_sorted = shuffled_file1.sort()
    f2_sorted = shuffled_file2.sort()
    shuffled_result = f1_sorted.jaccard(f2_sorted)

    pybedtools.cleanup()
    return shuffled_result['jaccard']


def createJaccardDistribution(file_name1, file_name2, genome_chrom_size, bootstrap_num=10000, process_num=4):
    print(file_name1, file_name2)
    #print(genome_chrom_size)

    global file1, file2, genome_chrom_sizes
    # Create shuffled BED files of file1 and file2
    file1 = bt(file_name1)
    file2 = bt(file_name2)
    genome_chrom_sizes = genome_chrom_size

    # set multiprocessing
    pool = Pool(processes=process_num)
    bootstrapped_jaccard = pool.map(bootstrapRandom, range(bootstrap_num))  # returns list of jaccard indices
    pool.close()
    pool.join()

    #step = 0.001
    #precision = 3
    #jaccard_count = [0 for i in range(int(1/step))]
    #print(bootstrapped_jaccard)
    #print(max(bootstrapped_jaccard))
    #for jaccard_value in bootstrapped_jaccard:
    #    rounded_value = round(jaccard_value, precision)
    #    jaccard_count[int(rounded_value/step)] += 1

    #jaccard_distribution = Histogram(step, jaccard_count)

    return numpy.sort(bootstrapped_jaccard)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find two largest BED file')
    parser.add_argument('--file1', '-f1', action="store", dest="file_1", help="Path to file 1")
    parser.add_argument('--file2', '-f2', action="store", dest="file_2", help="Path to file 2")
    parser.add_argument('--chromfile', '-c', action="store", dest="chrom_file", help="Path to chromosome sizes file")
    parser.add_argument('--output', '-o', action="store", dest="pickle_output", help="Output name for pickle file")
    parser.add_argument('--bootstrap', '-b', action="store", dest="bootstrap_num", help="Path to chromosome sizes file",
                        type=int, nargs='?', default=10000)
    parser_result = parser.parse_args()

    jaccard_distribution = createJaccardDistribution(parser_result.file_1, parser_result.file_2,
                                                     parser_result.chrom_file, parser_result.bootstrap_num)

    print(jaccard_distribution)
    output = open(parser_result.pickle_output, 'wb')
    pickle.dump(jaccard_distribution, output)
    output.close()
