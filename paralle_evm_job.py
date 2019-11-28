# -*- coding: utf-8 -*-
# @Author: FT
# @Date:   2019-11-28
# @Last Modified by:   tao
# @Last Modified time: 2019-11-28

import os
import sys
command_list = sys.argv[1]
work_path = sys.argv[2]
command_path = sys.argv[3]

def partion_command(command_list):
	fi = open(command_list, "r")
	i = 1
	f = 1
	os.chdir(command_path)
	fo = open(str(f) + "_command.sh", "w")
	for line in fi:
		if i == 1:
			fo.close()
			fo = open(str(f)+ "_command.sh", "w")
			fo.write("#!/bin/bash" + "\n")
		if i < 24:
			fo.write("yhrun -n 1 -c 1 " + line.strip() + " &" + "\n")
		if i == 24:
			fo.write("yhrun -n 1 -c 1 " + line.strip() + "\n")
			i += 1
		if i < 24:
			i += 1
		if i == 25:
			fo.write("wait\n")
			i = 1
			f += 1
	if i != 25:
		fo.write("wait\n")

        # raw - bak
		# if i < 24:
		# 	fo.write("yhrun -n 1 -c 1 " + line.strip() + " &" + "\n")
		# 	i += 1
		# if i = 24:
		# 	fo.write("yhrun -n 1 -c 1 " + line.strip() + "\n" + "wait")
		# 	i = 1
		# 	f += 1
		# 	fo.close()
		# 	fo = open(str(f), "w")
		# 	fo.write("#!/bin/bash" + "\n")

def submit_job(work_path,command_path):
	os.chdir(work_path)                      # cd work_path
	for command in os.listdir(command_path): # be sure that no other files other than command.sh files
		os.mkdir(command.strip('.sh'))       # eg. mkdir 1_command
		os.chdir(command.strip('.sh'))       # cd ./1_command
		os.system("sbatch -N 1 " + command_path + command) # submit job, generate slurm-xxx.txt
		os.chdir("..")                       # go back to work_path

if __name__ == '__main__':
	partion_command(command_list)
	submit_job(work_path,command_path)

