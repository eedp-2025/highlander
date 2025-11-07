import gregorian

def get_name():
    return input("What is your name? ")



##### main part of script
print("Hello World")
name = get_name()
birth_year = int(input("What is your birth year? "))
leap_year = gregorian.is_leap_year(birth_year)
if leap_year:
    print("That was a leap year!")
