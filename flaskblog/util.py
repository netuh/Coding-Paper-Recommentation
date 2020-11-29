import plotly
import plotly.graph_objs as go

import pandas as pd
import json

from bs4 import BeautifulSoup
from scraper_api import ScraperAPIClient
import requests

colors = ['lightseagreen', 'lightsalmon', 'lightsteelblue',
          'lightcoral', 'lightgoldenrodyellow', 'lime']
URL = "http://api.scraperapi.com/"
API_KEY = "8fccbfbc3c3d3d708cb9691af4099a2a"


def create_plot_pie(c):
    labels = []
    values = []
    for element in c:
        labels.append(element)
        values.append(int(c[element]))
    data = [
        go.Pie(
            labels=labels,
            values=values
        )
    ]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def create_plot_violin(dic_data, message='total'):
    data = []
    counter = 0
    for key, piece_of_data in dic_data.items():
        df = pd.DataFrame({'y': piece_of_data})
        total = 0
        for data_point in piece_of_data:
            total += data_point
        data.append(go.Violin(y=df['y'], box_visible=True, line_color='black',
                              meanline_visible=True, fillcolor=colors[counter], opacity=0.6,
                              x0=f"{message} = {total}", name=key))
        counter += 1
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def create_plot_bar(c, byKeys=True):
    x = []
    y = []
    # for element in c.items():
    if (byKeys):
        for element in sorted(c.items()):
            if element[0] and element[1]:
                x.append(element[0])
                y.append(element[1])
    else:
        for element in c.most_common():
            if element[0] and element[1]:
                x.append(element[0])
                y.append(element[1])
    df = pd.DataFrame({'x': x, 'y': y})  # creating a sample dataframe
    data = [
        go.Bar(
            # marker_color='indianred',
            x=df['x'],  # assign x as the dataframe column 'x'
            y=df['y']

        )
    ]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def google_scholar_grap(search):
    soup = get_papers_google(search)
    item = soup.select('[data-lid]')[0]
    result = {"title": item.select('h3')[0].get_text(),
              "authors": select_authors(item.select('.gs_a')[0]),
              "abstract": item.select('.gs_rs')[0].get_text(),
              "url": item.select('h3 a')[0]['href']}
    return result


def select_authors(element_authors):
    authors = ""
    for item in element_authors.select('a'):
        if not authors:
            authors = item.get_text()
        else:
            authors = "{0}, {1}".format(authors, item.get_text())

    return authors


def get_papers_google(search):
    client = ScraperAPIClient(API_KEY)
    url = 'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q={0}&btnG='.format(search)
    response = client.get(url=url, retry=5)
    print(response)
    soup = BeautifulSoup(response.text,
                         'lxml')
    while response.status_code == 500 and not soup.select('[data-lid]'):
        response = client.get(url=url, retry=5)
        print(response)
        soup = BeautifulSoup(response.text,
                             'lxml')

    return soup
