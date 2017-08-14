# test file
import pandas as pd;
import matplotlib.pyplot as plt;

# full_xls = pd.ExcelFile('test_data_plate1.xlsx');
full_xls = pd.ExcelFile('06222016 Staph Array Data Test.xlsx');

# will come back to grab all sheets, work with first plate
# for sheet in range(11):
#     pass;

df_plate = full_xls.parse(0, skiprows=1);
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

# visit number color coding dictionary
visit_color = {"V1": "r", "V2": "b", "V3": "g"};

# group by patient id
patient_id = df_plate.groupby("PatientID");
for patient_name, patient_data in patient_id:
    figure_num = 1;
    for plot_col in plot_columns:
        # set figure and width/height
        plt.figure(figure_num, figsize=(5,5));
        visits = patient_data.groupby("Visit");
        # remove?
        patient_name = str(patient_name);
        for visit_name, visit_data in visits:
            # make a plot for visits

            # width = 6  # setting width
            # height = 6  # setting height
            # plt.figure(figsize=(width, height))
            plt_title = patient_name + " (" + patient_data["Gender"].iloc[0] + str(
                patient_data["Age"].iloc[0]) + " yr " + patient_data[
                            "Hospital"].iloc[0] + ") " + plot_col;
            plt.suptitle(plt_title, fontsize=14, fontweight='bold')
            plt.loglog(visit_data["Dilution"], visit_data[plot_col], color=visit_color[visit_name],
                       marker='o', markerfacecolor='none',
                       markersize=10,
                       markeredgewidth=2, label=visit_name[1]);
        plt.xlabel('Dilution', fontsize=14);
        plt.ylabel('Intensity', fontsize=14);
        plt.legend(title="Visit",loc=1);
        plt.savefig(plt_title + ".png");
        plt.clf();
        figure_num += 1;
        break;
    break;



