import xlrd
import pandas as pd
import numpy as np
import re

full_xls = pd.ExcelFile('06222016 Staph Array Data.xlsx')
df_plate1 = full_xls.parse(0, skiprows=1)# to see the program work for other the sheets just change the first digit

# this transforms the troublesome 'Sample ID' column into an array
column1_array = df_plate1['Sample ID'].values
# print(column1_array)

# taking mark's advice this list comprehension inverts the contents of each element (i.e. cell) in the array
column1_array = [cell[::-1] for cell in column1_array]

# will send an email later that explains each part of this thing, but I believe works for all sheets in the excel file
rex = re.compile(r'(?:(?P<Dilution> *[0]+1) *)?(?:(?P<Visit> *[1-3][v|V] *))?(?P<PatientID>[ |[A-Za-z0-9_]+)')
outputs = [rex.match(x) for x in column1_array]

# this takes the named groups from the regular expression above converts everything into a list of dictionaries where
# the keys are group names (PatientID, Visit and Dilution) and the values are the corresponding string components
lst_of_dcts = []
for i, o in enumerate(outputs):
    try:
        lst_of_dcts.append(o.groupdict())
        # print(o.groupdict())
    except:
        print(column1_array[i])
# print(lst_of_dcts)

# up until this point all the values we are interested in are still inverted from the cell[::-1]. This changes them back
for dct in lst_of_dcts:
    for k, v in dct.items():
        if v == None:
            continue
        else:
            vv = v[::-1].strip() # added the strip to take away any extra white space still attached
            dct[k] = vv
# print(lst_of_dcts)

# this deletes the old 'SampleID' column
df_plate1.drop('Sample ID', axis = 1, inplace = True)

# This block of code goes through the list of dictionaries and appends the values to a list of their specific category
# e.g. a dilution of '100' is added to the dilution_list. These lists are then added to the dataframe as columns at
# the specified index so they are at the front of the dataframe and not slapped on at the end.
id_list = []
visit_list = []
dilution_list = []
for dct in lst_of_dcts:
    id_list.append(dct['PatientID'])
    visit_list.append(dct['Visit'])
    dilution_list.append(dct['Dilution'])
df_plate1.insert(0, 'PatientID', id_list)
df_plate1.insert(1, 'Visit', visit_list)
df_plate1.insert(2, 'Dilution', dilution_list)
print(df_plate1.iloc[:,0:5]) #just prints a portion of the updated dataframe to see that all changes worked
