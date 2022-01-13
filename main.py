import re
import csv
import numpy as np
import pandas as pd
import requests as rq
from bs4 import BeautifulSoup

livros_para_comprar = []

links = pd.read_csv('links_estante.csv')

for index, rows in links.iterrows():

    dic_livro = {}

    url = 'https://www.estantevirtual.com.br{}'.format(links['link'][index])
    print(url)
    response = rq.get(url)
    html = BeautifulSoup(response.text, 'html.parser')

    article = html.find('article', {'class': 'livro-exemplar'})
    #print(article)
    dic_livro['Nome do Livro'] = article.find('h1', {'class': 'livro-titulo'}).get_text().strip()
    dic_livro['Autor'] = article.find('h2', {'class': 'livro-autor'}).get_text().strip()
    #print(dic_livro)

    div_preço = html.find('div', {'class': 'info-livro-vendedor-aside'})
    #print(div_preço)
    dic_livro['Valor'] = div_preço.find('strong', {'class': 'livro-preco-valor'}).get_text().strip()
    dic_livro['Frete'] = div_preço.find('span', {'class': 'livro-preco-frete'}).get_text().strip().strip('+').strip('envio*').strip()
    #print(dic_livro)

    section = html.find('section', {'class': 'livro__info m-info'})
    #print(section)
    dic_livro['Condição'] = section.find_all('p')[0].get_text().strip('Tipo:').strip().strip().strip()
    dic_livro['Editora'] = section.find('p', {'class': 'livro-specs info-publisher'}).get_text().strip().strip('Editora:').strip()
    dic_livro['Ano de Publicação'] = section.find('p', {'class': 'livro-specs info-year'}).get_text().strip().strip('Ano:').strip()
    dic_livro['ISBN'] = section.find_all('p')[5].get_text().strip().strip('ISBN:').strip()
    dic_livro['Idioma'] = section.find('p', {'class': 'livro-specs info-language'}).get_text().strip().strip('Idioma:').strip()
    #dic_livro['Descrição da condição'] = section.find('span', {'itemprop': 'description'}).get_text().strip()
    #print(dic_livro)

    aside = html.find('aside', {'class': 'sobre-o-livreiro'})
    #print(aside)
    dic_livro['Loja'] = [a['href'] for a in html.select('a[href]')][100:101]
    dic_livro['Reviews da Loja'] = aside.find('div', {'class': 'seller-review-box'}).get_text().strip().strip()
    #print(dic_livro)
    livros_para_comprar.append(dic_livro)

    #print(livros_para_comprar)

livros = pd.DataFrame(livros_para_comprar)

livros.to_csv('livros_para_estante.csv', index=False)

print(livros)

for livro in livros_para_comprar:
    print(livros)