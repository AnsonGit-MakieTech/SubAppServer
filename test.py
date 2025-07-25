from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('psemibold', 'fonts/Poppins-SemiBold.ttf'))
pdfmetrics.registerFont(TTFont('plight', 'fonts/Poppins-Light.ttf'))
pdfmetrics.registerFont(TTFont('plightitalic', 'fonts/Poppins-LightItalic.ttf'))


doc = SimpleDocTemplate(
    "sample.pdf",
    pagesize=A4,
    rightMargin=1.5*cm,
    leftMargin=1*cm,
    topMargin=1.5*cm,
    bottomMargin=1.5*cm,
)

elements = []

styles = getSampleStyleSheet()
psemibold_styles = ParagraphStyle(
    name="psemibold",
    parent=styles['Heading1'],
    fontName="psemibold", 
    alignment=TA_LEFT,
)
light_styles = ParagraphStyle(
    name='light',
    parent=styles['Normal'],
    fontName="plight",
    alignment=TA_LEFT,
)
lightitalic_styles = ParagraphStyle(
    name="lightitalic",
    parent=styles["Normal"],
    fontName="plightitalic",
    alignment=TA_LEFT,
)

def overide_styles(style, font_size=12, font_color=colors.HexColor("#242624"), space_after=None, space_before=None, leading=None, alignment=None):
    new_style = ParagraphStyle(
        name=style.name,
        parent=style,
        fontSize=font_size,
        textColor=font_color,
    )
    if space_after:
        new_style.spaceAfter = space_after
    if space_before:
        new_style.spaceBefore = space_before
    if leading:
        new_style.leading = leading
    if alignment:
        new_style.alignment = alignment

    return new_style

logo = Image("justlogo 1.png", height=2*cm, width=2*cm)
company_name = Paragraph(
    "Charles Catv Inc.",
    overide_styles(psemibold_styles, font_size=14)
)
company_location = Paragraph(
    "Osmena Masbate City",
    overide_styles(light_styles, font_size=10)
)

header_text_table = Table(
    [[company_name], [company_location]],
    colWidths=10*cm,
    hAlign='LEFT',
    rowHeights=[0.8*cm, 0.5*cm]
)
header_text_table.setStyle(TableStyle([
    ('VALIGN', (0,0), (0,0), 'BOTTOM'),
    ('VALIGN', (1,0), (1,0), 'TOP'),
]))

header = Table(
    [[logo, header_text_table]],
    colWidths=[2*cm, 10*cm],
    hAlign='LEFT'
)

header.setStyle(TableStyle([
    ('ALIGN', (0,0), (1, 0), 'CENTER'),
    ('VALIGN', (0,0), (0,0), 'MIDDLE'),
    ('VALIGN', (1,0) , (1,0), 'MIDDLE')
]))

elements.append(header)


elements.append(Spacer(1, 1*cm))

generated_title = Paragraph(
    "Generated Report by;",
    overide_styles(psemibold_styles, font_size=10, space_after=0, space_before=0, leading=10),
)
generated_name = Paragraph(
    "&nbsp;&nbsp;&nbsp;&nbsp;John Albert Catamora",
    overide_styles(light_styles, font_size=10, space_after=0, space_before=0.4 * cm, leading=10),
)
elements.append(generated_title)
elements.append(generated_name)
elements.append(Spacer(1, 0.8*cm))

subject_title = Paragraph(
    "Subject to; ",
    overide_styles(psemibold_styles, font_size=10, space_after=0, space_before=0, leading=10)
)
subject_name = Paragraph(
    "&nbsp;&nbsp;&nbsp;&nbsp;All In-Active for Termination Report",
    overide_styles(light_styles, font_size=10, space_after=0, space_before=0.4 *cm, leading=10)
)
subject_date = Paragraph(
    "&nbsp;&nbsp;&nbsp&nbsp;December 1, 2025",
    overide_styles(lightitalic_styles, font_size=8, space_after=0, space_before=0.2*cm, leading=10)
)
elements.append(subject_title)
elements.append(subject_name)
elements.append(subject_date)
elements.append(Spacer(1, 1*cm))

data = [
    [
        Paragraph('Account Number', overide_styles(psemibold_styles, font_size=8, leading=8, space_after=0, space_before=0, alignment=TA_CENTER)), 
        Paragraph('Name', overide_styles(psemibold_styles, font_size=8, leading=8, space_after=0, space_before=0, alignment=TA_CENTER)), 
        Paragraph('Address', overide_styles(psemibold_styles, font_size=8, leading=8, space_after=0, space_before=0, alignment=TA_CENTER)), 
        Paragraph('Stations', overide_styles(psemibold_styles, font_size=8, leading=8, space_after=0, space_before=0, alignment=TA_CENTER)), 
        Paragraph('Plans', overide_styles(psemibold_styles, font_size=8, leading=8, space_after=0, space_before=0, alignment=TA_CENTER))
    ],
    [
        Paragraph('534533242', overide_styles(light_styles, font_size=8, leading=18, space_after=0, space_before=0, alignment=TA_CENTER)), 
        Paragraph('John Catamora', overide_styles(light_styles, font_size=8, leading=18, space_after=0, space_before=0, alignment=TA_CENTER)), 
        Paragraph('Osmena Street Masbate City', overide_styles(light_styles, font_size=8, leading=18, space_after=0, space_before=0, alignment=TA_CENTER)), 
        Paragraph('Masbate', overide_styles(light_styles, font_size=8, leading=18, space_after=0, space_before=0, alignment=TA_CENTER)), 
        Paragraph('Family 160 Plans', overide_styles(light_styles, font_size=8, leading=18, space_after=0, space_before=0, alignment=TA_CENTER))
    ],
    [
        Paragraph('534533242', overide_styles(light_styles, font_size=8, leading=18, space_after=0, space_before=0, alignment=TA_CENTER)), 
        Paragraph('John Catamora', overide_styles(light_styles, font_size=8, leading=18, space_after=0, space_before=0, alignment=TA_CENTER)), 
        Paragraph('Osmena Street Masbate City', overide_styles(light_styles, font_size=8, leading=18, space_after=0, space_before=0, alignment=TA_CENTER)), 
        Paragraph('Masbate', overide_styles(light_styles, font_size=8, leading=18, space_after=0, space_before=0, alignment=TA_CENTER)), 
        Paragraph('Family 160 Plans', overide_styles(light_styles, font_size=8, leading=18, space_after=0, space_before=0, alignment=TA_CENTER))
    ],
    [
        Paragraph('534533242', overide_styles(light_styles, font_size=8, leading=18, space_after=0, space_before=0, alignment=TA_CENTER)), 
        Paragraph('John Catamora', overide_styles(light_styles, font_size=8, leading=18, space_after=0, space_before=0, alignment=TA_CENTER)), 
        Paragraph('Osmena Street Masbate City', overide_styles(light_styles, font_size=8, leading=18, space_after=0, space_before=0, alignment=TA_CENTER)), 
        Paragraph('Masbate', overide_styles(light_styles, font_size=8, leading=18, space_after=0, space_before=0, alignment=TA_CENTER)), 
        Paragraph('Family 160 Plans', overide_styles(light_styles, font_size=8, leading=18, space_after=0, space_before=0, alignment=TA_CENTER))
    ],
    [
        Paragraph('534533242', overide_styles(light_styles, font_size=8, leading=18, space_after=0, space_before=0, alignment=TA_CENTER)), 
        Paragraph('John Catamora', overide_styles(light_styles, font_size=8, leading=18, space_after=0, space_before=0, alignment=TA_CENTER)), 
        Paragraph('Osmena Street Masbate City', overide_styles(light_styles, font_size=8, leading=18, space_after=0, space_before=0, alignment=TA_CENTER)), 
        Paragraph('Masbate', overide_styles(light_styles, font_size=8, leading=18, space_after=0, space_before=0, alignment=TA_CENTER)), 
        Paragraph('Family 160 Plans', overide_styles(light_styles, font_size=8, leading=18, space_after=0, space_before=0, alignment=TA_CENTER))
    ]
]



content_table = Table(
    data,
    colWidths=[3*cm, 4.5*cm, 4.5*cm, 4*cm, 3*cm],
    hAlign='LEFT', 
)

content_table.setStyle(TableStyle([
    ('ALIGN', (0,0) , (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('BACKGROUND', (0,0),(-1,0), colors.HexColor("#D9D9D9")),
    # ('TOPPADDING', (0,1), (-1,1), 9),
    ('TOPPADDING', (0,0), (-1,0), 8),    # more space inside header cells
    ('BOTTOMPADDING', (0,0), (-1,0), 8),
]))
elements.append(content_table)





doc.build(elements)
