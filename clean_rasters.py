import numpy as np
import matplotlib.pyplot as plt
from IPython import embed
from thunderfish.harmonicgroups import unique

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

    freqs = []
    for pairs in arr:
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
    # embed()
    # exit()
    habitat_freq_mat = []
    habitat_temp_mat = []

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), facecolor='w', edgecolor='k', sharex=True, sharey=True)
    for index in range(len(dates)):
        date = dates[index]
        temp = np.unique(habitat_data[date]['temp'])
        freqs = habitat_data[date]['freqs_and_amps']
        embed()
        exit()
        ori_cleaned_freqs = eodfs_cleaner(freqs, 1)
        cleaned_freqs = unique(freqs, 1, mode='power')
        temp_freqs = cleaned_freqs * (1.62 ** ((299.65 - temp) / 10))
        final_freqs = freqs_from_date(cleaned_freqs)
        final_temp_freqs = freqs_from_date(temp_freqs)
        habitat_freq_mat.append(final_freqs)
        habitat_temp_mat.append(final_temp_freqs)
    print(habitat_temp_mat)
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
    return list[idx % len(list)]


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