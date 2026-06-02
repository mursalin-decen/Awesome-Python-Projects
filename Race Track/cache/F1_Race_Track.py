import fastf1
import matplotlib.pyplot as plt

# Cache enable
fastf1.Cache.enable_cache("cache")

# Load Monaco 2024 Qualifying session
session = fastf1.get_session(2024, "Monaco", "Q")
session.load()

# Fastest lap
lap = session.laps.pick_fastest()

# Position data
pos = lap.get_pos_data()

# Plot track map
plt.figure(figsize=(8, 8))
plt.plot(
    pos["X"],
    pos["Y"],
    lw=4
)

plt.axis("equal")
plt.title("Monaco GP Track")
plt.show()