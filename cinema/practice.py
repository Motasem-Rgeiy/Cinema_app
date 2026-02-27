from reportlab.pdfgen import canvas
import io

p = canvas.Canvas('hello.pdf')

p.drawString(100 , 100 , 'Hello, i am here')

p.showPage()

p.save()