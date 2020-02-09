from flask import Flask, render_template, request
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
        myListofDicts = []
        missingItems = []
        totalPrice = 0.00
        for ing in ingList:
            product = Router.getItemRoute(ing)
            if product['name'] == "No availabilities at this location" or product['name'] == "No prices available":
                missingItems.append(ing)
            else:
                myListofDicts.append(product)
                totalPrice += product['price']

        return render_template("result.html", dictList=myListofDicts, missing=missingItems, price=round(totalPrice,2))

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
