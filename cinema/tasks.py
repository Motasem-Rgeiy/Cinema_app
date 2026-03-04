from django.utils import timezone
from .models import Showtime , Movie , ShowtimeStatus , TicketStatus , Cart
from datetime import datetime

def showtime_processing():

    showtimes = Showtime.objects.all()
    for showtime in showtimes:

                start_datetime = datetime.fromisoformat(f"{str(showtime.date)} {str(showtime.start_time)}")
                end_time = start_datetime + showtime.movie.run_time
                current_datetime = datetime.today()
                print(end_time , showtime)
                if current_datetime >= end_time and showtime.status == ShowtimeStatus.RUNNING:
                      showtime.status = ShowtimeStatus.FINISHED
                      for ticket in showtime.ticket_set.all():
                              ticket.status = TicketStatus.COMPLETED
                              ticket.save()
                            
                      showtime.save()
                      print('Yes')
                      continue
                if current_datetime >= start_datetime and showtime.status == ShowtimeStatus.OPEN:
                        showtime.status = ShowtimeStatus.RUNNING
                        showtime.save()
                       
                    
                
    return "Success to update status of the showtime" 
                    