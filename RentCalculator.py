import numpy as np
import locale
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker

# A calculator for seeing how much each roommate should pay for rent based on their income.
# Great for working couples or friends who have decided to live together but have differing income.
# This could be translated to monthly bills, groceries, whatever.
# The calculations are based on the assumption that the fairest split is to pay the same amount of your monthly income.
# Even though the percentages will be the same the actual amounts will differ based on income such that the higher
# income individual will pay more than the lower income individual while still maintaining a level of fairness since
# the percentages of income for each person will be the same.

# YOUR FAIR SHARE WAS DEVELOPED BY BOYER SIMPKINS M.S. STARTING ON 11/22/2022 R.I.P. JFK
# POSSIBLE IMPROVEMENTS
# 1: Make a general application for mortgage, monthly bills, groceries, etc.
# 2: Make it general such that any number of users can input their income.
# 3: Adjust the amount of monthly income that is to be spent on rent.
# 4: Add a GUI that could easily be put into a website.
# 5: Adding commas to numbers.
# 6: Add a graph that shows your savings over time.


# Adds commas to the values and rounds decimals
def format_currecy_value(value):
    locale.setlocale(locale.LC_ALL, '')
    return locale.currency(value, symbol=False, grouping=True)


# Calculations are based on the assumption that an individuals shouldn't spend more than 25% of their monthly income
# on rent.
def fair_share(rent, income1, income2):
    if (income1 + income2) < rent:
        print("You are spending too much on rent. Look for a better deal!")

    else:
        # Using good ole Linear Algebra to solve the systems of equations
        incomes = np.array([[income1, income2], [1, -1]])
        equals = np.array([rent, 0])
        solved = np.linalg.solve(incomes, equals)

        # Print out how much each person should spend on rent per month
        print("Individual one should spend: $", format_currecy_value(solved[1] * income1))
        print("Individual two should spend: $", format_currecy_value(solved[1] * income2))

        print("---------------------------------------------------------------------"
              "---------------------------------------------------------------------")
        print("Total savings for current rent price:")

        # How much of surplus money does each individual have that they could spend on rent
        print("Individual one could spend $", format_currecy_value((1 - solved[1]) * income1), "more on rent and still be frugal.")
        print("Individual two could spend $", format_currecy_value((1 - solved[1]) * income2), "more on rent and still be frugal.")

        print("---------------------------------------------------------------------"
              "---------------------------------------------------------------------")
        print("If the savings were invested into the stock market:")

        # How much each individual could earn if they put saved money into the market
        summation1 = 0
        summation2 = 0
        x_axis = []
        y_axis = []
        for i in range(1, 11):
            summation1 += ((1 - solved[1]) * income1 * 12) * (1.06 ** i)
            summation2 += ((1 - solved[1]) * income2 * 12) * (1.06 ** i)
        combined_income = summation1 + summation2
        x_axis.append(10)
        y_axis.append(int(combined_income))
        print("Combined savings could grow to $", format_currecy_value(combined_income), "in 10 years")

        summation1 = 0
        summation2 = 0
        for i in range(1, 21):
            summation1 += ((1 - solved[1]) * income1 * 12) * (1.06 ** i)
            summation2 += ((1 - solved[1]) * income2 * 12) * (1.06 ** i)
        combined_income = summation1 + summation2
        x_axis.append(20)
        y_axis.append(int(combined_income))
        print("Combined savings could grow to $", format_currecy_value(combined_income), "in 20 years")

        summation1 = 0
        summation2 = 0
        for i in range(1, 31):
            summation1 += ((1 - solved[1]) * income1 * 12) * (1.06 ** i)
            summation2 += ((1 - solved[1]) * income2 * 12) * (1.06 ** i)
        combined_income = summation1 + summation2
        x_axis.append(30)
        y_axis.append(int(combined_income))
        print("Combined savings could grow to $", format_currecy_value(combined_income), "in 30 years")

        summation1 = 0
        summation2 = 0
        for i in range(1, 41):
            summation1 += ((1 - solved[1]) * income1 * 12) * (1.06 ** i)
            summation2 += ((1 - solved[1]) * income2 * 12) * (1.06 ** i)
        combined_income = summation1 + summation2
        x_axis.append(40)
        y_axis.append(int(combined_income))
        print("Combined savings could grow to $", format_currecy_value(combined_income), "in 40 years")

        # Create chart of future savings.
        x = np.array(x_axis)
        y = np.array(y_axis)
        plt.plot(x, y)  # Plot the chart
        plt.xlabel("Years")  # add X-axis label
        plt.ylabel("Retirement Savings (USD Millions)")  # add Y-axis label
        plt.title("Retirement Savings Generated by Housing Savings")  # add title
        plt.show()  # display


keep_calculating = True
while keep_calculating:
    print("Welcome to Fair Share!")
    print("The app for calculating how much each partner or roommate should pay "
          "by considering the price of the property and the indivdual's income.")
    print("---------------------------------------------------------------------"
          "---------------------------------------------------------------------")
    # Getting input from the user.
    monthlyRent = input("What is your monthly rent?: ")
    incomeType1 = input("Is your income salaried or hourly? (Enter 1 for salaried and 2 for hourly) ")
    if int(incomeType1) == 1:
        incomeOne = input("What is the yearly income of the 1st individual?: ")
    if int(incomeType1) == 2:
        incomeOne = input("What is the hourly income of the 1st individual?: ")
        timeWorked = input("How many hours does individual one typically work in a week?: ")

        # calculates yearly income
        incomeOne = float(incomeOne) * float(timeWorked) * 52

    incomeType2 = input("Is your income salaried or hourly? (Enter 1 for salaried and 2 for hourly) ")
    if int(incomeType2) == 1:
        incomeTwo = input("What is the yearly income of the 2nd individual?: ")
    if int(incomeType2) == 2:
        incomeTwo = input("What is the hourly income of the 2nd individual?: ")
        timeWorked = input("How many hours does individual two typically work in a week?: ")

        # calculates yearly income
        incomeTwo = float(incomeTwo) * float(timeWorked) * 52

    print("---------------------------------------------------------------------"
          "---------------------------------------------------------------------")

    # Calculating the weekly income of each person which translates to the amount you should spend on rent per month.
    incomeOne = float(incomeOne) / 52
    incomeTwo = float(incomeTwo) / 52

    # Passing these values into the definition that does the calculation
    fair_share(float(monthlyRent), incomeOne, incomeTwo)

    print("---------------------------------------------------------------------"
          "---------------------------------------------------------------------")

    keep_calculating_input = input("Would you like to make another calculation? (0 for yes and 1 for no) ")
    if int(keep_calculating_input) == 0:
        keep_calculating = True
    else:
        keep_calculating = False
        print("---------------------------------------------------------------------"
              "---------------------------------------------------------------------")
        print("Thanks for using fair share!!")