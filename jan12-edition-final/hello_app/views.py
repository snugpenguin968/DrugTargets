from datetime import datetime
from flask import Flask, Blueprint, render_template, request
from . import app
import pandas as pd

@app.route("/")
def home():
    return render_template("base.html")

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route("/hello/")
def hello():
    return render_template("base2.html")
    
    
@app.route("/hello/<param1>/<param2>")
def hello_there(param1 = None, param2 = None):
    df=pd.read_csv('final2.csv')
    prot=param1
    idx=0
    if df['Gene_Symbol'].isin([prot]).any():
        idx=df[df['Gene_Symbol'].isin([prot])].index[0]
    elif df['Uniprot_Acc'].isin([prot]).any():
        idx=df[df['Uniprot_Acc'].isin([prot])].index[0]
    elif df['Omim ID'].isin([prot]).any():
        idx=df[df['Omim ID'].isin([prot])].index[0]
    elif df['Ensemble Gene ID'].isin([prot]).any():
        idx=df[df['Ensemble Gene ID'].isin([prot])].index[0]
    row=df.loc[idx,:]
    url= "https://www.uniprot.org/uniprot/"+ row[1]  
    url2 = "https://omim.org/entry/"+str(row[2])+"?search="+row[0]+"&highlight="+row[0].lower()+"#geneFunction"
    url3= "https://omim.org/entry/"+str(row[2])+"?search="+row[0]+"&highlight="+row[0].lower()+"#animalModel"
    url4 = "https://depmap.org/portal/gene/" + row[0]
    url5 = "https://www.proteinatlas.org/" + row[1] + "/subcellular"
    url6 ="https://www.uniprot.org/uniprot/" + row[1]+"#subcellular_location"
    url7 ="https://www.proteinatlas.org/"  + row[1] + "/tissue"
    url8 ="https://www.proteinatlas.org/" + row[1] + "/cell+line"
    url9 ="https://www.cbioportal.org/results/cancerTypesSummary?case_set_id=all&gene_list=" + row[0] + "&cancer_study_list=5c8a7d55e4b046111fee2296"
    url10 ="https://www.cbioportal.org/results/comparison?case_set_id=all&gene_list=" + row[0] + "&cancer_study_list=5c8a7d55e4b046111fee2296"
    url11 ="https://www.mousephenotype.org/data/search?term=" + row[0] +"&type=gene"
    url12 ="https://pharos.nih.gov/targets/" + row[1]
    url13 ="https://platform.opentargets.org/target/" + row[3]

    myValue = param2
    to_open=[]
    checkedValue = int(param2)
    if  (checkedValue)& 1 == 1: #function
        to_open.append(url)
        to_open.append(url2)
    if  (checkedValue) & 2 == 2: #animal model
        to_open.append(url3)
    if (checkedValue) & 4 == 4: #protein level in cell lines
        to_open.append(url4)
    if  (checkedValue) & 8 == 8: #subcellular location
        to_open.append(url5)
        to_open.append(url6)
    if  (checkedValue) & 16 == 16: #tissue distribution
         to_open.append(url7)
    if  (checkedValue) & 32 == 32: #rna expression in different cell lines
        to_open.append(url8)
    if  (checkedValue) & 64 == 64: # mutation frequency in cancer and survival rate
        to_open.append(url9)
        to_open.append(url10)
    if  (checkedValue) & 128 == 128: #mouse phenotypes
        to_open.append(url11)
    if  (checkedValue) & 256 == 256: #drug targets
        to_open.append(url12)
        to_open.append(url13)
    
    return render_template(
        "base2.html",
        name= to_open,
        date=datetime.now()
    )







@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")
