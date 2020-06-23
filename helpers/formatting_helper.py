"""

Helper functions for the purely graphical aspect

e.g. which styles we might want to give to our tables

"""

from reportlab.platypus import TableStyle
from reportlab.lib.colors import black, white, Color

default_table = TableStyle([
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('TEXTCOLOR', (0, 1), (-1, -1), black),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('BACKGROUND', (0, 0), (-1, 0), Color(70/255, 130/255, 180/255)),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, Color(240/255, 250/255, 250/255)])])

default_header = TableStyle([
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TEXTCOLOR', (0, 0), (-1, -1), black),
    ('BACKGROUND', (0, 0), (-1, -1), Color(255/255, 255/255, 255/255)),
    ('FONTSIZE', (0, 0), (-1, -1), 16),
    ('LEADING', (0, 0), (-1, -1), 16),
    ('LINEBELOW', (0, 0), (-1, -1), 2, Color(0/255, 0/255, 0/255))])

default_page_header = TableStyle([
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TEXTCOLOR', (0, 0), (-1, -1), black),
    ('BACKGROUND', (0, 0), (-1, -1), Color(153/255, 255/255, 204/255)),
    ('FONTSIZE', (0, 0), (-1, -1), 12),
    ('LEADING', (0, 0), (-1, -1), 12)])


dict_of_styles = {'default_table': default_table, 'default_header': default_header,
                  'default_page_header': default_page_header}


def verify_style_label(style_label, dict_styles):
    """

    When we decide to use a certain style, check whether it has been properly defined

    :param style_label:
    :param dict_styles:
    :return:
    """
    if style_label not in dict_styles.keys():
        raise NameError('Style ' + style_label + ' not found in the dictionary of styles')
