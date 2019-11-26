# -*- coding: utf-8 -*-
# @Author: FT
# @Date:   2019-11-26
# @Last Modified by:   tao
# @Last Modified time: 2019-11-26
# -*- coding: utf-8 -*-
# @Author: ChenJun
# @Email:  chenjun4663@novogene.com
# @Qmail:  1170101471@qq.com
# @Date:   2019-11-26 19:04:39
# @Last Modified by:   11701
# @Last Modified time: 2019-11-26 19:14:54

import sys

gff1 = sys.argv[1]
gff2 = sys.argv[2]

with open(gff1, 'rb') as fi,\
        open(gff2, 'wb') as fo:
    Ltmp = []
    for line in fi:        
        if line.startswith(b'#'):
            fo.write(line)
            continue
        Lline = line.strip().split(b'\t')
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
                    fo.write(line_tmp.split('Parent')[0] + 'ID=cds_of_' + mRNA + ';Parent' + line_tmp.split('Parent')[1] + '\n')
            Ltmp = []
        else:
            Ltmp.append(line.strip('\n'))
