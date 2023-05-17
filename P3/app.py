from flask import Flask, render_template, make_response, request
import requests, json
from datetime import date

app = Flask(__name__, template_folder='templates')
url = 'https://script.google.com/macros/s/AKfycbxzW3QGiAbYIialGTzt2sAZkj7AzskLCABYf-gCmWL70S79Fh6pIZlHvILatc7qqAp6/exec'
data_atual = date.today()



@app.route('/')
def index():
    year = request.args.get('ano')

    if year:
        livro_mes = []
        if int(year) < data_atual.year:
            for month in range(1,13):
                params = '?mes='+str(month)+'&ano='+year+'&rota=getGrafico'
                response = requests.get(url+params)
                data = response.json()
                livro_mes.append(data)

        else:
            for month in range(1,data_atual.month):
                params = '?mes='+str(month)+'&ano='+year+'&rota=getGrafico'
                response = requests.get(url+params)
                data = response.json()
                livro_mes.append(data)
        
        resp =  make_response(render_template("index.html", data=livro_mes))
        return resp
    else :
        return render_template("index.html")

@app.route('/livros')
def livros():
    params = '?rota=getLivros'
    response = requests.get(url+params)
    data = response.json()
    resp =  make_response(render_template("livros.html", livros=data))
    return resp
   #return render_template("livros.html", data="teste")


@app.route('/livro')
def livro():
    isbn = request.args.get('isbn')
    if isbn:
        params = '?isbn='+isbn+'&rota=getLivro'
        
        response = requests.get(url+params)
        data = response.json()

        resp =  make_response(render_template("livro.html", livro=data))
        return resp
    else :
        return render_template("livro.html", data="teste")

if __name__ == '__main__':
    app.run()
