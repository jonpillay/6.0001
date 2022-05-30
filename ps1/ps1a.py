"""Returns as a string the amount of months it will take to save for a down payment.

Takes user input for:
1.Their starting annual salary (annual_salary) 
2.The portion of salary to be saved (portion_saved) 
3.The cost of your dream home (total_cost) 
"""

annual_sallary = int(input("What is your annual salary? "))
portion_saved = float(input("What portion do you want to save? "))
total_cost = int(input("How much does the gaff cost? "))

month = 0
current_savings = 0
portion_down_payment = total_cost * .25
r = 0.04

while True:
    month += 1
    current_savings += current_savings*r/12
    current_savings += (annual_sallary/12)*portion_saved
    if current_savings >= portion_down_payment:
        print("Months to save downpayent: " + str(month))
        break

