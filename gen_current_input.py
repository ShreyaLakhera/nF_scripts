import numpy as np
import sys
import matplotlib.pyplot as plt

"""
Created by Shreya Lakhera on 19 March 2019 for nerveFlow implementation

Inputs

1 - time of 1 batch of simulation, number of batches
2 - type of PN current - 0 
3 - PN current details separated by ',' see below
4 - type of LN current - 0
5 - LN current details separated by ',' see below

Need to add - kinds of external current (gaussian distributed current input)

"""

nPN = 90
nLN = 30
nN = nPN + nLN

tT, nB = float(sys.argv[1].split(',')[0]), int(sys.argv[1].split(',')[1])
t = 0.01

aT = np.arange(0, tT, t)

current_input = np.zeros((nN, len(aT)))

# PN current

if int(sys.argv[2]) == 0:
        iC = [_i for _i in sys.argv[3].split(',')]
        nSN = int(iC[0])                    # number of stimulated neurons
        mSN = int(iC[1])                    # middle of the stimulated neurons
        cSN = float(iC[2])                  # current to stimulated neurons
        cNSN = float(iC[3])                 # current to non-stimulated neurons
        bcN = float(iC[4])                  # base current to all neurons
        thN = float(iC[5])                  # threshold current for width calculation
        stC = int(iC[6])                    # start time for current
        etC = int(iC[7])                    # end time for current
        rR = float(iC[8])                   # rate of rise of current
        rF = float(iC[9])                   # rate of fall of current
       
        _t = np.arange(stC, etC, t)                                                         # Time during ext current inc
        _t2 = np.arange(etC, tT, t)                                                         # Time after ext current inc
        
        _cS = cSN + (bcN - cSN)*np.exp(-(_t - stC)/rR)                                      # value of current to stimulated neurons during ext current inc
        _cAS = bcN + (cSN - bcN)*np.exp(-(_t2 - etC)/rF)                                    # value of current to stimulated neurons after ext current inc
        
        _cNS = cNSN + (bcN - cNSN)*np.exp(-(_t - stC)/rR)                                   # value of current to non-stimulated neurons during current inc
        _cANS = bcN + (cNSN - bcN)*np.exp(-(_t2 - etC)/rF)                                  # value of current to non-stimulated neurons after current inc

        current_input[:nPN,:] = bcN
        current_input[int(mSN-(nSN/2)):int(mSN+(nSN/2)),stC*100:etC*100] = _cS              # current to stimulated neurons during external current inc
        current_input[int(mSN-(nSN/2)):int(mSN+(nSN/2)),etC*100:] = _cAS                    # current to stimulated neurons after external current
        current_input[:int(mSN-(nSN/2)),stC*100:etC*100] = _cNS                             # current to non-atimulated neurons during ext current inc
        current_input[:int(mSN-(nSN/2)),etC*100:] = _cANS                                   # current to non-stimulated neurons after ext current inc
        current_input[int(mSN+(nSN/2)):nPN,stC*100:etC*100] = _cNS                          # current to non-stimulated neurons during ext current inc
        current_input[int(mSN+(nSN/2)):nPN,etC*100:] = _cANS                                # current to non-stimulated neurons after ext current inc

        cS_PN = np.hstack((_cS,_cAS)) - bcN
        cNS_PN = np.hstack((_cNS,_cANS)) - bcN
        nSN_PN = nSN
        mSN_PN = mSN
        stC_PN = stC
        bcPN = bcN

elif int(sys.argv[2]) == 1:
        iC = [_i for _i in sys.argv[3].split(',')]
        nSN = int(iC[0])                    # number of stimulated neurons
        mSN = int(iC[1])                    # middle of the stimulated neurons
        cSN = float(iC[2])                  # maximum current to stimulated neurons
        cNSN = float(iC[3])                 # low current to non-stimulated neurons
        bcN = float(iC[4])                  # base current to all neurons
        thN = float(iC[5])                  # threshold current for width calculation
        stC = int(iC[6])                    # start time for current
        etC = int(iC[7])                    # end time for current
        rR = float(iC[8])                   # rate of rise of current
        rF = float(iC[9])                   # rate of fall of current

        _gH = cSN - cNSN                                        # Height of gaussian
        _gtN = thN - cNSN
        print([_gH,_gtN])
        _gS = nSN/2 * np.sqrt(-1/(2*np.log(_gtN/_gH)))          # Sigma for gaussian
        _idN = np.arange(0,nPN)
        _gmaxN = _gH * np.exp(-(_idN-mSN)**2/(2*(_gS**2)))
       
        print(mSN-nSN/2)

        _gmaxN[:int(mSN-(nSN/2))] = 0
        _gmaxN[int(mSN+(nSN/2)):] = 0
        _gmaxN += cNSN

        _t = np.arange(stC, etC, t)                                                         # Time during ext current inc
        _t2 = np.arange(etC, tT, t)                                                         # Time after ext current inc
        
        _cS = np.zeros((nPN,np.size(_t)))
        _cAS = np.zeros((nPN,np.size(_t2)))
        for i in range(nPN):
                _cS[i] = _gmaxN[i] + (bcN - _gmaxN[i])*np.exp(-(_t - stC)/rR)
                _cAS[i] = bcN + (_gmaxN[i] - bcN)*np.exp(-(_t2 - etC)/rF)                                          # value of current to stimulated neurons after

        current_input[:nPN,:] = bcN
        current_input[:nPN,stC*100:etC*100] = _cS
        current_input[:nPN,etC*100:] = _cAS

        cS_PN = np.hstack((_cS[int(mSN-(nSN/2)):int(mSN+(nSN/2)),:], _cAS[int(mSN-(nSN/2)):int(mSN+(nSN/2)),:])) - bcN
        cNS_PN1 = np.hstack((_cS[:int(mSN-(nSN/2)),:], _cAS[:int(mSN-(nSN/2)),:])) - bcN
        cNS_PN2 = np.hstack((_cS[int(mSN+(nSN/2)):,:], _cAS[int(mSN+(nSN/2)):,:])) - bcN
        cNS_PN = np.vstack((cNS_PN1,cNS_PN2))
        nSN_PN = nSN
        mSN_PN = mSN
        stC_PN = stC
        bcPN = bcN


# LN current

if int(sys.argv[4]) == 0:
        iC = [_i for _i in sys.argv[5].split(',')]
        nSN = int(iC[0])                    # number of stimulated neurons
        mSN = int(iC[1])                    # middle of the stimulated neurons
        cSN = float(iC[2])                  # current to stimulated neurons
        cNSN = float(iC[3])                 # current to non-stimulated neurons
        bcN = float(iC[4])                  # base current to all neurons
        thN = float(iC[5])                  # threshold current for width calculation
        stC = int(iC[6])                    # start time for current
        etC = int(iC[7])                    # end time for current
        rR = float(iC[8])                   # rate of rise of current
        rF = float(iC[9])                   # rate of fall of current
       
        _t = np.arange(stC, etC, t)                                                         # Time during ext current inc
        _t2 = np.arange(etC, tT, t)                                                         # Time after ext current inc
        
        _cS = cSN + (bcN - cSN)*np.exp(-(_t - stC)/rR)                                      # value of current to stimulated neurons during ext current inc
        _cAS = bcN + (cSN - bcN)*np.exp(-(_t2 - etC)/rF)                                    # value of current to stimulated neurons after ext current inc
        
        _cNS = cNSN + (bcN - cNSN)*np.exp(-(_t - stC)/rR)                                   # value of current to non-stimulated neurons during current inc
        _cANS = bcN + (cNSN - bcN)*np.exp(-(_t2 - etC)/rF)                                  # value of current to non-stimulated neurons after current inc

        current_input[nPN:,:] = bcN
        current_input[nPN+int(mSN-(nSN/2)):nPN+int(mSN+(nSN/2)),stC*100:etC*100] = _cS
        current_input[nPN+int(mSN-(nSN/2)):nPN+int(mSN+(nSN/2)),etC*100:] = _cAS
        current_input[nPN:nPN+int(mSN-(nSN/2)),stC*100:etC*100] = _cNS
        current_input[nPN:nPN+int(mSN-(nSN/2)),etC*100:] = _cANS
        current_input[nPN+int(mSN+(nSN/2)):,stC*100:etC*100] = _cNS
        current_input[nPN+int(mSN+(nSN/2)):,etC*100:] = _cANS

        cS_LN = np.hstack((_cS, _cAS)) - bcN
        cNS_LN = np.hstack((_cNS, _cANS)) - bcN
        nSN_LN = nSN
        mSN_LN = mSN
        stC_LN = stC
        bcLN = bcN

elif int(sys.argv[4]) == 1:
        iC = [_i for _i in sys.argv[5].split(',')]
        nSN = int(iC[0])                    # number of stimulated neurons
        mSN = int(iC[1])                    # middle of the stimulated neurons
        cSN = float(iC[2])                  # maximum current to stimulated neurons
        cNSN = float(iC[3])                 # low current to non-stimulated neurons
        bcN = float(iC[4])                  # base current to all neurons
        thN = float(iC[5])                  # threshold current for width calculation
        stC = int(iC[6])                    # start time for current
        etC = int(iC[7])                    # end time for current
        rR = float(iC[8])                   # rate of rise of current
        rF = float(iC[9])                   # rate of fall of current

        _gH = cSN - cNSN                                        # Height of gaussian
        _gtN = thN - cNSN
        print([_gH,_gtN])
        _gS = nSN/2 * np.sqrt(-1/(2*np.log(_gtN/_gH)))          # Sigma for gaussian
        _idN = np.arange(0,nLN)
        _gmaxN = _gH * np.exp(-(_idN-mSN)**2/(2*(_gS**2)))

        _gmaxN[:int(mSN-(nSN/2))] = 0
        _gmaxN[int(mSN+(nSN/2)):] = 0
        _gmaxN += cNSN

        _t = np.arange(stC, etC, t)                                                         # Time during ext current inc
        _t2 = np.arange(etC, tT, t)                                                         # Time after ext current inc
        
        _cS = np.zeros((nLN,np.size(_t)))
        _cAS = np.zeros((nLN,np.size(_t2)))

        for i in range(nLN):
                _cS[i] = _gmaxN[i] + (bcN - _gmaxN[i])*np.exp(-(_t - stC)/rR)
                _cAS[i] = bcN + (_gmaxN[i] - bcN)*np.exp(-(_t2 - etC)/rF)                                          # value of current to stimulated neurons after

        current_input[nPN:,:] = bcN
        current_input[nPN:,stC*100:etC*100] = _cS
        current_input[nPN:,etC*100:] = _cAS

        cS_LN = np.hstack((_cS[int(mSN-(nSN/2)):int(mSN+(nSN/2)),:], _cAS[int(mSN-(nSN/2)):int(mSN+(nSN/2)),:])) - bcN
        cNS_LN1 = np.hstack((_cS[:int(mSN-(nSN/2)),:], _cAS[:int(mSN-(nSN/2)),:])) - bcN
        cNS_LN2 = np.hstack((_cS[int(mSN+(nSN/2)):,:], _cAS[int(mSN+(nSN/2)):,:])) - bcN
        cNS_LN = np.vstack((cNS_LN1,cNS_LN2))
        nSN_LN = nSN
        mSN_LN = mSN
        stC_LN = stC
        bcLN = bcN



current = np.hstack((current_input,)*nB)

if sys.argv[6] != 0:
        _offset_time = float(sys.argv[6])
        _offset_timesteps = 100 * int(_offset_time)
        curr1 = np.zeros((nN,  _offset_timesteps))
        curr1[:nPN,:].fill(bcPN)
        curr1[nPN:,:].fill(bcLN)

current = np.hstack((curr1,current))

noise = np.random.uniform(-0.1*current,0.1*current,np.shape(current))
current += noise

np.save("current", current)

plt.figure(1)
plt.imshow(current,aspect='auto')
plt.savefig('current.png')
"""
nS_PN_time = int((tT - stC_PN)*100)
nS_LN_time = int((tT - stC_LN)*100)

noise_S_PN = np.hstack((0.05*cS_PN,)*nB)
noise_NS_PN = np.hstack((0.05*cNS_PN,)*nB)
noise_S_LN = np.hstack((0.05*cS_LN,)*nB)
noise_NS_LN = np.hstack((0.05*cNS_LN,)*nB)

noiseSN_PN = np.random.uniform(-noise_S_PN,noise_S_PN,(nSN_PN,nS_PN_time*nB))
noiseNSN_PN = np.random.uniform(-noise_NS_PN,noise_NS_PN,(nPN-nSN_PN,nS_PN_time*nB))
noiseSN_LN = np.random.uniform(-noise_S_LN,noise_S_LN,(nSN_LN,nS_LN_time*nB))
noiseNSN_LN = np.random.uniform(-noise_NS_LN,noise_NS_LN,(nLN-nSN_LN,nS_LN_time*nB))


S_PN = list(range(int(mSN_PN-(nSN_PN/2)),int(mSN_PN+(nSN_PN/2)),1))
S_LN = list(range(nPN+int(mSN_LN-(nSN_LN/2)),nPN+int(mSN_LN+(nSN_LN/2)),1))

NS_PN = list(range(0, int(mSN_PN-(nSN_PN/2)), 1)) + list(range(int(mSN_PN+(nSN_PN/2)), nPN, 1))
NS_LN = list(range(nPN, nPN+int(mSN_LN-(nSN_LN/2)), 1)) + list(range(nPN+int(mSN_LN+(nSN_LN/2)), nN, 1))


t_PN = []
t_LN = []

for _i in list(range(nB)):
        _t_PN = [int(_x) for _x in list(np.arange(stC_PN+_i*tT,tT+_i*tT,0.01)*100)]
        _t_LN = [int(_x) for _x in list(np.arange(stC_LN+_i*tT,tT+_i*tT,0.01)*100)] 

        t_PN += _t_PN
        t_LN += _t_LN

print(len(S_PN))
print(len(t_PN))

current[np.r_[S_PN],np.c_[t_PN]] += np.transpose(noiseSN_PN)
current[np.r_[NS_PN],np.c_[t_PN]] += np.transpose(noiseNSN_PN)
current[np.r_[S_LN],np.c_[t_LN]] += np.transpose(noiseSN_LN)
current[np.r_[NS_LN],np.c_[t_LN]] += np.transpose(noiseNSN_LN)



"""
