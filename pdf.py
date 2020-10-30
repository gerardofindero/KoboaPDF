####### PDF


doc = SimpleDocTemplate("Prueba_cluster.pdf",pagesize=A4,
                         rightMargin=2*cm,leftMargin=2*cm,
                         topMargin=2*cm,bottomMargin=2*cm)

doc.build([Paragraph(my_text.replace("\n", "<br />"), getSampleStyleSheet()['Normal']),])
