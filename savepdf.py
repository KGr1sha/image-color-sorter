# testing writing to pdf
from reportlab.pdfgen import canvas

PAGE_SIZE = (700, 1200)

def draw_to_pdf(images : list[str]) -> None:
    c = canvas.Canvas('output.pdf')
    for image in images:
        w, h = c.drawImage(image, 0, 0, width=None, height=None, preserveAspectRatio=True)
        c.setPageSize((w, h))
        c.drawImage(image, 0, 0, width=w, height=h, preserveAspectRatio=True)
        c.showPage()

    c.save()

if __name__ == '__main__':
    draw_to_pdf(['images/1.jpg',
                 'images/2.jpg',
                 'images/3.jpg'])
