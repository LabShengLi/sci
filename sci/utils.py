import shlex
import subprocess
import sys
from iced import filter
from iced.normalization import ICE_normalization

def _LaunchJob(sCommand,sStdin=None):
	'''
	Launch any command using pipes 
	'''
	aArgs = shlex.split(sCommand)
	print aArgs
	if sStdin != None:
		oProcess = subprocess.Popen(aArgs, shell=False, 
					    stdin = subprocess.PIPE,
					    stdout=subprocess.PIPE, 
					    stderr = subprocess.PIPE)
		tOutput = oProcess.communicate(sStdin)
	else:
		oProcess = subprocess.Popen(aArgs, shell=False,stdout=subprocess.PIPE, stderr = subprocess.PIPE)
		print oProcess
		tOutput = oProcess.communicate()
	#print tOutput
	return tOutput



def run_LINE(inFile,samples,mode):
	'''
	inFile is a graph file, should be undirected in our case
	samples how many edges to sample from that graph in order of millions
	mode: can be 1,2,both
	'''

	if mode!="both":
		outFile = '%s_order_%s_samples_%dM.embedding'%(inFile.split(".")[0],mode,samples)
		command = 'bin/LINE/line -train %s -order %s -samples %d -output %s'%(inFile,mode,samples,outFile)
		tOutput = _LaunchJob(command)
		if tOutput[1]!='':
			sys.exit(tOutput[1])
		return outFile
	else:
		#run line for both 1 and 2 orders
		outFile1 = '%s_order_1_samples_%dM.embedding'%(inFile.split(".")[0],samples)
		command = 'bin/LINE/line -train %s -order 1 -samples %d -output %s'%(inFile,samples,outFile1)
		tOutput = _LaunchJob(command)
		if tOutput[1]!='':
			sys.exit(tOutput[1])
		command = 'bin/LINE/line -train %s -order 2 -samples %d -output %s'%(inFile,samples,outFile2)
		_LaunchJob(command)
		if tOutput[1]!='':
			sys.exit(tOutput[1])
		return (outFile1,outFile2)




def get_expected_counts(contact_matrix):
	bins_count = contact_matrix.shape[0]
	dExpected_counts = {}
	dCount = {}
	for i in range(bins_count):
		dExpected_counts[i] = 0.0
		dCount[i] = 0
	rows,cols = contact_matrix.shape

	for i in range(rows):
		for j in range(cols):
			band_length = abs(i-j)
			dExpected_counts[band_length]+=contact_matrix[i,j]
			dCount[band_length] += 1
	for i in range(bins_count):
		dExpected_counts[i] /= dCount[i]
	return dExpected_counts



def filter_matrix(contact_matrix):
	filtered_matrix = filter.filter_low_counts(contact_matrix,remove_all_zeros_loci=True, sparsity=False)
	rows, cols =  filtered_matrix.shape
	nan_sum =0
	to_keep = []
	for i in range(rows):
		if sum(np.isnan(filtered_matrix[i,:])) < cols:
			to_keep.append(i)
	row_filtered = filtered_matrix[to_keep,:]
	return (row_filtered[:,to_keep],to_keep) # finally remove cols


def normalize_by_distance(contact_matrix,dExpected_counts):

	rows, cols = contact_matrix.shape
	for i in range(rows):
		for j in range(cols):
			band_length = abs(i-j)
			contact_matrix[i,j]/=dExpected_counts[band_length]
	return contact_matrix


