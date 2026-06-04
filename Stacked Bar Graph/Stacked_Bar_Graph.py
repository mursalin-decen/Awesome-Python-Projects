import matplotlib.pyplot as pyplot

# Set up the data
labels = ('Python', 'Scala', 'C#', 'Java', 'PHP')
index = (1, 2, 3, 4, 5)

web_usage = [20, 2, 5, 10, 14]
data_science_usage = [15, 8, 5, 15, 2]
games_usage = [10, 1, 5, 5, 4]

# Set up the bar chart
pyplot.bar(index, web_usage, tick_label=labels, label='Web')

pyplot.bar(
    index,
    data_science_usage,
    tick_label=labels,
    label='Data Science',
    bottom=web_usage
)

web_and_games_usage = [
    web_usage[i] + data_science_usage[i]
    for i in range(len(web_usage))
]

pyplot.bar(
    index,
    games_usage,
    tick_label=labels,
    label='Games',
    bottom=web_and_games_usage
)

# Configure the Layout
pyplot.ylabel('Usage')
pyplot.xlabel('Programming Languages')
pyplot.legend()

# Display the chart
pyplot.show()