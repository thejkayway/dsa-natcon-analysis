import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import charts
import utils.filters as filters

voters = pd.read_csv("resources/DSANatCon2021Votes_withCluster.csv")
cluster_voters_in_each_chapter = voters[['Delegate', 'City', 'Cluster']] \
                        .drop_duplicates() \
                        .groupby('City') \
                        .agg(Count=pd.NamedAgg(column="Cluster", aggfunc="value_counts")) \
                        .reset_index()
cities = voters['City'].unique()
cities.sort()

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)
server = app.server


#############################
##### BEGIN UI CREATION #####
#############################

### Main SPA Layout
app.layout = html.Div([
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Clusters", href="/clusters")),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("Chapters in Each Cluster", href="/plots/chaptersByCluster"),
                    dbc.DropdownMenuItem("Clusters in Each Chapter", href="/plots/clustersByChapter"),
                ],
                nav=True,
                in_navbar=True,
                label="Sunburst Plots",
            ),
        ],
        brand="DSA NatCon 2021 Analysis",
        brand_href="/home",
        color="primary",
        dark=True,),
    dbc.Container(id='page-content'),
    dcc.Location(id='url', refresh=False),
])

### Pages ###
home_page = html.Div([
    dcc.Graph(id='all-votes-heatmap'),
    dbc.Container([
        dbc.Row([
            dbc.Col(
                dbc.InputGroup([
                    dbc.InputGroupAddon("Filter Rows", addon_type="prepend"),
                    dbc.Input(value='', id='filter-all-voters-heatmap-rows-input', placeholder='Delegate name / chapter', debounce=False),
                ]),
                width={"size": 6},
            ),
            dbc.Col(
                dbc.InputGroup([
                    dbc.InputGroupAddon("Filter Columns", addon_type="prepend"),
                    dbc.Input(value='', id='filter-all-voters-heatmap-columns-input', placeholder='Motion Acronym', debounce=False),
                ]),
                width={"size": 6},
            ),
        ]),
    ],
        style={"padding": "1rem"}
    ),
    html.Div('Each row in the above heatmap is a single delegate and each column is the votes of all delegates for that voting item.'),
    html.Div('"Yes" votes are yellow, "No" votes are blue, and abstentions are left blank.'),
])

clusters_page = html.Div([
    dcc.Graph(id='clusters-heatmap', style={"height": "1400px"}),
    dbc.Container(
        [
            dbc.Row([
                dbc.Col(
                    dbc.InputGroup([
                        dbc.InputGroupAddon("Filter Rows", addon_type="prepend"),
                        dbc.Input(value='', id='filter-clusters-heatmap-rows-input', placeholder='Delegate name / chapter', debounce=False),
                    ]),
                    width={"size": 6},
                ),
                dbc.Col(
                    dbc.InputGroup([
                        dbc.InputGroupAddon("Filter Columns", addon_type="prepend"),
                        dbc.Input(value='', id='filter-clusters-heatmap-columns-input', placeholder='Motion Acronym', debounce=False),
                    ]),
                    width={"size": 6},
                ),
            ])
        ],
        style={"padding": "1rem"}
    ),
    html.Div('Each one of the six heatmaps above represents a group of DSA voters who voted similarly. Note that this weights every vote equally, from the "germane" motion to bylaws change. Adjusting for the relative importance of each vote is a work in progress.'),
    html.Div('"Yes" votes are yellow, "No" votes are blue, and abstentions are left blank.'),
    html.Br(),
    html.Div('After much manual inspection, I believe the clusters tend to contain the following groups (along with assorted unidentified others of course, as no caucus represents e.g. 300 members):'),
    dbc.Container(
        [
            dbc.Row([
                dbc.Col(
                    dbc.Table([
                        html.Thead(html.Tr([html.Th("Cluster"), html.Th("Groups Found In Cluster")])),
                        html.Tbody([
                            html.Tr([html.Td("First"), html.Td("SMC")]),
                            html.Tr([html.Td("Second"), html.Td("Alternates")]),
                            html.Tr([html.Td("Third"), html.Td("R&R")]),
                            html.Tr([html.Td("Fourth"), html.Td("\"Lazy\" voters")]),
                            html.Tr([html.Td("Fifth"), html.Td("B&R")]),
                            html.Tr([html.Td("Sixth"), html.Td("CPN, LSC, Red Star, Red Caucus")]),
                        ]),
                    ], bordered=True),
                    width={"size": 8, "offset": 2}
                )
            ]),
        ],
        style={"padding": "1rem"}
    ),

])

clusters_by_chapter_page = html.Div([
    dcc.Graph(id='clusters-by-chapter-sunburst', style={"height": "600px"}),
    dbc.Container([
        dbc.Row([
            dbc.Col(
                dcc.Dropdown(
                    id='filter-clusters-by-chapter-chapter-input',
                    options=[{'label': city, 'value': city} for city in cities],
                    placeholder="Select chapters",
                    multi=True
                ),
                width={"size": 6},
            ),
            dbc.Col(
                dcc.Dropdown(
                    id='filter-clusters-by-chapter-cluster-input',
                    options=[
                        {'label': 'First', 'value': 'First'},
                        {'label': 'Second', 'value': 'Second'},
                        {'label': 'Third', 'value': 'Third'},
                        {'label': 'Fourth', 'value': 'Fourth'},
                        {'label': 'Fifth', 'value': 'Fifth'},
                        {'label': 'Sixth', 'value': 'Sixth'},
                    ],
                    placeholder="Select clusters",
                    multi=True
                ),
                width={"size": 6},
            ),
        ]),
    ],
        style={"padding": "1rem"}
    ),
])

chapters_by_cluster_page = html.Div([
    dcc.Graph(id='chapters-by-cluster-sunburst', style={"height": "600px"}),
    dbc.Container([
        dbc.Row([
            dbc.Col(
                dcc.Dropdown(
                    id='filter-chapters-by-cluster-chapter-input',
                    options=[{'label': city, 'value': city} for city in cities],
                    placeholder="Select chapters",
                    multi=True
                ),
                width={"size": 6},
            ),
            dbc.Col(
                dcc.Dropdown(
                    id='filter-chapters-by-cluster-cluster-input',
                    options=[
                        {'label': 'First', 'value': 'First'},
                        {'label': 'Second', 'value': 'Second'},
                        {'label': 'Third', 'value': 'Third'},
                        {'label': 'Fourth', 'value': 'Fourth'},
                        {'label': 'Fifth', 'value': 'Fifth'},
                        {'label': 'Sixth', 'value': 'Sixth'},
                    ],
                    placeholder="Select clusters",
                    multi=True
                ),
                width={"size": 6},
            ),
        ]),
    ],
        style={"padding": "1rem"}
    ),
])

not_found_page = html.Div([
    html.H1('Page not found')
])



################################
##### UI INTERACTION LOGIC #####
################################

### Update the index so we display correct page
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/home' or pathname == '/':
        return home_page
    elif pathname == '/clusters':
        return clusters_page
    elif pathname == '/plots/chaptersByCluster':
        return chapters_by_cluster_page
    elif pathname == '/plots/clustersByChapter':
        return clusters_by_chapter_page
    else:
        return not_found_page

### Interactive "all voters" heatmap
@app.callback(
    Output('all-votes-heatmap', 'figure'),
    Input('filter-all-voters-heatmap-rows-input', 'value'),
    Input('filter-all-voters-heatmap-columns-input', 'value'))
def update_heatmap_all_voters(rows_filter, columns_filter):
    return charts.all_votes_heatmap(filters.filter_heatmap(voters, rows_filter, columns_filter))

### Interactive "clusters" heatmaps
@app.callback(
    Output('clusters-heatmap', 'figure'),
    Input('filter-clusters-heatmap-rows-input', 'value'),
    Input('filter-clusters-heatmap-columns-input', 'value'))
def update_heatmap_all_voters(rows_filter, columns_filter):
    return charts.clusters_heatmaps(filters.filter_heatmap(voters, rows_filter, columns_filter))

### Interactive "clusters by chaper" sunburst
@app.callback(
    Output('clusters-by-chapter-sunburst', 'figure'),
    Input('filter-clusters-by-chapter-chapter-input', 'value'),
    Input('filter-clusters-by-chapter-cluster-input', 'value'))
def update_clusters_by_chapter_sunburst(chapter_filter, cluster_filter):
    return charts.clusters_by_chapter(filters.filter_sunburst(cluster_voters_in_each_chapter, chapter_filter, cluster_filter))

### Interactive "chapters by cluster" sunburst
@app.callback(
    Output('chapters-by-cluster-sunburst', 'figure'),
    Input('filter-chapters-by-cluster-chapter-input', 'value'),
    Input('filter-chapters-by-cluster-cluster-input', 'value'))
def update_chapters_by_cluster_sunburst(chapter_filter, cluster_filter):
    return charts.chapters_by_cluster(filters.filter_sunburst(cluster_voters_in_each_chapter, chapter_filter, cluster_filter))


if __name__ == '__main__':
    app.run_server(debug=True)