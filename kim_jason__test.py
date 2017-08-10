# test file
import pandas as pd;

# Plate1 = pd.read_excel('06222016 Staph Array Data.xlsx',na_values='',sheetname="Plate 1");
full_xls = pd.ExcelFile('06222016 Staph Array Data.xlsx');

# will come back to grab all sheets, work with first plate
# for sheet in range(11):
#     pass;

df_plate1 = full_xls.parse(0,skiprows=1);

print(df_plate1)