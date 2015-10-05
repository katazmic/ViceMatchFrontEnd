from a_Model import ModelIt
from app import app
from flask import render_template, request
import pymysql as mdb
import numpy as np

@app.route('/input')
def cities_input():
    return render_template("input.html")

    
@app.route('/output')

def cigar_output():
    def rearranged(V1,V2):
        idx = list(np.zeros(len(V1)))
        k=0
        j=0
        for i in range(len(V1)):
            if V1[i] != 0:
                idx[k] = i
                k=k+1
            else:
                idx[-1-j] = i
                j=j+1

        nonZ = k
        idx2 = idx[:]
        j=0
        k=0
        for i in range(nonZ):
            if V2[idx[i]] == 0:
                idx2[k] = idx[i]
                k=k+1
            else:
                idx2[nonZ-j] = idx[i]
                j=j+1
        j=0
        k=nonZ-1
        i= nonZ-1
        while i>=0:
            if V2[idx[i]] != 0:
                idx2[k] = idx[i]
                k=k-1
            else:
                idx2[j] = idx[i]
                j=j+1
            i=i-1

        i=nonZ
        j=0
        k=nonZ
        while i<len(V2):
            if V2[idx[i]] !=0:
                idx2[k] = idx[i]
                k=k+1
            else:
                idx2[-1-j] = idx[i]
                j=j+1
            i=i+1

        return idx2


    #pull 'ID' from input field and store it
    WhiskeyName = request.args.get('ID')
    db = mdb.connect(user = "root", host = "localhost", db = "ViceMatch", charset = 'utf8')
    
    with db:
        cur = db.cursor()
        ################### info about the whiskey #################
        cur.execute("USE ViceMatchUpdated;")
        cur.execute("SELECT wood, fruits, spice, earth, nuts, cereal, chocolate, vanilla, flowers, coffee, feint, mineral, name, notes,image,strength,categories FROM whiskey_info WHERE name = '%s';"%(WhiskeyName))
        query_whiskey = cur.fetchall()
    crsW = query_whiskey[0]
    categories = ['wood', 'fruit', 'spice', 'earth', 'nuts', 'cereal', 'chocolate', 'vanilla', 'flowers', 'coffee', 'feinty','mineral']

    


        #########################  BM CIGAR ##########################
    with db:
        cur = db.cursor()
        cur.execute("USE ViceMatchUpdated;")
        cur.execute("SELECT cigarName FROM Vmatch_more WHERE whiskeyName = '%s' AND category = 'ALL' ORDER BY overallMatch DESC LIMIT 1;" %(WhiskeyName))
        query_best_match = cur.fetchall()            
    cigar_BM_name = query_best_match[0]

    with db:
        cur = db.cursor()
    
        cur.execute("USE ViceMatchUpdated;")
        cur.execute("SELECT wood, fruits, spice, earth, nuts, cereal, chocolate, vanilla, flowers, coffee, feint, mineral, name, notes,image,strength,categories FROM cigar_info WHERE name = '%s';"%(cigar_BM_name))
        query_cigar_info = cur.fetchall()
    crs = query_cigar_info[0]
    
    cigar_BM = dict(wood = crs[0], fruits = crs[1], spice = crs[2], earth = crs[3], nuts = crs[4], cereal = crs[5], chocolate = crs[6], vanilla = crs[7], flowers = crs[8], coffee = crs[9], feint = crs[10], name = crs[12] ,notes = crs[13], image = crs[14], strength = crs[15], categories = crs[16])

    idx = rearranged(crsW[:12],crs[:12])
    whiskey = {categories[idx[0]] :crsW[idx[0]], categories[idx[1]] : crsW[idx[1]],  categories[idx[2]] : crsW[idx[2]],  categories[idx[3]] :crsW[idx[3]],  categories[idx[4]]: crsW[idx[4]],  categories[idx[5]] : crsW[idx[5]],  categories[idx[6]]: crsW[idx[6]],  categories[idx[7]]: crsW[idx[7]],  categories[idx[8]]: crsW[idx[8]],  categories[idx[9]]: crsW[idx[9]],  categories[idx[10]]:crsW[idx[10]], categories[idx[11]]:crsW[idx[11]], 'name' : crsW[12] ,'notes' : crsW[13], 'image' : crsW[14], 'strength': crsW[15], 'categories': crsW[16]}
    
    whiskeyCat = [categories[i] for i in idx] 
    whiskeyCatV = [crsW[i] for i in idx]
    cigarBMCat = [categories[i] for i in idx] 
    cigarBMCatV = [crs[i] for i in idx] 

        

        ############## More Matches info ##################
    with db:
        cur = db.cursor()

        cur.execute("USE ViceMatchUpdated;")
        cur.execute("SELECT cigarName FROM Vmatch_more WHERE whiskeyName = '%s' AND category != 'ALL';" %(WhiskeyName))
        query_more_matches = cur.fetchall()

    if len(query_more_matches)!=0:
        conditionMatch = 'name = '
        for i in query_more_matches[:-1]:
            conditionMatch = conditionMatch +  '\''+i[0]+'\'' + ' OR name = '

        conditionMatch = conditionMatch +  ' \'' + query_more_matches[-1][0] + '\''

        
        with db:
            cur = db.cursor()
            cur.execute("USE ViceMatchUpdated;")
            cur.execute("SELECT wood, fruits, spice, earth, nuts, cereal, chocolate, vanilla, flowers, coffee, feint,mineral, name, notes,image,strength,categories FROM cigar_info WHERE %s;"%(conditionMatch))
            query_more_matches_info = cur.fetchall()
    else:
        query_more_matches_info = []
        
    moreMatches = []
    cigarCat_m = []
    cigarCatV_m = []
    whiskeyCat_m = []
    whiskeyCatV_m = []

    for crs in query_more_matches_info:
        if crs[13] != 'https://cdn2.jrcigars.com/images/item/default.jpg/220/220':
            idx = rearranged(crsW[:12],crs[:12])
            cigarCat_m.append([categories[i] for i in idx])
            cigarCatV_m.append([crs[i] for i in idx])
            whiskeyCat_m.append([categories[i] for i in idx])
            whiskeyCatV_m.append([crsW[i] for i in idx])


            moreMatches.append(dict(wood = crs[0], fruits = crs[1], spice = crs[2], earth = crs[3], nuts = crs[4], cereal = crs[5], chocolate = crs[6], vanilla = crs[7], flowers = crs[8], coffee = crs[9], feint = crs[10],mineral = crs[11] ,name = crs[12] ,notes = crs[13], image = crs[14],strength = crs[15],categories = crs[16]))
 
        
    return render_template("output.html", whiskey = whiskey, cigar_BM = cigar_BM, moreMatches = moreMatches,whiskeyCat = whiskeyCat, whiskeyCatV = whiskeyCatV,cigarCat_m = cigarCat_m, cigarCatV_m = cigarCatV_m, whiskeyCatV_m = whiskeyCatV_m, whiskeyCat_m = whiskeyCat_m,cigarBMCat = cigarBMCat, cigarBMCatV = cigarBMCatV)



@app.route('/fullmatchF')
def fullOutputf():
    return render_template("fullmatchF.html")

@app.route('/fullmatchMF')
def fullOutputmf():
    return render_template("fullmatchMF.html")

@app.route('/fullmatchM')
def fullOutputm():
    return render_template("fullmatchM.html")

@app.route('/fullmatchLM')
def fullOutputlm():
    return render_template("fullmatchLM.html")

@app.route('/fullmatchL')
def fullOutputl():
    return render_template("fullmatchL.html")

