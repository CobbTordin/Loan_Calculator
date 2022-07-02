import argparse
import math

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Computes differentiated or non-differentiated loan information.')
    parser.add_argument('--type', type=str, choices=['diff', 'annuity'], required=True,
                        help='Chooses either differential or annuity loan calculations.')
    parser.add_argument('-p', '--principal', type=int, help='Loan principal amount')
    parser.add_argument('-n', '--periods', type=int, help='Total number of monthly payments')
    parser.add_argument('-a', '--payment', type=float, help='Monthly annuity payment amount')
    parser.add_argument('-i', '--interest', type=float, required=True, help='Loan interest rate')

    
# i = interest rate input as an integer then converted to a float for calculation
# n = number of separate loan payments
# a = value of each payment (only used for 'type=annuity')
# p = loan principal
    

def i_calc(x):
    return x / 100 / 12


def diff_calc(p, n, i):
    payment_list = []
    total = 0
    for m in range(n, 0, -1):
        current_payment = math.ceil((p / n) + (i_calc(i) * (p - (p * (m - 1) / n))))
        payment_list.append(current_payment)
        total = total + current_payment
        overpayment = total - p
    rev_loan = payment_list[::-1]
    for payment in rev_loan:
        month_num = rev_loan.index(payment) + 1
        print(f'Month {month_num}: payment is {payment}')
    print(f'\nOverpayment = {overpayment}')


def n_calc(p, a, i):
    n_periods = math.log((a / (a - i_calc(i) * p)), (1 + i_calc(i)))
    n_overpayment = int((math.ceil(n_periods) * a) - p)
    return n_periods, n_overpayment


def a_calc(p, n, i):
    a_payment = p * (i_calc(i) * (1 + i_calc(i)) ** n) / ((1 + i_calc(i)) ** n - 1)
    a_overpayment = (math.ceil(a_payment) * n) - p
    return a_payment, a_overpayment, p


def p_calc(a, n, i):
    p_principal = a / ((i_calc(i) * (1 + i_calc(i)) ** n) / ((1 + i_calc(i)) ** n - 1))
    p_total = (a * n)
    p_overpayment = p_total - p_principal
    return p_principal, p_overpayment


args = parser.parse_args()


if args.type == 'diff':
    diff_calc(args.principal, args.periods, args.interest)
if args.type == 'annuity':
    if args.principal is None:
        p_tup = p_calc(args.payment, args.periods, args.interest)
        p_output = math.floor(p_tup[0])
        p_over = math.ceil(p_tup[1])
        print(f"Your loan principal = {p_output}!\nOverpayment = {p_over}")
    if args.payment is None:
        a_tup = a_calc(args.principal, args.periods, args.interest)
        a_output = math.ceil(a_tup[0])
        a_over = a_tup[1]
        print(f"Your annuity payment = {a_output}!\nOverpayment = {a_over}")
    if args.periods is None:
        n_tup = n_calc(args.principal, args.payment, args.interest)
        n_output = n_tup[0]
        n_over = n_tup[1]
        n_year = math.floor(math.ceil(n_output / 12))
        n_month = math.ceil(n_output % 12) % 12
        if n_year == 0:
            if n_month == 0:
                print("This loan will be repaid instantly!")
            if n_month == 1:
                print(f"It will take {n_month} month to repay this loan!\nOverpayment = {n_over}")
            if n_month > 1:
                print(f"It will take {n_month} months to repay this loan!\nOverpayment = {n_over}")
        if n_year == 1:
            if n_month == 0:
                print(f"It will take {n_year} year to repay this loan!\nOverpayment = {n_over}")
            if n_month == 1:
                print(f"It will take {n_year} year and {n_month} month to repay this loan!\nOverpayment = {n_over}")
            if n_month > 1:
                print(f"It will take {n_year} year and {n_month} months to repay this loan!\nOverpayment = {n_over}")
        if n_year > 1:
            if n_month == 0:
                print(f"It will take {n_year} years to repay this loan!\nOverpayment = {n_over}")
            if n_month == 1:
                print(f"It will take {n_year} years and {n_month} month to repay this loan!\nOverpayment = {n_over}")
            if n_month > 1:
                print(f"It will take {n_year} years and {n_month} months to repay this loan!\nOverpayment = {n_over}")
