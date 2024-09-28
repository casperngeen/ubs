import json
import logging
from routes import app

logger = logging.getLogger(__name__)


@app.route('/ub5-flags', methods=['GET'])
def decode():
    response = {
        "sanityScroll": {
            "flag": "UB5{w3lc0m3_70_c7f_N0ttyB01}"
        },
        "openAiExploration": {
            "flag": "sk-ilOvESpoRTs"
        },
        "dictionaryAttack": {
            "flag": "UB5{FLAG_CONTENT_HERE}",
            "password": "PASSWORD_HERE"
        },
        "pictureSteganography": {
            "flagOne": "UB5-1{1_am_d3f_n0t_old}",
            "flagTwo": "UB5-2{FLAG_TWO_CONTENTS_HERE}"
        },
        "reverseEngineeringTheDeal": {
            "flag": "FLAG_CONTENT_HERE",
            "key": "KEY_HERE"
        }
    }
    return json.dumps(response)
