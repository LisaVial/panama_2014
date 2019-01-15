import os
import numpy as np
from IPython import embed
import matplotlib.pyplot as plt
import csv
import lisa_functions as li_fu
import pandas as pd

# load fish_table as pandas data frame
fish_table_dir = r'/home/lisa/PycharmProjects/panama_data/fish_table.csv'
ft_data = pd.read_csv(fish_table_dir)
fish_dict = {col: list(ft_data[col]) for col in ft_data.columns}
fish_dict['frequencies'] = []
fish_dict['amplitudes'] = []

# get different days and habitats, to store the thunderfisch frequencies right
unique_habitats = np.unique(fish_dict['Habitat'])
unique_habitats = [x for x in unique_habitats if str(x) != 'nan']
unique_date = np.unique(fish_dict['Date'])

# open new lists, to store the frequencies in them
habitat_a_freqs = []
habitat_a_amps = []

habitat_b_freqs = []
habitat_b_amps = []

habitat_c_freqs = []
habitat_c_amps = []

habitat_d_freqs = []
habitat_d_amps = []

habitat_e_freqs = []
habitat_e_amps = []

habitat_f_freqs = []
habitat_f_amps = []

habitat_g_freqs = []
habitat_g_amps = []

# change directory to the thunderfish csvs:
tables_dir = r'../../programs/thunderfish_results/'
os.chdir(tables_dir)

# get file names to iterate through them
file_names = np.sort([i for i in li_fu.find_all_csvs(tables_dir) if ('wavefish_eodfs.csv') in i])

count = 0
for current_file in file_names:
    # open csv with pandas
    df = pd.read_csv(current_file)
    # get amplitudes of recording
    powers = list(abs(df['power (dB)']))

    # get freqs of recording
    freqs = list(df['fundamental frequency (Hz)'])

    # define variables to compare, where the frequencies and amplitudes have to be in the fish dictionary
    current_file = current_file.split('/')
    date = fish_dict['Date'][count].split('-')

    if str(fish_dict['filename'][count]) in str(current_file[-1]).strip() and str(date[1]) in str(current_file[4]):
        # if - clause which corrects the EODf for days after the 17-05-2014
        if str(date[1]) in unique_date[0]:
            fish_dict['frequencies'].append(freqs)
            fish_dict['amplitudes'].append(powers)
        else:
            corr_f = []
            for i in np.arange(len(freqs)):
                corr_f.append(freqs[i]*(1.62**((300-299.5)/10)))
            fish_dict['frequencies'].append(corr_f)
            fish_dict['amplitudes'].append(powers)

    # match frequencies and amplitudes to habitats:
    if fish_dict['Habitat'][count] == unique_habitats[0]:
        if str(date[1]) in unique_date[0]:
            habitat_a_freqs.append(freqs)
            habitat_a_amps.append(powers)
        else:
            corr_f = []
            for i in np.arange(len(freqs)):
                corr_f.append(freqs[i] * (1.62 ** ((300 - 299.5) / 10)))
            habitat_a_freqs.append(corr_f)
            habitat_a_amps.append(powers)

    elif fish_dict['Habitat'][count] == unique_habitats[1]:
        if str(date[1]) in unique_date[0]:
            habitat_b_freqs.append(freqs)
            habitat_b_amps.append(powers)
        else:
            corr_f = []
            for i in np.arange(len(freqs)):
                corr_f.append(freqs[i] * (1.62 ** ((300 - 299.5) / 10)))
            habitat_b_freqs.append(corr_f)
            habitat_b_amps.append(powers)

    elif fish_dict['Habitat'][count] == unique_habitats[2]:
        if str(date[1]) in unique_date[0]:
            habitat_c_freqs.append(freqs)
            habitat_c_amps.append(powers)
        else:
            corr_f = []
            for i in np.arange(len(freqs)):
                corr_f.append(freqs[i] * (1.62 ** ((300 - 299.5) / 10)))
            habitat_c_freqs.append(corr_f)
            habitat_c_amps.append(powers)

    elif fish_dict['Habitat'][count] == unique_habitats[3]:
        if str(date[1]) in unique_date[0]:
            habitat_d_freqs.append(freqs)
            habitat_d_amps.append(powers)
        else:
            corr_f = []
            for i in np.arange(len(freqs)):
                corr_f.append(freqs[i] * (1.62 ** ((300 - 299.5) / 10)))
            habitat_d_freqs.append(corr_f)
            habitat_d_amps.append(powers)

    elif fish_dict['Habitat'][count] == unique_habitats[4]:
        if str(date[1]) in unique_date[0]:
            habitat_e_freqs.append(freqs)
            habitat_e_amps.append(powers)
        else:
            corr_f = []
            for i in np.arange(len(freqs)):
                corr_f.append(freqs[i] * (1.62 ** ((300 - 299.5) / 10)))
            habitat_e_freqs.append(corr_f)
            habitat_e_amps.append(powers)

    elif fish_dict['Habitat'][count] == unique_habitats[5]:
        if str(date[1]) in unique_date[0]:
            habitat_f_freqs.append(freqs)
            habitat_f_amps.append(powers)
        else:
            corr_f = []
            for i in np.arange(len(freqs)):
                corr_f.append(freqs[i] * (1.62 ** ((300 - 299.5) / 10)))
            habitat_f_freqs.append(corr_f)
            habitat_f_amps.append(powers)

    elif fish_dict['Habitat'][count] == unique_habitats[6]:
        if str(date[1]) in unique_date[0]:
            habitat_g_freqs.append(freqs)
            habitat_g_amps.append(powers)
        else:
            corr_f = []
            for i in np.arange(len(freqs)):
                corr_f.append(freqs[i] * (1.62 ** ((300 - 299.5) / 10)))
            habitat_g_freqs.append(corr_f)
            habitat_g_amps.append(powers)

    # set count plus one after everything's computed & matched
    count += 1

habitats = list(enumerate(fish_dict['Habitat']))

# delete double similar frequencys for habitat a
same_freqs_a, amps_a = li_fu.freq_comparison(habitat_a_freqs, habitat_a_amps, 0.5)
# think of a way to avoid this analyzation step
indices_a, fitting_amps_a = li_fu.get_amps(same_freqs_a, habitat_a_amps, 0.5)

# delete entry in list which consists of nans only
del fitting_amps_a[67]

amps_only_a, max_amps_a, amp_indices_a, saving_amps_a = li_fu.freq_selection(fitting_amps_a)
freqs_to_save_a = np.array(same_freqs_a)[np.array(amp_indices_a)]
saving_freqs_a = []
for i in np.arange(len(freqs_to_save_a)):
    saving_freqs_a.append(freqs_to_save_a[i][0][0])

clean_amps_a = li_fu.entry_remover(fitting_amps_a, saving_amps_a)
del_freqs_a = []
for i in range(len(clean_amps_a)):
  del_freqs_a.append(habitat_a_freqs[clean_amps_a[i][-2]][clean_amps_a[i][-1]])

for i in range(len(del_freqs_a)):
    for j in range(len(habitat_a_freqs)):
        if del_freqs_a[i] in habitat_a_freqs[j]:
            # print(str(del_freqs_a[i]) + ' is removed from ' + str(habitat_a_freqs[j]) + ' in ' + str(j) + 's list.')
            habitat_a_freqs[j].remove(del_freqs_a[i])

# figure out, how many lists are from day one, day two and so on
date_indices_a = []
dict_indices = []
for i in range(len(unique_date)):
    dict_indices.append(fish_dict['Date'].count(unique_date[i]))
    if i == 0:
        date_indices_a.append(fish_dict['Habitat'][:dict_indices[i]].count('A'))
    if i > 0:
        date_indices_a.append(fish_dict['Habitat'][dict_indices[i-1]:dict_indices[i-1]+dict_indices[i]].count('A'))

plot_freqs_a = [[]] * len(date_indices_a)
save_freqs_a = [[]] * len(date_indices_a)
for i in np.arange(len(date_indices_a)):
    if i == 0:
        plot_freqs_a[i] = habitat_a_freqs[:date_indices_a[i]]
        save_freqs_a[i] = saving_freqs_a[:date_indices_a[i]]
    else:
        plot_freqs_a[i] = habitat_a_freqs[sum(date_indices_a[:i]):sum(date_indices_a[:i+1])]
        save_freqs_a[i] = saving_freqs_a[sum(date_indices_a[:i]):sum(date_indices_a[:i+1])]

flat_plot_a = []

for i in np.arange(len(plot_freqs_a)):
    if plot_freqs_a[i] == []:
        pass
    else:
        flat_plot_a.append(np.hstack(plot_freqs_a[i]))


plt.eventplot(flat_plot_a, colors='k')
plt.eventplot(save_freqs_a, colors='r')
plt.title('Habitat A')
plt.xlim([400, 1000])
plt.xlabel('frequencies')
plt.ylabel('days')
plt.savefig('Habitat_A'+'.pdf')
plt.show()

same_freqs_b, amps_b = li_fu.freq_comparison(habitat_b_freqs, habitat_b_amps, 0.5)
indices_b, fitting_amps_b = li_fu.get_amps(same_freqs_b, habitat_b_amps, 0.5)
amps_only_b, max_amps_b, amp_indices_b, saving_amps_b = li_fu.freq_selection(fitting_amps_b)

freqs_to_save_b = np.array(same_freqs_b)[np.array(amp_indices_b)]
saving_freqs_b = []
for i in np.arange(len(freqs_to_save_b)):
    saving_freqs_b.append(freqs_to_save_b[i][0][0])

clean_amps_b = li_fu.entry_remover(fitting_amps_b, saving_amps_b)
del_freqs_b = []
for i in range(len(clean_amps_b)):
  del_freqs_b.append(habitat_b_freqs[clean_amps_b[i][-2]][clean_amps_b[i][-1]])

for i in range(len(del_freqs_b)):
    for j in range(len(habitat_b_freqs)):
        if del_freqs_b[i] in habitat_b_freqs[j]:
            # print(str(del_freqs_b[i]) + ' is removed from ' + str(habitat_b_freqs[j]) + ' in ' + str(j) + 's list.')
            habitat_b_freqs[j].remove(del_freqs_b[i])

date_indices_b = []
dict_indices = []
for i in range(len(unique_date)):
    dict_indices.append(fish_dict['Date'].count(unique_date[i]))
    if i == 0:
        date_indices_b.append(fish_dict['Habitat'][:dict_indices[i]].count('B'))
    if i > 0:
        date_indices_b.append(fish_dict['Habitat'][dict_indices[i-1]:dict_indices[i-1]+dict_indices[i]].count('B'))

plot_freqs_b = [[]] * len(date_indices_b)
save_freqs_b = [[]] * len(date_indices_b)
for i in np.arange(len(date_indices_b)):
    if i == 0:
        plot_freqs_b[i] = habitat_b_freqs[:date_indices_b[i]]
        save_freqs_b[i] = saving_freqs_b[:date_indices_b[i]]
    else:
        plot_freqs_b[i] = habitat_b_freqs[sum(date_indices_b[:i]):sum(date_indices_b[:i+1])]
        save_freqs_b[i] = saving_freqs_b[sum(date_indices_b[:i]):sum(date_indices_b[:i+1])]

flat_plot_b = []
for i in np.arange(len(plot_freqs_b)):
    if plot_freqs_b[i] == []:
        pass
    else:
        flat_plot_b.append(np.hstack(plot_freqs_b[i]))
del save_freqs_b[0]
print(save_freqs_b)
plt.eventplot(flat_plot_b, colors='k')
plt.eventplot(save_freqs_b, colors='r')
plt.title('Habitat B')
plt.xlim([400, 1000])
plt.xlabel('frequencies')
plt.ylabel('days')
plt.savefig('Habitat_B'+'.pdf')
plt.show()


same_freqs_c, amps_c = li_fu.freq_comparison(habitat_c_freqs, habitat_c_amps, 0.5)
indices_c, fitting_amps_c = li_fu.get_amps(same_freqs_c, habitat_c_amps, 0.5)
amps_only_c, max_amps_c, amp_indices_c, saving_amps_c = li_fu.freq_selection(fitting_amps_c)

freqs_to_save_c = np.array(same_freqs_c)[np.array(amp_indices_c)]
saving_freqs_c = []
for i in np.arange(len(freqs_to_save_c)):
    saving_freqs_c.append(freqs_to_save_c[i][0][0])

clean_amps_c = li_fu.entry_remover(fitting_amps_c, saving_amps_c)
del_freqs_c = []
for i in range(len(clean_amps_c)):
  del_freqs_c.append(habitat_c_freqs[clean_amps_c[i][-2]][clean_amps_c[i][-1]])

for i in range(len(del_freqs_c)):
    for j in range(len(habitat_c_freqs)):
        if del_freqs_c[i] in habitat_c_freqs[j]:
            # print(str(del_freqs_c[i]) + ' is removed from ' + str(habitat_c_freqs[j]) + ' in ' + str(j) + 's list.')
            habitat_c_freqs[j].remove(del_freqs_c[i])

date_indices_c = []
dict_indices = []
for i in range(len(unique_date)):
    dict_indices.append(fish_dict['Date'].count(unique_date[i]))
    if i == 0:
        date_indices_c.append(fish_dict['Habitat'][:dict_indices[i]].count('C'))
    if i > 0:
        date_indices_c.append(fish_dict['Habitat'][dict_indices[i-1]:dict_indices[i-1]+dict_indices[i]].count('C'))

plot_freqs_c = [[]] * len(date_indices_c)
save_freqs_c = [[]] * len(date_indices_c)
for i in np.arange(len(date_indices_c)):
    if i == 0:
        plot_freqs_c[i] = habitat_c_freqs[:date_indices_c[i]]
        save_freqs_c[i] = saving_freqs_c[:date_indices_c[i]]
    else:
        plot_freqs_c[i] = habitat_c_freqs[sum(date_indices_c[:i]):sum(date_indices_c[:i+1])]
        save_freqs_c[i] = saving_freqs_c[sum(date_indices_c[:i]):sum(date_indices_c[:i + 1])]

flat_plot_c = []
for i in np.arange(len(plot_freqs_c)):
    if plot_freqs_c[i] == []:
        pass
    else:
        flat_plot_c.append(np.hstack(plot_freqs_c[i]))
del save_freqs_c[0]
print(list(enumerate(save_freqs_c)))

plt.eventplot(flat_plot_c, colors='k')
plt.eventplot(save_freqs_c, colors='r')
plt.title('Habitat C')
plt.xlim([400, 1000])
plt.xlabel('frequencies')
plt.ylabel('days')
plt.savefig('Habitat_C'+'.pdf')
plt.show()


same_freqs_d, amps_d = li_fu.freq_comparison(habitat_d_freqs, habitat_d_amps, 0.5)
indices_d, fitting_amps_d = li_fu.get_amps(same_freqs_d, habitat_d_amps, 0.5)
amps_only_d, max_amps_d, amp_indices_d, saving_amps_d = li_fu.freq_selection(fitting_amps_d)

freqs_to_save_d = np.array(same_freqs_d)[np.array(amp_indices_d)]
saving_freqs_d = []
for i in np.arange(len(freqs_to_save_d)):
    saving_freqs_d.append(freqs_to_save_d[i][0][0])

clean_amps_d = li_fu.entry_remover(fitting_amps_d, saving_amps_d)
del_freqs_d = []
for i in range(len(clean_amps_d)):
  del_freqs_d.append(habitat_d_freqs[clean_amps_d[i][-2]][clean_amps_d[i][-1]])

for i in range(len(del_freqs_d)):
    for j in range(len(habitat_d_freqs)):
        if del_freqs_d[i] in habitat_d_freqs[j]:
            # print(str(del_freqs_d[i]) + ' is removed from ' + str(habitat_d_freqs[j]) + ' in ' + str(j) + 's list.')
            habitat_d_freqs[j].remove(del_freqs_d[i])

date_indices_d = []
dict_indices = []
for i in range(len(unique_date)):
    dict_indices.append(fish_dict['Date'].count(unique_date[i]))
    if i == 0:
        date_indices_d.append(fish_dict['Habitat'][:dict_indices[i]].count('D'))
    if i > 0:
        date_indices_d.append(fish_dict['Habitat'][dict_indices[i-1]:dict_indices[i-1]+dict_indices[i]].count('D'))

plot_freqs_d = [[]] * len(date_indices_d)
save_freqs_d = [[]] * len(date_indices_d)
for i in np.arange(len(date_indices_d)):
    if i == 0:
        plot_freqs_d[i] = habitat_d_freqs[:date_indices_d[i]]
        save_freqs_d[i] = saving_freqs_d[:date_indices_d[i]]
    else:
        plot_freqs_d[i] = habitat_d_freqs[sum(date_indices_d[:i]):sum(date_indices_d[:i+1])]
        save_freqs_d[i] = saving_freqs_d[sum(date_indices_d[:i]):sum(date_indices_d[:i + 1])]

flat_plot_d = []
flat_saving_d = []
for i in np.arange(len(plot_freqs_d)):
    if plot_freqs_d[i] == []:
        pass
    else:
        flat_plot_d.append(np.hstack(plot_freqs_d[i]))


plt.eventplot(flat_plot_d, colors='k')
plt.eventplot(saving_freqs_d, colors='r')
plt.title('Habitat D')
plt.xlim([400, 1000])
plt.xlabel('frequencies')
plt.ylabel('days')
plt.savefig('Habitat_D'+'.pdf')
plt.show()


same_freqs_e, amps_e = li_fu.freq_comparison(habitat_e_freqs, habitat_e_amps, 0.5)
indices_e, fitting_amps_e = li_fu.get_amps(same_freqs_e, habitat_e_amps, 0.5)
amps_only_e, max_amps_e, amp_indices_e, saving_amps_e = li_fu.freq_selection(fitting_amps_e)

freqs_to_save_e = np.array(same_freqs_e)[np.array(amp_indices_e)]
saving_freqs_e = []
for i in np.arange(len(freqs_to_save_e)):
    saving_freqs_e.append(freqs_to_save_e[i][0][0])

clean_amps_e = li_fu.entry_remover(fitting_amps_e, saving_amps_e)
del_freqs_e = []
for i in range(len(clean_amps_e)):
  del_freqs_e.append(habitat_e_freqs[clean_amps_e[i][-2]][clean_amps_e[i][-1]])

for i in range(len(del_freqs_e)):
    for j in range(len(habitat_e_freqs)):
        if del_freqs_e[i] in habitat_e_freqs[j]:
            # print(str(del_freqs_e[i]) + ' is removed from ' + str(habitat_e_freqs[j]) + ' in ' + str(j) + 's list.')
            habitat_e_freqs[j].remove(del_freqs_e[i])

date_indices_e = []
dict_indices = []
for i in range(len(unique_date)):
    dict_indices.append(fish_dict['Date'].count(unique_date[i]))
    if i == 0:
        date_indices_e.append(fish_dict['Habitat'][:dict_indices[i]].count('E'))
    if i > 0:
        date_indices_e.append(fish_dict['Habitat'][dict_indices[i-1]:dict_indices[i-1]+dict_indices[i]].count('E'))

plot_freqs_e = [[]] * len(date_indices_e)
save_freqs_e = [[]] * len(date_indices_e)
for i in np.arange(len(date_indices_e)):
    if i == 0:
        plot_freqs_e[i] = habitat_e_freqs[:date_indices_e[i]]
        save_freqs_e[i] = saving_freqs_e[:date_indices_e[i]]
    else:
        plot_freqs_e[i] = habitat_e_freqs[sum(date_indices_e[:i]):sum(date_indices_e[:i+1])]
        save_freqs_e[i] = saving_freqs_e[sum(date_indices_e[:i]):sum(date_indices_e[:i+1])]

flat_plot_e = []
flat_saving_e = []
for i in np.arange(len(plot_freqs_e)):
    if plot_freqs_e[i] == []:
        pass
    else:
        flat_plot_e.append(np.hstack(plot_freqs_e[i]))


plt.eventplot(flat_plot_e, colors='k')
plt.eventplot(saving_freqs_e, colors='r')
plt.title('Habitat E')
plt.xlim([400, 1000])
plt.xlabel('frequencies')
plt.ylabel('days')
plt.savefig('Habitat_E'+'.pdf')
plt.show()


same_freqs_f, amps_f = li_fu.freq_comparison(habitat_f_freqs, habitat_f_amps, 0.5)
indices_f, fitting_amps_f = li_fu.get_amps(same_freqs_f, habitat_f_amps, 0.5)
amps_only_f, max_amps_f, amp_indices_f, saving_amps_f = li_fu.freq_selection(fitting_amps_f)

freqs_to_save_f = np.array(same_freqs_f)[np.array(amp_indices_f)]
saving_freqs_f = []
for i in np.arange(len(freqs_to_save_f)):
    saving_freqs_f.append(freqs_to_save_f[i][0][0])

clean_amps_f = li_fu.entry_remover(fitting_amps_f, saving_amps_f)
del_freqs_f = []
for i in range(len(clean_amps_f)):
  del_freqs_f.append(habitat_f_freqs[clean_amps_f[i][-2]][clean_amps_f[i][-1]])

for i in range(len(del_freqs_f)):
    for j in range(len(habitat_f_freqs)):
        if del_freqs_f[i] in habitat_f_freqs[j]:
            # print(str(del_freqs_b[i]) + ' is removed from ' + str(habitat_b_freqs[j]) + ' in ' + str(j) + 's list.')
            habitat_f_freqs[j].remove(del_freqs_f[i])

date_indices_f = []
dict_indices_f = []
for i in range(len(unique_date)):
    dict_indices_f.append(fish_dict['Date'].count(unique_date[i]))
    if i == 0:
        date_indices_f.append(fish_dict['Habitat'][:dict_indices_f[i]].count('F'))
    if i > 0:
        date_indices_f.append(fish_dict['Habitat'][dict_indices_f[i-1]:dict_indices_f[i-1]+dict_indices_f[i]].count('F'))

plot_freqs_f = [[]] * len(date_indices_f)
save_freqs_f = [[]] * len(date_indices_e)
for i in np.arange(len(date_indices_f)):
    if i == 0:
        plot_freqs_f[i] = habitat_f_freqs[:date_indices_f[i]]
        save_freqs_f[i] = saving_freqs_f[:date_indices_f[i]]
    else:
        plot_freqs_f[i] = habitat_f_freqs[sum(date_indices_f[:i]):sum(date_indices_f[:i+1])]
        save_freqs_f[i] = saving_freqs_f[sum(date_indices_f[:i]):sum(date_indices_f[:i+1])]


flat_plot_f = []
flat_saving_f = []
for i in np.arange(len(plot_freqs_f)):
    if plot_freqs_f[i] == []:
        pass
    else:
        flat_plot_f.append(np.hstack(plot_freqs_f[i]))

# embed()
# exit()
plt.eventplot(flat_plot_f, colors='k')
plt.eventplot(saving_freqs_f, colors='r')
plt.title('Habitat F')
plt.xlim([400, 1000])
plt.xlabel('frequencies')
plt.ylabel('days')
plt.savefig('Habitat_F'+'.pdf')
plt.show()


same_freqs_g, amps_g = li_fu.freq_comparison(habitat_g_freqs, habitat_g_amps, 0.5)
indices_g, fitting_amps_g = li_fu.get_amps(same_freqs_g, habitat_g_amps, 0.5)
amps_only_g, max_amps_g, amp_indices_g, saving_amps_g = li_fu.freq_selection(fitting_amps_g)

freqs_to_save_g = np.array(same_freqs_g)[np.array(amp_indices_g)]
saving_freqs_g = []
for i in np.arange(len(freqs_to_save_g)):
    saving_freqs_g.append(freqs_to_save_g[i][0][0])

clean_amps_g = li_fu.entry_remover(fitting_amps_g, saving_amps_g)
del_freqs_g = []
for i in range(len(clean_amps_g)):
  del_freqs_g.append(habitat_g_freqs[clean_amps_g[i][-2]][clean_amps_g[i][-1]])

for i in range(len(del_freqs_g)):
    for j in range(len(habitat_g_freqs)):
        if del_freqs_g[i] in habitat_g_freqs[j]:
            # print(str(del_freqs_g[i]) + ' is removed from ' + str(habitat_g_freqs[j]) + ' in ' + str(j) + 's list.')
            habitat_g_freqs[j].remove(del_freqs_g[i])

date_indices_g = []
dict_indices = []
for i in range(len(unique_date)):
    dict_indices.append(fish_dict['Date'].count(unique_date[i]))
    if i == 0:
        date_indices_g.append(fish_dict['Habitat'][:dict_indices[i]].count('G'))
    if i > 0:
        date_indices_g.append(fish_dict['Habitat'][dict_indices[i-1]:dict_indices[i-1]+dict_indices[i]].count('G'))

plot_freqs_g = [[]] * len(date_indices_g)
save_freqs_g = [[]] * len(date_indices_g)
for i in np.arange(len(date_indices_g)):
    if i == 0:
        plot_freqs_g[i] = habitat_g_freqs[:date_indices_g[i]]
        save_freqs_g[i] = saving_freqs_g[:date_indices_g[i]]
    else:
        plot_freqs_g[i] = habitat_g_freqs[sum(date_indices_g[:i]):sum(date_indices_g[:i+1])]
        save_freqs_g[i] = saving_freqs_g[sum(date_indices_g[:i]):sum(date_indices_g[:i+1])]

flat_plot_g = []
flat_saving_g = []
for i in np.arange(len(plot_freqs_g)):
    if plot_freqs_g[i] == []:
        pass
    else:
        flat_plot_g.append(np.hstack(plot_freqs_g[i]))

plt.eventplot(flat_plot_g, colors='k')
plt.eventplot(saving_freqs_g, colors='r')
plt.title('Habitat G')
plt.xlim([400, 1000])
plt.xlabel('frequencies')
plt.ylabel('days')
plt.savefig('Habitat_G'+'.pdf')
plt.show()
# # # get list of frequencies to determine the shape
# # freqs_matrix = fish_dict['frequencies']
# # amps_matrix = fish_dict['amplitudes']
# # # find out the size of the biggest list
# # max_len = np.max([len(freqs_matrix[i]) for i in np.arange(len(freqs_matrix))])
# #
# # # create a matrix which consists of NaNs and has the shape of the list of frequencies & its longest list
# # freqs_matrix_full = np.full((len(freqs_matrix), max_len), np.nan)
# # amps_matrix_full = np.full((len(amps_matrix), max_len), np.nan)
# # # get frequency values into the NaN-Matrix
# # for i in np.arange(len(freqs_matrix_full)):
# #     freqs_matrix_full[i, :len(freqs_matrix[i])] = freqs_matrix[i]
# #     amps_matrix_full[i, :len(amps_matrix[i])] = amps_matrix[i]
#
# # iterate through every frequency and find out, if there's another similar frequency
# same_freqs = []
# same_amps = []
# same_freq_recording = []
# same_freq_idx = []
# for current_list in np.arange(len(freqs_matrix_full)):
#     for current_frequency in np.arange(len(freqs_matrix_full[current_list])):
#         cf = freqs_matrix_full[current_list, current_frequency]
#         list_idx, idx = np.unravel_index(np.argsort(np.abs(freqs_matrix_full - cf), axis=None),
#                                          np.shape(freqs_matrix_full))
#         same_freqs.append(freqs_matrix_full[list_idx, idx])
#         same_amps.append(amps_matrix_full[list_idx, idx])
#         same_freq_recording.append(list_idx)
#         same_freq_idx.append(idx)
# # embed()
# # exit()

os.chdir(r'../../PycharmProjects/panama_2014')
# create a data frame from the fish dict:
fish_table = pd.DataFrame.from_dict(fish_dict, orient='index')
fish_table.to_csv('fish_table.csv', sep=',')
