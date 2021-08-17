import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def toInt(voteChoice):
  if voteChoice == "Yes":
    return 1
  if voteChoice == "No":
    return 0
  return np.nan

def all_votes_heatmap(voters):
     heatmap_all_votes = go.Figure(data=go.Heatmap(
               z=voters["Vote Choice"].apply(toInt),
               x=voters["Motion #"],
               y=voters["Delegate"]))
     heatmap_all_votes.update_layout(title_text='Votes - All Delegates, All Motions')
     return heatmap_all_votes

def clusters_heatmaps(voters):
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
     cluster_heatmaps.update_layout(title_text="The Six Types of DSA NatCon 2021 Voter")
     return cluster_heatmaps

def clusters_by_chapter(grouped_voters):
    return px.sunburst(grouped_voters,
          path=['City', 'Cluster'],
          values='Count',
          color='Cluster',
          title='Clusters in Each Chapter')

def chapters_by_cluster(grouped_voters):
     return px.sunburst(grouped_voters,
          path=['Cluster', 'City'],
          values='Count',
          color='Cluster',
          title='Chapters in Each Cluster')