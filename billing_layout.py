from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from billing_data import data



pdfmetrics.registerFont(TTFont('psemibold', 'fonts/Poppins-SemiBold.ttf'))
pdfmetrics.registerFont(TTFont('pregular', 'fonts/Poppins-Regular.ttf'))
pdfmetrics.registerFont(TTFont('plight', 'fonts/Poppins-Light.ttf'))
pdfmetrics.registerFont(TTFont('plightitalic', 'fonts/Poppins-LightItalic.ttf'))

doc = SimpleDocTemplate(
    "billing-statement.pdf",
    pagesize=A4,
    rightMargin=0*cm,
    leftMargin=0 *cm,
    topMargin=1 *cm,
    bottomMargin=0 *cm
)

elements = []

styles = getSampleStyleSheet()
semibold = ParagraphStyle(
    name='Semibold',
    fontName="psemibold", 
    parent= styles['Heading1']    
)
regular = ParagraphStyle(
    name='Regular',
    fontName="pregular",
    parent=styles['BodyText']
)
light = ParagraphStyle(
    name='Light',
    fontName="plight",
    parent=styles['BodyText']
)
lightitalic = ParagraphStyle(
    name='LightItalic',
    fontName="plightitalic",
    parent=styles['BodyText']
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





company_logo = Image(
    data.get('company_logo', None),
    width=1.8 * cm,
    height=1.8 * cm
)

company_name = Paragraph(
    data.get('company_name', 'Not-Set'),
    style=overide_styles(semibold, font_size=12, space_after=0, space_before=0, leading=12, alignment=TA_LEFT)
)
comapny_address = Paragraph(
    data.get("company_address", "Not Available"),
    style=overide_styles(regular, font_size=8, space_after=0, space_before=0 ,leading=8, alignment=TA_LEFT)
)

company_name_address_table = Table(
    [[company_name], [comapny_address]],
    colWidths= 9 * cm,
    hAlign='LEFT',
)
company_name_address_table.setStyle(TableStyle([
    # ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#D9D9D9")),
]))

company_logo_table = Table(
    [[company_logo, company_name_address_table]],
    colWidths=[1.8 * cm, 9 * cm],
    hAlign='LEFT',
)
company_logo_table.setStyle(TableStyle([
    # ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#C52C2CFF")),
    ('ALIGN', (0,0) , (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
]))

company_logo_table_total_width = (1.8 + 9) * cm

company_semibold_style = overide_styles(semibold, font_size=9, space_after=0, space_before=0, leading=9, alignment=TA_RIGHT)
company_light_style = overide_styles(light, font_size=9, space_after=0, space_before=0, leading=9, alignment=TA_LEFT)

company_phone_title = Paragraph(
    'Phone :',
    style=company_semibold_style
)
company_phonet_content = Paragraph(
    data.get('company_contact', 'Not-Set'),
    style=company_light_style
)
company_mobile_title = Paragraph(
    'Mobile :',
    style=company_semibold_style
)
company_mobile_content = Paragraph(
    data.get('company_contact', 'Not-Set'),
    style=company_light_style
)
company_email_title = Paragraph(
    'Email :',
    style=company_semibold_style
)
company_email_content = Paragraph(
    data.get('company_email', 'Not-Set'),
    style=company_light_style
)
company_tin_title = Paragraph(
    'Tin :',
    style=company_semibold_style
)
company_tin_content = Paragraph(
    data.get('tin_number', 'Not-Set'),
    style=company_light_style
)

company_additional_info_table = Table(
    [
        [company_phone_title, company_phonet_content],
        [company_mobile_title, company_mobile_content],
        [company_email_title, company_email_content],
        [company_tin_title, company_tin_content],
    ],
    colWidths=[1.8 * cm, 5*cm]
)
 
company_additional_info_table.setStyle(TableStyle([
    # ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#2C5AC5FF")),
    ('ALIGN', (0,0) , (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
]))

company_additional_info_table_total_width = (1.8 + 5 ) * cm



company_header_table = Table(
    [[ company_logo_table , company_additional_info_table]],
    colWidths=[company_logo_table_total_width , company_additional_info_table_total_width],
    hAlign='CENTER'
) 
company_header_table.setStyle(TableStyle([
    # ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#2C5AC5FF")),
    ('ALIGN', (0,0) , (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
]))


# Add Header Layout <---------------------------------------
elements.append(company_header_table)

# Add Horizontal Line <---------------------------------------
elements.append(
    HRFlowable(
        width="95%",        # can be a fixed width (like 10*cm) or percentage
        thickness=2,         # thickness in points
        lineCap='round',     # shape of line ends: 'butt', 'round', 'projecting'
        color=colors.black,  # line color
        spaceBefore=5,       # space before the line
        spaceAfter=5,        # space after the line
        hAlign='CENTER',     # alignment: LEFT, CENTER, RIGHT
        vAlign='BOTTOM',     # vertical alignment
        dash=None            # or (3,3) for dashed lines
    )
)



person_bill_info = data.get("statements", [])
person_bill_info = person_bill_info[0] if len(person_bill_info) > 0 else {}

#  Add Bill Info <---------------------------------------
person_light_style = overide_styles(light, font_size=9, leading=9, space_after=0, space_before=0) 
person_bill_to = Paragraph(
    '<font name="psemibold">Bill To: </font> '
    f'<font name="plight">{person_bill_info.get("account_name", "Unknown")}</font>',
    style=person_light_style 
)
person_station = Paragraph(
    '<font name="psemibold">Station: </font> '
    f'<font name="plight">{person_bill_info.get("station", "Unknown")}</font>',
    style=person_light_style
)
person_address = Paragraph(
    f'<font name="plight">{person_bill_info.get("address", "Unknown")}</font>',
    style=person_light_style 
)
person_sub_no = Paragraph(
    '<font name="psemibold">Subscriber\'s ID No:</font> '
    f'<font name="plight">{person_bill_info.get("account_number", "Unknown")}</font>',
    style=person_light_style
)
table_person_bill_to_station = Table(
    [
        [person_bill_to, person_station],
        [person_address, person_sub_no]
    ],
    colWidths=[6.8 * cm, 6.8 * cm],
    hAlign='LEFT'
)

table_person_bill_to_station.setStyle(TableStyle([
    # ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#B12CC5FF")),
    ('ALIGN', (0,0) , (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
]))


 
# Person Billed Table Info <--------------------------------
transactions = person_bill_info.get('transcation_data', [])
transactions_data = []
count = len(transactions)

max_font = 9
min_font = 1
max_leading = 12
min_leading = 2
max_rows_before_scaling = 9 # up to 20 rows, keep max size

if count <= max_rows_before_scaling:
    font_size = max_font
else:
    # scale down proportionally
    scale = max_rows_before_scaling / float(count)
    font_size = max(min_font, max_font * scale)

# leading: scale with font size
leading = max(min_leading, font_size * (max_leading / max_font))

transaction_semibold_style = overide_styles(semibold, font_size=font_size, leading=leading, space_after=1, space_before=1, alignment=TA_CENTER)
transaction_light_style = overide_styles(light, font_size=font_size, leading=leading, space_after=1, space_before=1, alignment=TA_CENTER)

transactions_data.append([
    Paragraph('Date' , style=transaction_semibold_style),
    Paragraph('Description', style=transaction_semibold_style),
    Paragraph('Amount' , style=transaction_semibold_style),
    Paragraph('Wallet', style=transaction_semibold_style),
    Paragraph('Balance', style=transaction_semibold_style),
]) 
transactions_data.append([
    Paragraph('' , style=transaction_semibold_style),
    Paragraph(' Balance from Previous Bill', style=transaction_semibold_style),
    Paragraph('' , style=transaction_semibold_style),
    Paragraph('', style=transaction_semibold_style),
    Paragraph(f'P {person_bill_info.get("previous_balance", "Unknown")}', style=transaction_semibold_style),
]) 
for transaction in transactions:
    transactions_data.append([
        Paragraph(f"{transaction.get('date', '' )}" , style=transaction_light_style),
        Paragraph(f"{transaction.get('transaction', '' )}" , style=transaction_light_style),
        Paragraph(f"P {transaction.get('amount', '' )}" , style=transaction_light_style),
        Paragraph(f"P {transaction.get('wallet', '' )}" , style=transaction_light_style),
        Paragraph(f"P {transaction.get('balance', '' )}" , style=transaction_light_style),
    ])

transaction_data_table = Table(
    transactions_data,
    colWidths = [2.3*cm, 6.1*cm, 1.8*cm, 1.8*cm, 1.9*cm]
)
transaction_data_table.setStyle(TableStyle([
    # ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#B12CC5FF")),
    ('ALIGN', (0,0) , (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('LINEABOVE' , (0 , 0) , ( -1, 0) , 2,  colors.black),
    ('LINEBELOW' , (0 , 0) , ( -1, 0), 2 , colors.black),
    ('LINEBELOW', (0, 1), (-1, -1), 0.5, colors.black),
]))


#  Person Billed Footer Info
person_billed_footer_data = []

person_billed_footer_data.append([
    Paragraph(
        "NOTE: Payments after the bill date will not be reflected here.",
        style=overide_styles(lightitalic, font_size=10, leading=11, space_after=1, space_before=1, alignment=TA_LEFT)
    )
])

person_billed_footer_regular = overide_styles(regular, font_size=10, leading=11)
person_billed_footer_data.append([
    Paragraph(
        '<font name="psemibold">Subscriber\'s ID No:</font> '
        f'{person_bill_info.get("account_number", "Unknown")}',
        style=person_billed_footer_regular
    )
])
person_billed_footer_data.append([
    Paragraph(
        '<font name="psemibold">Due Date:</font> '
        f'{person_bill_info.get("due_date", "Not Available")}',
        style=person_billed_footer_regular
    )
])
person_billed_footer_data.append([
    Paragraph(
        '<font name="psemibold">Total Amount Due::</font> '
        f'P {person_bill_info.get("final_balance", "0.0")}',
        style=person_billed_footer_regular
    )
])

person_billed_footer_table = Table(
    person_billed_footer_data,
    colWidths=[14*cm ],
    hAlign='LEFT'
)
person_billed_footer_table.setStyle(TableStyle([
    # ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#B12CC5FF")),
    ('ALIGN', (0,0) , (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
]))

# Add Bill Info OverAll <---------------------------------------

main_left_content_table = Table(
    [
        [table_person_bill_to_station],
        [transaction_data_table],
        [person_billed_footer_table]
    ],
    colWidths=[14*cm ],
)
main_left_content_table.setStyle(TableStyle([
    # ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#C52C2CFF")),
    ('ALIGN', (0,0) , (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
]))

vertical_add_image = Image(
    data.get("ads_portrait", "None"),
    width=6*cm,
    height=20 * cm
)
main_content_table = Table(
    [[main_left_content_table , vertical_add_image]],
    colWidths=[14.2*cm , 6*cm],
    hAlign='RIGHT'
)
main_content_table.setStyle(TableStyle([
    # ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#2CC5B3FF")),
    ('ALIGN', (0,0) , (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
]))
elements.append(main_content_table)

 

horizonal_add_image = Image(
    data.get("ads_landscape", "None"),
    width=21*cm,
    height=5.3 * cm
)
elements.append(horizonal_add_image)











doc.build(elements)

