# -*- coding: utf-8 -*-
import numpy as np
import io
import os
import kaldi_io
import argparse

parser=argparse.ArgumentParser(description='''Maps Fisher speech utterances to parallel ids with translations.''')
parser.add_argument('-i', '--inputark', type=str, help='path to input speech arkfile', required=True)
parser.add_argument('-m', '--map', type=str, help='path to corresponding map file, e.g.  ../maps/fisher_dev', required=True)
parser.add_argument('-a','--arktype', type=str, default='bin', help='[bin|text] type of input ark file (binary or text). default is binary.')
parser.add_argument('-o','--output', type=str, default='npz', help='[npz|bin|text] output type (binary ark, text ark, or npz). default is npz.')
args=parser.parse_args()
#------------------------

arkname = args.inputark
uttmap  = args.map
prefix  = os.path.splitext(os.path.basename(arkname))[0]
filtark = prefix + '.mapped'
print('ark file: %s, uttmap: %s, new ark file: %s' % (arkname, uttmap, filtark))

#reads map file
mapname   = io.open(uttmap,mode='r',encoding='utf-8')
map_lines = mapname.read().split('\n')

#reads binary vs text ark file format
if args.arktype=='bin':
    arkd = {k: v for k,v in kaldi_io.read_mat_ark(arkname)}
else:
    arkd = dict()
    with open(arkname,'r') as f:
        line = f.readline().strip()
        while line:
            all = line.split()
            k = all[0]
            rest = ' '.join(all[1:]).strip('[]').strip()
            rest = rest.split()
            rest = filter(None,rest)
            arkd[k] = v
            line = f.readline().strip()

print('ark file read in: %s, num keys: %d' % (arkname, len(arkd.keys())))
#------------------------------------------------------------------------

mats = []
keys = []
counter = 0
if args.output=='bin':
    newark = open(filtark+'.ark','wb')
elif args.output=='text':
    newark = open(filtark+'.ark','w')
    
for uttid in map_lines:
    allids = uttid.strip().split(';')
    idlist = [x for x in allids if x in arkd]

    #if we have multiple utterances to concatenate
    if ';' in uttid and len(idlist)>0:
        uttkey = idlist[0] if idlist[0] not in keys else idlist[0]+'+' #'+' marks lines as merged. useful where they duplicated lines when merging
        keys.append(uttkey)

        mapids = list(map(lambda x: arkd.get(x,None), idlist))
        tmpmat = np.concatenate(mapids, axis=0) #need to wrap map in list for python3
        if args.output=='bin':
            kaldi_io.write_mat(newark, tmpmat, key=uttkey)
        elif args.output=='text':
            newark.write(uttkey + ' ' + str(list(tmpmat)).replace(',','') + '\n')
        else:
            mats.append(list(tmpmat))
        counter+=1
    else:
        if len(idlist)>0 and idlist[0] in arkd:
            tmpmat = arkd.get(idlist[0],None)
            uttkey = idlist[0] if idlist[0] not in keys else idlist[0]+'+' #'+' marks lines as merged. useful where they duplicated lines when merging
            keys.append(uttkey)
            if args.output=='bin':
                kaldi_io.write_mat(newark, tmpmat, key=uttkey)
            elif args.output=='text':
                newark.write(uttkey + ' ' + str(tmpmat).replace(',','') + '\n')
            else:
                mats.append(tmpmat)
            counter+=1

print('final number of utterances: %d' % counter)
if args.output=='npz':
    np.savez_compressed(filtark, *mats)
else:
    newark.close()
#---------------------------
print('done %s!' % prefix)
