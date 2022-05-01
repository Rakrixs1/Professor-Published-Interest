from mongodb import mongodbconnect
from my_sql import mysqlconnect #establishing connection to mySQL academic world tables and database
from neo4j1 import neo4jconnect
from dash import html, dcc, Input, Output
from jupyter_dash import JupyterDash
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
from pandas.io.json import json_normalize 
from dash import dash_table as dt

#CONNECTING TO NEO4J
neoconn = neo4jconnect("academicworld")

#CONNECTION TO MONGO DB
mongodb1 = mongodbconnect()


#For this section I tried to minimizing the dataframe to create a seperate dataframe for top key word publications map.
#Memory would run out after running the code on my local machine. 
#In order to minimize memory allocation a csv file was created using the following functions.
#-----------------------------------------------------------------------------------------------------------------------------------------
#USED ADDITIONAL DATABASE TO COMBINE STATES WITH UNIVERSITIES
#df = pd.read_csv(r'C:\Users\rakix\Downloads\CS411\CS411\prof_score.csv') #using additional state data to seperate the universities by state
#using mysql academic world database to create data for tree map (chart2)

#VIEW DB TECHNIQUE
#publication_sql = mysqlconnect('select distinct f.id, k.name, pk.score* fk.score as pf, pk.publication_id from faculty f join university u on f.university_id = u.id join faculty_keyword fk on f.id = fk.faculty_id join publication_keyword pk on fk.keyword_id = pk.keyword_id join keyword k on fk.keyword_id = k.id join publication p on pk.publication_id = p.id')
#newdf.to_csv(r'pf.csv')


#using additional state data to seperate the universities by state
req_cols = ['faculty_id', 'name', 'university_id', 'university_name', 'City', 'StateCode', 'score', 'keyword_name']
newdf = pd.read_csv(r'C:\Users\rakix\Downloads\CS411\CS411\prof_score.csv', usecols=req_cols)
req_cols1 = ['faculty_id', 'name', 'university_id', 'university_name', 'City', 'StateCode']
newdf1 = pd.read_csv(r'C:\Users\rakix\Downloads\CS411\CS411\prof_score.csv', usecols=req_cols1)
publication_sql = pd.read_csv(r'C:\Users\rakix\Downloads\CS411\CS411\pf.csv')
publication_sql.rename(columns = {'id': 'faculty_id'}, inplace = True)
publication_sql.rename(columns = {'name': 'keyword_name'}, inplace = True)
publidf = pd.merge(newdf1, publication_sql, on=['faculty_id'])

chart2 = px.treemap(newdf, path=['university_name', 'keyword_name'], values = 'score', width=1980, height=700, title = "Keyword Scores")
chart2.update(layout=dict(title=dict(x=0.5)))
chart2.update_traces(textinfo = 'label + value')

#US Map Diplaying top published keywords??
filtered_data = publidf.iloc[publidf.reset_index().groupby(['StateCode'])['pf'].idxmax()] #Indexing DB Technique used 

fig = go.Figure(data=go.Choropleth(
    locations= filtered_data['StateCode'].unique(),
    z = filtered_data['pf'].astype(float),
    locationmode='USA-states',
    colorscale="Reds",
    text = filtered_data['StateCode'] + '<br>' + \
    'University Name: ' + filtered_data['university_name'] + '<br>' + \
    'Keyword: ' + filtered_data['keyword_name'] + '<br>' + \
    'Professor Name: ' + filtered_data['name'] + '<br>' + \
    'Published Title: ' + filtered_data['title'],
    marker_line_color='white', # line markers between states
    colorbar_title="Publication Scores"
    ))

fig.update_layout(
    title_text='Top Published Keyword Scores in the US',
    geo = dict(
        scope='usa',
        projection=go.layout.geo.Projection(type = 'albers usa'),
        showlakes=True, # lakes
        lakecolor='rgb(255, 255, 255)'),
    width=1980, height=700
    )

#using neo4j data to create keyword pi chart - VIEW DB TECHNIQUE
query = '''MATCH p=(p1:PUBLICATION)-[l:LABEL_BY]->(k1:KEYWORD), 
    (f1:FACULTY)-[:PUBLISH]->(p1:PUBLICATION),
    (f1:FACULTY)-[:INTERESTED_IN]->(k1:KEYWORD),
    (f1:FACULTY)-[:AFFILIATION_WITH]->(i1:INSTITUTE)
    WITH f1.name as faculty, sum(l.score * p1.numCitations) as accumalated_citations, k1.name as keyword, i1.name as institute 
    RETURN faculty,keyword, accumalated_citations, institute '''

keyword_count = list(neoconn.run(query))

keyword_search = pd.DataFrame([dict(_) for _ in keyword_count])
#lm = keyword_search.reset_index().groupby(['faculty'])['accumalated_citations'].idxmax()
    
fig1 = px.bar(keyword_search, x='faculty', y='accumalated_citations',
             hover_data=['keyword', 'accumalated_citations', 'institute'], color='accumalated_citations',
             labels={'accumalated_citations':'total citations'}, height=400)

fig4= px.bar(keyword_search, 
             x = keyword_search.groupby('faculty')['accumalated_citations'].agg(sum), 
             y = keyword_search['faculty'].unique(), 
             labels={
                     "x": "Accumalated Citations",
                     "y": "Faculty"
                 },
              color = keyword_search.groupby('faculty')['accumalated_citations'].agg(sum),
              color_continuous_scale=px.colors.sequential.Reds,
              #color_discrete_sequence=['rgb(253,180,98)','rgb(190,186,218)'],
              text = keyword_search.groupby('faculty')['accumalated_citations'].agg(sum),
             title = 'Recorded Accumalated Citations per Faculty',
              #,barmode = 'group'
              orientation = 'h'
             )
fig4.update_layout( title = dict(x=0.5))
fig4.update_traces(texttemplate = '%{text:.2s}')

#using mongo db faculty database
collection = mongodb1["faculty"]
details = collection.find()
faculty_mongo = pd.DataFrame(details)
#data cleaning to bring affiliation dictionary values out   
df = json_normalize(faculty_mongo['affiliation']).filter(like='name')
df.columns = df.columns.str.replace('.name','.id')
faculty_mongo['university_name'] = df['name']
faculty_mongo1 = faculty_mongo.drop(columns = ['_id', 'affiliation', 'keywords', 'publications', 'researchInterest', 'id'])

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = JupyterDash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div(
    children=[ 
        html.Div( 
            children=[
                html.H1(
                    children="Professors Published Interests",style={'textAlign': 'center'}, className="header-title"
                ), #Header title
                html.H2(
                    children="Analyze professors"
                    " published interests in "
                    " each state "
                    " ",
                    className="header-description", style={'textAlign': 'center'},
                ),
            ],
            className="header", style={'backgroundColor':'#D7D1D1'},
        ), #Description below the header
        
        html.Div(
            children=[
                html.Div(
                children = dcc.Graph(
                    #id = 'map1',
                    figure = fig,
                  #  config={"displayModeBar": False},
                ), style={'width': '100%', 'height': '100%', 'float': 'center', 'display': 'inline-block'}),
            ],
        ),

        html.Div(
            children=[
                html.Div(children = 'State', style={'fontSize': "24px"},className = 'state-title'),
                dcc.Dropdown(
                    id = 'state-filter',
                    options = [
                        {'label': State, 'value':State}
                        for State in newdf.StateCode.unique()
                    ], #'StateCode' is the filter
                    value = None,
                    clearable = False,
                    searchable = True,
                    placeholder = "Select State...",
                    className = 'dropdown', style={'fontSize': "24px",'textAlign': 'center'},
                ),
            ],
            className = 'state',
        ), #the dropdown function
        
        html.Div(
            children=[
                html.Div(
                children = dcc.Graph(
                    id = 'graph2',
                    figure = chart2,
                  #  config={"displayModeBar": False},
                ), style={'width': '100%', 'float': 'center', 'display': 'inline-block'}
            ),
            
         html.Div(
            children=[
                html.Div(children = 'Faculty', style={'fontSize': "24px"},className = 'faculty-title'),
                dcc.Dropdown(
                    id = 'faculty-filter',
                    options = [
                        {'label': Faculty, 'value':Faculty}
                        for Faculty in faculty_mongo.name.unique()
                    ], #'university_name' is the filter
                    value = None,
                    clearable = False,
                    searchable = True,
                    placeholder = "Select Faculty... ",
                    className = 'dropdown', style={'fontSize': "24px",'textAlign': 'center'},
                ),
            ],style = {'width': '49%', 'float': 'right'},
            className = 'uni', 
        ),
        html.Div(
            children=[
                html.Div(children = 'Keyword', style={'fontSize': "24px"},className = 'keyword-title'),
                dcc.Dropdown(
                    id = 'keyword-filter',
                    options = [
                        {'label': Keyword, 'value':Keyword}
                        for Keyword in keyword_search.keyword.unique()
                    ], #'keyword_name' is the filter
                    value = None,
                    clearable = False,
                    searchable = True,
                    placeholder = "Select Keyword... ",
                    className = 'dropdown', style={'fontSize': "24px",'textAlign': 'center'},
                ),
            ],style = {'width': '49%', 'float': 'left'},
            className = 'keyword'
        ),
                html.Div(
                children = dcc.Graph(
                    id = 'pi',
                    figure = fig1,
                    #config={"displayModeBar": False},
                ),
                style={'width': '50%', 'float': 'left'},
            ),
                html.Div(
                children = dcc.Graph(
                    id = 'pi2',
                    figure = fig4,
                    #config={"displayModeBar": False},
                ),
                style={'width': '50%', 'float': 'right'},
            ),
        ],
            className = 'double-graph'), 
        html.Div(
            children=[
                dt.DataTable(id='faculty_table', 
                    columns = [{'name': 'name', 'id': 'name'},
                    {'name': 'position', 'id': 'position'},
                    {'name': 'email', 'id': 'email'},
                    {'name': 'phone', 'id': 'phone'},
                    {'name': 'university_name', 'id': 'university_name'},
                    {'name': 'photoUrl', 'id': 'photoUrl'}],
                    data = faculty_mongo1.to_dict("rows"),
                    editable=True,
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    column_selectable="single",
                    row_selectable="multi",
                    row_deletable=True,
                    selected_columns=[],
                    selected_rows=[],
                    page_action="native",
                    page_current= 0,
                    page_size= 10), #Charles Sodini
                ], style = {'float': 'right' ,'backgroundColor':'#D7D1D1'},
            className = 'table',
        ) 
    ]
) #Four graphs

@app.callback(
    Output("map1", "figure"),
    [Input("state-filter", "value")],
)
def update_map(StateCode):

    filtered_data1 = publidf.iloc[publidf.reset_index().groupby(['StateCode'])['pf'].idxmax()]
    
    filtered_data = filtered_data1[filtered_data1["StateCode"] == StateCode]
    
    fig = go.Figure(data=go.Choropleth(
    locations= filtered_data['StateCode'].unique(),
    z = filtered_data['pf'].head(1),
    locationmode='USA-states',
    colorscale="Viridis",
    text = filtered_data['StateCode'] + '<br>' + \
    'University Name: ' + filtered_data['university_name'] + '<br>' + \
    'Keyword: ' + filtered_data['keyword_name'],
    marker_line_color='white', # line markers between states
    colorbar_title="Keyword Scores",
    ))

    fig.update_layout(
    title_text='Top Published Keyword Scores in the US',
    geo = dict(
        scope='usa',
        projection=go.layout.geo.Projection(type = 'albers usa'),
        showlakes=True, # lakes
        lakecolor='rgb(255, 255, 255)'),
    )
    return fig

@app.callback(
    Output("graph2", "figure"),
    [Input("state-filter", "value")],
)
def update_charts(StateCode):
    
    #filtered_data = newdf[newdf["score"]].abs
    filtered_data = newdf[newdf["StateCode"] == StateCode]
    chart2 = px.treemap(filtered_data, path=['university_name', 'keyword_name'], values = 'score', title = "Keyword Scores", width=1920, height=700)
    chart2.update(layout=dict(title=dict(x=0.5)))
    chart2.update_traces(textinfo = 'label + value')

    return chart2


@app.callback(
    Output("pi", "figure"),
    [Input("keyword-filter", "value")],
)

def update_charts(Keyword1):

    filtered_data = keyword_search[keyword_search["keyword"] == Keyword1]
    
    fig = px.bar(filtered_data, x='faculty', y='accumalated_citations',
             hover_data=['keyword', 'accumalated_citations', 'institute'], color='accumalated_citations',
             color_continuous_scale='Reds',
             labels={'accumalated_citations':'total citations'}, height=400)
    return fig

@app.callback(
    Output("pi2", "figure"),
    [Input("faculty-filter", "value")],
)

def update_charts(faculty1):

    filtered_data = keyword_search[keyword_search["faculty"] == faculty1]
    
    fig4= px.bar(filtered_data, 
             x = filtered_data.groupby('faculty')['accumalated_citations'].agg(sum), 
             y = filtered_data['faculty'].unique(), 
             labels={
                     "x": "Accumalated Citations",
                     "y": "Faculty"
                 },
              color = filtered_data.groupby('faculty')['accumalated_citations'].agg(sum),
              color_continuous_scale=px.colors.sequential.Reds,
              #color_discrete_sequence=['rgb(253,180,98)','rgb(190,186,218)'],
              text = filtered_data.groupby('faculty')['accumalated_citations'].agg(sum),
             title = 'Sum of Accumalated Citations per Faculty',
              #,barmode = 'group'
              orientation = 'h'
             )
    fig4.update_layout( title = dict(x=0.5))
    fig4.update_traces(texttemplate = '%{text:.2s}')
    return fig4

if __name__ == '__main__':
    app.run_server(mode='jupyterlab',port = 8090, dev_tools_ui=True,# debug=True,
                dev_tools_hot_reload =True, threaded=True)