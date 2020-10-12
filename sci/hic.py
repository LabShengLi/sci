import os
import numpy as np
from itertools import combinations
from tqdm import tqdm


class HicData:
    def __init__(self, res, name):
        '''
        '''
        self.res = res
        self.contact_matrices = {}
        self.dExpected_counts = {}
        self.toKeep = {}
        self.GW_contact_matrix = []
        self.GW_meta_data = []
        self.GW_toKeep = []
        self.GW_location2index = {}
        self.dChrBins = {}
        self.name = name
        self.ordered_pairs = []
        self.embedding_mode = None
        self.interchrom_contact_matrix = []

    def get_chromosomes_bin_counts(self, chrsize_file):
        oF = open(chrsize_file)
        for line in oF.readlines():
            parts = line.strip().split()
            self.dChrBins[parts[0]] = int(parts[1])/self.res + 1
        return

    def initialize(self, chr_size_file):
        self.get_chromosomes_bin_counts(chr_size_file)
        # generate genomewide mapping
        for i in range(1, 23):
            chrom = "chr%d" % i
            for j in range(self.dChrBins[chrom]):
                self.GW_meta_data.append((chrom, j*self.res,
                                          j*self.res+self.res))

        for i, location in enumerate(self.GW_meta_data):
            self.GW_location2index[(location[0], location[1])] = i

    def initialize_contact_matrix(self):
        # initialize cis interaction matrices
        for chrom in self.dChrBins.keys():
            shape = self.dChrBins[chrom]
            self.contact_matrices[(chrom, chrom)] = np.zeros((shape, shape))

        # initialize trans matricies
        for chrom1, chrom2 in combinations(self.dChrBins.keys(), 2):
            rows = self.dChrBins[chrom1]
            cols = self.dChrBins[chrom2]
            self.contact_matrices[(chrom1, chrom2)] = np.zeros((rows, cols))
            self.ordered_pairs.append((chrom1, chrom2))
        return

    def load_interaction_data(self, contact_file):
        '''
        contact file should contain all interactions from cis
        and trans interactions
        '''

        self.initialize_contact_matrix()
        oF = open(contact_file, "r")
        for line in tqdm(oF.readlines(), desc='Reading %s' % contact_file):
            (chrom1, start1, end1, chrom2,
                start2, end2, count) = line.strip().split()

            if count.split('.')[0].isdigit() and start1.isdigit() and start2.isdigit():
                i = int(start1) / self.res
                j = int(start2) / self.res
            else:
                continue
            # Debug snnipet
            try:
                row, col = self.contact_matrices[(chrom1, chrom2)].shape
                if i >= row or j >= col:
                    continue
            except KeyError:
                row, col = self.contact_matrices[(chrom2, chrom1)].shape
                if j >= row or i >= col:
                    continue

            try:
                self.contact_matrices[(chrom1, chrom2)][i, j] +=\
                    float(count)
            except KeyError:
                try:
                    self.contact_matrices[(chrom2, chrom1)][j, i] +=\
                        float(count)
                except KeyError:
                    print("ignoring pair: %s,"
                          "chromoses are not in"
                          "chromsomes size file") % line.strip()
        return

    def get_contact_matrix(self, chrom1, chrom2):
        return self.contact_matrices[(chrom1, chrom2)]

    def get_bins_info(self):
        return self.GW_meta_data

    def write_inter_chrom_graph(self):
        outfile = "%s_HiC_graph.txt" % self.name
        oF = open(outfile, "w")

        for (chrom1, chrom2) in tqdm(self.ordered_pairs,
                                     desc="writing HiC graph"):
            if chrom1 != chrom2:
                if self.embedding_mode == "oe":
                    c1 = int(chrom1.strip("chr"))
                    c2 = int(chrom2.strip("chr"))

                    if c1 % 2 == 1 and c2 % 2 == 0:
                        self.dump_interchrom_block(oF, chrom1, chrom2)
                else:
                    self.dump_interchrom_block(oF, chrom1, chrom2)
        return outfile

    def dump_interchrom_block(self, oF, chrom1, chrom2):
        row, col = self.contact_matrices[(chrom1, chrom2)].shape
        for i in range(row):
            for j in range(col):
                node1 = self.GW_location2index[(chrom1, i*self.res)]
                node2 = self.GW_location2index[(chrom2, j*self.res)]
                value = self.contact_matrices[(chrom1, chrom2)][i, j]
                if value >= 1:
                    oF.write("%d\t%d\t%f\n" % (node1, node2, np.log(value)))
                    oF.write("%d\t%d\t%f\n" % (node2, node1, np.log(value)))

    def write_GW_matrix(self, mat_file, cis=False):
        rows = []
        for i in range(1, 23):
            chrom1 = "chr%d" % i
            cols = []
            for j in range(1, 23):
                chrom2 = "chr%d" % j
                if (i == j):
                    if cis:
                        cols.append(self.contact_matrices
                                    [(chrom1, chrom1)])
                    else:
                        size = self.dChrBins[chrom1]
                        cols.append(np.zeros((size, size)))
                else:
                    try:
                        cols.append(self.contact_matrices
                                    [(chrom1, chrom2)])
                    except KeyError:
                        try:
                            cols.append(self.
                                        contact_matrices
                                        [(chrom2, chrom1)]
                                        .T)
                        except KeyError:
                            print("Can not find matrix "
                                  "for%s %s, will add "
                                  "zeroes to GW matrix"
                                  % (chrom1, chrom2))
                            row = self.dChrBins[chrom1]
                            col = self.dChrBins[chrom2]
                            cols.append(np.zeros(
                                        (row, col)))
            row = np.concatenate(cols, axis=1)
            rows.append(row)
        self.interchrom_contact_matrix = np.concatenate(rows, axis=0)
        np.savetxt(mat_file, self.interchrom_contact_matrix, delimiter=",")
        return
