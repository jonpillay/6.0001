"""Returns as a string the best rate of savings to achieve 
a down payment on a $1M house in 36 months. 

Takes user input for:
1. Annual Sallary
"""

annual_sallary = int(input("What is your annual salary? "))

total_cost = 1000000
semi_annual_raise = 0.07
epsilon = 100
portion_down_payment = total_cost * .25
r = 0.04
low = 0
high = 1000
guess = (high + low)/2
number_of_guesses = 0
current_savings = 0

if annual_sallary * 36 < total_cost: # do I need to add in the salary raise?
    print("It is not possible to pay the down payment in 3 years.")
else:
    while abs(portion_down_payment-current_savings) >= epsilon:
        dummy_sallary = annual_sallary
        number_of_guesses += 1
        current_savings = 0
        for i in range(1,37):
            current_savings += (current_savings*r)/12
            current_savings += (dummy_sallary/12)*(guess/1000)
            if i % 6 == 0:
                dummy_sallary += dummy_sallary * semi_annual_raise
        if portion_down_payment - current_savings > 0:
            low = guess
        else:
            high = guess
        guess = (high+low)/2
        
    print("Best savings Rate: " + str(round(guess/1000, 4)))
    print("Steps in bisection search: " + str(number_of_guesses))