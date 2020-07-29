#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

import dash
import dash_table

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

## Download and wrangle the ANES data
anes = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/anes_pilot2019_clean.csv")

anes_state = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/anes_pilot_2019.csv")
anes_state = anes_state[['caseid', 'inputstate']]
anes_state['state'] = anes_state['inputstate'].map({1:'Alabama',2:'Alaska',60:'American Samoa',
                                                    3:'American Samoa',4:'Arizona',5:'Arkansas',
                                                    81:'Baker Island',6:'California',7:'Canal Zone',
                                                    8:'Colorado',9:'Connecticut',10:'Delaware',
                                                    11:'District of Columbia',12:'Florida',
                                                    64:'Federated States of Micronesia',13:'Georgia',
                                                    14:'Guam',66:'Guam',15:'Hawaii',84:'Howland Island',
                                                    16:'Idaho',17:'Illinois',18:'Indiana',19:'Iowa',
                                                    86:'Jarvis Island',67:'Johnston Atoll',20:'Kansas',
                                                    21:'Kentucky',89:'Kingman Reef',22:'Louisiana',
                                                    23:'Maine',68:'Marshall Islands',24:'Maryland',
                                                    25:'Massachusetts',26:'Michigan',71:'Midway Islands',
                                                    27:'Minnesota',28:'Mississippi',29:'Missouri',
                                                    30:'Montana',76:'Navassa Island',31:'Nebraska',
                                                    32:'Nevada',33:'New Hampshire',34:'New Jersey',
                                                    35:'New Mexico',36:'New York',37:'North Carolina',
                                                    38:'North Dakota',69:'Northern Mariana Islands',
                                                    39:'Ohio',40:'Oklahoma',41:'Oregon',70:'Palau',
                                                    95:'Palmyra Atoll',42:'Pennsylvania',43:'Puerto Rico',
                                                    72:'Puerto Rico',44:'Rhode Island',45:'South Carolina',
                                                    46:'South Dakota',47:'Tennessee',48:'Texas',
                                                    74:'U.S. Minor Outlying Islands',49:'Utah',
                                                    50:'Vermont',51:'Virginia',
                                                    52:'Virgin Islands of the U.S.',
                                                    78:'Virgin Islands of the U.S.',79:'Wake Island',
                                                    53:'Washington',54:'West Virginia',55:'Wisconsin',
                                                    56:'Wyoming'})
anes_state['state_abb'] = anes_state['inputstate'].map({1:'AL',2:'AK',60:'AS',3:'AS',4:'AZ',5:'AR',
                                                    81:'UM',6:'CA',7:'CZ',8:'CO',9:'CT',10:'DE',
                                                    11:'DC',12:'FL',64:'FM',13:'GA',
                                                    14:'GU',66:'GU',15:'HI',84:'UM',
                                                    16:'ID',17:'IL',18:'IN',19:'IA',
                                                    86:'UM',67:'UM',20:'KS', 21:'KY',89:'UM',22:'LA',
                                                    23:'ME',68:'UM',24:'MD',25:'MA',26:'MI',71:'UM',
                                                    27:'MN',28:'MS',29:'MO',30:'MT',76:'UM',31:'NE',
                                                    32:'NV',33:'NH',34:'NJ',35:'NM',36:'NY',37:'NC',
                                                    38:'ND',69:'MP',39:'OH',40:'OK',41:'OR',70:'PW',
                                                    95:'Palmyra Atoll',42:'PA',43:'PR',72:'PR',44:'RI',45:'SC',
                                                    46:'SD',47:'TN',48:'TX',74:'UM',49:'UT',
                                                    50:'VT',51:'VA',52:'VI',78:'VI',79:'UM',
                                                    53:'WA',54:'WV',55:'WI',56:'WY'})
anes_state = anes_state.rename({'inputstate':'stateID'}, axis=1)
anes = pd.merge(anes, anes_state, on='caseid', validate='one_to_one')

## Generate the individual tables and figures

### Markdown text
markdown_text = '''
The [American National Election Study](https://electionstudies.org) (ANES) is a massive public opinion survey conducted after every national election. It is one of the greatest sources of data available about the voting population of the United States. It contains far more information than a typical public opinion poll. Iterations of the survey contain thousands of features from thousands of respondents, and examines people's attitudes on the election, the candidates, the parties, it collects massive amounts of demographic information and other characteristics from voters, and it records people's opinions on a myriad of political and social issues.

Prior to each election the ANES conducts a "pilot study" that asks many of the questions that will be asked on the post-election survey. The idea is to capture a snapshot of the American electorate prior to the election and to get a sense of how the survey instrument is working so that adjustments can be made in time. Here we will work with the [2019 ANES pilot data](https://electionstudies.org/data-center/2019-pilot-study/). To understand the features and the values used to code responses, the data have an associated [questionnaire](https://electionstudies.org/wp-content/uploads/2020/02/anes_pilot_2019_questionnaire.pdf) and [codebook](https://electionstudies.org/wp-content/uploads/2020/02/anes_pilot_2019_userguidecodebook.pdf). The pilot data were collected in December 2019 and contain 900 features collected from 3,165 respondents. 
'''

### Table
anes_display = anes.groupby('vote').agg({'vote':'size',
                                        'age':'mean'})
anes_display['percent'] = 100*anes_display.vote / sum(anes_display.vote)

anes_display = pd.merge(anes_display, 100*pd.crosstab(anes.vote, anes.liveurban, normalize='index'), 
         left_index=True, right_index=True)
anes_display = anes_display[['vote', 'percent', 'age', 
                            'City', 'Rural', 'Suburb', 'Town']]
anes_display = anes_display.rename({'vote':'Votes',
                                   'age':'Avg. age',
                                   'percent':'Percent',
                                   'City':'% City',
                                   'Rural':'% Rural',
                                   'Suburb':'% Suburban',
                                   'Town':'% Town'}, axis=1)
anes_display = round(anes_display, 2)
anes_display = anes_display.reset_index().rename({'vote':'Candidate'}, axis=1)
anes_display

table = ff.create_table(anes_display)
table.show()

### Barplot
colpercent = round(100*pd.crosstab(anes.vote, anes.partyID, normalize='columns'),2).reset_index()
colpercent = pd.melt(colpercent, id_vars = 'vote', value_vars = ['Democrat', 'Republican', 'Independent'])
colpercent = colpercent.rename({'value':'colpercent'}, axis=1)

rowpercent = round(100*pd.crosstab(anes.vote, anes.partyID, normalize='index'),2).reset_index()
rowpercent = pd.melt(rowpercent, id_vars = 'vote', value_vars = ['Democrat', 'Republican', 'Independent'])
rowpercent = rowpercent.rename({'value':'rowpercent'}, axis=1)

votes = pd.crosstab(anes.vote, anes.partyID).reset_index()
votes = pd.melt(votes, id_vars = 'vote', value_vars = ['Democrat', 'Republican', 'Independent'])
votes = votes.rename({'value':'votes'}, axis=1)

ftb = pd.crosstab(anes.vote, anes.partyID, values=anes.ftbiden, aggfunc='mean').round(2).reset_index()
ftb = pd.melt(ftb, id_vars = 'vote', value_vars = ['Democrat', 'Republican', 'Independent'])
ftb = ftb.rename({'value':'Biden thermometer'}, axis=1)

ftt = pd.crosstab(anes.vote, anes.partyID, values=anes.fttrump, aggfunc='mean').round(2).reset_index()
ftt = pd.melt(ftt, id_vars = 'vote', value_vars = ['Democrat', 'Republican', 'Independent'])
ftt = ftt.rename({'value':'Trump thermometer'}, axis=1)

anes_groupbar = pd.merge(colpercent, rowpercent, on=['vote', 'partyID'], validate='one_to_one')
anes_groupbar = pd.merge(anes_groupbar, votes, on=['vote', 'partyID'], validate='one_to_one')
anes_groupbar = pd.merge(anes_groupbar, ftb, on=['vote', 'partyID'], validate='one_to_one')
anes_groupbar = pd.merge(anes_groupbar, ftt, on=['vote', 'partyID'], validate='one_to_one')

anes_groupbar['coltext'] = anes_groupbar['colpercent'].astype(str) + '%'
anes_groupbar['rowtext'] = anes_groupbar['rowpercent'].astype(str) + '%'

fig_bar = px.bar(anes_groupbar, x='partyID', y='rowpercent', color='partyID', 
             facet_col='vote', facet_col_wrap=2,
             hover_data = ['votes', 'Biden thermometer', 'Trump thermometer'],
            labels={'partyID':'Party Identification', 'rowpercent':'Percent'},
            text='rowtext', width=1000, height=600)
fig_bar.update(layout=dict(title=dict(x=0.5)))
fig_bar.update_layout(showlegend=False)
fig_bar.for_each_annotation(lambda a: a.update(text=a.text.replace("vote=", "")))

### Line plot
def q25(x):
    return x.quantile(.25)
def q75(x):
    return x.quantile(.75)
def iqr(x):
    return x.quantile(.75) - x.quantile(.25)

anes_line = anes.query("age <= 85").groupby('age').agg({'ftbiden':['mean','median',q25, q75, iqr]})
anes_line.columns = anes_line.columns.droplevel()
anes_line = anes_line.reset_index()
anes_line['candidate'] = 'Joe Biden'

anes_line2 = anes.query("age <= 85").groupby('age').agg({'fttrump':['mean','median',q25, q75, iqr]})
anes_line2.columns = anes_line2.columns.droplevel()
anes_line2 = anes_line2.reset_index()
anes_line2['candidate'] = 'Donald Trump'

anes_line = anes_line.append(anes_line2)

fig_line = px.line(anes_line, x='age', y='mean', color='candidate', 
              line_dash = 'candidate',
              labels={'age':'Age', 
                      'mean':'Average thermometer rating'},
              hover_data=['median', 'q25', 'q75', 'iqr'],
              height=400, width=600)
fig_line.update_layout(yaxis=dict(range=[0,100]))
fig_line.update(layout=dict(title=dict(x=0.5)))

### Violin plot
anes_cand = pd.melt(anes, id_vars = ['caseid'], 
                    value_vars = ['ftbiden', 'fttrump',
                                 'ftobama', 'ftsanders'])
anes_cand = anes_cand.rename({'variable':'candidate',
                             'value':'thermometer'}, axis=1)
anes_cand['candidate'] = anes_cand['candidate'].map({'ftbiden':'Joe Biden',
                                                     'fttrump':'Donald Trump',
                                                     'ftobama':'Barack Obama',
                                                     'ftsanders':'Bernie Sanders'})

fig_vio = px.violin(anes_cand, y='thermometer', x = 'candidate', color = 'candidate',
                   labels={'thermometer':'Feeling thermometer rating', 'candidate':''},
                   title = 'Distribution of Thermometer Ratings')
fig_vio.update(layout=dict(title=dict(x=0.5)))

### Map
anes_state = pd.crosstab(anes.state_abb, anes.vote)
anes_state = anes_state[['Donald Trump', 'Joe Biden']].reset_index()
anes_state['difference'] = anes_state['Donald Trump'] - anes_state['Joe Biden']
anes_state['result'] = pd.cut(anes_state.difference, [-100, -.00001, 0, 100], labels=['biden','tie','trump'])
anes_state = pd.merge(anes_state, anes.groupby(['state', 'state_abb']).size().reset_index(), on='state_abb')
anes_state = anes_state.rename({0:'voters'}, axis=1)

fig_map = px.choropleth(anes_state, locations='state_abb', 
                    hover_name='state', hover_data = ['Donald Trump', 'Joe Biden', 'difference', 'voters'],
                    locationmode='USA-states', color='result', scope="usa",
                   color_discrete_map = {'biden':'blue', 
                                         'tie':'purple', 
                                         'trump':'red'})

### Scatterplot data
ft_columns = [col for col in anes if col.startswith('ft')] 
cat_columns = ['sex', 'partyID', 'vote', 'ideology'] 
anes_ft = anes[ft_columns + cat_columns].dropna()

### Create app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div(
    [
        html.H1("Exploring the 2019 American National Election Pilot Study"),
        
        dcc.Markdown(children = markdown_text),
        
        html.H2("Comparing Trump and Biden Voters"),
        
        dcc.Graph(figure=table),
        
        html.H2("Vote Choice By Party"),
        
        dcc.Graph(figure=fig_bar),
        
        html.H2("Distribution of Support for Political Figures"),
        
        dcc.Graph(figure=fig_vio),
        
        html.Div([
            
            html.H2("Vote Choice By State"),
            
            dcc.Graph(figure=fig_map)
            
        ], style = {'width':'48%', 'float':'left'}),
        
        html.Div([
            
            html.H2("Support by Age Group"),
            
            dcc.Graph(figure=fig_line)
            
        ], style = {'width':'48%', 'float':'right'}),
        
        html.H2("Feeling Thermometer Scatterplot"),
        
        html.Div([
            html.H3("x-axis feature"),
            dcc.Dropdown(id='x-axis',
                         options=[{'label': i, 'value': i} for i in ft_columns],
                     value='ftbiden'),
            html.H3("y-axis feature"),
            dcc.Dropdown(id='y-axis',
                         options=[{'label': i, 'value': i} for i in ft_columns],
                         value='fttrump'),
            html.H3("colors"),
            dcc.Dropdown(id='color',
                         options=[{'label': i, 'value': i} for i in cat_columns],
                         value=None)], style={"width": "25%", "float": "left"}),
        
        html.Div([dcc.Graph(id="graph", style={"width": "70%", "display": "inline-block"})])
    
    ]
)
@app.callback(Output(component_id="graph",component_property="figure"), 
                  [Input(component_id='x-axis',component_property="value"),
                   Input(component_id='y-axis',component_property="value"),
                   Input(component_id='color',component_property="value")])

def make_figure(x, y, color):
    return px.scatter(
        anes_ft,
        x=x,
        y=y,
        color=color,
        trendline='ols',
        hover_data=['sex', 'partyID', 'vote', 'ideology'],
        height=700,
        opacity = .25
)

app.run_server(debug=True)

