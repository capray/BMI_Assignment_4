# import modules
import pandas as pd;
import matplotlib.pyplot as plt;

# import excel data file
full_xls = pd.ExcelFile('06222016 Staph Array Data Test.xlsx');

# loop through each sheet
for sheet_num in range(11):
    # grab corresponding sheet as a dataframe, skipping the first row as it contains meaningless data
    df_plate = full_xls.parse(sheet_num, skiprows=1);

    # clean up column headers and reassign
    df_plate.columns = map(lambda x: x.strip(), df_plate.columns);

    # fill in the info for hospital, age, gender according to existing data
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
        # go through each data column to plot
        for plot_col in plot_columns:
            print("plotting figure "+str(figure_num));
            # set figure and width/height
            plt.figure(figure_num, figsize=(5,5));
            # making sure patient name is a string
            patient_name = str(patient_name);
            # create title and assign it
            plt_title = patient_name + " (" + patient_data["Gender"].iloc[0] + " " + str(
                "%.f"%patient_data["Age"].iloc[0]) + " yr " + patient_data[
                            "Hospital"].iloc[0] + ") " + plot_col;
            plt.suptitle(plt_title, fontsize=14, fontweight='bold')
            # plot each visit
            visits = patient_data.groupby("Visit");
            for visit_name, visit_data in visits:
                # plotting with log axis, colors according to the visit_color dictionary
                plt.loglog(visit_data["Dilution"], visit_data[plot_col], color=visit_color[visit_name],
                           marker='o', markerfacecolor='none',
                           markersize=10,
                           markeredgewidth=2, label=visit_name[1]);
            # assigning other misc plot axis and legend information
            plt.xlabel('Dilution', fontsize=14);
            plt.ylabel('Intensity', fontsize=14);
            plt.legend(title="Visit",loc=1);
            # save plot in the correct directory
            plt.savefig("Plate "+str(sheet_num+1)+"/"+plt_title + ".png");
            print("saved figure ["+plt_title+"]");
            plt.close();
            figure_num += 1;
        break;
    break;

