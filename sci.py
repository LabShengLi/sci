import sys
import argparse


from sci.hic import HicData
from sci.Compartments import Compartments



def run_sci():
	parser = argparse.ArgumentParser(description='SCI a method to predict sub-compartments from HiC data',add_help=False)
	requiredArguments = parser.add_argument_group('Required arguments')
	requiredArguments.add_argument("-n","--name",action="store",dest="name",help="Name of the experiment",type=str,required=True)
	requiredArguments.add_argument("-f","--infile",action="store",dest="infile",help="Name of HiC interaction file",type=str,required=True)
	requiredArguments.add_argument("-r","--resolution",action="store",dest="res",
					help="Required resolution to predict compartments,provided bins\' size should have resolution greater than or equal the provided value",
					type=int,required=True)
	requiredArguments.add_argument("-g","--genome_size",action="store",dest="genome_size",help="File containing chromosome size of the target genome",type=str,required=True)
	
	#optionalArguments = parser.add_argument_group('optional arguments')
	optional = parser.add_argument_group('optional arguments')
	optional.add_argument("-h", "--help", action="help", help="show this help message and exit")
	optional.add_argument("-o","--order",action="store",dest="order",help="Graph order to consider when performing graph embedding. Available options are 1,2 or both. Default: 1",
					type=str,default="1")
	optional.add_argument("-s","--samples",action="store",dest="samples",help="Number of edges to sample in millions order from the graph. Default: 25",type=int,default=25)
	optional.add_argument("-k","--clusters",action="store",dest="clusters",help="Nubmer of sub-compartments to be predicted. Default: 5",type=int,default=5)

	oArgs = parser.parse_args()
	myobject = HicData(oArgs.res,oArgs.name)
	myobject.initialize(oArgs.genome_size)
	myobject.load_interaction_data(oArgs.infile)
	hic_graph = myobject.write_inter_chrom_graph()
	GW_metadata = myobject.get_bins_info()

	predictor = Compartments(oArgs.name,GW_metadata)
	predictor.predict_subcompartents(hic_graph,oArgs.order,oArgs.samples,oArgs.clusters)
	#predict_subcompartents(self,graphFile,order,samples,k=5)


if __name__ == '__main__':
	run_sci()