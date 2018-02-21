
from django.conf import settings

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Spacer
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from django.contrib.staticfiles.finders import find

from pec.models import Domaine

LOGO_EPC = find('img/logo_EPC.png')
LOGO_ESNE = find('img/logo_ESNE.png')

class PlanFormationPdf(SimpleDocTemplate):

    def __init__(self, filename):
        self.flowable = list()
        MyDocTemplateES.__init__(self, filename, 'Formation ASE', 'Plan de formation', portrait=False)

    def produce(self, filiere):
        table_style = []
        data = [['Domaine', 'Année1', 'Année 2', 'Année 3']]

        if filiere == 'FE':
            domaines = Domaine.objects.exclude(abrev='CIE')
            for row, d in enumerate(domaines):
                c1 = '\n'.join('{0} ({1} pér.)'.format(x.nom, x.periode) for x in d.cours_fe_annee_1())
                c2 = '\n'.join('{0} ({1} pér.)'.format(x.nom, x.periode) for x in d.cours_fe_annee_2())
                c3 = '\n'.join('{0} ({1} pér.)'.format(x.nom, x.periode) for x in d.cours_fe_annee_3())
                data.append([d.nom, c1, c2, c3])
                color = '{0}'.format(d.couleur[:7])
                table_style.append(('BACKGROUND', (0, row + 1), (3, row + 1), HexColor(color)), )
        else:
            domaines = Domaine.objects.all().exclude(abrev='ECG').exclude(abrev='EPH')
            for row, d in enumerate(domaines):
                c1 = '\n'.join('{0} ({1} pér.)'.format(x.nom, x.periode) for x in d.cours_mp_annee_1())
                c2 = '\n'.join('{0} ({1} pér.)'.format(x.nom, x.periode) for x in d.cours_mp_annee_2())
                c3 = '\n'.join('{0} ({1} pér.)'.format(x.nom, x.periode) for x in d.cours_mp_annee_3())
                data.append([d.nom, c1, c2, c3])
                color = '{0}'.format(d.couleur[:7])
                table_style.append(('BACKGROUND', (0, row + 1), (3, row + 1), HexColor(color)), )

        t = Table(data, colWidths=[6.5 * cm, 6.5 * cm, 6.5 * cm, 6.5 * cm], spaceBefore=0.5 * cm, spaceAfter=1 * cm)
        table_style.extend(
            [
                ('SIZE', (0, 0), (-1, -1), 7),
                ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
            ]
        )
        t.setStyle(TableStyle(table_style))
        self.flowable.append(t)
        self.build(self.flowable)


class MyDocTemplate(SimpleDocTemplate):
    
    def __init__(self, filename, title_left, title_right, portrait=True):
        if portrait is True:
            page_size = A4
            column_width = 8*cm
        else:
            page_size = landscape(A4)
            column_width = 13*cm
        SimpleDocTemplate.__init__(self, filename, pagesize=page_size,
                                   topMargin=0*cm,
                                   leftMargin=2 * cm,
                                   rightMargin=2 * cm,
                                   bottomMargin=0.5 * cm,
                                   )
        self.fileName = filename
        im1 = Image(settings.MEDIA_ROOT + 'logo_EPC.png', width=170, height=80, hAlign=TA_LEFT)
        data = list()
        data.append([im1, ''])
        data.append([Spacer(0, 0.5*cm)])

        data.append([title_left, title_right])
        t = Table(data, colWidths=[column_width]*2, hAlign=TA_LEFT)
        t.setStyle(
            TableStyle(
                [
                    ('SIZE', (0, 0), (-1, -1), 9),
                    ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                    ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
                    ('LINEABOVE', (0, 0), (-1, -1), 0.5, colors.black),
                    ('LINEBELOW', (0, -1), (-1, -1), 0.5, colors.black),
                ]
            )
        )
        self.flowable.append(t)

    def beforePage(self):
        # page number
        self.canv.saveState()
        self.canv.setFontSize(8)
        self.canv.drawCentredString(self.pagesize[0]/2, 2.5*cm, "Page : " + str(self.canv.getPageNumber()))
        self.canv.restoreState()


class MyDocTemplateES(SimpleDocTemplate):
    def __init__(self, filename, title_left, title_right, portrait=True):
        if portrait is True:
            page_size = A4
            column_width = 8 * cm
        else:
            page_size = landscape(A4)
            column_width = 13 * cm
        SimpleDocTemplate.__init__(self, filename, pagesize=page_size,
                                   topMargin=0 * cm,
                                   leftMargin=2 * cm,
                                   rightMargin=2 * cm,
                                   bottomMargin=0.5 * cm,
                                   )
        self.fileName = filename
        im1 = Image(LOGO_EPC, width=170, height=80)
        im2 = Image(LOGO_ESNE, width=170, height=80)
        data = list()
        data.append([im1, im2])
        data.append([Spacer(0, 0.5 * cm)])
        data.append([title_left, title_right])
        t = Table(data, colWidths=[column_width] * 2, hAlign=TA_LEFT)
        t.setStyle(
            TableStyle(
                [
                    ('SIZE', (0, 0), (-1, -1), 9),
                    ('FONT', (0, 0), (-1, -1), 'Helvetica-Bold'),
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                    ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
                    ('LINEABOVE', (0, 2), (-1, 2), 0.5, colors.black),
                    ('LINEBELOW', (0, -1), (-1, -1), 0.5, colors.black),
                ]
            )
        )
        self.flowable.append(t)

    def beforePage(self):
        # page number
        self.canv.saveState()
        self.canv.setFontSize(8)
        self.canv.drawCentredString(self.pagesize[0] / 2, 2.5 * cm, "Page : " + str(self.canv.getPageNumber()))
        self.canv.restoreState()
