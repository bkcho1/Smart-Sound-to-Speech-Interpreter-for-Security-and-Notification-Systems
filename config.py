import os

# directory of project files
DIRECTORY = os.path.dirname(os.path.realpath(__file__))

# directory of sound files
SOUNDS = os.path.dirname(os.path.realpath(__file__)) + '/sounds'

# handle to the database
DATABASE_URI = 'sqlite+pysqlite:///' + DIRECTORY + '/sounds-and-messages.db'
