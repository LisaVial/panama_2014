import numpy as np
from IPython import embed

def unify_eodfs(eodfs, df_thresh):

    mask = [np.ones(len(eodfs[i]), dtype=bool) for i in range(len(eodfs))]
    for j in range(len(eodfs)-1):
        for i, freqi in reversed(list(enumerate(eodfs[j]))):
            for k, freqk in enumerate(eodfs[j+1]):
                print(freqi, ' is compared to ', freqk)
                if np.abs(freqi[0]-freqk[0]) < df_thresh:
                    if freqi[1] > freqk[1]:
                        mask[j+1][k] = False
                        # eodfses[j+1] = np.delete(eodfses[j+1], k, axis=0)
                    else:
                        # eodfses[j] = np.delete(eodfses[j], len(eodfs[j])-i-1, axis=0)
                        mask[j][i] = False
                    break
    eodfs = np.array(eodfs)
    final_data = [[]]*len(eodfs)
    for l in range(len(eodfs)):
        final_data[l] = eodfs[l][mask[l]]

    return final_data


def eodfs_cleaner(eodfs, df_thresh):

    mask = [np.ones(len(eodfs[i]), dtype=bool) for i in range(len(eodfs))]

    for j in range(len(eodfs)-1):
        # print('j=',j)
        current_eodfs = np.array(eodfs[j])
        # embed()
        for l in range(len(current_eodfs)):
            # print('l=', l)
            eodf = current_eodfs[l]
            for k in range(j+1, len(eodfs)):
                # print('k=', k)
                comparing_eodfs = np.array(eodfs[k])
                minidx = np.argmin(np.abs(comparing_eodfs[:,0] - eodf[0]))
                comparing_eodf = comparing_eodfs[minidx]
                print(eodf, ' is compared to ', comparing_eodf)
                if np.abs(eodf[0] - comparing_eodf[0]) < df_thresh:
                    # # for m in range(len(comparing_eodfs)):
                    # # # print('m=', m)
                    # # # print(j,l,k,m)
                    # # minidx = np.argmin(np.abs(comparing_eodfs-eodfs))
                    # # comparing_eodf = comparing_eodfs[m]
                    # # print(eodf, ' is compared to ', comparing_eodf)
                    # if np.abs(eodf[0] - comparing_eodf[0]) < df_thresh:

                        if eodf[1] > comparing_eodf[1]:
                            mask[k][minidx] = False
                            # eodfses[j+1] = np.delete(eodfses[j+1], k, axis=0)
                            # continue
                        else:
                            # eodfses[j] = np.delete(eodfses[j], len(eodfs[j])-i-1, axis=0)
                            mask[j][l] = False
                            # continue
                        # break
        print('mask changed: ', mask)
    final_data = [[]]*len(eodfs)

    for m in range(len(eodfs)):
        final_data[m] = eodfs[m][mask[m]]

    return final_data


if __name__ == '__main__':
    test = [np.array([[500, -5], [653.6, -37], [805.6, -7]]), np.array([[654, -36]]), np.array([[806, -79]]),
            np.array([[500.3, -4], [653.8, -100], [500.4, -16], [805.8, -8]]),
            np.array([[653.8, -14], [805.7, -81]])]

    final_test = unify_eodfs(test, 0.5)

    comparing_final_test = eodfs_cleaner(test, 0.5)

    print('original data: ', test)
    print('after Jans function: ', final_test)
    print('new approach: ', comparing_final_test)

