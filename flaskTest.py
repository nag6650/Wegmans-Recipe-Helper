from flask import Flask, render_template, request, g
import nlp_parser
import scraping


app = Flask(__name__)
ingList = []


#@app.route('/result', methods = ['POST', 'GET'])
#def hello_world():
#    if request.method == 'POST':
#        return scraping.scrape(request.form['Name'])
#        #return render_template("result.html", result=res)

@app.route('/confirm', methods = {'POST', 'GET'})
def confirm():
    if request.method == 'POST':
        global ingList
        # ingList = get array
        try:
            ingName = request.form['submit_button']
            #print("hi " + ingName)
            ingList.remove(ingName)
        except Exception:
            try:
                ingList = nlp_parser.ingredient_getter(scraping.scrape(request.form['Name']))
            except Exception:
                pass
            #print("failure")
            pass
        return render_template("confirm.html", ingList=ingList)


@app.route('/')
def index():
    return render_template('testsite.html')
