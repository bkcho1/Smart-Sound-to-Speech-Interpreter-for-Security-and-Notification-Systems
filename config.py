import os

# handle to the database
DATABASE_URI = 'sqlite+pysqlite:///' + os.path.dirname(os.path.realpath(__file__)) +'/sounds-and-messages.db'
