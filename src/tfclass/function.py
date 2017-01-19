"""
A separate helper functions for tfclass application.
There are 3 helper funcitons.
**checkPeakFile** - to check if the peakfile is correct format or if there are any peak in the file.
**createPeakToBedFile** - to convert a peakfile to a BED file suitable for uses for analysis.
**createUserPeakBed** - to create a BED file from users input file data
"""

from __future__ import division

from .models import Genes_db

from django.conf import settings
from django.db import connection
from multiprocessing import Pool
from pybedtools import BedTool as bt
import numpy as np

import re
import csv
import os
import pickle
import math

global DISTAL_DISTRIBUTION, PROXIMAL_DISTRIBUTION

DISTAL_DISTRIBUTION = pickle.load(open(os.path.join(settings.MEDIA_ROOT, 'background_distribution', 'distal_dist.pickle')))
PROXIMAL_DISTRIBUTION = pickle.load(open(os.path.join(settings.MEDIA_ROOT, 'background_distribution', 'proximal_dist.pickle')))

# check if the Peakfile is correct format or if there are any peaks in the file
def checkPeakFile(peakfile_list):
    for peakfile in peakfile_list:
        peak_dict = {}
        for line in peakfile:
            if re.search('chr[\dA-Z]+', line):
                chromosome = re.search('^chr[\dA-Z]+', line)
                # positions of both start and end of peaks
                pos = re.search('\s+\d+\s+\d+\s*', line)
                # split the start and end into separate variables
                if not chromosome or not pos:
                    # Invalid file format!
                    return False
                start = re.search('^\s\d+\s', pos.group())
                end = re.search('\s\d+\s$', pos.group())
                # remove any whitespaces
                start = re.sub('\s*', '', start.group(0))
                end = re.sub('\s*', '', end.group(0))
                midpoint = int((int(start) + int(end))/2)
                if chromosome.group(0) not in peak_dict.keys():
                    peak_dict[chromosome.group(0)] = []
                peak_dict[chromosome.group(0)].append([int(start), int(end), midpoint])
        if not peak_dict:
            # list is empty i.e. there is no peaks in file
            return False
    return True


# convert a peakfile to a BED file suitable for uses for analysis
# Jacard has specific template for BED file and this function generate this
# Jacard also need chromosome to be sorted
def createPeakToBedFile(peakfile_list, session_id, db_name):
    for peakfile in peakfile_list:
        filename = peakfile.name
        peak_dict = {}
        for line in peakfile:
            if re.search('chr[\dA-Z]+', line):
                chromosome = re.search('^chr[\dA-Z]+', line)
                # positions of both start and end of peaks
                pos = re.search('\s+\d+\s+\d+\s*', line)
                # split the start and end into separate variables
                if not chromosome or not pos:
                    return False
                start = re.search('^\s\d+\s', pos.group())
                end = re.search('\s\d+\s$', pos.group())
                # remove any whitespaces
                start = re.sub('\s*', '', start.group(0))
                end = re.sub('\s*', '', end.group(0))
                midpoint = int( (int(start) + int(end))/2 )
                if chromosome.group(0) not in peak_dict.keys():
                    peak_dict[chromosome.group(0)] = []
                peak_dict[chromosome.group(0)].append([int(start), int(end), midpoint])

        if not peak_dict:
            # list is empty i.e. there is no peaks in file
            return False
        else:
            path = os.path.join(settings.MEDIA_ROOT, 'users_peak_files', session_id, db_name)
            # calculate gene dist and return as a dict
            peak_dict = getGeneDist(peak_dict, db_name)
            # write to a bedfile with gene_dist so that in the future when user dynamically ask for different cutoff, it can use
            # other function to create another file
            # store to the db Peaks_db_file with cutoff as 0 and with given path and then return
            createUserPeakBed(peak_dict, filename, db_name, path)
    return True


# Create a BED file from users input file data
def createUserPeakBed(peak_dict, filename, db_name, path):
    if not os.path.exists(path):
        os.makedirs(path)
    path = os.path.join(path, '')
    # indexes for peaks
    start = 0
    end = 1
    gene_dist = 3
    with open(path + filename, 'w') as tsvfile:
        for chromosome in sorted(peak_dict):
            fieldnames = ['chromosome', 'start', 'end', 'gene_dist']
            writer = csv.DictWriter(tsvfile, fieldnames=fieldnames, delimiter='\t')
            for peak in peak_dict[chromosome]:
                writer.writerow({'chromosome': chromosome, 'start': peak[start], 'end': peak[end], 'gene_dist': peak[gene_dist]})
    tsvfile.close()
    return


# Get the gene distance from peak to closest gene transcription start site
def getGeneDist(peak_dict, db_name):
    chromosome_set = peak_dict.keys()
    # index for peaks_list
    start = 0
    midpoint = 2
    genes_table = Genes_db.objects.filter(gene_db_name=db_name).values('name', 'chromosome', 'tsSite') 
    for chromo in chromosome_set:
        genes_list = genes_table.filter(chromosome=chromo).order_by('tsSite')
        peak_dict[chromo].sort(key=lambda l: l[midpoint]) # sort by midpoint
        peaks_list = peak_dict[chromo]
        geneSearchIndex = 0 # default at start
        glistLength = len(genes_list)
        plistLength = len(peaks_list)
        for peakIndex, peak in enumerate(peaks_list):
            dist_to_prev_gene = 10000000000000
            for geneIndex, gene in enumerate(genes_list[geneSearchIndex:]):
                dist_to_cur_gene = abs(gene['tsSite'] - peak[midpoint])
                if dist_to_prev_gene < dist_to_cur_gene:
                    peak.append(dist_to_prev_gene)
                    if geneIndex > 0:
                        geneSearchIndex = geneIndex - 1
                    else:
                        geneSearchIndex = 0

                    dist_to_prev_gene = 10000000000000
                    break
                else: # dist_to_prev_gene >= dist_to_cur_gene
                    dist_to_prev_gene = dist_to_cur_gene
            # case when there still are peaks but not genes
            if ((geneIndex+geneSearchIndex) == glistLength-1) and (peakIndex < plistLength):
                if len(peak) == 3:
                    if dist_to_prev_gene < dist_to_cur_gene:
                        newdist = dist_to_prev_gene
                    else:
                        newdist = dist_to_cur_gene
                    peak.append(newdist)
            # case for the last peak when it has not found closest yet
            if peakIndex == plistLength-1:
                if len(peak) == 3: # gene_dist is not appended
                    peak.append(dist_to_prev_gene)
        peak_dict[chromo] = peaks_list
        peak_dict[chromo].sort(key=lambda l: l[start])
    return peak_dict


# Calculate the pvalue of jaccard index given empirical distribution
def calculateJaccardPval(jaccard_index, proxdis):
    if proxdis == "proximal":
        count = len(PROXIMAL_DISTRIBUTION[np.where(PROXIMAL_DISTRIBUTION >= jaccard_index)]) * 1.0
        pval = count/len(PROXIMAL_DISTRIBUTION)
    elif proxdis == "distal":
        count = len(DISTAL_DISTRIBUTION[np.where(DISTAL_DISTRIBUTION >= jaccard_index)]) * 1.0
        pval = count/len(DISTAL_DISTRIBUTION)
    else:
        pval = 0

    return pval

def calculateJaccardFC(jaccard_index, proxdis):
    if proxdis == "proximal":
        fc = jaccard_index/np.median(PROXIMAL_DISTRIBUTION)
    elif proxdis == "distal":
        fc = jaccard_index/np.median(DISTAL_DISTRIBUTION)

    return math.log10(fc+0.1)


# Calculate jaccard index of all randoms in shuffledFile
def bootstrapRandom(file_pair):
    f1, f2 = file_pair
    f1_sorted = f1.sort()
    f2_sorted = f2.sort()
    shuffled_result = f1_sorted.jaccard(f2_sorted)
    return shuffled_result


def createJaccardDistribution(file_name1, file_name2, gene_database_name):
    path = os.path.join(settings.MEDIA_ROOT, 'peak_file_db', str(gene_database_name))
    file_name1 = os.path.join(path, file_name1)
    file_name2 = os.path.join(path, file_name2)

    # Create shuffled BED files of file1 and file2
    file1 = bt(file_name1)
    file2 = bt(file_name2)

    genome_chrom_size = os.path.join(settings.MEDIA_ROOT, 'genome_chrom_sizes')

    randomised_files = []
    for rep in range(10000):
        shuffled_file1 = file1.shuffle(g=genome_chrom_size + '/mm9.chrom.sizes', chrom=True)
        shuffled_file2 = file2.shuffle(g=genome_chrom_size + '/mm9.chrom.sizes', chrom=True)
        randomised_files.append((shuffled_file1, shuffled_file2))

    # set multiprocessing
    pool = Pool(processes=4)
    bootstrapped_jaccard = pool.map(bootstrapRandom, randomised_files)  # returns list of jaccard indices
    pool.join()
    pool.close()

    return bootstrapped_jaccard


def getPrecomputedJaccardValuePerFile(file_name1):
    jaccard_indices = {}
    with connection.cursor() as cursor:
        cursor.execute("SELECT file_one, file_two, jaccard_index FROM jaccard_indeces WHERE file_one = %s OR file_two = %s",
                       [file_name1, file_name1])
        for row in cursor.fetchall():
            file_one, file_two, jaccard_index = row
            if file_one == file_name1:
                jaccard_indices[file_two] = jaccard_index
            else:
                jaccard_indices[file_one] = jaccard_index
    return jaccard_indices
