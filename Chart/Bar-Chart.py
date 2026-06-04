from matplotlib import pyplot as plot

categories = ['A', 'B', 'C', 'D']
values = [25, 40, 30, 20]

plot.bar(categories, values)
plot.title('Bar Chart')
plot.xlabel('Categories')
plot.ylabel('Values')
plot.show()