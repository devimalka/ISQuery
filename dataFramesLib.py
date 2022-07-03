import pandas as pd


def ExcelSaver(df,filename):
    xlswriter = pd.ExcelWriter(filename,engine='xlsxwriter')
    df.to_excel(xlswriter,index=False)
    xlswriter.save()

