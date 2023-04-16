from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
import numpy as np

# Set the figure size and create a Basemap object
fig = plt.figure(figsize=(10, 10))
m = Basemap(projection='merc', resolution='h', llcrnrlon=68,
            llcrnrlat=7, urcrnrlon=97, urcrnrlat=37,lat_0=22, lon_0=78)

m.drawmapboundary(fill_color='#46bcec')
m.fillcontinents(color='#ffff', lake_color='#46bcec')
m.drawcoastlines()
m.drawcountries()
m.readshapefile('india', 'india', drawbounds=True)

# set the title of the plot
plt.title('Top 25 busiest airports in India')

# Define the input filename
flight_data=pd.read_csv("./Time_Period/07_00-07_59.csv")

# Load the CSV file into a Pandas DataFrame
df = pd.DataFrame(flight_data)

# Display the data
data = df.values.tolist()

# Read the latitude and longitude data from the CSV file
airports_data=pd.read_csv('airports25.csv')

# Plot each point on the map with a label
for index, row in airports_data.iterrows():
    x, y = m(row['Longitude'], row['Latitude'])
    label = row['Label']
    plt.text(x, y,"✈"+label, fontsize=7, color='orange',weight='bold')

# Initialize the scatter and line objects
start_points = m.scatter([], [], s=100, marker='o',facecolors='r', edgecolors='k', zorder=10)
end_points = m.scatter([], [], s=100, marker='o',facecolors='b', edgecolors='k', zorder=10)
lines = []

def update(frame):
    # Clear the previous lines
    for line in lines:
        line.remove()
    lines.clear()
    # Update the starting and ending points
    for i, d in enumerate(data):
        start_lat, start_lon, end_lat, end_lon = d
        # Interpolate the latitude and longitude between the starting point and current position
        cur_lat = start_lat + (end_lat - start_lat) * frame / 20
        cur_lon = start_lon + (end_lon - start_lon) * frame / 20
        lats = [start_lat, cur_lat]
        lons = [start_lon, cur_lon]
        # Plot the line connecting the interpolated points
        x, y = m(lons, lats)
        line = m.plot(x, y, linewidth=1, color='gray', zorder=5)
        lines.append(line[0])
    # Update the scatter points for starting and ending points
    start_lats = [d[0] for d in data]
    start_lons = [d[1] for d in data]
    end_lats = [d[2] for d in data]
    end_lons = [d[3] for d in data]
    if frame < 19:
        start_lats = [d[0] + (frame + 1) * 0.05 for d in data]
        start_lons = [d[1] - (frame + 1) * 0.05 for d in data]
        end_lats = [d[2] + (frame + 1) * 0.05 for d in data]
        end_lons = [d[3] - (frame + 1) * 0.05 for d in data]
    start_points.set_offsets(list(zip(start_lons, start_lats)))
    end_points.set_offsets(list(zip(end_lons, end_lats)))

    # Return the updated artists
    return lines + [start_points, end_points]

# Create the animation object
ani = FuncAnimation(fig, update, frames=20, interval=100)
plt.show()