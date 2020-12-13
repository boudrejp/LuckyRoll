import flask
from flask import request, jsonify
from scipy.stats import ttest_1samp
import numpy as np


app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Dice rolling calculator</h1><p>Use this API to calculate the luck of any sort of dice rolling session.</p>"

@app.route('/v1/d6', methods=['GET'])
def d6_calculator():
    '''
    Calculates p value of a set of d6 rolls being statistically different than expected values.
    INPUTS: a string integers separated by commas (no spaces) representing rolls of a d6 as argument "rolls"
    OUTPUTS: a string with a statement about the rolls called ret_str
    TODO: logic on values not being above 6
    '''
    # retrieve params and format appropriately
    query_parameters = request.args
    rolls = [int(roll) for roll in query_parameters.get('rolls').split(',')]

    # catch if length of rolls isn't long enough to do statistics
    if len(rolls) < 3:
        ret_str = "Looks like there's not enough rolls here to see if you're lucky or not!"
    else:
        rolls_mean = np.mean(rolls)
        # perform hypothesis test
        hyp_test = ttest_1samp(rolls, 3.5)
        if hyp_test.pvalue <= 0.05:
            ret_str = f"Look at that! There's something lucky going on with your dice. You had an average roll of {round(rolls_mean, 3)} and an associated p-value of {round(hyp_test.pvalue, 3)}, which is statistically significant. Good stuff!"
        else:
            ret_str = f"Looks like your dice are working as expected. You had an average roll of {round(rolls_mean, 3)} and an associated p-value of {round(hyp_test.pvalue, 3)}, which isn't statistically significant. Don't blame this one on the dice!"


    return f"<p>{ret_str}</p>"

# the above code is theoretically reworkable into a general API but I'll do a d20 for extrapolating
@app.route('/v1/d20', methods=['GET'])
def d20_calculator():
    '''
    Calculates p value of a set of d20 rolls being statistically different than expected values.
    INPUTS: a string integers separated by commas (no spaces) representing rolls of a d6 as argument "rolls"
    OUTPUTS: a string with a statement about the rolls called ret_str
    '''
    # retrieve params and format appropriately
    query_parameters = request.args
    rolls = [int(roll) for roll in query_parameters.get('rolls').split(',')]

    # catch if length of rolls isn't long enough to do statistics
    if len(rolls) < 3:
        ret_str = "Looks like there's not enough rolls here to see if you're lucky or not!"
    else:
        rolls_mean = np.mean(rolls)
        # perform hypothesis test
        hyp_test = ttest_1samp(rolls, 10.5)
        if hyp_test.pvalue <= 0.05:
            ret_str = f"Look at that! There's something lucky going on with your dice. You had an average roll of {round(rolls_mean, 3)} and an associated p-value of {round(hyp_test.pvalue, 3)}, which is statistically significant. Good stuff!"
        else:
            ret_str = f"Looks like your dice are working as expected. You had an average roll of {round(rolls_mean, 3)} and an associated p-value of {round(hyp_test.pvalue, 3)}, which isn't statistically significant. Don't blame this one on the dice!"


    return f"<p>{ret_str}</p>"


app.run()
