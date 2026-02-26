from . import models

def ticket_website(request):

    my_tickets = []
    total = 0
    cart = models.Cart.objects.filter(user = request.user.id).last()
    if cart and cart.items:
        ticket_ids = cart.items
        tickets = models.Ticket.objects.filter(pk__in=ticket_ids)
    
        for ticket in tickets:
            total +=ticket.showtime.price
            my_tickets.append(ticket)

    
    return {
        'my_tickets':my_tickets , 
        'total':total , 
        'ticket_counts': len(my_tickets)}
    

#get all ticket ids that i reserved from the cart
#get all showtimes of each ticket

