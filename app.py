import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

def toInt(voteChoice):
  if voteChoice == "Yes":
    return 1
  if voteChoice == "No":
    return 0
  return np.nan

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

server = app.server

voters = pd.read_csv("resources/DSANatCon2021Votes_withCluster.csv")

# Main Heatmap
all_votes = go.Figure(data=go.Heatmap(
                   z=voters["Vote Choice"].apply(toInt),
                   x=voters["Motion #"],
                   y=voters["Delegate"]))
all_votes.update_layout(title_text='Votes - All Delegates, All Motions')


# Dataframe for each cluster because I'm lazy
first_cluster = voters[voters['Cluster'] == 'First']
second_cluster = voters[voters['Cluster'] == 'Second']
third_cluster = voters[voters['Cluster'] == 'Third']
fourth_cluster = voters[voters['Cluster'] == 'Fourth']
fifth_cluster = voters[voters['Cluster'] == 'Fifth']
sixth_cluster = voters[voters['Cluster'] == 'Sixth']

cluster_heatmaps = make_subplots(rows=6, cols=1, subplot_titles=(
    'Cluster 1: %s delegates' % first_cluster['Delegate'].nunique(),
    'Cluster 2: %s delegates' % second_cluster['Delegate'].nunique(),
    'Cluster 3: %s delegates' % third_cluster['Delegate'].nunique(),
    'Cluster 4: %s delegates' % fourth_cluster['Delegate'].nunique(),
    'Cluster 5: %s delegates' % fifth_cluster['Delegate'].nunique(),
    'Cluster 6: %s delegates' % sixth_cluster['Delegate'].nunique(),
))
cluster_heatmaps.add_trace(go.Heatmap(
                   z=first_cluster["Vote Choice"].apply(toInt),
                   x=first_cluster["Motion #"],
                   y=first_cluster["Delegate"],
                   ),
              row=1, col=1)
cluster_heatmaps.add_trace(go.Heatmap(
                   z=second_cluster["Vote Choice"].apply(toInt),
                   x=second_cluster["Motion #"],
                   y=second_cluster["Delegate"],
                   ),
              row=2, col=1)
cluster_heatmaps.add_trace(go.Heatmap(
                   z=third_cluster["Vote Choice"].apply(toInt),
                   x=third_cluster["Motion #"],
                   y=third_cluster["Delegate"],
                   ),
              row=3, col=1)
cluster_heatmaps.add_trace(go.Heatmap(
                   z=fourth_cluster["Vote Choice"].apply(toInt),
                   x=fourth_cluster["Motion #"],
                   y=fourth_cluster["Delegate"],
                   ),
              row=4, col=1)
cluster_heatmaps.add_trace(go.Heatmap(
                   z=fifth_cluster["Vote Choice"].apply(toInt),
                   x=fifth_cluster["Motion #"],
                   y=fifth_cluster["Delegate"],
                   ),
              row=5, col=1)
cluster_heatmaps.add_trace(go.Heatmap(
                   z=sixth_cluster["Vote Choice"].apply(toInt),
                   x=sixth_cluster["Motion #"],
                   y=sixth_cluster["Delegate"],
                   ),
              row=6, col=1)

cluster_heatmaps.update_xaxes(categoryorder='category ascending')
cluster_heatmaps.update_layout(height=1600, width=1200, title_text="The Six Types of DSA NatCon 2021 Voter")


# Sunburst Plots
clusters_by_city = voters[['City', 'Cluster']].groupby('City').agg(Count=pd.NamedAgg(column="Cluster", aggfunc="value_counts")).reset_index()
clusters_by_city_sunburst = px.sunburst(clusters_by_city,
                  path=['City', 'Cluster'],
                  values='Count',
                  color='Cluster',
                  title='Clusters by City')
cities_by_cluster_sunburst = px.sunburst(clusters_by_city,
                  path=['Cluster', 'City'],
                  values='Count',
                  color='Cluster',
                  title='Cities by Cluster')



######## HTML Layout ########
app.layout = html.Div([
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Clusters", href="/clusters")),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("Cities by Cluster", href="/plots/citiesByCluster"),
                    dbc.DropdownMenuItem("Clusters by City", href="/plots/clustersByCity"),
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
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Pages 
home_page = html.Div([
    dcc.Graph(figure=all_votes),
    html.Div('Each row in the above heatmap is a single delegate and each column is the votes of all delegates for that voting item.'),
    html.Div('"Yes" votes are yellow, "No" votes are blue, and abstentions are left blank.'),
])

clusters_page = html.Div([
    dcc.Graph(figure=cluster_heatmaps),
])

clusters_by_city_page = html.Div([
    dcc.Graph(figure=clusters_by_city_sunburst),
])

cities_by_cluster_page = html.Div([
    dcc.Graph(figure=cities_by_cluster_sunburst),
])

not_found_page = html.Div([
    html.H1('Page not found')
])

# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/home' or pathname == '/':
        return home_page
    elif pathname == '/clusters':
        return clusters_page
    elif pathname == '/plots/citiesByCluster':
        return cities_by_cluster_page
    elif pathname == '/plots/clustersByCity':
        return clusters_by_city_page
    else:
        return not_found_page

if __name__ == '__main__':
    app.run_server(debug=True)