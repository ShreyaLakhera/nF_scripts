import sys
import json

params_list = sys.argv[1].split(',')
outfilename = sys.argv[2]

params_dict = {


    "g_ach_pn" : 0.0,
    "g_ach_ln" : 0.1,
    "g_fgaba_pn" : 1.0,
    "g_fgaba_ln" : 0.6,

    "g_sgaba_pn" : 0.0,
    "g_sgaba_ln" : 0.0,


    "p0_ach" : 1,
    "deltap_ach" : 0.0,
    "maxp_ach" : 1,
    "tauf_ach" : 15000,
    "p_ach" : 1,

    "p0_fgaba_ln" : 1,
    "deltap_fgaba_ln" : 0,
    "maxp_fgaba_ln" : 1,
    "tauf_fgaba_ln" : 14000,
    "p_fgaba_ln" : 1,

    "p0_fgaba_pn" : 1,
    "deltap_fgaba_pn" : 0,
    "maxp_fgaba_pn" : 1,
    "tauf_fgaba_pn" : 17000,
    "p_fgaba_pn" : 1,

    "p0_sgaba" : 0.1,
    "deltap_sgaba" : 0,
    "maxp_sgaba" : 1,
    "tauf_sgaba" : 14000,
    "p_sgaba" : 0.1,

    "peakcurrent_PN" : 5.5,
    "peakcurrent_LN" : 3.0

}

params_dict['g_ach_pn'] = float(params_list[0])
params_dict['g_ach_ln'] = float(params_list[1])
params_dict['g_fgaba_pn'] = float(params_list[2])
params_dict['g_fgaba_ln'] = float(params_list[3])

with open(outfilename, 'w') as outfile:
    json.dump(params_dict, outfile, indent=4)
