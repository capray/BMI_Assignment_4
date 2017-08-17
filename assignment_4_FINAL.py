##### Pre-requisites to run this script #####################################################
# This script should be in the same directory as document "06222016 Staph Array Data.xlsx"
# Folders for 11 Plates should be created in the same directory (e.g. Plate 1, Plate 2, etc)
#############################################################################################

# import modules
import pandas as pd
import matplotlib.pyplot as plt
import re

# function to clean up Sample ID column into PatientID, Visit, Dilution columns
def clean_sample_id_column(df_plate):
    # this transforms the troublesome 'Sample ID' column into an array
    column1_array = df_plate['Sample ID'].values

    # taking mark's advice this list comprehension inverts the contents of each element (i.e. cell) in the array
    column1_array = [cell[::-1] for cell in column1_array]

    # cleaning up data
    rex = re.compile(r'(?:(?P<Dilution> *[0]+1) *)?(?:(?P<Visit> *[1-3][v|V] *))?(?P<PatientID>[ |[A-Za-z0-9_]+)')
    outputs = [rex.match(x) for x in column1_array]

    # this takes the named groups from the regular expression above converts everything into a list of dictionaries
    # where the keys are group names (PatientID, Visit and Dilution) and the values are the corresponding string
    # components
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

    # This block of code goes through the list of dictionaries and appends the values to a list of their specific
    # category. e.g. a dilution of '100' is added to the dilution_list. These lists are then added to the dataframe
    # as columns at the specified index so they are at the front of the dataframe and not slapped on at the end.
    id_list = []
    visit_list = []
    dilution_list = []
    for dct in lst_of_dcts:
        id_list.append(dct['PatientID'])
        visit_list.append(dct['Visit'])
        dilution_list.append(dct['Dilution'])
    df_plate.insert(0, 'PatientID', id_list)
    df_plate.insert(1, 'Visit', visit_list)
    df_plate.insert(2, 'Dilution', dilution_list)

    # return new dataframe
    return df_plate

# function to find columns with null values, so we can comment "___ is missing"
def return_null_cols(df):
    null_col_list = [col for col in df.columns if df[col].isnull().any()]
    okay_list = ['Visit', 'Dilution', 'Hospital', 'Age', 'Gender']
    null_list = list(set(null_col_list) - set(okay_list))
    return null_list

# import excel data file
full_xls = pd.ExcelFile('06222016 Staph Array Data.xlsx')

# creating an index html file
fh_index = open("index.html", "w")
index_html_message = ""

# loop through each sheet
for sheet_num in range(11):
    # grab corresponding sheet as a dataframe, skipping the first row as it contains meaningless data
    df_plate_dirty = full_xls.parse(sheet_num, skiprows=1)

    # run dataframe through clean up function to divide Sample ID column
    df_plate = clean_sample_id_column(df_plate_dirty)

    # clean up column headers and reassign them
    df_plate.columns = map(lambda x: x.strip(), df_plate.columns)

    # fill in the info for hospital, age, gender according to existing implied data
    # skip the last Plate as there are no relevant columns
    if sheet_num != 10:
        df_plate['Hospital'] = df_plate['Hospital'].ffill()
        df_plate['Age'] = df_plate['Age'].ffill()
        df_plate['Gender'] = df_plate['Gender'].ffill()

    # export clean sheet as a tab delimited file
    df_plate.to_csv("Plate " + str(sheet_num + 1) + ".txt", index=False, sep='\t')
    print("File " + "Plate " + str(sheet_num + 1) + ".txt" + " created")

    # update index.html section with Plate # header
    index_html_message += "<p><b>"+"Plate " + str(sheet_num + 1)+"</b><p>"

    # name of columns that we will plot against dilution (in order of output layout)
    plot_columns = ['surface protein ext', 'cytoplasmic ext', 'Exoprotein ext', 'LukE', 'LukD', 'LukS-PV', 'LukF-PV',
                    'LukAB(Lab)', 'LukAB(cc30)', 'Hemolysin gamma A', 'Hemolysin gamma B', 'Hemolysin gamma C', 'HLA-1',
                    'HLA -2', 'HLA', 'Betatoxin', 'PNAG', 'SEO', 'SP', 'SEG', 'SEI', 'SEU', 'SEN', 'SEM', 'SEB',
                    'PSMalpha2', 'PSMalpha3', 'psmalpah4', 'PSM 4variant', 'Pn CWPS', 'PC4', 'PC-12', 'PC16', 'Pn PS12',
                    'Pn PS23', 'S.Pyogenese arcA', 'PLY', 'Tetanus Toxoid', 'Glom.extract', 'hIgG', 'SpA domD5-WT',
                    'SpA domD5FcNull', 'hIgA', 'BSA', 'HSA', 'Rabbit IgG', 'ABA', 'LDL']

    # visit number color coding dictionary
    visit_color = {"V1": "r", "V2": "b", "V3": "g"}

    # group by patient id and loop through each one
    patient_id = df_plate.groupby("PatientID")
    for patient_name, patient_data in patient_id:
        # if there are no dilution values, then don't plot (mainly for "Standard")
        if patient_data["Dilution"].isnull().any():
            continue
        # get list of null columns that will not be included in the summary html page
        null_list = return_null_cols(patient_data)
        # making sure patient name is a string
        patient_name = str(patient_name)
        # create html file for the patient
        fh = open("Plate " + str(sheet_num + 1) + "-" + patient_name + ".html", "w")
        html_message = "<table>\n<tr>\n"
        figure_num = 1
        # go through each data column to plot
        for plot_col in plot_columns:
            print("plotting figure " + str(figure_num))
            # set figure and width/height so axis labels are not cut off
            plt.figure(figure_num, figsize=(6.5, 6))
            plt_title = patient_name

            # if it is a "standard" patient, plot with no misc information or visits
            if "Standard" in patient_name:
                patient_name = "Standard"
                plt_title = plt_title + " " + plot_col
                plt.suptitle(plt_title, fontsize=14, fontweight='bold')
                plt.loglog(patient_data["Dilution"], patient_data[plot_col], color='k',
                           marker='o', markerfacecolor='none',
                           markersize=10,
                           markeredgewidth=2, label="N/A")
            else:
                # create title and assign it
                # for last sheet, no gender/age/hospital columns available, so create different title
                if sheet_num == 10:
                    plt_title = plt_title + " " + plot_col
                else:
                    plt_title = plt_title + " (" + patient_data["Gender"].iloc[0] + " " + str(
                        "%.f" % patient_data["Age"].iloc[0]) + " yr " + patient_data[
                                    "Hospital"].iloc[0] + ") " + plot_col
                plt.suptitle(plt_title, fontsize=14, fontweight='bold')
                # if visit value is empty, fill it with V1
                patient_data["Visit"].fillna(value="V1", inplace=True)
                # plot each visit on the same figure
                visits = patient_data.groupby("Visit")
                for visit_name, visit_data in visits:
                    # plotting with log axis, colors according to the visit_color dictionary
                    plt.loglog(visit_data["Dilution"], visit_data[plot_col], color=visit_color[visit_name.upper()],
                               marker='o', markerfacecolor='none',
                               markersize=10,
                               markeredgewidth=2, label=visit_name[1])
            # assigning other misc plot axis and legend information
            plt.xlabel('Dilution', fontsize=13)
            plt.ylabel('Intensity', fontsize=13)
            plt.legend(title="Visit", loc=1)
            # save plot in the correct directory
            fig_png_name = "Plate " + str(sheet_num + 1) + "/" + plt_title + ".png"
            plt.savefig(fig_png_name)
            print("saved figure [" + plt_title + "]")
            plt.close()
            # add figure to patient html page; if there are null values, print "___ missing"
            if plot_col in null_list:
                html_message += "<td><center>" + plot_col + "<br>missing</td>"
            else:
                html_message += "<td><img src=\"" + fig_png_name + "\" width=\"150\"></td>"
            # adding appropriate breaking points on patient html page
            if figure_num in [3, 9, 17, 25, 29, 39]:
                html_message += "</tr>\n<tr>"
            elif figure_num == 48:
                html_message += "</tr>\n</table>"
            figure_num += 1
        # update index.html and write/close out patient html page
        html_name = "Plate " + str(sheet_num + 1) + "-" + patient_name
        index_html_message += "<a href=\"" + html_name + ".html" + "\">"+html_name+"</a><br>"
        fh.write(html_message)
        fh.close()
# write/close out index.html page
fh_index.write(index_html_message)
fh_index.close()
