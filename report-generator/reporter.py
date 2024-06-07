#LIBRERIAS
import pandas as pd
from docxtpl import DocxTemplate
from docx2pdf import convert
from datetime import datetime

#INPUTS
df = pd.read_excel(r"D:\Users\Dell\curso_python\python-courses-main\PROJECT_01\BD_muestra.xlsx") 
doc1 = DocxTemplate(r"D:\Users\Dell\curso_python\python-courses-main\PROJECT_01\reportTmpl3.docx") 
fecha = datetime.today()

#agrupar el dataframe según el par de combinaciones CECO y RUC
group_df = df.groupby(['CECO','RUC'])
group_dict = {name: group for name, group in group_df}



#iterar para cada combinación
for name, group in group_dict.items():
    #print(group.dtypes)
    #convertir un Dataframe a Diccionario, en el formato de Orientación por 'records'
    Tabla_resumen = group.query('MONTO_MONEDA_ORIGINAL > 0').to_dict(orient='records')
    Tabla_detalle = group.to_dict(orient='records')
    #print(Tabla_resumen)
    #print(type(Tabla_resumen))
    Tabla_detalle[0]["OPERACIÓN_DETRACCIÓN"]="{:.2f}".format(Tabla_detalle[0]["OPERACIÓN_DETRACCIÓN"])
    print(type(Tabla_detalle[0]["OPERACIÓN_DETRACCIÓN"]))
    

           
    Proveedor = group["SUBCONTRATISTA"].max()
    Moneda = group["MONEDA"].max()
    Monto_Total_Val = group["MONTO_VAL_INC_IGV"].sum()
    Monto_Total_Pagado = group["MONTO_PAGO"].sum()
    deuda = Monto_Total_Val - Monto_Total_Pagado 

    context = {
    
    "fecha" : fecha.strftime('%d/%m/%Y'),
    "ceco" : name[0],
    "ruc" : name[1],
    "proveedor" : Proveedor,
    "moneda" : Moneda,
    "Monto_Total_Val" : f'{Monto_Total_Val:,.2f}',
    "Monto_Total_Pagado" : f'{Monto_Total_Pagado:,.2f}',
    "deuda" : f'{deuda:,.2f}',
    "Tabla01" : Tabla_resumen,
    "Tabla02" : Tabla_detalle
    }

    doc1.render(context)

    #OUTPUTS
    doc1.save(f'D:\\Users\\Dell\\curso_python\\python-courses-main\\PROJECT_01\\Output\\{name[0]}_{name[1]}.docx')
    #convert(f'D:\\Users\\Dell\\curso_python\\python-courses-main\\PROJECT_01\\Output\\{name[0]}_{name[1]}.docx',f'D:\\Users\\Dell\\curso_python\\python-courses-main\\PROJECT_01\\Output\\{name[0]}_{name[1]}.pdf')
    #group.to_excel(f'D:\\Users\\Dell\\curso_python\\python-courses-main\\PROJECT_01\\Output\\{name[0]}_{name[1]}.xlsx', index=False)
    