from flask import Flask

app = Flask(__name__)
import routes.thetourist
import routes.klotski
import routes.wordle
import routes.square
