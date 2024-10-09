from reportlab.pdfgen import canvas

def draw_to_pdf(images : list[str], output_name='output') -> None:
    c = canvas.Canvas(output_name + '.pdf')
    for image in images:
        w, h = c.drawImage(image, 0, 0, width=None, height=None, preserveAspectRatio=True)
        c.setPageSize((w, h))
        c.drawImage(image, 0, 0, width=w, height=h, preserveAspectRatio=True)
        c.showPage()

    c.save()

