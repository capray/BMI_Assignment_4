# test file
import pandas as pd;

Plate1 = pd.read_excel('06222016 Staph Array Data.xlsx',na_values='',sheetname="Plate 1");
full_xls = pd.ExcelFile('06222016 Staph Array Data.xlsx')
# will come back to grab all sheets, work with first plate
for sheet in range(11):
    df_plate = full_xls.parse(sheet, skiprows=1)
    x = list(df_plate.columns)
    final_bac_columns = ['PSMalpha2', 'PSMalpha3',
                         'psmalpah4', 'BSA', 'Betatoxin', 'hIgA', 'LDL', 'SEB',
                         'S.Pyogenese arcA', 'LukE', 'Pn PS12', 'LukD', 'Pn PS23', 'HLA-1',
                         'SpA domD5-WT', 'Glom.extract', 'SpA domD5FcNull', 'SEN', 'hIgG', 'SEU',
                         'HLA', 'SEI', 'LukAB(Lab)', 'SEM', 'LukAB(cc30)', 'surface protein ext',
                         'SEB.1', 'cytoplasmic ext', 'Hemolysin gamma A', 'Pn CWPS',
                         'Hemolysin gamma B', 'ABA', 'Hemolysin gamma C', 'PC-12', 'LukS-PV',
                         'SEO', 'SP', 'SEG', 'PLY', 'HSA', 'Exoprotein ext', 'Rabbit IgG',
                         'LukF-PV', 'PSM 4variant', 'PC4', 'PNAG', 'PC16', 'HLA -2',
                         'Tetanus Toxoid']
    print(len(final_bac_columns))



