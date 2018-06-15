#!/usr/bin/env python

import ase, ase.neighborlist
import numpy as np

# Lookup table pre-computed in Coeffs_Table.py
# Syntax for the table is:
#   precomputed_coeffs[element_1][element_2][CN]
# So for example, to get the value for a Cu-Ag bond, with Cu @ CN6 and Ag @ CN12:
#   precomputed_coeffs["Cu"]["Ag"][6] + precomputed_coeffs["Ag"]["Cu"][12]

lookup_table = {'Au': {'Au': [None,  # 0
                              -1.0998522628062373,  # 1
                              -0.77771299333365917,  # 2
                              -0.63500000000000012,  # 3
                              -0.54992613140311863,  # 4
                              -0.49186888496834202,  # 5
                              -0.44901280605345778,  # 6
                              -0.41570508089956554,  # 7
                              -0.38885649666682959,  # 8
                              -0.36661742093541244,  # 9
                              -0.34780382401578053,  # 10
                              -0.33161793459560446,  # 11
                              -0.31750000000000006],  # 12

                       'Ag': [None,  # 0
                              -1.4078108963919838,  # 1
                              -0.99547263146708376,  # 2
                              -0.81280000000000019,  # 3
                              -0.70390544819599188,  # 4
                              -0.62959217275947776,  # 5
                              -0.57473639174842595,  # 6
                              -0.53210250355144395,  # 7
                              -0.49773631573354188,  # 8
                              -0.4692702987973279,  # 9
                              -0.44518889474019907,  # 10
                              -0.42447095628237369,  # 11
                              -0.40640000000000009],  # 12

                       'Cu': [None,  # 0
                              -2.5956513402227199,  # 1
                              -1.8354026642674355,  # 2
                              -1.4986000000000004,  # 3
                              -1.29782567011136,  # 4
                              -1.1608105685252872,  # 5
                              -1.0596702222861605,  # 6
                              -0.98106399092297469,  # 7
                              -0.91770133213371774,  # 8
                              -0.86521711340757335,  # 9
                              -0.82081702467724205,  # 10
                              -0.7826183256456265,  # 11
                              -0.74930000000000019]  # 12
                       },
                'Ag': {
                    'Au': [None,  # 0
                           -0.61314598587938263,  # 1
                           -0.43355968447262255,  # 2
                           -0.35400000000000004,  # 3
                           -0.30657299293969131,  # 4
                           -0.27420722091148514,  # 5
                           -0.25031580054003788,  # 6
                           -0.23174739943062392,  # 7
                           -0.21677984223631128,  # 8
                           -0.20438199529312753,  # 9
                           -0.1938937853568288,  # 10
                           -0.18487047062495113,  # 11
                           -0.17700000000000002],  # 12

                    'Ag': [None,  # 0
                           -0.85159164705469814,  # 1
                           -0.60216622843419798,  # 2
                           -0.49166666666666675,  # 3
                           -0.42579582352734907,  # 4
                           -0.38084336237706268,  # 5
                           -0.34766083408338594,  # 6
                           -0.3218713880980888,  # 7
                           -0.30108311421709899,  # 8
                           -0.28386388235156607,  # 9
                           -0.26929692410670669,  # 10
                           -0.25676454253465436,  # 11
                           -0.24583333333333338],  # 12

                    'Cu': [None,  # 0
                           -1.1837123894060304,  # 1
                           -0.83701105752353522,  # 2
                           -0.68341666666666678,  # 3
                           -0.5918561947030152,  # 4
                           -0.5293722737041171,  # 5
                           -0.48324855937590649,  # 6
                           -0.44740122945634342,  # 7
                           -0.41850552876176761,  # 8
                           -0.39457079646867682,  # 9
                           -0.37432272450832232,  # 10
                           -0.35690271412316954,  # 11
                           -0.34170833333333339]  # 12
                    },
                'Cu': {
                    'Au': [None,  # 0
                           0.36269143910492291,  # 1
                           0.25646157606939873,  # 2
                           0.2094,  # 3
                           0.18134571955246145,  # 4
                           0.1622005425391666,  # 5
                           0.14806815998046308,  # 6
                           0.1370844786462504,  # 7
                           0.12823078803469937,  # 8
                           0.12089714636830763,  # 9
                           0.11469310354158178,  # 10
                           0.10935558347136938,  # 11
                           0.1047],  # 12

                    'Ag': [None,  # 0
                           -0.61456049403889723,  # 1
                           -0.43455989278425899,  # 2
                           -0.35481666666666672,  # 3
                           -0.30728024701944862,  # 4
                           -0.27483980819136566,  # 5
                           -0.25089327107800691,  # 6
                           -0.2322820332617021,  # 7
                           -0.2172799463921295,  # 8
                           -0.20485349801296573,  # 9
                           -0.19434109211212472,  # 10
                           -0.18529696088204259,  # 11
                           -0.17740833333333336],  # 12

                    'Cu': [None,  # 0
                           -1.0074762197358971,  # 1
                           -0.71239326685944104,  # 2
                           -0.58166666666666678,  # 3
                           -0.50373810986794854,  # 4
                           -0.45055706260879619,  # 5
                           -0.41130044439017521,  # 6
                           -0.38079021846180672,  # 7
                           -0.35619663342972052,  # 8
                           -0.33582540657863236,  # 9
                           -0.31859195428217163,  # 10
                           -0.30376550964269278,  # 11
                           -0.29083333333333339]  # 12
                    }
                }

def calculate_CE(cluster):
    assert isinstance(cluster, ase.Atoms)

    # Because we're not optimizing these structures, we just take the CN from the Cu structure
    # Really, the Cu-Cu bond length is closer to 2.55, but we want to ensure we don't miss any.
    # I tested this against some analytical formulas for the CN counts in an icosahedral and octahedral cluster,
    # and it works fine.
    search_radius = 2.8

    # Generate a table of bonds present in the system.
    # For example, if bonds_table[3] were looked up and returned (0,8), this would indicate a bond exists between
    # atom 0 and atom 8
    bond_sources, bond_destinations = ase.neighborlist.neighbor_list("ij", cluster, search_radius)
    bond_table = zip(bond_sources, bond_destinations)

    # Generate a table of atom coordination numbers
    # For example, cn_table[0] returns the CN of atom 0
    cn_table = np.bincount(bond_sources)

    # Main loop
    accumulator = 0
    for bond in bond_table:
        atom1 = cluster[bond[0]]
        atom2 = cluster[bond[1]]

        addend = lookup_table[atom1.symbol][atom2.symbol][cn_table[bond[0]]]
        accumulator += addend

    # Energy in eV
    energy = accumulator / len(cluster)
    return energy
