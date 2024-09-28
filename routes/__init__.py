from flask import Flask

app = Flask(__name__)

import routes.square
import routes.wordle
import routes.klotski
import routes.thetourist
import routes.mailtime