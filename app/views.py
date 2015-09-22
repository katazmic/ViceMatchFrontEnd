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
    db = mdb.connect(user = "root", host = "localhost", db = "WhiskeyAndCigars", charset = 'utf8')
    with db:
        cur = db.cursor()
        cur.execute("SELECT notes, image, Palate, Nose, categories FROM whiskey_info WHERE name='%s';" % WhiskeyName)
        query_whiskey_input = cur.fetchall()
    
    for whisk in query_whiskey_input:
        WhiskeyNotes = whisk[0]
        WhiskeyImage = whisk[1]
        WhiskeyPalate= whisk[2]
        WhiskeyNose= whisk[3]
        WhiskeyCategories = whisk[4]
            
    with db:
        cur = db.cursor()
        cur.execute("SELECT cigarName, matchScore FROM cigar_whiskey_match WHERE whiskeyName='%s' ORDER BY matchScore DESC LIMIT 3;" % WhiskeyName)
        query_match_output = cur.fetchall()
            
    cigName = []
    matchScores = []
    for result in query_match_output:
        cigName.append(result[0])
        matchScores.append(result[1])

    with db:
        cur = db.cursor()
        cur.execute("SELECT name, notes, flavor, image FROM cigar_info WHERE name = '%s' OR name = '%s' OR name = '%s';" %(cigName[0],cigName[1], cigName[2]))
        query_cigar_output = cur.fetchall()

    matchedCigars = []
    for result in query_cigar_output:
        matchedCigars.append(dict(name=result[0], notes=result[1], flavor=result[2], image=result[3], matchScore = matchScores[cigName.index(result[0])]))



    return render_template("output.html", WhiskeyImage = WhiskeyImage ,matchedCigars = matchedCigars, WhiskeyName = WhiskeyName , WhiskeyNotes = WhiskeyNotes,WhiskeyCategories = WhiskeyCategories, WhiskeyPalate= WhiskeyPalate,WhiskeyNose = WhiskeyNose, cigN = cigName[1])


