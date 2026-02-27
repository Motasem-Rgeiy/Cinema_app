from io import BytesIO
from django.core.files.base import ContentFile
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from .templatetags.my_filters import seat_number


def ticket_generation_pdf(ticket_obj):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer , pagesize = A4)    
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph('Cinema Ticket' , styles['Title']))
    elements.append(Spacer(1 , 0.5 * inch))
    elements.append(Paragraph(f"Code: {ticket_obj.code}" , styles['Normal']))
    elements.append(Paragraph(f"Username: {ticket_obj.user.username}" , styles['Normal']))
    elements.append(Paragraph(f"Movie: {ticket_obj.showtime.movie}" , styles['Normal']))
    elements.append(Paragraph(f"Location: {ticket_obj.showtime.location.city}" , styles['Normal']))
    elements.append(Paragraph(f"Show date: {ticket_obj.showtime.date}" , styles['Normal']))
    elements.append(Paragraph(f"Show time: {ticket_obj.showtime.start_time}" , styles['Normal']))
    elements.append(Paragraph(f"Seat: {seat_number(ticket_obj.seat[0])}{ticket_obj.seat[1]}" , styles['Normal']))
    

    doc.build(elements)

    pdf_content = buffer.getvalue()
    buffer.close()

    ticket_obj.pdf_file.save(
        f"ticket_{ticket_obj.code}.pdf",
        ContentFile(pdf_content)
    )
    ticket_obj.save()



def convert_to_numeric(show_seats):
     new = []
     for seat in show_seats:
          row = ord(seat[0]) -  65  + 1
          new.append((row , int(seat[1])))
     return new