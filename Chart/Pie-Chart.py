from matplotlib import pyplot as plt

labels = ['Category A', 'Category B', 'Category C']
sizes = [30,45,25]


plt.pie(sizes, labels=labels, autopct='%1.1f%%')
plt.title('Pie Chart')
plt.show()