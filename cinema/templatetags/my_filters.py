from django import template

register = template.Library()

def seat_number(row):
    if row == 1:
        row = 65
    else:
        row = 64 + row
    return chr(row)


register.filter('name', seat_number)