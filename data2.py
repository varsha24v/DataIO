import pandas as pd
import folium
from folium.plugins import MarkerCluster

#Get all data

data = pd.concat(map(pd.read_csv, ['Data-IO 2024 Dataset/September.csv', 'Data-IO 2024 Dataset/October.csv','Data-IO 2024 Dataset/November.csv']))
data['route'] = data['start_station_name'] + ' to ' + data['end_station_name']
all_routes = data['route']
all_routes.drop_duplicates()
route_counts = {}
i = 0

for route in all_routes:
    route_counts[route] = data[data['route'] == route].shape[0]

route_counts_df = pd.DataFrame(list(route_counts.items()), columns=['route', 'count'])
rt_ct = pd.concat([all_routes.reset_index(drop=True), route_counts_df], axis=1)

m = folium.Map(location=[41.88, -87.63], tiles="cartodbdark_matter")
marker_cluster = MarkerCluster().add_to(m)

start_counts = data['start_station_name'].value_counts()
end_counts = data['end_station_name'].value_counts()

# Function to determine the color based on the count
def get_color(count):
    if count > 2000:  # You can adjust this threshold based on your data
        return 'red'
    elif count > 1000:
        return 'orange'
    else:
        return 'yellow'

for index, row in data.iterrows():
    start_station = row['start_station_name']
    start_count = start_counts.get(start_station, 0)  # Get the count, default to 0 if not found
    color = get_color(start_count)
    folium.Marker(
        location=[row['start_lat'], row['start_lng']],
        icon=folium.Icon(color=color),
        popup=f"Start Station: {start_station}<br>Count: {start_count}"
    ).add_to(marker_cluster)


for index, row in data.iterrows():
    end_station = row['end_station_name']
    end_count = end_counts.get(end_station, 0)  # Get the count, default to 0 if not found
    color = get_color(end_count)
    folium.Marker(
        location=[row['end_lat'], row['end_lng']],
        icon=folium.Icon(color=color),
        popup=f"End Station: {end_station}<br>Count: {end_count}"
    ).add_to(marker_cluster)


m.save("routes.html")

sept_data = pd.read_csv("Data-IO 2024 Dataset/September.csv")
oct_data = pd.read_csv("Data-IO 2024 Dataset/October.csv")
nov_data = pd.read_csv("Data-IO 2024 Dataset/November.csv")

sept_data['coordinate'] = sept_data['end_lng'].astype(str) + ',' + sept_data['end_lat'].astype(str)
oct_data['coordinate'] = oct_data['end_lng'].astype(str) + ',' + oct_data['end_lat'].astype(str)
nov_data['coordinate'] = nov_data['end_lng'].astype(str) + ',' + nov_data['end_lat'].astype(str)

#Location

most_popular_coord1 = sept_data['coordinate'].value_counts().idxmax()
sept_station_name = sept_data.loc[sept_data['coordinate'] == most_popular_coord1, 'end_station_name'].iloc[0]

most_popular_coord2 = oct_data['coordinate'].value_counts().idxmax()
oct_station_name = oct_data.loc[oct_data['coordinate'] == most_popular_coord2, 'end_station_name'].iloc[0]

most_popular_coord3 = nov_data['coordinate'].value_counts().idxmax()
nov_station_name = nov_data.loc[nov_data['coordinate'] == most_popular_coord3, 'end_station_name'].iloc[0]

#Ride type

type1 = sept_data['rideable_type'].value_counts().idxmax()

type2 = oct_data['rideable_type'].value_counts().idxmax()

type3 = nov_data['rideable_type'].value_counts().idxmax()

#Member

mem1 = sept_data['member_casual'].value_counts().idxmax()

mem2 = oct_data['member_casual'].value_counts().idxmax()

mem3 = nov_data['member_casual'].value_counts().idxmax()

#routes
sept_data['route'] = sept_data['start_station_name'] + ' to ' + sept_data['end_station_name']
oct_data['route'] = oct_data['start_station_name'] + ' to ' + oct_data['end_station_name']
nov_data['route'] = nov_data['start_station_name'] + ' to ' + nov_data['end_station_name']

#Find mode routes
mode_route1 = sept_data['route'].mode()[0]
mode_route2 = oct_data['route'].mode()[0]
mode_route3 = nov_data['route'].mode()[0]

num_rows_sept = sept_data.shape[0] - 1
