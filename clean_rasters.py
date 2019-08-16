import numpy as np
import matplotlib.pyplot as plt
from IPython import embed
from thunderfish.harmonicgroups import unique, similar_indices

def get_dates(data_dict):
    """
       This function gets different dates from weakly electric fish recordings from a single habitat

       Parameters
       ----------
       data_dict: dictionary, which contains all relevant data of recordings from different habitats

       Returns
       -------
       unique_dates: list of all dates, that appear in different habitats
    """
    dates = []
    for habitat in data_dict.keys():
        dates += list(data_dict[habitat].keys())
    unique_dates = list(set(dates))
    # set removes duplicates, convert to list again to sort
    unique_dates.sort()
    return unique_dates


def extract_freqs_from_array(arr):
    """
        This function extract frequencies from dictionary arrays

        Parameters
        ----------
        arr: array, got by indexing in a dictionary with its keys, with this datatype, it is usually a list of tuples,
            containing fish frequencies and their amplitudes, but only the frequencies are saved in this step

        Returns
        -------
        freqs: list of list with different fish frequencies (length of single lists can vary)
     """

    arr = list(arr)
    freqs = []
    for pairs in list(arr):
        if type(pairs) == np.float64 and pairs > 100:
            freqs.append(pairs)
        elif type(pairs) == np.float64 and pairs < 100:
            continue
        else:
            freqs.append(pairs[0])

    return freqs


def freqs_from_date(list_of_lists):
    """
        This function makes a flat list out of a list from lists

        Parameters
        ----------
        list_of_list: a list of sublists, which should be flattend (for the original project it was a list of lists of
            different frequencies)
        Returns
        -------
        flat_list: list of list with different fish frequencies (length of single lists can vary)
     """

    arrays = list_of_lists
    freqs = []
    for arr in arrays:
        freqs += extract_freqs_from_array(arr)

    return freqs


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
        final_data[m] = np.asarray(eodfs[m])[mask[m]]

    return final_data


def indices_similar_freqs(freq_mat, df_thresh):
    # embed()
    # quit()
    max_len = np.max(list(map(lambda x: len(x), freq_mat)))
    cp_freq_mat = np.full((len(freq_mat), max_len), np.nan)
    for i in range(len(freq_mat)):
        cp_freq_mat[i, :len(freq_mat[i])] = freq_mat[i]
    mask = np.full(np.shape(cp_freq_mat), np.nan)
    uni_freq = np.unique(np.hstack(cp_freq_mat))

    id_counter = 0
    for f in uni_freq:
        i0s, i1s = np.unravel_index(np.argsort(np.abs(cp_freq_mat - f), axis=None), np.shape(cp_freq_mat))
        for i0, i1 in zip(i0s, i1s):
            if cp_freq_mat[i0, i1] - f == 0:
                ori_i0, ori_i1 = i0, i1

            if np.isnan(mask[ori_i0, ori_i1]):
                id = id_counter
                id_counter += 1
                mask[ori_i0, ori_i1] = id
            else:
                id = mask[ori_i0, ori_i1]

            if np.abs(cp_freq_mat[i0, i1] - f) < df_thresh:
                if np.isnan(mask[i0, i1]):
                    mask[i0, i1] = id
            else:
                continue

    # fig, ax = plt.subplots()
    # for i in np.unique(mask)[~np.isnan(np.unique(mask))]:
    #     ax.plot(np.ones(len(cp_freq_mat[mask == i])) * i, cp_freq_mat[mask == i], 'o')
    # # plt.show()

    # embed()
    # exit()
    # for freq_ls_idx in range(len(freq_mat)):
    #     for freq_idx in range(len(freq_mat[freq_ls_idx])):
    #         freq1 = freq_mat[freq_ls_idx][freq_idx]
    #         nn = len(freq_mat) if nextfs == 0 else freq_ls_idx+1+nextfs
    #         if nn > len(freq_mat):
    #             nn = len(freq_mat)
    #         # for comp_idx in range(freq_ls_idx+1, nn):

    return cp_freq_mat, mask

def rasterplot_for_habitat(habitat_data, habitat_id):
    """
    This function gets weakly electric fish recordings. These recordings are sorted and portrayed as a raster plot,
        containing the different fish frequencies, which were found in each habitat for each day

    Parameters
    ----------
    habitat_data: dictionary (of subdictionaries) containing data of different recordings from different days
    habitat_id: in the original project, there was a subdictionary for all the different habitats, so you need the
    habitat keys/ids, to make clear, which habitat is processed

    Returns
    -------
    habitat_freq_mat: list of lists, where each list represents fish frequencies of one day and habitat
    rasterplots of the different habitats, in which each line represents recordings from one day
    """

    dates = list(habitat_data.keys())
    dates.sort()

    habitat_freq_mat = []
    habitat_temp_mat = []

    similar_freqs = []
    similar_freq_mat = []

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), facecolor='w', edgecolor='k', sharex=True, sharey=True)

    for index in range(len(dates)):
        date = dates[index]

        temp = np.unique(habitat_data[date]['temp'])
        freqs = habitat_data[date]['freqs_and_amps']

        index_list = similar_indices(freqs, 5)
        # for indices in index_list:
        #     for elements in indices:
        #         for single_tuples in elements:
        #             similar_freqs.append(freqs[single_tuples[0]][single_tuples[1]])
        #
        # similar_freq_mat.append(final_similar_freqs)
        # embed()
        # exit()

        ori_cleaned_freqs = eodfs_cleaner(freqs, 1)
        cleaned_freqs = unique(freqs, 1, mode='power')
        temp_freqs = cleaned_freqs * (1.62 ** ((299.65 - temp) / 10))


        final_freqs = freqs_from_date(cleaned_freqs)
        final_temp_freqs = freqs_from_date(temp_freqs)
        final_similar_freqs = freqs_from_date(similar_freqs)

        habitat_freq_mat.append(final_freqs)
        habitat_temp_mat.append(final_temp_freqs)

    # embed()
    # exit()
    cp_freq_mat, mask = indices_similar_freqs(habitat_temp_mat, 5)
    fig, ax = plt.subplots()
    for i in np.unique(mask)[~np.isnan(np.unique(mask))]:
        ax.plot(np.ones(len(cp_freq_mat[mask == i])) * i, cp_freq_mat[mask == i], 'o')
    # plt.show()

    colors = np.random.rand(int(np.nanmax(mask)), 3)
    color_mask = np.full((*np.shape(mask), 3), 0)

    for i in range(int(np.nanmax(mask))):
        if len(color_mask[mask == i]) > 3:
            color_mask[mask == i] = colors[i]

    list_freq_mat = []
    list_color_mask = []
    list_dada = []

    for i in range(len(color_mask)):
        list_freq_mat.append(list(cp_freq_mat[i][~np.isnan(cp_freq_mat[i])]))
        for c in color_mask[i][~np.isnan(cp_freq_mat[i])]:
            list_color_mask.append(c)
        # list_color_mask.extend(list(color_mask[i][~np.isnan(cp_freq_mat[i])]))
        list_dada.extend(np.ones(len(cp_freq_mat[i][~np.isnan(cp_freq_mat[i])])) * i)

    plt.figure()
    plt.scatter(np.hstack(list_freq_mat), list_dada, color=np.array(list_color_mask), s = 50)
    plt.show()
    # plt.figure()
    # plt.eventplot(list_freq_mat, colors=list_color_mask)
    # plt.show()
    embed()
    quit()
    for i in np.unique(mask)[~np.isnan(np.unique(mask))]:
        c = np.random.rand(3)
        plt_f = np.full(np.shape(mask), np.nan)
        plt_f[mask == i] = cp_freq_mat[mask == i]
        ax2.eventplot(cp_freq_mat[mask == i])

    ax1.set_title('Habitat ' + habitat_id)
    ax1.set_xlabel('frequencies [Hz]')
    ax1.set_ylabel('dates')
    ax1.set_xlim(500, 1000)
    ax1.set_yticks(range(len(dates)))
    ax1.set_yticklabels(dates)
    # fig.savefig('Habitat_' + habitat_id + '.pdf')
    ax1.eventplot(habitat_freq_mat, orientation='horizontal', linelengths=0.5, linewidths=1.5, colors='k')
    # plt.show()

    ax2.set_title('Q 10 corrected frequencies')
    ax2.set_xlabel('frequencies [Hz]')
    ax2.set_ylabel('dates')
    ax2.set_xlim(500, 1000)
    ax2.set_yticks(range(len(dates)))
    ax2.set_yticklabels(dates)
    # fig.savefig('Habitat_' + habitat_id + '.pdf')
    ax2.eventplot(habitat_temp_mat, orientation='horizontal', linelengths=0.5, linewidths=1.5, colors='k')
    plt.show()
    return habitat_freq_mat



def colors_func(idx):
    list = ['#BA2D22', '#F47F17', '#53379B', '#3673A4', '#AAB71B', '#DC143C', '#1E90FF']
    # list[idx % len(list)] for modulo operations
    return list[idx]


def flatten_recording(recording):
    frequencies = []

    for pairs in recording:
        frequencies.append(pairs[0])

    return frequencies


if __name__ == '__main__':
    data = np.load('fish_dict.npy').item()

    habitats = list(data.keys())
    habitats.sort()
    dates = get_dates(data)

    for i in range(len(habitats)):
        habitat_freq_mat = rasterplot_for_habitat(data[habitats[i]], habitats[i])