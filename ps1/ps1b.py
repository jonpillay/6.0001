"""Returns as a string the ammount of months it will take save
for the down payment for the house.

Takes user input for:
1. The starting annual salary (annual_salary)
2. The percentage of salary to be saved (portion_saved)
3. The cost of your dream home (total_cost)
4. The semi annual salary raise (semi_annual_raise)

Differs from ps1a.py as it take into account wage increases.
"""


annual_sallary = int(input("What is your annual salary? "))
portion_saved = float(input("What portion do you want to save? "))
total_cost = int(input("How much does the gaff cost? "))
semi_annual_raise = float(input("What is your semi annual pay rise? "))

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
    if month % 6 == 0:
        annual_sallary+=annual_sallary*semi_annual_raise