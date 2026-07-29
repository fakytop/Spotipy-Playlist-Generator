import json
import pandas as pd

def save_json_file(data,file_name):
    with open(file_name,'w',encoding='utf-8') as file:
        json.dump(data,file,indent=4,ensure_ascii=False)
    
    print(f"Se guardó el archivo {file_name}.json en la raíz del directorio.")
    
def save_xlsx_file(data,file_name):
    df = pd.DataFrame(data)
    df.to_excel(file_name,index=False)
