from . import get_pdf_details 

#import pandas 
import requests
import json

def gettradingdataframes(df, id_json, pdf_file_url):
    trading_dataframes = {}
    for last_name in id_json:
        first_name = id_json[last_name][0]
        last_doc_id = id_json[last_name][1]
        try:
            df_name = df[(df["Last"] == last_name) & (df["First"] == first_name)]
            doc_id = df_name.iloc[-1]["DocID"] #most recent
            
            if doc_id != last_doc_id:
                r = requests.get(f"{pdf_file_url}{doc_id}.pdf")
                outputpdf=f"pdfs/{doc_id}.pdf"
                with open(outputpdf,'wb') as pdf_file:
                    pdf_file.write(r.content)
                df_details = get_pdf_details.getpdfdetails(outputpdf)
                trading_dataframes[last_name] = df_details
                
                id_json[last_name][1] = int(doc_id) #update doc_id
                
                with open('ids.json', 'w', encoding='utf-8') as json_file:
                    json.dump(id_json, json_file, ensure_ascii=False, indent=4)
            else:
                pass
        except IndexError as err:
            #Given name not found
            pass
    return trading_dataframes