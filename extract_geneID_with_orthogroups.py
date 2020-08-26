# -*- coding: utf-8 -*-
# @Author: FT
# @Date:   2020-06-22
# @Last Modified by:   tao
# @Last Modified time: 2020-06-22
'''
Given the orthogroup clusering information from OrthoFinder, extract specific gene ids that identified by CAFE
'''

import os
import re

def orthogroup2gene(orthogroup,orthogroup_interested,specie_id,gene_interested):
	with open(orthogroup, "r") as OR, open(orthogroup_interested, "r") as ORI, open(gene_interested, "w") as output:
		ORI_LIST = []
		for line in ORI:
			ORI_LIST.append(line)
		for line in OR:
			line = re.split(",|\t", line)
			if line[0] in ORI_LIST:
				for gene in line:
					if gene.startswith(specie_id):
						output.write(gene + "\n")
	OR.close()
	ORI.close()
	gene_interested()

def main(orthogroup,orthogroup_interested,specie_id,gene_interested):
	orthogroup2gene(orthogroup,orthogroup_interested,specie_id,gene_interested)

if __name__ == '__main__':
	if len(sys.argv) != 5:
		print "usage: python extract_geneID_with_orthogroups.py orthogroup,orthogroup_interested,specie_id,gene_interested"
	
	orthogroup,orthogroup_interested,specie_id,gene_interested = sys.argv[1:]
	main(orthogroup,orthogroup_interested,specie_id,gene_interested)
