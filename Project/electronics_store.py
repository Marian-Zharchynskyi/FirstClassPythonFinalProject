import pandas as pd
from flask import jsonify
import matplotlib.pyplot as plt
from electronic import Electronic
from pandasql import sqldf
from datetime import datetime as dt


class Electronics_store:
    def __init__(self):

        self.__electronics: list[Electronic] = []

    def add_electronic(self, electronic: Electronic):
        self.__electronics.append(electronic)
        self.update_file()
        return "electronic was added"

    def delete_electronic(self, id: str):
        self.__electronics = list(filter(lambda x: x.id != id, self.__electronics))
        self.update_file()
        return "electronic was deleted"

    def get_all_electronics(self):
        return list(map(lambda x: {"id": x.id, "electronic name": x.name}, self.__electronics))

    def get_some_electronic(self, id: str):
        return [elec.__dict__ for elec in self.__electronics if id == elec.id]

    def update_file(self):
        electronics_file = open("table.csv", 'w')
        electronics_file.write('name,id,price,released_at,manufacturer,guarantee')
        electronics_file.writelines([f"\n{electronic.name},{electronic.id},{electronic.price},{electronic.released_at},{electronic.manufacturer},{electronic.guarantee} "for electronic in self.__electronics])

    def update_electronic(self, electronic: Electronic):
        for _elec in self.__electronics:
            if _elec.id == electronic.id:
                _elec.name = electronic.name
                _elec.price = electronic.price
                _elec.released_at = electronic.released_at
                _elec.manufacturer = electronic.manufacturer
                _elec.guarantee = electronic.guarantee
        self.update_file()
        return "electronic was updated"

    def read_file(self):
        electronics_file = open('table.csv', 'r')

        for line in self.get_data_from_file():
            user_input = line.split(',')
            if len(user_input) == 6:
                input_name = user_input[0].strip()
                input_id = user_input[1].strip()
                input_price = user_input[2].strip()
                input_released_at = user_input[3].strip()
                input_manufacturer = user_input[4].strip()
                input_guarantee = user_input[5].strip()

                self.__electronics.append(Electronic(input_name, input_id, float(input_price), input_released_at,
                                                     input_manufacturer, int(input_guarantee)))

    def get_data_from_file(self):
        products_file = open("table.csv", "r")
        return [line for line in products_file][1:]

    def get_electronics_in_some_period(self, _from: str, _to: str):
        input = pd.read_csv('table.csv', delimiter=',')
        input['released_at'] = pd.to_datetime(input['released_at'], format="%Y.%m.%d")
        expired_at_from = dt.strptime(_from, "%Y.%m.%d")
        expired_at_to = dt.strptime(_to, "%Y.%m.%d")

        query = f'''
                select * from input as i
                where date(i.released_at) >= date('{expired_at_from}')
                and date(i.released_at) <= date('{expired_at_to}')
            '''
        result = sqldf(query)
        print(result)
        return jsonify(result.to_dict(orient="records"))

    def get_most_expensive_electronics(self):
        input = pd.read_csv('table.csv', delimiter=',')

        query = '''
            select i.name, i.manufacturer, i.price from input as i
            group by i.manufacturer
            having max(i.price)
        '''

        result = sqldf(query)
        return jsonify(result.to_dict(orient="records"))

    def most_expensive_diagram(self):
        df = pd.read_csv('table.csv', delimiter=',')

        most_expensive_by_manufacturer = df[['manufacturer', 'price']].groupby('manufacturer').agg(['max'])

        plt.figure(figsize=(10, 6))
        plt.xlabel('Company')
        plt.ylabel('Max Sale')
        plt.xticks(range(len(most_expensive_by_manufacturer.index)), most_expensive_by_manufacturer.index, rotation=90, fontsize=8)
        plt.title('The most expensive electronic by the company')

        plt.bar(most_expensive_by_manufacturer.index, most_expensive_by_manufacturer[('price', 'max')], color='green', alpha=0.7)

        plt.savefig('The_most_expensive_electronic_by_the_company.png')
