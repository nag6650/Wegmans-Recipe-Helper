from flask import Flask, render_template, request
import scraping


app = Flask(__name__)
ingList = []
ButtonPressed = 0

#@app.route('/result', methods = ['POST', 'GET'])
#def hello_world():
#    if request.method == 'POST':
#        return scraping.scrape(request.form['Name'])
#        #return render_template("result.html", result=res)

@app.route('/confirm', methods = {'POST', 'GET'})
def confirm():
    if request.method == 'POST':
        # ingList = get array
        # try:
        #     ingName = request.form['value']
        #     ingList.remove(ingName)
        # except Exception:
        #     pass
        return render_template("confirm.html", ingList=ingList)


@app.route('/')
def index():
    ingList = ['apple', 'orange', 'milk']
    return render_template('testsite.html')
