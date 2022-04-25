from utils import *
import numpy as np
from sklearn import preprocessing
from sklearn.cluster import KMeans
from scipy.stats import pearsonr
from numpy import linalg as LA
from sklearn.metrics.pairwise import pairwise_distances


class Compartments:
    def __init__(self, name, GW_metadata):
        self.GWtoKeep = []
        self.toKeep = []
        self.GW_meta_data = GW_metadata
        self.name = name

    def process_LINE_embedding(self, embedding_file):
        features = []
        nodes = []
        oF = open(embedding_file)
        oF.readline()
        for line in oF.readlines():
            parts = line.strip().split()
            nodes.append(int(parts[0]))
            features.append([float(a) for a in parts[1:]])

        self.GW_toKeep = np.array(nodes)
        return features

    def predict_subcompartents(self, graphFile, order, samples, k=5):
        # run graph embedding
        embedding_files = run_LINE(graphFile, samples, order)

        # process embedding
        if order != "both":
            data = self.process_LINE_embedding(embedding_files)
        else:
            data_1 = self.process_LINE_embedding(embedding_files[0])
            data_2 = self.process_LINE_embedding(embedding_files[1])
            data = np.concatenate((data_1, data_2), axis=1)
            data = preprocessing.normalize(data, norm='l2')

        # cluster embedding
        #data = preprocessing.scale(data)
        model = KMeans(n_clusters=k, random_state=12345)
        model.fit(data)
        GW_compartments = model.predict(data)

        # writing compartments to file
        compartments = np.zeros(len(self.GW_meta_data))
        compartments += -10
        compartments[self.GW_toKeep] = GW_compartments
        outfile = ("%s_compartments.txt" % (self.name))
        oF = open(outfile, "w")
        oF.write("%s\t%s\t%s\t%s\n" % ("chr", "start", "end", "compartment"))

        for coord, compartment in zip(self.GW_meta_data, compartments):
            if compartment == -10:
                value = "NA"
            else:
                value = str(compartment)
            oF.write("%s\t%d\t%d\t%s\n" %
                     (coord[0], coord[1], coord[2], value))
        oF.close()

    def predict_ab_one_chrom(self, contact_matrix):
        # do some normalizations
        AB_compartments = []
        bins_count = contact_matrix.shape[0]
        contact_matrix, to_keep = filter_matrix(count_matrix)
        contact_matrix = ICE_normalization(count_matrix)

        dExpected_counts = get_expected_counts(count_matrix)
        count_matrix = normalize_by_distance(count_matrix, dExpected_counts)
        count_matrix = np.nan_to_num(count_matrix)  # fixing rounding errors

        # calculate correlations
        corr_matrix = 1 - pairwise_distances(conntact_matrix,
                                             metric='correlation')
        W, V = LA.eig(corr_matrix)
        AB_comp_ = V[:, 0]
        AB_comp = np.zeros(bins_count)
        AB_comp += -10  # some dummy thing
        AB_comp[to_keep] = AB_comp_

        return
