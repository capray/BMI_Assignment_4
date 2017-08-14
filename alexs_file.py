# test file
import pandas as pd;
import numpy as np
import re

# Plate1 = pd.read_excel('06222016 Staph Array Data.xlsx',na_values='',sheetname="Plate 1");
full_xls = pd.ExcelFile('06222016 Staph Array Data_AS_.xlsx');

# will come back to grab all sheets, work with first plate
# for sheet in range(11):
#     pass;

df_plate1 = full_xls.parse(0,skiprows=1);

column1_array = df_plate1['Sample ID'].values
print(column1_array)
# print (type(column1_array))

PatientID = []
Dilution = []
Visit =[]

for cell in column1_array:
    m = None
    matcher = r"(?P<reverse_dilution>[0]+1)\s*(?P<reverse_visit>[1-3](V|v))\s*(?P<reverse_patient_id>[0-9]+(\s+)?(.)*)"
    matcher = r"(?P<patient_id>.*)?\s*(?P<visit>(v|V[1-3]))?\s*(?P<dilution>1[0]+)?\s*"
    m = re.match(matcher, cell)


matcher = r'(?P<visit>((v|V)[1-3])'
m = re.match(matcher(column1_array[0]))

    # everything = re.findall(' ?[0-9]+ \d?V? ?.+', cell[::-1])
    # _patientid_ = re.findall(' ?[0-9]+ \d?V?( ?.+)', cell[::-1])
    # PatientID.append(_patientid_[::-1])
    # _dilution_ = re.findall('( ?[0-9]+) \d?V? ?.+', cell[::-1])
    # Dilution.append(_dilution_)
    # _visit_ = re.findall(' ?[0-9]+( \d?V?) ?.+', cell[::-1])
    # Visit.append(_visit_)
    # print(everything[0][::-1])
print(m.groupdict())
# print(PatientID)
# print(Dilution)
# print(Visit)



