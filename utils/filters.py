"""Removes delegates (rows) and votes (columns) not containing filter queries from main voter dataframe"""
def filter_heatmap(voters, rows_filter, columns_filter):
    filtered = voters
    if rows_filter:
        filtered = filtered[(filtered['Delegate'].str.contains(rows_filter, case=False)) | (filtered['City'].str.contains(rows_filter, case=False))]
    if columns_filter:
        filtered = filtered[filtered['Motion #'].str.contains(columns_filter, case=False)]
    return filtered

"""Removes chapters/cities and clusters from the voter dataframe grouped by city"""
def filter_sunburst(grouped_voters, chapter_filter, cluster_filter):
    print(chapter_filter)
    filtered = grouped_voters
    if chapter_filter:
        filtered = filtered[filtered['City'].str.contains('|'.join(chapter_filter), case=False)]
    if cluster_filter:
        filtered = filtered[filtered['Cluster'].str.contains('|'.join(cluster_filter), case=False)]
    return filtered