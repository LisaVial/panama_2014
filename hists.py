import numpy as np
import matplotlib.pyplot as plt
from IPython import embed
from scipy.stats import gaussian_kde
from itertools import *
import pandas as pd


def get_dates(data_dict):
    dates = []
    for habitat in data_dict.keys():
        dates += list(data_dict[habitat].keys())
    unique_dates = list(set(dates)) # set removes duplicates, convert to list again to sort
    unique_dates.sort()
    return unique_dates


def extract_freqs_from_array(arr):
    # extract frequencies from dictionary arrays
    # input:
    # arr: array, got by indexing in a dictionary with its keys, with this datatype, it is usually a list of tuples,
    # containing fish frequencies and their amplitudes, but only the frequencies are saved in this step
    # output: freqs is a list of list with different fish frequencies (length of single lists can vary)

    freqs = []
    for pairs in arr:
        freqs.append(pairs[0])

    return np.asarray(freqs)


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
    # flat_list = [item for sublist in freqs for item in sublist]
    # print(flat_list)
    return freqs


def q10_normalizer(freqs, current_temperature):
    # ... to be continued
    # this function normalizes the frequencies of weakly electric fish according to the q10 value
    # input:
    # frequencies: flat lists of different fish frequencies
    corr_f = []
    for i in np.arange(len(freqs)):
        corr_f.append(freqs[i] * (1.62 ** ((299.65 - current_temperature) / 10)))

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
        final_data[m] = np.asarray(eodfs[m])[mask[m]]

    return final_data


def colors_func(idx):
    list = ['#BA2D22', '#F47F17', '#53379B', '#3673A4', '#AAB71B', '#DC143C', '#1E90FF']
    # list[idx % len(list)] for modulo operations
    # n_list = tuple(int(list[i:i+2], 16) for i in (0, 2, 4))
    return list[idx % len(list)]


def hab_mat_creator(habitat_data, habitat_id):
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
        # lines of different colors
        ori_freqs = freqs_from_date(habitat_data[date]['freqs_and_amps'])
        freqs = habitat_data[date]['freqs_and_amps']
        cleaned_freqs = eodfs_cleaner(freqs, 0.5)
        final_freqs = freqs_from_date(cleaned_freqs)
        original_freq_mat.append(ori_freqs)
        habitat_freq_mat.append(final_freqs)

    return habitat_freq_mat, dates


if __name__ == '__main__':
    data = np.load('fish_dict.npy').item()

    habitats = list(data.keys())
    habitats.sort()
    dates = get_dates(data)

    all_freqs = []
    all_diff_freqs = []
    all_temp_freqs = []
    diff_freqs_w_abs = []

    fig, axs = plt.subplots(1, len(habitats), figsize=(15, 6), facecolor='w', edgecolor='k', sharex=True)
    fig.subplots_adjust(hspace=.5, wspace=.001)
    axs = axs.ravel()



    fig_2, ax_2 = plt.subplots(figsize=(15, 6), facecolor='w', edgecolor='k')

    fig_3, ax_3 = plt.subplots(figsize=(15, 6), facecolor='w', edgecolor='k')

    fig_4, ax_4 = plt.subplots(figsize=(15, 6), facecolor='w', edgecolor='k')

    sex_fig, sex_ax = plt.subplots(1, len(habitats), figsize=(15,6), facecolor='w', edgecolor='k')
    sex_fig.subplots_adjust(hspace=.5, wspace=.001)
    sex_ax = sex_ax.ravel()

    colors = ['#BA2D22', '#3673A4']

    overall_female_freqs = []
    overall_male_freqs = []
    overall_sex_freqs = []

    for i in range(len(habitats)):
        habitat_freq_mat, habitat_dates = hab_mat_creator(data[habitats[i]], habitats[i])
        dates = list(data[habitats[i]].keys())
        dates.sort()

        all_norm_temp_freqs = []
        all_day_freqs = []

        female_day_freqs = []
        male_day_freqs = []
        fish_counts = [[], []]

        for j in range(len(habitat_freq_mat)):
            day_freqs = habitat_freq_mat[j]

            female_day_freqs = ([x for x in day_freqs if (x > 500.0) and (x < 700.0)])# day_freqs[(day_freqs>500.0)&(day_freqs<700.0)]
            male_day_freqs = ([x for x in day_freqs if (x > 700.0) and (x < 1000.0)])
            sex_day_freqs = [female_day_freqs, male_day_freqs]
            for k in range(len(sex_day_freqs)):
                fish_counts[k].append(len(sex_day_freqs[k]))

            temp = np.unique(data[habitats[i]][habitat_dates[j]]['temp'])[0]
            temp_freqs = q10_normalizer(day_freqs, temp)
            # lambda function in mapping function, with map() a new list is returned which contains items returned by
            # that function for each item (from docu).

            diff_freqs_no_abs = []
            for x in range(len(temp_freqs)):
                    # diff_freqs_no_abs += [(temp_freqs[x] - temp_freqs[y]) for y in range(x+1, len(temp_freqs))]
                    diff_freqs_no_abs += list(map(lambda y: temp_freqs[x] - temp_freqs[y],
                                                  list(range(x+1, len(temp_freqs)))))
            # diff_freqs = [np.abs(diff) for diff in diff_freqs_no_abs]
            diff_freqs = list(map(lambda d: np.abs(d), diff_freqs_no_abs))

            overall_female_freqs.append(female_day_freqs)
            overall_male_freqs.append(male_day_freqs)
            overall_sex_freqs.append(sex_day_freqs)

            all_day_freqs += day_freqs
            all_norm_temp_freqs += temp_freqs
            all_diff_freqs += diff_freqs
            diff_freqs_w_abs += diff_freqs_no_abs

        barWidth = 0.5
        xses = range(len(dates))
        xses2 = [x + barWidth for x in xses]
        sex_ax[i].bar(xses, fish_counts[0], width=barWidth, color=colors[0], label='females')
        sex_ax[i].bar(xses2, fish_counts[1], width=barWidth, color=colors[1], label='males')
        sex_ax[i].set_title(habitats[i])
        sex_ax[i].set_xlabel('dates')
        sex_ax[0].set_ylabel('fish count')
        sex_ax[i].set_xticks(range(len(dates)))
        sex_ax[i].set_xticklabels(dates, rotation=45)
        plt.legend(loc='best')

        all_freqs += all_day_freqs
        all_temp_freqs += all_norm_temp_freqs

        # freq_diff = np.abs(np.diff(norm_day_freqs))
        kde = gaussian_kde(all_norm_temp_freqs, .05)
        xkde = np.arange(0, 1000, 0.5)
        ykde = kde(xkde)

        axs[i].hist(all_day_freqs, bins=50, alpha=0.5, color='#BA2D22', label='original freqs')
        axs[i].hist(all_norm_temp_freqs, bins=50, alpha=0.6, color='#AAB71B', label='Q_10 corrected')
        axs[i].set_xlim([0, 1000])
        axs[i].set_title('habitat ' + habitats[i])
        axs[i].set_xlabel('frequencies [Hz]')
        axs[i].set_ylabel('rate')
        axs[i].legend(loc=1, frameon=False, ncol=2)
        ax_2.plot(xkde, ykde, color=colors_func(i), label=habitats[i], linewidth=2)
        plt.legend(loc=1, ncol=2)
        plt.legend(loc=1, ncol=2)
        plt.tight_layout()
    plt.show()

    all_kde = gaussian_kde(all_temp_freqs, .05)
    all_xkde = np.arange(0, 1000, 0.5)
    all_ykde = all_kde(all_xkde)

    ax_3.hist(all_freqs, bins=100, alpha=0.5, color='#BA2D22', label='original freqs')
    ax_3.hist(all_temp_freqs, bins=100, alpha=0.6, color='#AAB71B', label='Q_10 corrected')
    # ax_2.plot(xkde, ykde, color=colors_func(i), linewidth=2)
    ax_2.plot(all_xkde, all_ykde, color='k', label='all frequencies', linewidth=4)
    ax_3.set_xlim([0, 1000])
    ax_3.set_xlabel('frequencies [Hz]')
    ax_3.set_ylabel('rate')
    ax_2.legend(loc=1, frameon=False, ncol=2, numpoints=1)
    ax_3.legend(loc=1, frameon=False, ncol=2, numpoints=1)
    ax_4.hist(all_diff_freqs, bins =50, alpha=0.5, color='#BA2D22')
    plt.show()

    plt.hist(diff_freqs_w_abs, bins=100, alpha=0.6, color='#AAB71B')
    plt.show()

    female_freqs = [x for x in all_freqs if (x > 500.0) and (x < 700.0)]
    diff_fem_freqs = []
    for x in range(len(female_freqs)):
        diff_fem_freqs += list(map(lambda y: np.abs(female_freqs[x] - female_freqs[y]), list(range(x+1, len(female_freqs)))))

    male_freqs = [x for x in all_freqs if (x > 700.0) and (x < 1000.0)]
    diff_male_freqs = []
    for x in range(len(male_freqs)):
        diff_male_freqs += list(map(lambda y: np.abs(male_freqs[x] - male_freqs[y]), list(range(x+1, len(male_freqs)))))

    plt.hist(diff_fem_freqs)
    plt.title('female difference frequencies')
    plt.show()
    plt.hist(diff_male_freqs)
    plt.title('male difference frequencies')
    plt.show()

    sex_freqs = [[diff_fem_freqs], [diff_male_freqs]]

    fig, ax1 = plt.subplots(facecolor='w', edgecolor='k', sharex=True)
    ax1.set_title('Females and Males')
    ax1.boxplot(sex_freqs)
    ax1.set_xlabel('sexes')
    ax1.set_xticks(range(3))
    ax1.set_xticklabels(['', 'female', 'male'])
    ax1.set_ylabel('frequency difference')
    plt.show()