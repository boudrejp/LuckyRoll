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
    Calculates p value of a set of dice rolls being statistically different than expected values.

    parameters
    ---------------------
    rolls : str
        a string of ints separated by a comma for each dice roll of a particular dice
    dice: integer
            integer representing number of sides of the dice

    OUTPUTS:
        ret_dict = {
            'pval': float. the p value of hypothesis test
            'exp_val': float. expected mean of the dice rolls
            'actual_mean': float. the actual mean of the dice rolls
        }

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

        ret_dict = {
            'pval': hyp_test.pvalue,
            'exp_val': exp_val,
            'actual_mean': rolls_mean
        }
    return ret_dict


# returning in next commit to finish this issue
# @app.route('/v1/all_dice', methods=['GET'])
# def all_dice_calculator():
#     '''
#     Calculates p value of a set of dice rolls being statistically different than expected values.
#
#     parameters
#     ---------------------
#     dice : json
#         a json object with the following structure:
#         {'all_dice':
#             [
#                 {dice: n_sides (integer),
#                  rolls: [] (a list of ints representing the dice rolls)}
#             ]
#         }
#
#     OUTPUTS: a string with a statement about the rolls called ret_str
#     # TODO: use simulated p value because you can't really look at all the rolls at the same time otherwise
#     # under the null hypothesis all sides are equal. So any number of rolls from all available dice should result in some distribution of a sum of the dice rolls
#     # we can check how far on the distribution the actual roll sum is in order to determine if all the dice together are skewing high or skewing low
#     '''
#     # retrieve params and format appropriately
#     query_parameters = flask.request.json
#     dice = query_parameters["all_dice"]
#     print(f"data passed: {dice}")
#     print(dice[1])
#
#     # overall algorithm
#     # storage
#     rolls_sums_list = []
#     actuals_sum = 0
#     n_simulations = 10000
#
#     # loop over all dice present
#     for die in dice:
#         # enforce correct data types
#         die_rolls = [int(roll) for roll in die['rolls']]
#         n_sides = int(die['sides'])
#         # enumerate the die sides. then, simulate the rolls and weight using multinomial distribution
#         die_sides = np.array(list(range(1, n_sides + 1)))
#         rolls = np.random.multinomial(len(die_rolls), [1/n_sides] * n_sides, size = n_simulations) * die_sides
#         rolls_sums = np.sum(rolls, axis = 1)
#
#         rolls_sums_list.append(rolls_sums)
#
#         # also need to populate the acutals
#         # map the rolls variable into the number of rolls of each number
#         def count_each_roll(n_sides, rolls):
#             output_list = [0 for i in range(n_sides)]
#             for roll in rolls:
#                 output_list[roll-1] += 1
#             return output_list
#
#         actuals_rolls_counts = count_each_roll(n_sides, die_rolls)
#         actuals_sum += np.sum(np.array(actuals_rolls_counts) * die_sides)
#
#
#
#     # bring all dice sum arrays together for the sums overall
#     all_simulated_rolls_sums = np.sum(np.stack(tuple([i for i in rolls_sums_list]), axis = -1), axis = 1)
#
#     simulated_mean = np.mean(all_simulated_rolls_sums)
#
#     # perform hypothesis test
#     # how many simulated rolls were at least as extreme as this one?
#     # simulates 2 tailed test
#     delta = np.absolute(simulated_mean - actuals_sum)
#     simulations_greater = np.greater_equal(all_simulated_rolls_sums, simulated_mean + delta)
#     simulations_less = np.less_equal(all_simulated_rolls_sums, simulated_mean - delta)
#     hyp_test = np.sum(np.logical_or(simulations_greater, simulations_less))/all_simulated_rolls_sums.shape[0]
#
#     if hyp_test <= 0.05:
#         # different response for if it's higher or lower
#         if actuals_sum >= simulated_mean:
#             ret_str = f"Look at that! There's something lucky going on with your dice. Your rolls added up to  {round(actuals_sum, 3)} and what you would normally expect is {int(round(simulated_mean, 0))}. This has an associated p-value of {round(hyp_test, 3)}, which is statistically significant. Good stuff!"
#         else:
#             ret_str = f"Yikes! There's something unlucky going on with your dice. Your rolls added up to {round(actuals_sum, 3)} and what you would normally expect is {int(round(simulated_mean, 0))}. This has an associated p-value of {round(hyp_test, 3)}, which is statistically significant. The dice gods are not on your side!"
#
#     else:
#         ret_str = f"Looks like your dice are working as expected. Your rolls added up to {round(actuals_sum, 3)} and what you would normally expect is {int(round(simulated_mean, 0))}. This has an associated p-value of {round(hyp_test, 3)}, which isn't statistically significant. Don't blame this one on the dice!"
#
#
#
#     return f"<p>{ret_str}</p>"


app.run()
