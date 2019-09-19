from flask import Flask, render_template 
import pandas as pd

app = Flask(__name__)

@app.route("/")
# This fuction for rendering the table
def index():
    df = pd.read_csv("vids.csv", encoding='latin-1') #adding the data frame

    '''
    You can prepocess your data here, for example you want to do the group_by or anything else
    "table" for creating the table, here I only select a couple variable that I want to show. 
    The output must be to html. Classes are costumization with bootstrap, see bootstrap4 guides for table for more info. 
    '''
    table = df[["title","category_id","views","likes","dislikes"]].to_html(classes=["table table-light table-bordered table-striped table-hover .thead-dark"])

    # Example if you want to use sqlite instead of csv
    # import sqlite3
    # conn = sqlite3.connect("chinook.db")
    # albums = pd.read_sql_query("SELECT * FROM albums", conn)
    # table = albums.to_html(classes=["table table-bordered table-striped table-dark table-condensed"])
    
    return render_template("index.html", table=table)


@app.route("/charts")
# this fuction for rendering the plot
def charts():
    import altair as alt #using altair library

    df = pd.read_csv("vids.csv", encoding='latin-1') #adding the same dataframe we use

    chart = (
        alt.Chart(df)
        .encode( # put the x and y
            x="likes", 
            y="dislikes",
            color=alt.Color("category_id", scale=alt.Scale(scheme='set2')), #color based on the category, you als can chose the color scheme
            tooltip=["likes", "dislikes"] 
        )
        .mark_circle(size=60).interactive() # choose the plot type here
    )
    return chart.to_json() 


if __name__ == "__main__": 
    app.run()
