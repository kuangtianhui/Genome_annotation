# -*- coding: utf-8 -*-
# @Author: FT
# @Date:   2020-06-18
# @Last Modified by:   tao
# @Last Modified time: 2020-07-26
"""
this script was derived from yangya (https://bitbucket.org/yangya/phylogenomic_dataset_construction/src/master/) and main changes are:
1. replace phyutility with trimal which can do gap trimming and simility-based trimming as well
2. use the fasta file ID to manully parallelize the job on HPC cluster

make sure that raxml, mafft, run_pasta.py, trimal, phyutility and fastree are in the path
"""

import os,sys
from mafft_wrapper import mafft
from pasta_wrapper import pasta
#from phyutility_wrapper import phyutility
from trimal_wrapper import trimal # phyutility is replaced by trimal
from fasttree_wrapper import fasttree
from raxml_wrapper import raxml
from raxml_bs_wrapper import raxml_bs
from seq import read_fasta_file

NUM_SEQ_CUTOFF = 1000 # Use different alignment and tree inference tools
# below vs. above this cutoff

def get_fasta_size(fasta):
	"""
	given a fasta file
	output the number of seqs and the length of the longest seq
	"""
	longest = 0
	seqlist = read_fasta_file(fasta)
	for s in seqlist:
		longest = max(longest,len(s.seq.replace("-","")))
	return len(seqlist),longest
	
def fasta_to_tree(DIR,fasta,num_cores,seqtype,num_seq_cutoff=NUM_SEQ_CUTOFF):
	"""
	given a fasta file
	align, trim alignment and build a tree
	choose appropriate tools depending on size of the fasta file
	"""
	if DIR[-1] != "/": DIR += "/"
	seqcount, maxlen = get_fasta_size(DIR+fasta)
	assert seqcount >= 3, "Less than three sequences in "+DIR+fasta
	print fasta,seqcount,"sequences"
	if seqcount >= NUM_SEQ_CUTOFF: # large cluster
		alignment = pasta(DIR,fasta,num_cores,seqtype)
#		cleaned = phyutility(DIR,alignment,0.01,seqtype)
		cleaned = trimal(DIR,alignment,0.5,0.001) # use trimal-added by Tao, now need to def trimal
		if len(read_fasta_file(DIR+cleaned)) >= 3:
			tree = fasttree(DIR,cleaned,seqtype)
		else: print "Less than 3 taxa in",cleaned
	else: # small cluster
		alignment = mafft(DIR,fasta,num_cores,seqtype)
#		cleaned = phyutility(DIR,alignment,0.1,seqtype) "phyutility can only trim gaps-added by tao"
		cleaned = trimal(DIR,alignment,0.5,0.001) # use trimal-added by Tao, now need to def trimal
		seqcount, maxlen = get_fasta_size(DIR+cleaned)
		print cleaned,seqcount,"sequences"
		if len(read_fasta_file(DIR+cleaned)) >= 3:
			tree = fasttree(DIR,cleaned,seqtype)
			#tree = raxml(DIR,cleaned,num_cores,seqtype)
		#if len(read_fasta_file(DIR+cleaned)) == 3: # added by Tao
			#tree = fasttree(DIR,cleaned,seqtype) # use added by Tao
		else:
			print "Less than 3 taxa in",cleaned

def fasta_to_bs_tree(DIR,fasta,num_cores,seqtype):
	"""
	given a fasta file for the final homolog
	align, trim alignment and build a tree with bootstrap support
	"""
	if DIR[-1] != "/": DIR += "/"
	seqcount, maxlen = get_fasta_size(DIR+fasta)
	assert seqcount >= 3, "Less than three sequences in "+DIR+fasta
	print fasta,seqcount,"sequences"
	alignment = mafft(DIR,fasta,num_cores,seqtype)
	#cleaned = phyutility(DIR,alignment,0.2,seqtype)
	cleaned = trimal(DIR,alignment,0.5,0.001) # use trimal-added by Tao, now need to def trimal
	if len(read_fasta_file(DIR+cleaned)) >= 4:
		tree = raxml_bs(DIR,cleaned,num_cores,seqtype)
	else: print "Less than 4 taxa in",cleaned

def main(DIR,num_cores,seqtype,bs,left,right,test=False): # this "test=True" like argument must be at the last position 
	"""if test, only process clusterID that ends with 0"""
	assert seqtype == "aa" or seqtype == "dna",\
		"Input data type: dna or aa"
	assert bs == "y" or bs=="n",\
		"bootstrap? (y/n)"
	if DIR[-1] != "/": DIR += "/"
	
	#check for really long sequences or large alignments.
	#These crashes the alignment program
	for i in os.listdir(DIR):
		if int(i[4:9]) >= int(left) and int(i[4:9]) <= int(right): #added by tao; "range_*" was passed to python by shell and was treated as str
			if i.endswith(".fa"):
				seqcount,maxlen = get_fasta_size(DIR+i)
				if (maxlen>=10000 and seqtype=="aa") or (maxlen>=30000 and seqtype=="dna"):
					print i,"has",seqcount,"sequences"
					print "longest sequence has",maxlen,"characters"
					print "Warning: sequence too long. May crash alignment process"
					#sys.exit()

			filecount = 0
			if not i.endswith(".fa"): continue
			if test and (i.split(".")[0])[-1] != "0": continue # to only run the first one orthogroup to test
			filecount += 1
			if bs == "n":
				fasta_to_tree(DIR=DIR,fasta=i,num_cores=num_cores,seqtype=seqtype) # can be fasta_to_tree(DIR,i,num_cores,seqtype) ?
			else: fasta_to_bs_tree(DIR=DIR,fasta=i,num_cores=num_cores,seqtype=seqtype)
			assert filecount > 0, "No file end with .fa found in "+DIR

if __name__ == "__main__":
	if len(sys.argv) != 7:
		print "python fasta_to_tree.py DIR number_cores dna/aa bootstrap(y/n) left right"
		sys.exit(0)
	else:
		main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6])


