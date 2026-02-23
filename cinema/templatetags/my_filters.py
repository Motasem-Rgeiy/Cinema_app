from django import template

register = template.Library()

def seat_number(row):
    if row == 1:
        row = 65
    else:
        row = 64 + row
    return chr(row)

@register.simple_tag
def is_exist(reserved_seats , row , column):
    for (row_seat , col_seat) in reserved_seats:
        if row_seat == row and col_seat == column:
            print(row_seat , column)
            return 'occupied'
    return 

def currency(price):
    return '{:.2f}'.format(price) + ' $'


register.filter('name', seat_number)
register.filter('currency' , currency)