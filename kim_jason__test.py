# test file
import pandas as pd;
import matplotlib.pyplot as plt;

# full_xls = pd.ExcelFile('test_data_plate1.xlsx');
full_xls = pd.ExcelFile('06222016 Staph Array Data Test.xlsx');

# will come back to grab all sheets, work with first plate
# for sheet in range(11):
#     pass;

df_plate = full_xls.parse(0,skiprows=1);
# test_data = full_xls.parse(0);

"""
# print(test_data)
dict_full_data = {};

# pull each patient's data
patient_id = df_plate.groupby("PatientID");

col_not_used = ["Sample ID","PatientID","Visit","Hospital","Age","Gender"];

# Visit #

for patient_name, patient_data in patient_id:
    dict_full_data[patient_name] = {};
    visits = patient_data.groupby("Visit");
    for visit_name, visit_data in visits:
        dict_full_data[patient_name][visit_name] = pd.DataFrame();
        for col_name in df_plate.columns:
            if col_name.strip() not in col_not_used:
        #         print(col_name);
                # dict_full_data[patient_name][visit_name][col_name] = dict_full_data[patient_name][visit_name].get(list(visit_data[col_name]),{});
                dict_full_data[patient_name][visit_name][col_name] = visit_data[col_name];




print(dict_full_data);
# pull dilution

# pull values of columns

"""
# # Clean up column headers and reassign
df_plate.columns = map(lambda x: x.strip(), df_plate.columns);
# print(len(df_plate.columns))

# fill in the data for hospital, age, gender
df_plate['Hospital'] = df_plate['Hospital'].ffill();
df_plate['Age'] = df_plate['Age'].ffill();
df_plate['Gender'] = df_plate['Gender'].ffill();

# name of columns that we will plot against dilution
plot_columns = ['PSMalpha2', 'PSMalpha3',
       'psmalpah4', 'BSA', 'Betatoxin', 'hIgA', 'LDL', 'SEB',
       'S.Pyogenese arcA', 'LukE', 'Pn PS12', 'LukD', 'Pn PS23', 'HLA-1',
       'SpA domD5-WT', 'Glom.extract', 'SpA domD5FcNull', 'SEN', 'hIgG', 'SEU',
       'HLA', 'SEI', 'LukAB(Lab)', 'SEM', 'LukAB(cc30)', 'surface protein ext',
       'SEB.1', 'cytoplasmic ext', 'Hemolysin gamma A', 'Pn CWPS',
       'Hemolysin gamma B', 'ABA', 'Hemolysin gamma C', 'PC-12', 'LukS-PV',
       'SEO', 'SP', 'SEG', 'PLY', 'HSA', 'Exoprotein ext', 'Rabbit IgG',
       'LukF-PV', 'PSM 4variant', 'PC4', 'PNAG', 'PC16', 'HLA -2',
       'Tetanus Toxoid'];

# group by patient id
patient_id = df_plate.groupby("PatientID");
for patient_name, patient_data in patient_id:
    for plot_col in plot_columns:
        visits = patient_data.groupby("Visit");
        plot_name = str(patient_name) + " " + plot_col;
        for visit_name, visit_data in visits:
            plt.plot(visit_data["Dilution"],visit_data[plot_col]);
            print(visit_data["Dilution"])
            print(visit_data[plot_col])
        plt.savefig(plot_name+".png");
        plt.clf();
        print(plot_name)
    break;



