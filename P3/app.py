from flask import Flask, render_template, make_response, request
import requests, json

app = Flask(__name__, template_folder='templates')
url = 'https://script.google.com/macros/s/AKfycbxzW3QGiAbYIialGTzt2sAZkj7AzskLCABYf-gCmWL70S79Fh6pIZlHvILatc7qqAp6/exec'


@app.route('/')
def index():
    year = request.args.get('ano')
    month = request.args.get('mes')
    #print("---------------------- ", request.headers)
    #year = args['ano']
    #month = args['mes']
    #url = 'https://script.google.com/macros/s/AKfycbxzW3QGiAbYIialGTzt2sAZkj7AzskLCABYf-gCmWL70S79Fh6pIZlHvILatc7qqAp6/exec?mes=3&ano=2023&rota=getLivrosPorMes'
    
    if month and year:
        params = '?mes='+month+'&ano='+year+'&rota=getLivrosPorMes'
        
        response = requests.get(url+params)
        data = response.json()

        resp =  make_response(render_template("index.html", data=data))
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
