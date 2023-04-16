from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

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
plt.title('Map of India with State Boundaries')

# Load the dataset
data = [
    [28.7041, 77.1025, 19.0760, 72.8777],  # Delhi to Mumbai
    [19.0760, 72.8777, 12.9716, 77.5946],  # Mumbai to Bangalore
    [12.9716, 77.5946, 28.7041, 77.1025],  # Bangalore to Delhi
    [22.5726, 88.3639, 12.9716, 77.5946],  # Kolkata to Bangalore
    [18.5204, 73.8567, 19.0760, 72.8777],  # Pune to Mumbai
    [11.1368, 75.9552, 28.5556, 77.0951]   # Calicut to Delhi
]

# Initialize the scatter and line objects
start_points = m.scatter([], [], s=100, marker='o',facecolors='r', edgecolors='k', zorder=10)
end_points = m.scatter([], [], s=100, marker='o',facecolors='b', edgecolors='k', zorder=10)
lines = []



import numpy as np

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
ani = FuncAnimation(fig, update, frames=20, interval=200)

# Save the animation as an MP4 video
# ani.save('flight_paths.mp4', writer='ffmpeg', fps=30)
plt.show()