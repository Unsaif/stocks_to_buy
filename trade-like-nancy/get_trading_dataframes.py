from . import get_pdf_details 
from .database import SessionLocal
from . import models

import requests

def gettradingdataframes(df, id_df, pdf_file_url):
    trading_dataframes = {}
    for i, entry in id_df.iterrows():
        id = entry["id"]
        last_name = entry["last_name"]
        first_name = entry["first_name"]
        last_doc_id = entry["last_doc_id"]
        try:
            df_name = df[(df["Last"] == last_name) & (df["First"] == first_name)]
            doc_id = df_name.iloc[-1]["DocID"] #most recent
            
            if str(doc_id) != last_doc_id:
                r = requests.get(f"{pdf_file_url}{doc_id}.pdf")
                outputpdf=f"pdfs/{doc_id}.pdf"
                with open(outputpdf,'wb') as pdf_file:
                    pdf_file.write(r.content)
                df_details = get_pdf_details.getpdfdetails(outputpdf)
                trading_dataframes[last_name] = df_details
                
                #update doc_id
                with SessionLocal() as session:
                    db_person = session.get(models.People, id)
                    if not db_person:
                        print("No person found")
                        #raise HTTPException(status_code=404, detail="Hero not found")
                    setattr(db_person, "last_doc_id", str(doc_id))
                    session.add(db_person)
                    session.commit()
                    session.refresh(db_person)
            else:
                pass
        except IndexError as err:
            pass
    return trading_dataframes