import numpy as np

with open('CAMELS/package_test.txt', 'r') as f:
    dat = f.readlines()
dat = [x.rstrip().split('\t') for x in dat]

print(sorted(dat, key=lambda x: x[1]))