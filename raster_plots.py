import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from IPython import embed
import os
import lisa_functions as li_fu
import thunderfish as th


def freq_cleaner(data, threshold):
    # check, if frequencies appear more often and delete the repeating ones with smaller amplitudes
    # input:
    # data: dictionary, which shows the arrays of frequencies and amplitudes
    # output:
    # clean_data: array of freq lists without double/similar entries
    for i in range(len(data)):
        current_freqs = data[i]
        # print('current freqs: ', current_freqs)
        for j in reversed(range(len(current_freqs))):
            cf = current_freqs[j]
            # print('current freq: ', cf)
            # this block might cause problems, because i + 1 should now call the array of the frequencies of the next
            # day, and not just the next value
            # for k in range(i + 1, len(data)):
            for k in range(i + 1, len(current_freqs)):
                # comparing_freqs = data[k]
                comparing_freqs = current_freqs[k]
                break_k = False
                for l in reversed(range(len(comparing_freqs))):
                    comp = comparing_freqs[l]
                    print('comparing freq: ', comp)
                    if len(cf) > 1 & len(comp) > 1:
                        if np.abs(cf[0] - comp[0]) < threshold:
                            if comp[1] < cf[1]:
                                # print('DELETE: ', data[k][l], data[k].shape, l)
                                data[k] = np.delete(data[k], l, axis=0)
                            else:
                                # print('DELETE: ', data[i][j], data[i].shape, j)
                                data[i] = np.delete(data[i], j, axis=0)
                                break_k = True
                                break
                    else:
                        if np.abs(cf - comp) < threshold:
                            if comp < cf:
                                print('DELETE: ', data[k][l], data[k].shape, l)
                                data[k] = np.delete(data[k], l, axis=0)
                            else:
                                print('DELETE: ', data[i][j], data[i].shape, j)
                                data[i] = np.delete(data[i], j, axis=0)
                                break_k = True
                                break
                            break
                if break_k:
                    break
    #print('Hopefully everything was deleted: ', data)
    return data


def extract_freqs_from_array(arr):
    # extract frequencies from the dictionary arrays
    freqs = []
    for pairs in arr:
      freqs.append(pairs[0])

    return freqs


def freqs_from_date(date_data, date):
    # get arrays from the dictionary, according to date
    arrays = date_data['freqs_and_amps']
    freqs = []
    for arr in arrays:
      freqs += extract_freqs_from_array(arr)

    return freqs


def rasterplot_for_habitat(habitat_data, habitat_id):
    # sort frequencies
    dates = list(habitat_data.keys())
    dates.sort()

    habitat_freq_mat = []
    #print('Sorted dates for habitat "' + habitat_id + '":', dates)
    for index in range(len(dates)):
        date = dates[index]
        freqs = freqs_from_date(habitat_data[date], date)
        habitat_freq_mat.append(freqs)
    print('This is the matrix: ', habitat_freq_mat)

    # habitat_freq_mat = freq_cleaner(habitat_freq_mat, 0.5)
    # print('CLEANED? ', habitat_freq_mat)
    # inch_factor = 2.54
    fig, ax = plt.subplots()
    ax.eventplot(habitat_freq_mat, orientation = 'horizontal', linelengths = 1, colors='k')
    ax.set_title('Habitat ' + habitat_id)
    ax.set_xlabel('frequencies [Hz]')
    ax.set_ylabel('dates')
    ax.set_xlim(400, 800)
    ax.set_yticks(range(len(dates)))
    ax.set_yticklabels(dates)
    plt.show()
    #fig.savefig('../../Dropbox/panama2014/' + habitat_id + '_zoom.pdf')

os.chdir('../../Dropbox/panama2014/')
data = np.load('../../Dropbox/panama2014/fish_dict.npy').item()
# print('This is the dictionary: ', data)

habitats = list(data.keys())
habitats.sort()

for habitat in habitats:
    # print('Data for Habitat', habitat, ':', data[habitat])
    #  print('Extracted freqs:')
    #  print(data[habitat])
    rasterplot_for_habitat(data[habitat], habitat)
