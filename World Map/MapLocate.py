import folium
# Import the Geocoder plugin
from folium.plugins import Geocoder

# 1. Initialize the map (centered globally at a neutral starting point)
m = folium.Map(location=[20.0, 0.0], zoom_start=2)

# 2. Add the global search bar plugin to the map
Geocoder(
    collapsed=False,         # Keeps the search box expanded and visible by default
    position='topright',     # Position of the search box on the screen
    add_marker=True,         # Automatically drops a pin on the found location
    zoom=12                  # The zoom level to snap to once a city is found
).add_to(m)


m.save("worldwide_search_map.html")