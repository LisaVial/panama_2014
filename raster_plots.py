import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import os
import pandas as pd
from collections import OrderedDict
from IPython import embed


def extract_freqs_from_array(arr):
    # extract frequencies from dictionary arrays
    # input:
    # arr: array, got by indexing in a dictionary with its keys, with this datatype, it is usually a list of tuples,
    # containing fish frequencies and their amplitudes, but only the frequencies are saved in this step
    # output: freqs is a list of list with different fish frequencies (length of single lists can vary)

    freqs = []

    for pairs in arr:
        freqs.append([pairs[0]])

    return freqs


def freqs_from_date(list_of_lists):
    # this function makes a flat list out of a list from lists
    # input:
    # list_of_list: a list of sublists, which should be flattend (for the original project it was a list of lists of
    # different frequencies)
    # output:
    # flat_list: a flat list, made of the sublists from list_of_lists

    arrays = list_of_lists
    freqs = []
    for arr in arrays:
        freqs += extract_freqs_from_array(arr)
    flat_list = [item for sublist in freqs for item in sublist]
    # print(flat_list)
    return flat_list


def q10_noramlizor(freqs, current_temperature):
    # ... to be continued
    # this function normalizes the frequencies of weakly electric fish according to the q10 value
    # input:
    # frequencies: flat lists of different fish frequencies
    corr_f = []
    for i in np.arange(len(freqs)):
        corr_f.append(freqs[i] * (1.62 ** ((338.15 - current_temperature) / 10)))

    return corr_f


def eodfs_cleaner(eodfs, df_thresh):
    """
    This function checks different frequencies and amplitudes from weakly electric fish recordings and gets rid of
    similar frequencies, keeping the frequencies with the highest amplitudes (because these are the main fish in the
    recording)

    Parameters
    ----------
    eodfs: list of lists, containing tuples,
        where the first entry are the different frequencies and the second entry
        are the different amplitudes
    df_thresh: float
        threshold for defining similar frequencies, only the closest frequency to the main frequency will be
        deleted to prevent different fishs with similar frequencies to be deleted

    Returns
    -------
    final_data: list of lists
        filtered frequencies and amplitudes
    """

    mask = [np.ones(len(eodfs[i]), dtype=bool) for i in range(len(eodfs))]

    for j in range(len(eodfs)-1):
        current_eodfs = np.array(eodfs[j])
        for l in range(len(current_eodfs)):
            eodf = current_eodfs[l]
            for k in range(j+1, len(eodfs)):
                comparing_eodfs = np.array(eodfs[k])
                minidx = np.argmin(np.abs(comparing_eodfs[:,0] - eodf[0]))
                comparing_eodf = comparing_eodfs[minidx]
                if np.abs(eodf[0] - comparing_eodf[0]) < df_thresh:
                    if eodf[1] > comparing_eodf[1]:
                        mask[k][minidx] = False
                    else:
                        mask[j][l] = False

    final_data = [[]]*len(eodfs)

    for m in range(len(eodfs)):
        final_data[m] = eodfs[m][mask[m]]

    return final_data


def rasterplot_for_habitat(habitat_data, habitat_id):
    # the function gets weakly electric fish recordings. These recordings are sorted and portrayed as a raster plot,
    # containing the different fish frequencies, which were found in each habitat for each day
    # input:
    # habitat_data: dictionary (of subdictionaries) containing data of different recordings from different days
    # habitat_id: in the original project, there was a subdictionary for all the different habitats, so you need the
    # habitat keys/ids, to make clear, which habitat is processed
    # output:
    # rasterplots of the different habitats, in which each line represents recordings from one day
    dates = list(habitat_data.keys())
    dates.sort()

    habitat_freq_mat = []
    original_freq_mat = []
    for index in range(len(dates)):
        date = dates[index]
        # ori freqs: all frequencies, which were in the original recordings, in the rasterplots, they're portrayed as
        # red lines
        ori_freqs = freqs_from_date(habitat_data[date]['freqs_and_amps'])
        freqs = habitat_data[date]['freqs_and_amps']
        cleaned_freqs = eodfs_cleaner(freqs, 0.5)
        final_freqs = freqs_from_date(cleaned_freqs)
        original_freq_mat.append(ori_freqs)
        habitat_freq_mat.append(final_freqs)

    # this passage defines the offsets, if you want to compare the frequencies of the original recordings with the
    # filtered ones
    original_lineoffsets = np.arange(len(original_freq_mat)) + 0.75
    final_lineoffsets = np.arange(len(habitat_freq_mat)) + 1.25

    fig, ax = plt.subplots()
    ax.eventplot(original_freq_mat, orientation='horizontal', linelengths=0.5, linewidths=1.5,
                 lineoffsets=original_lineoffsets, colors='r')
    ax.eventplot(habitat_freq_mat, orientation = 'horizontal', linelengths=0.5, linewidths=1.5,
                 lineoffsets=final_lineoffsets, colors='k')
    ax.set_title('Habitat ' + habitat_id)
    ax.set_xlabel('frequencies [Hz]')
    ax.set_ylabel('dates')
    ax.set_xlim(400, 800)
    ax.set_yticks([1, 2, 3, 4, 5, 6, 7, 8])
    ax.set_yticklabels(dates)
    plt.show()
    fig.savefig('Habitat_' + habitat_id + '.pdf')

    return habitat_freq_mat

if __name__ == '__main__':
    os.chdir('../../PycharmProjects/panama_2014/')
    data = np.load('fish_dict.npy').item()

    habitats = list(data.keys())
    habitats.sort()
    dates = list(data[habitats[0]].keys())
    # print(dates)
    dates.sort()

    fish_table_dir = 'fish_table.csv'
    ft_data = pd.read_csv(fish_table_dir)
    fish_dict = {col: list(ft_data[col]) for col in ft_data.columns}
    od_fish_dict = OrderedDict(fish_dict.items())


    for habitat in habitats:
        habitat_freq_mat = rasterplot_for_habitat(data[habitat], habitat)
        # norm_freqs = q10_noramlizor(final_freqs)
        # embed()
        # exit()
        for i in range(len(habitat_freq_mat)):
            day_freqs = habitat_freq_mat[i]
            norm_day_freqs = q10_noramlizor(day_freqs)
            freq_diff = np.abs(np.diff(norm_day_freqs))

            # embed()
            # exit()

            # fig, ax = plt.subplots()
            # ax.hist(freq_diff, bins=20, alpha=0.5)
            # ax.set_title('distribution of frequency differences in habitat ' + habitat + ': ' + dates[i])
            # ax.set_xlabel('frequencies [Hz]')
            # ax.set_ylabel('rate')
            # plt.show()
            # fig.savefig('df_hist' + habitat + dates[i] + '.pdf')

