"""

Helper for the formatting section of the report

Simplifies PDF generation with ReportLab

"""
from abc import ABC, abstractmethod
import pandas as pd
from copy import deepcopy

from reportlab.platypus import Table
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4

from helpers.formatting_helper import dict_of_styles, verify_style_label


class Element(ABC):
    @abstractmethod
    def __init__(self):
        self.drawable = None

    def get_element(self):
        return self.drawable

    def get_width(self):
        return self.drawable.warp(0, 0)[0]

    def get_height(self):
        return self.drawable.warp(0, 0)[1]


class LineSkip(Element):

    def __init__(self, separator=1*mm):
        super().__init__()
        self.drawable = Spacer(height=separator, width=1*mm)


class PageBreaker(Element):

    def __init__(self):
        super().__init__()
        self.drawable = PageBreak()


class DataTable(Element):

    def __init__(self, dataframe: pd.DataFrame, colwidths=None, rowheights=None, halign='LEFT', valign='MIDDLE',
                 style_label='default_table', style=None):
        super().__init__()
        self.dataframe = dataframe
        self.drawable = Table(self.init_data_table(), colWidths=colwidths, rowHeights=rowheights, hAlign=halign,
                              vAlign=valign)
        self.style = style
        self.style_label = style_label
        self.init_table_style()

    def init_data_table(self):
        """

        Attach back the header part of the table and convert the dataframe to a list of lists

        :return:
        """

        table_header = self.dataframe.columns.tolist()
        table_data = self.dataframe.values.tolist()

        return [table_header] + table_data

    def init_table_style(self):
        """

        Set the style of the Table to the desired value

        :return:
        """
        verify_style_label(self.style_label, dict_of_styles)
        self.style = deepcopy(dict_of_styles[self.style_label])
        self.drawable.setStyle(self.style)

    def set_column_format(self, col_name, format_style):
        """

        Assign the desired column format

        :param col_name:
        :param format_style:
        :return:
        """

        num_col = self.dataframe.columns.tolist().index(col_name)

        for row in self.drawable._cellvalues[1:]:
            row[num_col] = format_style.format(row[num_col])

    def set_columns_format(self, col_names, format_style):
        """

        Format multiple columns at the same time

        :param col_names:
        :param format_style:
        :return:
        """

        for col_name in col_names:
            self.set_column_format(col_name, format_style)


class Header(Element):

    def __init__(self, text, header_style_label='default_header', header_style=None, header_width=None,
                 halign='CENTER', valign='MIDDLE'):
        super().__init__()
        self.text = text
        self.style_label = header_style_label
        self.style = header_style
        self.header_width = header_width
        self.drawable = Table(data=[[text]], colWidths=self.compute_header_width(), hAlign=halign, vAlign=valign)
        self.init_header_style()

    def compute_header_width(self):
        """

        Get the desired header width. Go to full page is none is specified

        :return:
        """

        if self.header_width is not None:
            if self.header_width == 'full_page':
                return A4[0]
            else:
                return self.header_width
        else:
            return None

    def init_header_style(self):
        """

        Initialize the header style

        :return:
        """

        if self.style is None:
            verify_style_label(self.style_label, dict_of_styles)
            self.style = deepcopy(dict_of_styles[self.style_label])

        self.drawable.setStyle(self.style)


class FullPageHeader(Header):

    def __init__(self, text, header_style_label='default_page_header', header_style=None, header_width='full_page',
                 halign='LEFT', valign='MIDDLE'):

        super().__init__(text, header_style_label=header_style_label, header_style=header_style,
                         header_width=header_width, halign=halign, valign=valign)


class Document(SimpleDocTemplate):
    def __init__(self, pdf_to_create, leftmargin=0, rightmargin=0, topmargin=0, bottommargin=0):
        super().__init__(filename=pdf_to_create, leftMargin=leftmargin, rightMargin=rightmargin, topMargin=topmargin,
                         bottomMargin=bottommargin)
        self.elements = []

    def add_element(self, element: Element):
        self.elements.append(element.drawable)

    def build_document(self):
        self.build(self.elements)
