import csv
city_dict = dict()

with open('uscities.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)
    for row in reader:
        city = row[0]
        state = row[1]
        if state in city_dict:
            city_dict[state].append(city)
        else:
            city_dict[state] = [city]

with open('cities.txt', 'w', encoding='utf-8') as txtfile:
    txtfile.write(str(city_dict))
