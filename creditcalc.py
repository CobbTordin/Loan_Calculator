import argparse
import math

# __name__ is a special var. If this script is called from another module, it will NOT be __main__
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Computes differentiated or non-differentiated loan information.')
    parser.add_argument('--type', type=str, choices=['diff', 'annuity'], required=True,
                        help='Chooses either differential or annuity loan calculations.')
    parser.add_argument('-p', '--principal', type=int, help='Loan principal amount')
    parser.add_argument('-n', '--periods', type=int, help='Total number of monthly payments')
    parser.add_argument('-a', '--payment', type=float, help='Monthly annuity payment amount')
    parser.add_argument('-i', '--interest', type=float, required=True, help='Loan interest rate')
# else??? might want to handle an unexpected value here...
    
# i = interest rate input as an integer then converted to a float for calculation
# n = number of separate loan payments
# a = value of each payment (only used for 'type=annuity')
# p = loan principal

def i_calc(x):
    # returning precentage over month?
    return x / 100 / 12

# You might consider having this return a value, too, even if this is a command line tool.
# Having it return a value makes it so you use it within other scripts or even build a UI
def diff_calc(p, n, i):
    payment_list = []
    total = 0
    for m in range(n, 0, -1):
        # might want to make this guy a function. This is a hell of a calculation for a single line...
        current_payment = math.ceil((p / n) + (i_calc(i) * (p - (p * (m - 1) / n))))
        payment_list.append(current_payment)
        # many languages have a shorthand syntax for x = x + y. x += y. Similarly x++ is x = x + 1
        total = total + current_payment
        overpayment = total - p

    # this is outside the for loop above, correct?    
    rev_loan = payment_list[::-1]

    # ditto?
    for payment in rev_loan:
        month_num = rev_loan.index(payment) + 1
        print(f'Month {month_num}: payment is {payment}')

    print(f'\nOverpayment = {overpayment}')


# what the hell does this do?? Comment, my dude.
# Or at least name the function something descriptive
def n_calc(p, a, i):
    n_periods = math.log((a / (a - i_calc(i) * p)), (1 + i_calc(i)))
    n_overpayment = int((math.ceil(n_periods) * a) - p)
    return n_periods, n_overpayment

# ditto. christ.
def a_calc(p, n, i):
    a_payment = p * (i_calc(i) * (1 + i_calc(i)) ** n) / ((1 + i_calc(i)) ** n - 1)
    a_overpayment = (math.ceil(a_payment) * n) - p
    return a_payment, a_overpayment, p

# what the hell. I quit.
def p_calc(a, n, i):
    p_principal = a / ((i_calc(i) * (1 + i_calc(i)) ** n) / ((1 + i_calc(i)) ** n - 1))
    p_total = (a * n)
    p_overpayment = p_total - p_principal
    return p_principal, p_overpayment


args = parser.parse_args()

# Usually serial "ifs" like this are better handled with a switch/case:

# you've got a lot of prints as output. Again, you may want to have this return values too.
match args.type:
    
    case 'diff':
        diff_calc(args.principal, args.periods, args.interest)

    case 'annuity':
        # lets clean this up a bit...
        messageOut = ''
        if args.principal is None:
            p_tup = p_calc(args.payment, args.periods, args.interest)
            p_output = math.floor(p_tup[0])
            p_over = math.ceil(p_tup[1])
            pmessageOut = (f"Your loan principal = {p_output}!\nOverpayment = {p_over}")
        if args.payment is None:
            a_tup = a_calc(args.principal, args.periods, args.interest)
            a_output = math.ceil(a_tup[0])
            a_over = a_tup[1]
            messageOut = (f"Your annuity payment = {a_output}!\nOverpayment = {a_over}")
        if args.periods is None:
            n_tup = n_calc(args.principal, args.payment, args.interest)
            n_output = n_tup[0]
            n_over = n_tup[1]
            n_year = math.floor(math.ceil(n_output / 12))
            n_month = math.ceil(n_output % 12) % 12
            
            # fixing month vs months
            # vars: wordValue coming in would be n_month or n_year 
            def returnPlural ( possiblePlural ):
                if possiblePlural > 1:
                    return "s"
                else:
                    return ""

            # try this...
            # repaid immediately!
            if n_month == 0 and n_year == 0:
                messageOut = "This loan will be repaid instantly!"
            # months not years
            elif n_month > 0 and n_year == 0:
                messageOut = (f"It will take {n_month} month{returnPlural(n_month)} to repay this loan!\nOverpayment = {n_over}")
            # years (and possibly months)
            else:                 
                messageOut = (f"It will take {n_year} year{returnPlural(n_year)} and {n_month} month{returnPlural(n_month)} to repay this loan!\nOverpayment = {n_over}")

            print (messageOut)
