from flask import Flask, render_template, make_response, request
import requests, json
from datetime import date
import base64
from io import BytesIO
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__, template_folder='templates')
url = 'https://script.google.com/macros/s/AKfycbxzW3QGiAbYIialGTzt2sAZkj7AzskLCABYf-gCmWL70S79Fh6pIZlHvILatc7qqAp6/exec'
data_atual = date.today()

@app.route('/')
def index():
    year = request.args.get('ano')
    if year:
        rows_data = []
        if int(year) < data_atual.year:
            rows_data = getData(13, year)
        else:
            rows_data = getData(data_atual.month, year)

       # img = plotBump(rows_data)
        resp =  make_response(render_template("index.html", data=rows_data, ano=year))
        return resp
    else :
        return render_template("index.html")

def getData(month_limit, year):
    rows = []
    for month in range(1,month_limit):
        params = '?mes='+str(month)+'&ano='+year+'&rota=getLivrosPorMes'
        response = requests.get(url+params)
        data = response.json()
        rows.append(data)
    return rows

@app.route('/livros')
def livros():
    params = '?rota=getLivros'
    response = requests.get(url+params)
    data = response.json()
    resp =  make_response(render_template("livros.html", livros=data))
    return resp

@app.route('/livro')
def livro():
    isbn = request.args.get('isbn')
    if isbn:
        params = '?isbn='+isbn+'&rota=getLivro'
        
        response = requests.get(url+params)
        data = response.json()
        livros = data["exemplares"]
        meses = [i["mes_ano"] for i in livros]
        qtd = [i["copias_vendidas"] for i in livros]
                
        img = plotLine(meses, qtd)
        resp =  make_response(render_template("livro.html", livro=data, img=img))
        return resp
    else :
        return render_template("livro.html", data="teste")
    
def plotLine(meses, qtd):
    buf = BytesIO()
    
    plt.figure(figsize=(max(qtd), len(meses)))
    fig, ax = plt.subplots()
    plt.plot(meses, qtd)
    
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    encoded = base64.b64encode(buf.getvalue()).decode('utf-8')
    img = f'data:image/png;base64,{encoded}'
    return img

if __name__ == '__main__':
    app.run()
