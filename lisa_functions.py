import os
import numpy as np
import matplotlib.pyplot as plt
from IPython import embed
import math


def find_all_csvs(in_path):
    # finds all csv files in the folder 'in_path' (including any subfolders)
    # returns a list of absolute paths to the found csv files
    found_files = []

    for root, directories, files in os.walk(in_path):
        for name in files:
            # get file extension (e.g. txt, csv)
            unused, file_extension = os.path.splitext(name)
            # compare (using lower case) and find especially the fish freq files
            if file_extension.lower() == '.csv':
                # add to list
                found_files.append(os.path.join(root, name))
    return found_files


def freq_raster(xses_list, titles_list, x_label, x_lim, y_label, y_tick_labels):
    # plot all frequencies of a day as a plot raster diagramm
    for i in np.arange(len(xses_list)):
        for j in np.arange(len(xses_list[i])):
            for k in np.arange(len(xses_list[i][j])):
                plt.plot((xses_list[i][j][k], xses_list[i][j][k]), (j-0.5, j+0.5), 'k-')
                plt.title(str(titles_list[i]))
                plt.xlabel(str(x_label))
                plt.xlim(x_lim)
                plt.ylabel(str(y_label))
                plt.ylim([-0.75, len(y_tick_labels)])
                plt.yticks([0, 1, 2, 3, 4, 5, 6, 7], y_tick_labels)
                plt.savefig(titles_list[i]+'.pdf')
        plt.show()
    return


def matrix_creator(freq_list):
    # for a given list of lists (of frequencies) the matrix_creator creates a matrix, with the length of the previous
    # list and the shape of the list of the maximum length
    max_len = np.max([len(freq_list[i]) for i in np.arange(len(freq_list))])
    freq_matrix = np.full((len(freq_list), max_len), np.nan)
    for i in np.arange(len(freq_list)):
        freq_matrix[i, :len(freq_list[i])] = freq_list[i]

    return freq_matrix


def find_interesting_ls_idx(freq_matrix):
    # this function compares the frequencies of a given matrix and checks if some values are mostly equal
    indices = []
    for current_list in np.arange(len(freq_matrix)):
        for current_frequency in np.arange(len(freq_matrix[current_list])):
            cf = freq_matrix[current_list, current_frequency]
            # use np.argsort() that the function gets the indices of the whole matrix
            ls_idx, idx = np.unravel_index(np.argsort(np.abs(freq_matrix - cf), axis=None), np.shape(freq_matrix))
            indices.append(ls_idx)
            indices.append(idx)
    return indices


def freq_comparison(freq_ls, amps_lst, threshold):
    similar_freqs = []
    amplitudes = []
    for idx, freq in enumerate(freq_ls):
        current_freq = freq
        for i in np.arange(len(freq_ls)):
            if current_freq == freq_ls[i]:
                continue
            for j in np.arange(len(current_freq)):
                for k in np.arange(len(freq_ls[i])):
                    if np.abs(current_freq[j] - freq_ls[i][k]) < threshold:
                        similar_freqs.append([current_freq[j], idx, j, i, k])
                        amplitudes.append([amps_lst[i][k], i, k])
    return similar_freqs, amplitudes


def get_amps(same_freq_lst, amps_lst, threshold):
    freqs_only = []
    for i in np.arange(len(same_freq_lst)):
        freqs_only.append(same_freq_lst[i][0])
    indices = np.argsort(freqs_only)
    amplitude = []
    amplitudes = [[]]
    for i in np.arange(len(same_freq_lst)-1):
        if np.abs(same_freq_lst[indices[i]][0] - same_freq_lst[indices[i+1]][0]) < threshold:
            amplitude = amps_lst[same_freq_lst[indices[i]][-2]][same_freq_lst[indices[i]][-1]]
            amplitudes[-1].append([amplitude, same_freq_lst[indices[i]][-2], same_freq_lst[indices[i]][-1]])
        elif np.abs(same_freq_lst[indices[i]][0] - same_freq_lst[indices[i+1]][0]) >= threshold:
            amplitude = amps_lst[same_freq_lst[indices[i]][-2]][same_freq_lst[indices[i]][-1]]
            amplitudes[-1].append([amplitude, same_freq_lst[indices[i]][-2], same_freq_lst[indices[i]][-1]])
            amplitudes.append([])
    if len(same_freq_lst) != len(amplitudes):
        amplitude = amps_lst[same_freq_lst[indices[-1]][-2]][same_freq_lst[indices[-1]][-1]]
        amplitudes[-1].append([amplitude, same_freq_lst[indices[i]][-2], same_freq_lst[indices[i]][-1]])
    return indices, amplitudes


def freq_selection(amp_ls):
    amps_only = [[]]
    max_amps = []
    amp_indices = []
    saving_amps = []
    saving_freqs = []
    for current_amp_ls in np.arange(len(amp_ls)):
        for current_amp in np.arange(len(amp_ls[current_amp_ls])):
            amps_only[-1].append(amp_ls[current_amp_ls][current_amp][0])
        amps_only.append([])
    del amps_only[-1]
    # amps_only = np.array(amps_only, dtype=np.float32)   # convert type to avoid getting an error with np.nanmax
    for comparing_amps in np.arange(len(amps_only)):
        max_amps.append(np.nanmax(amps_only[comparing_amps], axis=0))
    for ls_idx in np.arange(len(amps_only)):
        idx = amps_only[ls_idx].index(max_amps[ls_idx])
        amp_indices.append([ls_idx, idx])
    for i in np.arange(len(amp_ls)):
        saving_amps.append(amp_ls[i][amp_indices[i][1]])
    return amps_only, max_amps, amp_indices, saving_amps


def entry_remover(amp_list, list_of_removing_values):
    del_amps = []
    for i in range(len(amp_list)):
        for j in range(len(amp_list[i])):
            if amp_list[i][j] not in list_of_removing_values:
                del_amps.append(amp_list[i][j])
            else:
                continue
    # # test only
    # for index in range(min(len(del_amps[0]), len(del_amps[1]))):
    #     print(del_amps[0][index], "vs", del_amps[1][index])
    # # end of test
    #
    # del_amps = del_amps[0]
    return del_amps


def get_rid_of_double_entries(list):
    name_of_new_list = []
    for i in np.arange(len(list)):
        if list[i] not in name_of_new_list:
            name_of_new_list.append(list[i])

    return name_of_new_list
