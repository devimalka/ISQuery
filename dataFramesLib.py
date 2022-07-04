import pandas as pd


def ExcelSaver(df,filename,fileExtension):
    
   
    if fileExtension =='xls':
        xlswriter = pd.ExcelWriter(filename,engine='xlsxwriter')
        df.to_excel(xlswriter,index=False)
        xlswriter.save()
    elif fileExtension == 'csv':
        df.to_csv(filename)
        
  

