import csv


def is_login(username, pwd):
    with open('data.csv') as f:
        for i in csv.reader(f):
            if i[1] == username and pwd == i[2]:
                return i[0]
        else:
            return None
