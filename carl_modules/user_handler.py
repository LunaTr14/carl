from csv_handler import CSV

class UserHandler():
    csv = CSV
    def __init__(self,csv:CSV) -> None:
        self.csv = csv

    def add_user(self, data : list) -> None:
        self.csv.append([data])

    def find_user(self, id : str) -> list:
        data = self.csv.read()
        for row in data:
            if(len(row) != 0 and row[0] == id):
                return row
        return []
    
    def update_user(self, id: str, data : list) -> None:
        data = self.csv.read()
        new_data = []
        for row in data:
            if(row[0] != id):
                new_data.append(row)
        new_data.append(data)
        self.csv.write(new_data)