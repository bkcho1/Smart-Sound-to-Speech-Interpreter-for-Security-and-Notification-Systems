import os

DEV_MODE = True

SHOW = False

# directory of project files
DIRECTORY = os.path.dirname(os.path.realpath(__file__))

# directory of sound files
SOUNDS = os.path.dirname(os.path.realpath(__file__)) + '/sounds'

# handle to the database
DATABASE_URI = 'sqlite+pysqlite:///' + DIRECTORY + '/sounds-and-messages.db'

DEFAULT_FS = 44100

DEFAULT_WINDOW_SIZE = 4096

DEFAULT_FAN_VALUE = 5

DEFAULT_OVERLAP_RATIO = 0.5

CONNECTIVITY_MASK = 2

PEAK_NEIGHBORHOOD_SIZE = 10

DEFAULT_AMP_MIN = 10

MIN_HASH_TIME_DELTA = 0
MAX_HASH_TIME_DELTA = 200

FINGERPRINT_REDUCTION = 20

