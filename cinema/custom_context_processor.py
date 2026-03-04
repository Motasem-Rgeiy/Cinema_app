from . import models

def ticket_website(request):

    my_tickets = []
    total = 0
    cart = models.Cart.objects.filter(user = request.user.id).last()
    if cart and cart.items:
        ticket_ids = cart.items
        tickets = models.Ticket.objects.filter(pk__in=ticket_ids)
        for ticket in tickets:
            if ticket.status == models.TicketStatus.COMPLETED or ticket.status == models.TicketStatus.CANCELLED:
                cart.items.remove(ticket.id)
                cart.save() 
                continue
            total +=ticket.showtime.price
            my_tickets.append(ticket)

    
    return {
        'my_tickets':my_tickets , 
        'total':total , 
        'ticket_counts': len(my_tickets)}
    

#get all ticket ids that i reserved from the cart
#get all showtimes of each ticket

