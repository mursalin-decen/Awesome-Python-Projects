import plotly.express as px

# Take country name from user
country = input("Enter the country name: ")

# Data for highlighting country
data = {
    'Country': [country],
    'Values': [100]
}

# Create world map
fig = px.choropleth(
    data,
    locations='Country',
    locationmode='country names',
    color='Values',
    color_continuous_scale='Inferno',
    title=f'Country Map Highlighting {country}'
)

# Show map
fig.show()