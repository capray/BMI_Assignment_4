import pandas as pd
import numpy as np

full_xls = pd.ExcelFile('test_data_plate1.xlsx')
df_plate = full_xls.parse(0)
# df_plate[df_plate[]==""] = np.NaN
df_plate['Hospital '] = df_plate['Hospital '].ffill()


print(df_plate)