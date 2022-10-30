import mariadb
import os
from sqlCommand import Command
from dotenv import load_dotenv


class Connections(): #connection DB, dataBasa = choice DB, commandData = sql command, soed = for inseert, update and delete command
    def __init__(self):
        pass

    def connect(self, dataBasa, commandData, soed=False):
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)
        try:
            self.conn_params = {
                "user": os.environ.get('user'),
                "password": os.environ.get('password'),
                "host": os.environ.get('host1'),
                "database": os.environ.get(f'{dataBasa}')
            }
            zapros = (self.conn_params)
            self.connection = mariadb.connect(**zapros)
            cursor = self.connection.cursor()
            print(commandData)
            if soed == False:
                cursor.execute(f"""{commandData}""")
                row = cursor.fetchall()
                cursor.close()
                self.connection.close()
                # print(row)
                return row
            if soed:
                cursor.execute(f"""{commandData}""", soed)
                self.connection.commit()
                cursor.close()
                self.connection.close()
                return True
        except:
            print('error connect')

class DataSync(Connections, Command): # sync ExpoCRM-DB and python-DB
    def __init__(self):
        super().CommandSQL()
        # self.basa = self.requestEspoCRM('databaseOne', self.mySqlCommandProverka)
        # self.addData(self.basa, 'databaseTwo', self.mySqlCommandSozdanie)
        pass

    def sravnenie(self, row, basa, database): # transfers the Espo-DB reminder to python-DB and delete the old python-DB reminder
        result1 = list(set(basa) - set(row))
        result2 = list(set(row) - set(basa))
        if result1:#transfer
            for i in result1:
                commandi = (f"INSERT INTO notifications(notification_id, data, class, user) VALUES (?,?,?,?)")
                self.connect(database, commandi, i)
        if result2:#delete
            for i in result2:
                commandi = (f"DELETE FROM notifications WHERE notification_id=?")
                turle = (i[0],)
                self.connect(database, commandi, turle)
        print(result1)
        print(result2)
        print(row)
        print(basa)
    def requestEspoCRM(self, database, commandMysql, soed=False): #connect EspoCRM and request all reminder
        try:
            row = self.connect(database, commandMysql, soed)
            return row
        except:
            print('error')
    def addData(self, basa, database, commandMysql): #connect pythhon-DB and request all reminder
        try:
            row = self.connect(database, commandMysql, False)
            self.sravnenie(row, basa, database)
        except:
            print('error')

    def startMysql(self):
        # self.basa = self.requestEspoCRM(database='databaseOne', commandMysql=self.mySqlCommandProverka)
        les = self.requestEspoCRM(database='databaseOne', commandMysql=self.requestReminder)
        for i in range(len(les)):
            # print(self.requsetTask)
            # print(les[i][0])
            self.raz=les[i][0]
            self.dva=les[i][1]
            self.tri=les[i][2]
            self.requsetTask = f"""SELECT * from {self.raz} WHERE {self.dva}.id = '{self.tri}';"""
            let = self.requestEspoCRM(database='databaseOne', commandMysql=self.requsetTask)
            print(let)
            # print(i)
        # s = [i for i in les]
        # print(s[0][0])

sin = DataSync()
sin.startMysql()