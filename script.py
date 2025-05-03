import locale
import numpy as np

# Adds commas to the values and rounds decimals
def format_currecy_value(value):
    locale.setlocale(locale.LC_ALL, '')
    return locale.currency(value, symbol=False, grouping=True)


def split_dict(input_dict, keys_to_split):
    """Splits a dictionary into two based on specified keys.

    Args:
        input_dict (dict): The dictionary to split.
        keys_to_split (list): A list of keys to extract into a new dictionary.

    Returns:
        tuple: A tuple containing two dictionaries:
            - The first dictionary contains the key-value pairs where the keys are in keys_to_split.
            - The second dictionary contains the remaining key-value pairs.
    """
    dict1 = {k: input_dict[k] for k in keys_to_split if k in input_dict}
    dict2 = {k: input_dict[k] for k in input_dict if k not in keys_to_split}
    return dict1, dict2


# Format the percent of household incomes into a string
def format_individual_contribution(individual_contributions, output_string):
    individual = "One"
    for contribution in individual_contributions:
        output_string.append("Individual " + individual + " should pay $" + format_currecy_value(contribution))
        individual = "Two"


def process_multiple_inputs(inputs):
    try:
        # Split keys into incomes and the rest of the inputs
        keys_to_move = ['income1', 'income2']
        income_dict, rest_dict = split_dict(inputs, keys_to_move)
        keys_to_move = ['debt1', 'debt2']
        debt_dict, rest_dict = split_dict(rest_dict, keys_to_move)
        keys_to_move = ['rentOrBuy']
        housing_option, rest_dict = split_dict(rest_dict, keys_to_move)

        # Calculate sum of the incomes
        incomes = [float(value) for value in income_dict.values()]  # Convert inputs to floats
        household_income = sum(incomes)  # Calculate sum
        output_string = [f"Yearly household income: ${format_currecy_value(household_income)}"] # Adds to the output list

        # Calculate sum of the debts
        debt = [float(value) for value in debt_dict.values()]  # Convert inputs to floats
        househould_debt = sum(debt)
        output_string.append("Household monthly debt payment: $" + format_currecy_value(househould_debt)) # Adds to the output list
        output_string.append("")

        # Get rent info
        housing_expense = [float(value) for value in rest_dict.values()]  # Convert inputs to floats
        housing_expense = sum(housing_expense)

        # Get if user is a renter or buyer
        housing_option = [str(value) for value in housing_option.values()]

        # Get the maximum amount this household should spend on rent a month
        maximum_housing_expense = ((household_income / 12) * 0.30) - househould_debt
        if housing_option[0] == 'buy' and househould_debt > 0:
            output_string.append("We recommend not buying a home until all debt is cleared")

        output_string.append("Maximum monthly housing expense: $" + format_currecy_value(maximum_housing_expense))

        # See if rent exceeds maximum
        if housing_expense > maximum_housing_expense:
            output_string.append("Your housing expense exceeds maximum housing expense")
        
        output_string.append("")
        
        # Using good ole Linear Algebra to solve the systems of equations
        incomes_operator = np.array([incomes, [1, -1]])
        equals = np.array([housing_expense, 0])
        solved = np.linalg.solve(incomes_operator, equals)
        individual_contributions = solved * incomes
        format_individual_contribution(individual_contributions, output_string)

        x_axis = []
        y_axis = []
        investment_total = 0
        monthly_investment = maximum_housing_expense - housing_expense
        if housing_expense < maximum_housing_expense:
            # Calculates how much a household could make a year by staying underneath the maximum and investing what would go to debt payments
            for year in range(1, 40):
                investment_total = (investment_total + ((monthly_investment) * 12)) * (1.10)
                x_axis.append(year + 1)
                y_axis.append(investment_total)
            
            output_string.append("")
            output_string.append("Investing $" + format_currecy_value(monthly_investment) + " each month instead of maxing housing expense would equal : $" + format_currecy_value(investment_total) + " in 40 years.")

        return {
            'result': "\n".join(output_string),
            'percentage_income_one': individual_contributions[0],
            'percentage_income_two': individual_contributions[1],
            'year': x_axis,
            'investment_total': y_axis
        }
    except ValueError:
        return "Please enter valid numbers."
