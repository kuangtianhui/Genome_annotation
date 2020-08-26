#!/bin/env python
# -*- coding: utf-8 -*-
# @Author: FT
# @Date:   2020-06-18
# @Last Modified by:   tao
# @Last Modified time: 2020-06-18

import os
import sys
import shutil
raw_orthogroups_sum=sys.argv[1]
raw_orthogroups_folder=sys.argv[2]
clean_orthogroups_folder=sys.argv[3]


def extract_orthogroups():
	'''extract gene families with all species present and the total copy number < 200'''
	clean_orthogroups=[]
	with open(raw_orthogroups) as ro:
		for line in ro:
			line = line.split("\t")
			if "0" not in line and int(line[5]) <= 200:
				line = line[1] + ".fa"   #append '.fa' to make the filename identified in next step
				clean_orthogroups.append(line)
	for file in clean_orthogroups:
		shutil.copy(sys.argv[2] + '/' + file, sys.argv[3] + '/' + file)


extract_orthogroups():