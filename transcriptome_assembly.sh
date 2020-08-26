# @Author: FT
# @Date:   2020-08-26
# @Last Modified by:   tao
# @Last Modified time: 2020-08-26
#!/bin/bash

#$1: species ID
#$2: trinity raw output
module load gcc/4.8.4

export PATH=~/app/transdecoder:~/app/diamond:~/app/hmmer3/bin:~/app/cd-hit:$PATH
var=$1

srun -n 1 -c 24 \
TransDecoder.LongOrfs -t $2 && \
diamond blastp -c 1 -b10 --more-sensitive --db ~/lib/plant_protein_database/alluniRefprexp070416 --query Trinity.fasta.transdecoder_dir/longest_orfs.pep -o blastp.outfmt6 && \
hmmscan --cpu 24 --domtblout pfam.domtblout ~/lib/Pfam/Pfam-A.hmm Trinity.fasta.transdecoder_dir/longest_orfs.pep && \
TransDecoder.Predict -t $2 --retain_pfam_hits pfam.domtblout --retain_blastp_hits blastp.outfmt6 && \
cd-hit -i Trinity.fasta.transdecoder.pep -o Trinity.fasta.transdecoder.pep.cdhit99 -c 0.99 -n 5 -M 60000 -d 0 -T 24 && \
cat Trinity.fasta.transdecoder.pep.cdhit99 | awk -v awk_var="$var" -F '[ _]' '{if ($0 ~ /^>/) print ">"awk_var"_"$2"_"$3"_"$4"_"$5; else print $0}' > $1.pep.fa && \
cat Trinity.fasta.transdecoder.cds | awk -v awk_var="$var" -F '[ _]' '{if ($0 ~ /^>/) print ">"awk_var"_"$2"_"$3"_"$4"_"$5; else print $0}' > $1.cds.fa