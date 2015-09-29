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
        
        cur.execute("USE ViceMatch;")
        cur.execute("SELECT notes, image, palate, nose, categories, strength FROM whiskey_info WHERE name='%s';" %WhiskeyName)
        query_whiskey_input = cur.fetchall()
    
    for whisk in query_whiskey_input:
        WhiskeyNotes = whisk[0]
        WhiskeyImage = whisk[1]
        WhiskeyPalate= whisk[2]
        WhiskeyNose= whisk[3]
        WhiskeyCategories = whisk[4]
        WhiskeyStrength = whisk[5]
            
  
    cur.execute("USE ViceMatch;")
    cur.execute("SELECT cigarName, matchScore FROM Vmatch WHERE whiskeyName = '%s' ORDER BY matchScore DESC LIMIT 2;" %(WhiskeyName))
    query_match_output = cur.fetchall()
            
    cigName = []
    matchScores = []
    for result in query_match_output:
        cigName.append(result[0])
        matchScores.append(result[1])


    cur.execute("USE ViceMatch;")
    cur.execute("SELECT name, notes, description, image, strength FROM cigar_info WHERE name = '%s' LIMIT 1;"%(cigName[0]))
    query_cigar_output = cur.fetchall()

        

    matchedCigars = []
    for result in query_cigar_output:
        matchedCigars.append(dict(name=result[0], notes=result[1], description=result[2], image=result[3], matchScore = matchScores[cigName.index(str(result[0]))],strength = result[4]))


    cur.execute("USE ViceMatch;")
    cur.execute("SELECT wood, fruits, spice, earth, nuts, cereal, chocolate, vanilla, flowers, coffee, feint, name, notesC FROM cigar_categories WHERE name = '%s' LIMIT 1;"%(whiskeyName))
    query_more_matches = cur.fetchall()

    moreMatches = []
    for crs in query_more_matches:
        moreMatches.append(dict(wood = crs[0], fruits = crs[1], spice = crs[2], earth = crs[3], nuts = crs[4], cereal = crs[5], chocolate = crs[6], vanilla = crs[7], flowers = crs[8], coffee = crs[9], feint = crs[10], name = crs[11] ,notesC = crs[12]))

    return render_template("output.html", WhiskeyImage = WhiskeyImage ,matchedCigars = matchedCigars, WhiskeyName = WhiskeyName , WhiskeyNotes = WhiskeyNotes,WhiskeyCategories = WhiskeyCategories, WhiskeyPalate= WhiskeyPalate,WhiskeyNose = WhiskeyNose,WhiskeyStrength = WhiskeyStrength, cigN = cigName[0], moreMatches = moreMatches, whiskey = whiskey)



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

