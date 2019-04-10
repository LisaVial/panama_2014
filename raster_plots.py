import numpy as np
import matplotlib.pyplot as plt
from IPython import embed


def flatten_recording(recording):
    frequencies = []

    for pairs in recording:
        # print(a)
        # d = [pairs[0] for pairs in a]
        frequencies.append(pairs[0])

    return frequencies


def flatten_ls(data):
    f_ls = []
    for i in range(len(data)):
        for j in range(len(data[i])):
            if type(data[i][j]) == np.ndarray:
                freq = data[i][j][0]
            else:
                freq = data[i][j]
            f_ls.append(freq)

    return f_ls


def extract_freqs_from_array(arr):
    # extract frequencies from dictionary arrays
    # input:
    # arr: array, got by indexing in a dictionary with its keys, with this datatype, it is usually a list of tuples,
    # containing fish frequencies and their amplitudes, but only the frequencies are saved in this step
    # output: freqs is a list of list with different fish frequencies (length of single lists can vary)

    freqs = []
    for pairs in arr:
        freqs.append(pairs[0])

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
        final_data[m] = eodfs[m][mask[m]]

    return final_data


def colors_func(idx):
    list = ['#BA2D22', '#F47F17', '#53379B', '#3673A4', '#AAB71B', '#DC143C', '#1E90FF']
    # list[idx % len(list)] for modulo operations
    # n_list = tuple(int(list[i:i+2], 16) for i in (0, 2, 4))
    return list[idx % len(list)]


def onclick(event):
    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          ('double' if event.dblclick else 'single', event.button,
           event.x, event.y, event.xdata, event.ydata))


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

    all_colors = []
    fig, ax = plt.subplots()
    for index in range(len(dates)):
        # print(index)
        date = dates[index]
        # ori freqs: all frequencies, which were in the original recordings, in the rasterplots, they're portrayed as
        # lines of different colors
        ori_freqs = freqs_from_date(habitat_data[date]['freqs_and_amps'])
        freqs = habitat_data[date]['freqs_and_amps']
        cleaned_freqs = eodfs_cleaner(freqs, 0.5)
        final_freqs = freqs_from_date(cleaned_freqs)
        original_freq_mat.append(ori_freqs)
        habitat_freq_mat.append(final_freqs)
        # embed()
        # exit()
        o_lo = np.arange(len(dates))+0.75
        for i in range(len(freqs)):
            plot_freqs = flatten_recording(freqs[i])
            cleaned_plot_freqs = flatten_recording(cleaned_freqs[i])
            # embed()
            # exit()
            # (print(plot_freqs))

            ax.eventplot(plot_freqs, linelengths=0.5, linewidths=1.5, lineoffsets=o_lo[index],
                         colors=[colors_func(i)])


    # this passage defines the offsets, if you want to compare the frequencies of the original recordings with the
    # filtered ones
    final_lineoffsets = np.arange(len(habitat_freq_mat)) + 1.25
    ax.set_title('Habitat ' + habitat_id)
    ax.set_xlabel('frequencies [Hz]')
    ax.set_ylabel('dates')
    ax.set_xlim(400, 800)
    ax.set_yticks([1, 2, 3, 4, 5, 6, 7, 8])
    ax.set_yticklabels(dates)
    # fig.savefig('Habitat_' + habitat_id + '.pdf')
    ax.eventplot(habitat_freq_mat, orientation='horizontal', linelengths=0.5, linewidths=1.5,
             lineoffsets=final_lineoffsets, colors='k')
    # fig.savefig('Habitat_' + habitat_id + '.pdf')
    # plt.show()
    # cid = fig.canvas.mpl_connect('button_press_event', onclick)
    # print(cid)
    # color_list = ['k', 'r', 'y', 'c', 'm', 'mediumorchid', 'indigo']
    # for pl_i in range(len(freqs)):
    #         for k in range(len(color_list)):
    #             print(freqs[pl_i], str(colors_func(k)))
    #             plt.eventplot(final_freqs)
    #         plt.show()
    # fig, ax = plt.subplots()
    # ax.eventplot(original_freq_mat, orientation='horizontal', linelengths=0.5, linewidths=1.5,
    #             lineoffsets=original_lineoffsets, colors=all_colors)
    # ax.eventplot(habitat_freq_mat, orientation='horizontal', linelengths=0.5, linewidths=1.5,
    #              lineoffsets=final_lineoffsets, colors='k')
    # ax.set_title('Habitat ' + habitat_id)
    # ax.set_xlabel('frequencies [Hz]')
    # ax.set_ylabel('dates')
    # ax.set_xlim(400, 800)
    # ax.set_yticks([1, 2, 3, 4, 5, 6, 7, 8])
    # ax.set_yticklabels(dates)
    # plt.show()
    # fig.savefig('Habitat_' + habitat_id + '.pdf')

    return habitat_freq_mat


if __name__ == '__main__':
    data = np.load('fish_dict.npy').item()
    habitats = list(data.keys())
    habitats.sort()
    dates = list(data[habitats[0]].keys())
    dates.sort()

    all_day_freqs = []
    all_freqs = []
    all_norm_temp_freqs = []

    fig, axs = plt.subplots(1, len(habitats), figsize=(15, 6), facecolor='w', edgecolor='k')
    fig.subplots_adjust(hspace=.5, wspace=.001)

    axs = axs.ravel()

    for i in range(len(habitats)):
        habitat_freq_mat = rasterplot_for_habitat(data[habitats[i]], habitats[i])
        for j in range(len(habitat_freq_mat)):
            day_freqs = habitat_freq_mat[j]
            if dates[j] not in data[habitats[i]]:
                continue
            else:
                temp = np.unique(data[habitats[i]][dates[j]]['temp'])
            temp_freqs = q10_normalizer(day_freqs, temp)
            all_day_freqs.append(day_freqs)
            all_norm_temp_freqs.append(temp_freqs)
            # embed()
        flat_all_habitat_freqs = flatten_ls(all_day_freqs)
        flat_temp_freqs = flatten_ls(all_norm_temp_freqs)
        all_freqs.append(flat_all_habitat_freqs)
        all_norm_temp_freqs.append(flat_temp_freqs)
        # freq_diff = np.abs(np.diff(norm_day_freqs))

        axs[i].hist(flat_all_habitat_freqs, bins=20, alpha=0.5, color='#BA2D22', label='original freqs')
        axs[i].hist(flat_temp_freqs, bins=20, alpha=0.5, color='#AAB71B', label='Q_10 corrected')
        axs[i].set_xlim([0, 1000])
        axs[i].set_title('habitat ' + habitats[i])
        axs[i].set_xlabel('frequencies [Hz]')
        axs[i].set_ylabel('rate')
        plt.legend()
        plt.tight_layout()
    plt.show()

    flat_freqs = flatten_ls(all_freqs)
    flat_temp_freqs = flatten_ls(all_norm_temp_freqs)

    fig, ax = plt.subplots(figsize=(15, 6), facecolor='w', edgecolor='k')
    ax.hist(flat_freqs, bins=20, alpha=0.5, color='#BA2D22', label='original freqs')
    ax.hist(flat_temp_freqs, bins=20, alpha=0.5, color='#AAB71B', label='Q_10 corrected')
    ax.set_xlabel('frequencies [Hz]')
    ax.set_ylabel('rate')
    plt.legend()
    plt.show()
    # embed()
    # exit()
            # fig.savefig('df_hist' + habitat + dates[i] + '.pdf')
        #
