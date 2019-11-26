# -*- coding: utf-8 -*-
# @Author: FT
# @Date:   2019-11-26
# @Last Modified by:   tao
# @Last Modified time: 2019-11-26
# -*- coding: utf-8 -*-


import sys

gff1 = sys.argv[1]
gff2 = sys.argv[2]

with open(gff1, 'rb') as fi, open(gff2, 'wb') as fo:
    Ltmp = []
    x = 0
    y = 1
    for line in fi:
        if line.startswith('#'):
            fo.write(line)
            continue
        Lline = line.strip().split('\t')
        if Lline[2] == b'gene':
            line = line.split(';')[0]
            name = line.split('=')[1]
            fo.write(line.replace('GAF','GeMoMa') + ';Name=' + name + '\n')
            for line_tmp in Ltmp:
                line_tmp = line_tmp.split(';')[0]
                if 'prediction' in line_tmp:
                    fo.write(line_tmp.replace('prediction','mRNA') + ';Parent=' + name + '\n')
                    mRNA = line_tmp.split('=')[1]
                if 'CDS' in line_tmp:
                    fo.write(line_tmp.split('Parent')[0].replace('CDS', 'exon') + 'ID=exon.' + str(x) + '.' + str(y) + ';Parent' + line_tmp.split('Parent')[1] + '\n')
                    fo.write(line_tmp.split('Parent')[0] + 'ID=cds_of_' + mRNA + ';Parent' + line_tmp.split('Parent')[1] + '\n')
                    y = y + 1
            x = x + 1
            y = 1
            Ltmp = []
        else:
            Ltmp.append(line.strip('\n'))
