import numpy as np
import matplotlib.pyplot as plt
import json
from mpl_toolkits.axes_grid1 import make_axes_locatable

def getData(add,nB):
    nB = 4
    for _i in list(range(1,nB+1)):
        if _i == 1:
            p1 = np.load(add + "batch1_part_1.npy")
            p2 = np.load(add + "batch1_part_2.npy")
            data = np.vstack((p1,p2))
        else:
            p1 = np.load(add + "batch" + str(_i) + "_part_1.npy")
            p2 = np.load(add + "batch" + str(_i) + "_part_2.npy")
            p = np.vstack((p1,p2))
            data = np.vstack((data,p))
    return data

PN_tV = 40 # Threshold Potential of PNs
LN_tV = -20 # Threshold Potential of LNs
PN_sd = 10 # Spike duration of PNs
LN_sd = 20 # Spike duration of LNs

nPN = 90
nLN = 30
nN = nPN + nLN

nB = 4

add = '/home/shreya/work/AL_90_30/nF1/results/gLN0.6LNPN1.3PNLN0.1_extPN7LN4_lowPN4.5LN2_pd1000/'
data = getData(add,nB)
current = np.load(add + 'current.npy')

V_PN = np.transpose(data[:,:nPN])
V_LN = np.transpose(data[:,nPN:nN])

t = np.size(V_PN)/(90*100)
x = t*5/90

print(np.shape(V_PN[:,50000:]))
print(np.shape(V_LN[:,50000:]))
print(np.shape(current[:,50000:]))

fig, (ax1,ax2,ax3,ax4) = plt.subplots(4,1,sharex=True)

img1 = ax1.imshow(np.transpose(V_PN[:,50000:]),cmap='binary')
divider = make_axes_locatable(plt.gca())
cax1 = divider.append_axes("right","1%",pad="1%")
plt.colorbar(img1,cax=cax1)
plt.setp(ax1.get_xticklabels(), visible=False)

img2 = ax2.imshow(np.transpose(V_LN[:,50000:]),cmap='binary')
divider = make_axes_locatable(plt.gca())
cax2 = divider.append_axes("right","1%",pad="1%")
plt.colorbar(img2,cax=cax2)
plt.setp(ax2.get_xticklabels(), visible=False)

img3 = ax3.imshow(np.transpose(current[:,50000:]))
divider = make_axes_locatable(plt.gca())
cax3 = divider.append_axes("right","1%",pad="1%")
plt.colorbar(img3,cax=cax3)
plt.setp(ax3.get_xticklabels(), visible=False)

plt.plot(current[45,50000:])
plt.setp(ax4.get_xticklabels(), fontsize=6)

plt.savefig('test.png')
plt.show()
