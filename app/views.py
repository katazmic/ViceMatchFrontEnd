from a_Model import ModelIt
from app import app
from flask import render_template, request
import pymysql as mdb

@app.route('/input')
def cities_input():
    return render_template("input.html")


@app.route('/output')
def cigar_output():
    #pull 'ID' from input field and store it
    WhiskeyName = request.args.get('ID')
    db = mdb.connect(user = "root", host = "localhost", db = "ViceMatch", charset = 'utf8')
    with db:
        cur = db.cursor()
        ################### info about the whiskey #################

    cur.execute("USE ViceMatchUpdated;")
    cur.execute("SELECT wood, fruits, spice, earth, nuts, cereal, chocolate, vanilla, flowers, coffee, feint, name, notes,image,strength FROM whiskey_info WHERE name = '%s';"%(WhiskeyName))
    query_whiskey = cur.fetchall()
    crs = query_whiskey[0]
    
    whiskey = dict(wood = crs[0], fruits = crs[1], spice = crs[2], earth = crs[3], nuts = crs[4], cereal = crs[5], chocolate = crs[6], vanilla = crs[7], flowers = crs[8], coffee = crs[9], feint = crs[10], name = crs[11] ,notes = crs[12], image = crs[13], strength = crs[14])




        #########################  BM CIGAR ##########################3
  
    cur.execute("USE ViceMatchUpdated;")
    cur.execute("SELECT cigarName FROM Vmatch_more WHERE whiskeyName = '%s' AND category = 'ALL' ORDER BY overallMatch DESC LIMIT 1;" %(WhiskeyName))
    query_best_match = cur.fetchall()            
    cigar_BM_name = query_best_match[0]

    
    cur.execute("USE ViceMatchUpdated;")
    cur.execute("SELECT wood, fruits, spice, earth, nuts, cereal, chocolate, vanilla, flowers, coffee, feint, name, notes,image,strength FROM cigar_info WHERE name = '%s';"%(cigar_BM_name))
    query_cigar_info = cur.fetchall()
    crs = query_cigar_info[0]
    
    cigar_BM = dict(wood = crs[0], fruits = crs[1], spice = crs[2], earth = crs[3], nuts = crs[4], cereal = crs[5], chocolate = crs[6], vanilla = crs[7], flowers = crs[8], coffee = crs[9], feint = crs[10], name = crs[11] ,notes = crs[12], image = crs[13], strength = crs[14])


        

        ############## More Matches info ##################
        

    cur.execute("USE ViceMatchUpdated;")
    cur.execute("SELECT cigarName FROM Vmatch_more WHERE whiskeyName = '%s' AND category != 'ALL';" %(WhiskeyName))
    query_more_matches = cur.fetchall()

    conditionMatch = 'name = '
    for i in query_more_matches[:-1]:
        conditionMatch = conditionMatch +  '\''+i[0]+'\'' + ' OR name = '

    conditionMatch = conditionMatch +  ' \'' + query_more_matches[-1][0] + '\''
    

    cur.execute("USE ViceMatchUpdated;")
    cur.execute("SELECT wood, fruits, spice, earth, nuts, cereal, chocolate, vanilla, flowers, coffee, feint, name, notes,image,strength FROM cigar_info WHERE %s;"%(conditionMatch))
    query_more_matches_info = cur.fetchall()
    print 'hi'
    moreMatches = []
    for crs in query_more_matches_info:
        if crs[13] != 'https://cdn2.jrcigars.com/images/item/default.jpg/220/220':
            moreMatches.append(dict(wood = crs[0], fruits = crs[1], spice = crs[2], earth = crs[3], nuts = crs[4], cereal = crs[5], chocolate = crs[6], vanilla = crs[7], flowers = crs[8], coffee = crs[9], feint = crs[10], name = crs[11] ,notes = crs[12], image = crs[13],strength = crs[14]))
 


        
    return render_template("output.html", whiskey = whiskey, cigar_BM = cigar_BM, moreMatches = moreMatches)



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

