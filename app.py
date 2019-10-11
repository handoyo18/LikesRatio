from flask import Flask, render_template 
import pandas as pd
import requests
from bs4 import BeautifulSoup 

app = Flask(__name__)

def scrap(url):
    url_get = requests.get(url)
    soup = BeautifulSoup(url_get.content,"html.parser")
    table = soup.find('table', attrs={'class':'table1'})
    tr = table.find_all('tr')

    temp = [] #initiating a tuple

    for i in range(1, len(tr)):
        row = table.find_all('tr')[i]
        
        #get bulan
        period = row.find_all('td')[0].text
        period = period.strip() #for removing the excess whitespace
        
        #get inflasi
        inflation = row.find_all('td')[1].text
        inflation = inflation.strip() #for removing the excess whitespace
        
        temp.append((period,inflation)) 
    
    temp = temp[::-1]

    df = pd.DataFrame(temp, columns = ('period','inflation'))
    df['inflation'] = df['inflation'].str.replace(" %","")
    df['inflation'] = df['inflation'].astype('float64')

    return df

@app.route("/")
# This fuction for rendering the table
def index():
    df = scrap('https://www.bi.go.id/id/moneter/inflasi/data/Default.aspx')
    df = df.to_html(classes=["table table-bordered table-striped table-dark table-condensed"])

    return render_template("index.html", table=df)


@app.route("/charts")
# This fuction for rendering the plot
def charts():
    import altair as alt #using altair library

    df = scrap('https://www.bi.go.id/id/moneter/inflasi/data/Default.aspx')
    order = df['period'].tolist()

    chart = (
        alt.Chart(df)
        .encode( # Put the x and y
            alt.X("period",
                sort=order
            ), 
            alt.Y("inflation",
                scale=alt.Scale(zero=False)
            ),
            tooltip=["period", "inflation"]
        )
        .mark_bar() # Choose the plot type here
        .interactive() # To make the plot interactive 
    )
    return chart.to_json() 


if __name__ == "__main__": 
    app.run()
