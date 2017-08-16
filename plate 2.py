# import modules
import pandas as pd;
import matplotlib.pyplot as plt;
import re;

# function to clean up Sample ID column into PatientID, Visit, Dilution columns
def clean_sample_id_column(df_plate):
    # this transforms the troublesome 'Sample ID' column into an array
    column1_array = df_plate['Sample ID'].values

    # taking mark's advice this list comprehension inverts the contents of each element (i.e. cell) in the array
    column1_array = [cell[::-1] for cell in column1_array]

    # cleaning up data
    # rex = re.compile(r'(?:(?P<Dilution> *[0]+1) *)?(?:(?P<Visit> *[1-3][v|V] *))?(?P<PatientID>[ |[A-Za-z0-9_]+)?|'
    #                  r'(?P<Standard> *[^'Standard']+)')
    # outputs = [rex.match(x) for x in column1_array]
    rex = re.compile(r'(?:(?P<Dilution> *[0]+1) *)?(?:(?P<Visit> *[1-3][v|V] *))?(?P<PatientID>[ |[A-Za-z0-9_]+)')
    outputs = [rex.match(x) for x in column1_array]


    # this takes the named groups from the regular expression above converts everything into a list of dictionaries where
    # the keys are group names (PatientID, Visit and Dilution) and the values are the corresponding string components
    lst_of_dcts = []
    for i, o in enumerate(outputs):
        try:
            lst_of_dcts.append(o.groupdict())
        except:
            print(column1_array[i])

    # up until this point all the values we are interested in are still inverted from the cell[::-1]. This changes them back
    for dct in lst_of_dcts:
        for k, v in dct.items():
            if v == None:
                continue
            else:
                vv = v[::-1].strip()  # added the strip to take away any extra white space still attached
                dct[k] = vv

    # this deletes the old 'SampleID' column
    df_plate.drop('Sample ID', axis=1, inplace=True)

    # This block of code goes through the list of dictionaries and appends the values to a list of their specific category
    # e.g. a dilution of '100' is added to the dilution_list. These lists are then added to the dataframe as columns at
    # the specified index so they are at the front of the dataframe and not slapped on at the end.
    id_list = []
    visit_list = []
    dilution_list = []
    standard_list = []
    for dct in lst_of_dcts:
        id_list.append(dct['PatientID'])
        visit_list.append(dct['Visit'])
        dilution_list.append(dct['Dilution'])
        standard_list.append(dct['Standard'])

    df_plate.insert(0, 'PatientID', id_list)
    df_plate.insert(1, 'Visit', visit_list)
    df_plate.insert(2, 'Dilution', dilution_list)
    # df_plate.insert(3, 'Standard', standard_list)

    # return new dataframe
    return df_plate;

# import excel data file
full_xls = pd.ExcelFile('Plate2_standard_emily_test.xlsx');
df_plate = full_xls.parse(skiprows=1)
df_plate_dirty = full_xls.parse(skiprows=1);

    # run dataframe through function to clean up Sample ID column
df_plate = clean_sample_id_column(df_plate_dirty);

    # clean up column headers and reassign
df_plate.columns = map(lambda x: x.strip(), df_plate.columns);

    # fill in the info for hospital, age, gender according to existing data
df_plate['Hospital'] = df_plate['Hospital'].ffill();
df_plate['Age'] = df_plate['Age'].ffill();
df_plate['Gender'] = df_plate['Gender'].ffill();

print(df_plate)

    # name of columns that we will plot against dilution
plot_columns = ['surface protein ext', 'cytoplasmic ext', 'Exoprotein ext', 'LukE', 'LukD', 'LukS-PV', 'LukF-PV',
                    'LukAB(Lab)', 'LukAB(cc30)', 'Hemolysin gamma A', 'Hemolysin gamma B', 'Hemolysin gamma C', 'HLA-1',
                    'HLA -2', 'HLA', 'Betatoxin', 'PNAG', 'SEO', 'SP', 'SEG', 'SEI', 'SEU', 'SEN', 'SEM', 'SEB',
                    'PSMalpha2', 'PSMalpha3', 'psmalpah4', 'PSM 4variant', 'Pn CWPS', 'PC4', 'PC-12', 'PC16', 'Pn PS12',
                    'Pn PS23', 'S.Pyogenese arcA', 'PLY', 'Tetanus Toxoid', 'Glom.extract', 'hIgG', 'SpA domD5-WT',
                    'SpA domD5FcNull', 'hIgA', 'BSA', 'HSA', 'Rabbit IgG', 'ABA', 'LDL'];

    # visit number color coding dictionary
visit_color = {"V1": "r", "V2": "b", "V3": "g"};

    # group by patient id
patient_id = df_plate.groupby("PatientID");
for patient_name, patient_data in patient_id:
        # making sure patient name is a string
    patient_name = str(patient_name);
    # create html file
    fh = open("Plate " + str(2) + "-" + patient_name + ".html", "w");
    html_message = "<table>\n<tr>\n";
    figure_num = 1;
    # go through each data column to plot
    for plot_col in plot_columns:
        print("plotting figure " + str(figure_num));
        # set figure and width/height
        plt.figure(figure_num, figsize=(5, 5));
        plt_title = patient_name;

        if plot_col == 'Nan'
            print(plot_col, 'missing')

        if "Standard" in patient_name:
            patient_name = "Standard";
            plt_title = plt_title + " " + plot_col;
            plt.suptitle( plt_title, fontsize=14, fontweight='bold' );
            plt.loglog( patient_data["Dilution"], patient_data[plot_col], color='k',
                        marker='o', markerfacecolor='none',
                        markersize=10,
                        markeredgewidth=2, label="N/A" );

# standard_id = df_plate.groupby("Standard")
# for standard_name, standard_data in standard_id:
#     # making sure patient name is a string
#     standard_name = str(standard_name)
#     # create html file
#     fh = open( "Plate " + str(2) + "-" + "Standard" + ".html", "w" )
#     html_message = "<table>\n<tr>\n";
#     figure_num = 1;
#     # go through each data column to plot
#     for plot_col in plot_columns:
#         print( "plotting figure " + str( figure_num ) );
#         # set figure and width/height
#         plt.figure( figure_num, figsize=(5, 5) );
#         plt_title = "Standard"

        else:
            # create title and assign it
            plt_title = plt_title + " (" + patient_data["Gender"].iloc[0] + " " + str(
            "%.f" % patient_data["Age"].iloc[0]) + " yr " + patient_data[
                                "Hospital"].iloc[0] + ") " + plot_col;
            plt.suptitle(plt_title, fontsize=14, fontweight='bold')
            # plot each visit
            visits = patient_data.groupby("Visit");
            for visit_name, visit_data in visits:
                if visit_name == "None":
                    visit_name = "V1";
                # plotting with log axis, colors according to the visit_color dictionary
                    plt.loglog(visit_data["Dilution"], visit_data[plot_col], color=visit_color[visit_name.upper()],
                               marker='o', markerfacecolor='none',
                               markersize=10,
                               markeredgewidth=2, label=visit_name[1]);
            # assigning other misc plot axis and legend information
                plt.xlabel('Dilution', fontsize=14);
                plt.ylabel('Intensity', fontsize=14);
                plt.legend(title="Visit", loc=1);
            # save plot in the correct directory
                fig_png_name = "Plate " + str(2) + "/" + plt_title + ".png";
                plt.savefig(fig_png_name);
                print("saved figure [" + plt_title + "]");
                plt.close();
            # add figure to html page
                html_message += "<td><img src=\""+fig_png_name+"\" width=\"120\"></td>";
                if (figure_num in [3,9,17,25,29,39]):
                    html_message += "</tr>\n<tr>"
                elif figure_num == 48:
                    html_message += "</tr>\n</table>"
                    figure_num += 1;
                    fh.write(html_message);
                    fh.close();