import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from IPython import embed
import os
import lisa_functions as li_fu
import thunderfish as th

# change directory to the thunderfish csvs:
tables_dir = r'../../programs/thunderfish_results/'
os.chdir(tables_dir)

# load fish_table as pandas data frame
fish_table_dir = 'fish_table.csv'
ft_data = pd.read_csv(fish_table_dir)
fish_dict = {col: list(ft_data[col]) for col in ft_data.columns}

filenames = np.sort([i for i in li_fu.find_all_csvs('.') if ('wavefish_eodfs.csv') in i])


def dict_creator(filenames, fish_dict):
    # function takes .csv-file ending to create an organized dictionary
    # input:
    # filename string: 'wavefish_eodfs.csv' (output of the thunderfish analyzation)
    # fish_dict: existing dictionary created from a table, which holds some important information
    # output:
    # data_dict: dictionary which organizes data to analyze the frequency distribution of transect data

    # get all filenames

    data_dict = {}
    # iterate through files
    for file in filenames:
        # load the data
        df = np.array(pd.read_csv(file))
        # split name of current file
        current_file = file.split('/')
        # change the current filename, so it can be compared to the information of the fish dict
        if 'L' in current_file[-1]:
            file_name = current_file[-1][5:8]
        else:
            file_name = current_file[-1][0:5]
        # get the date of the current file and restructure it, so it can be compared to the information of the fish dict
        date = current_file[1][0:4] + '-' + current_file[1][6:8] + '-' + current_file[1][4:6]
        # set negative index, to check existence of current file in fish dict
        index = -1
        for i in range(len(fish_dict['Habitat'])):
            if fish_dict['filename'][i] == file_name and fish_dict['Date'][i] == date:
                # print(file_name, ' belongs to ', fish_dict['filename'][i], ' at the ', fish_dict['Date'][i],
                #  ' in Habitat ', fish_dict['Habitat'][i])
                # when there's a match, change the index
                index = i
                break
        if index < 0:
            continue

        habitat = fish_dict['Habitat'][index]
        if habitat not in data_dict.keys():
            data_dict[habitat] = {}
        if date not in data_dict[habitat]:
            data_dict[habitat][date] = {'filename': [], 'freqs_and_amps': []}
        data_dict[habitat][date]['filename'].append(file_name)
        data_dict[habitat][date]['freqs_and_amps'].append(df)
    return data_dict


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

data = dict_creator(filenames, fish_dict)
# data = freq_cleaner(data, 0.5)
np.save('../../Dropbox/panama2014/fish_dict.npy', data)
os.chdir('../../Dropbox/panama2014/')
data = np.load('../../Dropbox/panama2014/fish_dict.npy').item()
#print('This is the dictionary: ', data)

habitats = list(data.keys())
habitats.sort()

for habitat in habitats:
    #print('Data for Habitat', habitat, ':', data[habitat])
    #print('Extracted freqs:')
    #print(data[habitat])
    rasterplot_for_habitat(data[habitat], habitat)





