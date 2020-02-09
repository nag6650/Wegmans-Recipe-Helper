from flask import Flask, render_template, request, g
import nlp_parser
import scraping
import Router


app = Flask(__name__)
ingList = []


#@app.route('/result', methods = ['POST', 'GET'])
#def hello_world():
#    if request.method == 'POST':
#        return scraping.scrape(request.form['Name'])
#        #return render_template("result.html", result=res)

@app.route('/result', methods = {'POST', 'GET'})
def result():
    if request.method == 'POST':
        #for ing in ingList:
            # call Router's method
            myListofDicts = [{
                "name": "salt",
                "price":"1.00",
                "shelf":"L",
                "aisle":12
            }, {
                "name": "pepper",
                "price": "10000.00",
                "shelf": "R",
                "aisle": 21

            }]
            return render_template("result.html", dictList=myListofDicts)

@app.route('/confirm', methods = {'POST', 'GET'})
def confirm():
    if request.method == 'POST':
        global ingList
        try:
            ingName = request.form['submit_button']
            ingList.remove(ingName)
        except Exception:
            try:
                ingList = nlp_parser.ingredient_getter(scraping.scrape(request.form['Name']))
            except Exception:
                try:
                    ingName = request.form['ing']
                    print(ingName)
                    ingList.append(ingName)
                except:
                    print("poop")
                    pass
                pass
            pass

        return render_template("confirm.html", ingList=ingList)


@app.route('/')
def index():
    return render_template('index.html')
