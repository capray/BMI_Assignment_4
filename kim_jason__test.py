# test file
import pandas as pd;

full_xls = pd.ExcelFile('test_data_plate1.xlsx');
# full_xls = pd.ExcelFile('06222016 Staph Array Data.xlsx');

# will come back to grab all sheets, work with first plate
# for sheet in range(11):
#     pass;

df_plate1 = full_xls.parse(0);

print(df_plate1)