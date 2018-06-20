#!/usr/bin/env python
from random import shuffle
import numpy
import ce_calc
from math import floor

def atomchanger(nanop, el1, el2):
    # nanop = ase Atom object
    # el1 = first element requested
    # el2 = second element requested
    nanoplist = nanop.get_chemical_symbols()
    nanonum = len(nanoplist)  # number of atoms in nanop
    # Read in data from atom object.


    totalloops = 5
    cemeanlist = [None]*21
    stdevlist = [None]*21
    mincelist = [None]*21
    maxcelist = [None]*21
    minatomlist = [None]*21
    maxatomlist = [None] * 21
    k=0

    for j in range(0, 101, 5):
        divider = floor(j * nanonum / 100)
        x = 0
        while x < nanonum:
            if x < divider:
                nanoplist[x] = el1
            elif x >= divider:
                nanoplist[x] = el2
            x = x + 1

        modlist = list(nanoplist)
        celist = [None] * totalloops
        j = 0
        for i in range(0, totalloops):
            shuffle(modlist)
            nanop.set_chemical_symbols(modlist)
            celist[i] = ce_calc.calculate_CE(nanop)
            if j == 0:
                maxce = celist[i]
                mince = celist[i]
                minatom = nanop
                maxatom = nanop
                j = 1
            else:
                if celist[i] < mince:
                    mince = celist[i]
                    minatom = nanop
                elif celist[i] > maxce:
                    maxce = celist[i]
                    maxatom = nanop

            if i == totalloops - 1:
                cemeanlist[k] = numpy.mean(celist)
                stdevlist[k] = numpy.std(celist)
                mincelist[k] = mince
                maxcelist[k] = maxce
                minatomlist[k] = minatom
                maxatomlist[k] = maxatom
                k += 1
    return cemeanlist, stdevlist, totalloops, mincelist, maxcelist, minatomlist, maxatomlist
