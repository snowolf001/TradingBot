# this file is responsible for all buying and selling actions and their logging
# the stock data is read out of the sqlite3 database


class Stock:
    def __init__(self, symbol, start_acc=1000, fee=0.01):
        # this function is the init
        self.symbol = symbol
        self.account = start_acc
        self.table_name = symbol.upper() + '_Account'
        self.broker_fee = fee
        self.units = 0

    def log_to_database(self, action, last_price=0, units=0, savingtoCsv=False):
        # this function will write the log for transactions
        # loading the needed modules
        import os
        import sqlite3
        import pandas as pd
        from datetime import datetime
        # checking for database
        # creating path
        file = '/home/niklas/Desktop/TradingBot/Transactions/Transactions-{}.db'.format(self.symbol)
        # getting current time
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        # checking if already exists
        if not os.path.isfile(file):
            # creating file and table
            conn = sqlite3.connect(file)
            c = conn.cursor()
            c.execute(
                'CREATE TABLE {} (Time TEXT, ID_Function TEXT, ID TEXT, symbol TEXT, price_each REAL, units REAL, '
                'price_total REAL, profit REAL, fee REAL, account REAL)'.format(self.table_name))
        else:
            # already existing, establishing connection
            conn = sqlite3.connect(file)
            c = conn.cursor()
            # now the database is connected through
            # next we are going to check if the table already exists
            table_check = "SELECT name FROM sqlite_master WHERE type='table' AND name='{}';".format(self.table_name)
            c.execute(table_check)
            result = c.fetchone()
            if result:
                # table found
                None
            else:
                # table not found
                c.execute(
                    'CREATE TABLE {} (Time TEXT, ID_Function TEXT, ID TEXT, symbol TEXT, price_each REAL, units REAL, '
                    'price_total REAL, profit REAL, fee REAL, account REAL)'.format(self.table_name))
            # read data which is already in database
            df = pd.read_sql_query("SELECT * FROM {}".format(self.table_name), conn)
            # calculating profit
            if action == 'BUY':
                profit = float(float(self.account) + float(units * float(last_price))) * 100 / float(self.account)
            elif action == 'SELL':
                profit = (self.account - float(units * float(last_price))) * 100 / self.account
            else:
                profit = 0
            # counting rows
            index = df.index
            count = len(index)
            # creating row with data
            # starting with dictionary
            row_dict = {
                'Time': [timestamp],
                'ID_Function': [action],
                'ID': [count],
                'symbol': [self.symbol],
                'price_each': [last_price],
                'units': [units],
                'price_total': [float(units * float(last_price))],
                'profit': [profit],
                'fee': [self.broker_fee],
                'account': [self.account]
            }
            df_row = pd.DataFrame(row_dict)
            # new row added to new dataframe
            new_df = pd.concat([df, df_row], ignore_index=True)
            # check if need to save to CSV-File
            if savingtoCsv:
                # saved data csv-file data
                new_df.to_csv('/home/niklas/Desktop/TradingBot/Transactions/Transactions-{}.csv'.format(self.symbol),
                              sep=';')
            # write data to database
            new_df.to_sql(self.table_name, conn, if_exists='replace', index=False)
            # committing the saves
            conn.commit()
            # closing the connection
            conn.close()

    def read_stock_price(self):
        # read the stock price latest
        import GetStockData
        data_latest = GetStockData.get_data_latest(self.symbol)
        return data_latest

    def change(self, value):
        # manually recharging the account
        self.account += value
        self.log_to_database()

    def buy(self, units_to_buy):
        # buying stock price
        latest = self.read_stock_price()
        last_price = latest[0]['05. price'][0]
        self.units += units_to_buy
        self.account -= units_to_buy * float(last_price) + units_to_buy * self.broker_fee
        self.log_to_database('BUY',last_price=last_price, units=units_to_buy, savingtoCsv=True)

    def sell(self, units_to_sell):
        None




    def __repr__(self):
        return self

    def __str__(self):
        return 'Symbol: ' + self.symbol + ' Balance: ' + str(self.account) + ' Units: ' + str(
            self.units) + ' Tabel name: ' + self.table_name


if __name__ == "__main__":
    ibm = Stock('IBM')
    ibm.buy(4)
    print(ibm)
