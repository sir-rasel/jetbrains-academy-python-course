import math
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--type', help='type of payment')
parser.add_argument('--principal', help='principal amount', type=float)
parser.add_argument('--periods', help='number of months needed to repay the credit.', type=int)
parser.add_argument('--interest', help='nominal interest - specified without a percent sign.', type=float)
parser.add_argument('--payment', help='monthly payment', type=float)

args = parser.parse_args()

# argument assignment
type = args.type
principal = args.principal
periods = args.periods
interest = args.interest
payment = args.payment

if not type or (type == 'diff' and payment) or not interest:
    print('Incorrect parameters')
    exit()

def cal_count_of_periods(credit_principal, monthly_payment, nominal_interest):
    x = monthly_payment / (monthly_payment - nominal_interest * credit_principal)
    base = 1 + nominal_interest
    return math.log(x, base)

def cal_annuity_monthly_payment(credit_principal, count_of_periods, nominal_interest):
    return credit_principal * ((nominal_interest * (1 + nominal_interest) ** count_of_periods) / ((1 + nominal_interest) ** count_of_periods -1))

def cal_credit_principal(monthly_payment, nominal_interest, count_of_periods):
    return monthly_payment / ( (nominal_interest * (1 + nominal_interest) ** count_of_periods) / ((1 + nominal_interest) ** count_of_periods - 1) )

def prep_no_months_string(no_months):
    actual_years = math.ceil(no_months // 12)
    actual_months = math.ceil(no_months % 12)
    year_prep = 'year'
    month_prep = 'month'

    if actual_months == 12:
        actual_years += 1
        actual_months = 0
    if actual_years > 1:
        year_prep = 'years'
    if actual_months > 1:
        month_prep = 'months'

    if actual_years == 0:
        return 'You need {} {} to repay this credit!'.format(actual_months, month_prep)
    elif actual_years >= 1 and actual_months == 0:
        return 'You need {} {} to repay this credit!'.format(actual_years, year_prep)
    else:
        return 'You need {} years and {} months to repay this credit!'.format(actual_years, actual_months)

def cal_annuity_overpayment(annuity_payment, periods, principal):
    overpayment = (annuity_payment * periods) - principal
    return 'Overpayment = {}'.format(math.ceil(overpayment))

def cal_diff_payment_per_month(principal, periods, nominal_interest, month):
    return principal/ periods + nominal_interest * (principal -  (principal * (month - 1)) / periods )

def cal_diff_overpayment(overall_diff_month_payment, principal):
    overpayment = overall_diff_month_payment - principal
    return 'Overpayment = {}'.format(math.ceil(overpayment))

nominal_interest = (interest / 100) * 1 / 12

if type == 'annuity':
    if principal and payment:
        no_months = cal_count_of_periods(principal, payment, nominal_interest)
        periods = math.ceil(no_months)
        print('No of months- ', no_months)
        print(prep_no_months_string(no_months))
        print(cal_annuity_overpayment(payment, periods, principal))

    elif principal and periods:
        annuity_payment = math.ceil(cal_annuity_monthly_payment(principal, periods, nominal_interest))
        print('Your annuity payment = {}!'.format(annuity_payment))
        print(cal_annuity_overpayment(annuity_payment, periods, principal))

    elif payment and periods: # p
        credit_principal = math.floor(cal_credit_principal(payment, nominal_interest, periods))
        print('Your credit principal = {}!'.format(credit_principal))
        print(cal_annuity_overpayment(payment, periods, credit_principal))

elif type == 'diff':
    overall_diff_month_payment = 0
    for each_month in range(1, periods + 1):
        diff_month_payment = math.ceil(cal_diff_payment_per_month(principal, periods, nominal_interest, each_month))
        overall_diff_month_payment += diff_month_payment
        print('Month {}: paid out {}'.format(each_month, diff_month_payment))
    print()
    print(cal_diff_overpayment(overall_diff_month_payment, principal))