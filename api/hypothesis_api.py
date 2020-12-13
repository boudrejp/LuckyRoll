import flask
from flask import request, jsonify
from scipy.stats import ttest_1samp
import numpy as np


app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Dice rolling calculator</h1><p>Use this API to calculate the luck of any sort of dice rolling session.</p>"

@app.route('/v1/single_dice', methods=['GET'])
def single_dice_calculator():
    '''
    Calculates p value of a set of d6 rolls being statistically different than expected values.
    INPUTS: a string integers separated by commas (no spaces) representing rolls of a dice as argument "rolls"
            an integer representing the number of sides on the dice called "dice"
    OUTPUTS: a string with a statement about the rolls called ret_str
    TODO: logic on values not being above 6
    '''
    # retrieve params and format appropriately
    query_parameters = request.args
    rolls = [int(roll) for roll in query_parameters.get('rolls').split(',')]
    dice = int(query_parameters.get('dice'))

    # catch if length of rolls isn't long enough to do statistics
    if len(rolls) < 3:
        ret_str = "Looks like there's not enough rolls here to see if you're lucky or not!"
    else:
        # figure out what the expected value of the dice is
        exp_val = sum(list(range(dice+1)))/dice
        rolls_mean = np.mean(rolls)

        # perform hypothesis test
        hyp_test = ttest_1samp(rolls, exp_val)

        if hyp_test.pvalue <= 0.05:
            # different response for if it's higher or lower
            if rolls_mean >= exp_val:
                ret_str = f"Look at that! There's something lucky going on with your d{dice}. You had an average roll of {round(rolls_mean, 3)} and an associated p-value of {round(hyp_test.pvalue, 3)}, which is statistically significant. Good stuff!"
            else:
                ret_str = f"Yikes! There's something unlucky going on with your d{dice}. You had an average roll of {round(rolls_mean, 3)} and an associated p-value of {round(hyp_test.pvalue, 3)}, which is statistically significant. The dice gods are not on your side!"

        else:
            ret_str = f"Looks like your d{dice} is working as expected. You had an average roll of {round(rolls_mean, 3)} and an associated p-value of {round(hyp_test.pvalue, 3)}, which isn't statistically significant. Don't blame this one on the dice!"


    return f"<p>{ret_str}</p>"



app.run()
