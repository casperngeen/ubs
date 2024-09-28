from flask import Flask

app = Flask(__name__)
import routes.square
import routes.wordle
import routes.lab_work
import routes.klotski
import routes.bugfixer_p1