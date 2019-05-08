import numpy as np
import pandas as pd
from IPython import embed
import os
import lisa_functions as li_fu
from collections import OrderedDict

# change directory to the thunderfish csvs:
tables_dir = r'../../PycharmProjects/panama_2014/'
os.chdir(tables_dir)

# load fish_table as pandas data frame
fish_table_dir = 'fish_table.csv'
ft_data = pd.read_csv(fish_table_dir)
fish_dict = {col: list(ft_data[col]) for col in ft_data.columns}
filenames = np.sort([i for i in li_fu.find_all_csvs(r'../../programs/thunderfish_results/')
                     if ('wavefish_eodfs.csv') in i])
# print(fish_dict)


def dict_creator(filenames, fish_dict):
    # function takes .csv-file ending to create an organized dictionary
    # input:
    # filename string: 'wavefish_eodfs.csv' (output of the thunderfish analyzation)
    # fish_dict: existing dictionary created from a table, which holds some important information
    # output:
    # data_dict: dictionary which organizes data to analyze the frequency distribution of transect data

    # get all filenames
    # embed()
    # quit()
    data_dict = {}
    # iterate through files
    for file in filenames:
        # print(file)
        # embed()
        # load the data
        df = np.array(pd.read_csv(file))
        df = np.asarray([x for x in df if x[0] < 1000])
        # split name of current file
        current_file = file.split('/')
        # print('Current file: ', current_file)
        # change the current filename, so it can be compared to the information of the fish dict
        if 'L' in current_file[-1]:
            file_name = current_file[-1][5:8]
        else:
            file_name = current_file[-1][0:5]
        # get the date of the current file and restructure it, so it can be compared to the information of the fish dict
        date = current_file[-2][0:4] + '-' + current_file[-2][6:8] + '-' + current_file[-2][4:6]
        # embed()
        # quit()
        # set negative index, to check existence of current file in fish dict
        index = -1
        for i in range(len(fish_dict['Habitat'])):
            # embed()
            # quit()
            if fish_dict['filename'][i] == file_name and fish_dict['Date'][i] == date:
                # print(file_name, ' belongs to ', fish_dict['filename'][i], ' at the ', fish_dict['Date'][i],
                #  ' in Habitat ', fish_dict['Habitat'][i])
                # when there's a match, change the index
                index = i
                # print(index)
                break
        if index < 0:
            continue

        habitat = fish_dict['Habitat'][index]
        # embed()
        # quit()

        if habitat not in data_dict.keys():
            data_dict[habitat] = {}
        if date not in data_dict[habitat]:
            data_dict[habitat][date] = {'filename': [], 'freqs_and_amps': [], 'temp': []}

        # temp = fish_dict[habitat][date]['temperature (degrees Fahrenheit)']
        temp = fish_dict['temperature (degrees Fahrenheit)'][index]
        data_dict[habitat][date]['filename'].append(file_name)
        data_dict[habitat][date]['freqs_and_amps'].append(df)
        data_dict[habitat][date]['temp'].append(temp)
        # embed()
    return data_dict


# embed()
# exit()
data = dict_creator(filenames, fish_dict)
print(data)
# data = freq_cleaner(data, 0.5)
np.save('../../PycharmProjects/panama_2014/fish_dict.npy', data)


