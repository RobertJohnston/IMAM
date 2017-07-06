import os
import json
from django.core.management.base import BaseCommand
from home.utilities import exception_to_sentry
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from django.core.mail import EmailMessage


PAGE_HEIGHT = defaultPageSize[1]
PAGE_WIDTH = defaultPageSize[0]

from home.views import json_for_charts

class Command(BaseCommand):
    help = 'Generates PDF reports'

    # A command must define handle
    @exception_to_sentry
    def handle(self, *args, **options):

        data = json_for_charts(2017, "National", None, "All")

        adm_chart = {
            "title": {"text": data["title"] + "<br>Admissions and Exits"},
            "subtitle": {
                "text": 'IMAM Nigeria ' + data["date"],
                "align": 'right',
                "verticalAlign": 'bottom',
                "x": -50,
                "y": 10
            },
            "xAxis": [{
                "labels": {
                    "formatter": "REPLACE_ME",
                },
                # highcharts automatically knows the first of 2 # in series is x axis.
                "type": 'datetime',
                "categories": data["categories"],
                "min": 0,
                "max": len(data["categories"]) -1,
                # length -1 is used because the counts are 1 to x and the data are 0 to x
        
                "crosshair": True,
                "title": {
                    "text": 'Week Number'
                },
            }],
             "credits": {
                "enabled": False
            },
            "yAxis": [{ # Primary yAxis
                "labels": {
                    "format": '{value}',
                    # "style": {
                    #    "color": Highcharts.getOptions().colors[1]
                    # }
                },
                "title": {
                    "text": 'Admissions',
                    # "style": {
                    #     color: Highcharts.getOptions().colors[1]
                    # }
                }
            }, { # Secondary yAxis
                "min": 0,
                "max": 100,
                "title": {
                    "text": 'Percentage',
                    # "style": {
                    #     "color": Highcharts.getOptions().colors[1]
                    # }
                },
                "labels": {
                    "format": '{value}',
                    # "style": {
                    #     "color": Highcharts.getOptions().colors[1]
                    # },
                },
                "opposite": True
            }],
            "legend": {
                "layout": 'vertical',
                "align": 'left',
                "x": 80,
                "verticalAlign": 'top',
                "y": 20,
                "floating": True,
                "borderColor": '#ddd',
                "borderRadius": 6,
                "borderWidth": 1,
                # "backgroundColor": (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'
                # Change Highcharts code if the legend overlaps the columns
            },
            "series":[{
                "name":"Admissions",
                "type": 'column',
                "data": data["adm_by_week"],
                "yAxis": 0,
                "color": '#ffcccc',
                "findNearestPointBy": 'x',
                "tooltip": {
                    "valueSuffix": ' cases'
                }
            },  {
                "name": 'Default Rate',
                "type": 'line',
                "yAxis": 1,
                "data": data["defu_rate_by_week"],
                "color": '#000000',
                "marker": { "enabled": True},
                "findNearestPointBy": 'x',
                "tooltip": {
                    "pointFormat": '<span style="color:{point.color}">\u25CF</span> {series.name}: <b>{point.y:,.1f}</b> %<br/>'
                }
            },  {
                "name": 'Transfer Rate',
                "type": 'line',
                "yAxis": 1,
                "data": data["tout_rate_by_week"],
                "dashStyle": 'shortdot',
                "color": '#FFA500',
                "marker": { "enabled": False},
                "findNearestPointBy": 'x',
                "tooltip": {
                    "pointFormat": '<span style="color:{point.color}">\u25CF</span> {series.name}: <b>{point.y:,.1f}</b> %<br/>'
                }
            }, {
                "name": 'Non-recovered Rate',
                "type": 'line',
                "yAxis": 1,
                "data": data["dmed_rate_by_week"],
                "dashStyle": 'dash',
                "color": '#9370DB',
                "marker": { "enabled": False},
                "findNearestPointBy": 'x',
                "tooltip": {
                    "pointFormat": '<span style="color:{point.color}">\u25CF</span> {series.name}: <b>{point.y:,.1f}</b> %<br/>'
                }
            }, {
                "name": 'Death Rate',
                "type": 'line',
                "yAxis": 1,
                "data": data["dead_rate_by_week"],
                "color": '#FF0000',
                "findNearestPointBy": 'x',
                "tooltip": {
                    "pointFormat": '<span style="color:{point.color}">\u25CF</span> {series.name}: <b>{point.y:,.1f}</b> %<br/>'
                }
            }],
            "chart":{"renderTo":"admissions-chart"},
        }

        formatting_function = """function() {
            function ISO8601_week_no(dt) {
                var tdt = new Date(dt.valueOf());
                var dayn = (dt.getDay() + 6) % 7;
                tdt.setDate(tdt.getDate() - dayn + 3);
                var firstThursday = tdt.valueOf();
                tdt.setMonth(0, 1);
                if (tdt.getDay() !== 4) {
                    tdt.setMonth(0, 1 + ((4 - tdt.getDay()) + 7) % 7);
                }
                return 1 + Math.ceil((firstThursday - tdt) / 604800000);
            }
            var a = new Date(0);
            a.setUTCMilliseconds(this.value);
            return a.getFullYear() + ' ' + ISO8601_week_no(a);
        }"""

        # formatting_function = "function() { return 'stuff' }"

        open("adm_chart.json", "w").write(json.dumps(adm_chart, indent=4).replace('"REPLACE_ME"', formatting_function))

        # javascript highcharts export is run in the shell instead as python command
        os.system("highcharts-export-server -infile adm_chart.json -outfile adm_chart.png -width 2000 -type png")

        # Warning: this is a beta version of this website, you can't consider the data here to be final

        def warning(c, doc):  # c is for canvas
            c.saveState()
            x, y = doc.pagesize

            # choose some colors
            c.setStrokeColorRGB(138/255., 0, 0)
            c.setFillColorRGB(1, 0, 0)

            # draw a rectangle
            # c.rect(0, y, x, (y - 200), fill=1)
            c.rect(0, PAGE_HEIGHT - 65, PAGE_WIDTH, 65, fill=1)
            # canvas.rect(x, y, width, height, stroke=1, fill=0)

            # change color
            c.setFillColorRGB(138/255., 0, 0)

            # define a large font
            c.setFont("Helvetica", 22)

            # c.drawString(0.3, 0, "BETA")
            c.drawCentredString(PAGE_WIDTH / 2.0, PAGE_HEIGHT - 30, "Warning: this is a beta version of this website")
            c.drawCentredString(PAGE_WIDTH / 2.0, PAGE_HEIGHT - 52, "You can't consider the data here to be final")

            c.restoreState()

        def myFirstPage(canvas, doc):
            canvas.saveState()

            warning(canvas, doc)

            # write title using absolute position
            canvas.setFont('Times-Bold', 16)
            canvas.drawCentredString(PAGE_WIDTH / 2.0, PAGE_HEIGHT - 108, "IMAM Weekly Report")

            # write page number bellow
            canvas.setFont('Times-Roman', 9)
            canvas.drawString(inch, 0.75 * inch, "First Page / platypus example")

            canvas.restoreState()

        def myLaterPages(canvas, doc):
            canvas.saveState()

            warning(canvas, doc)

            canvas.setFont('Times-Roman', 9)
            canvas.drawString(inch, 0.75 * inch, "Page %d platypus example" % doc.page)

            canvas.restoreState()

        doc = SimpleDocTemplate("phello.pdf")
        story = [Spacer(1, 2 * inch)]

        styles = getSampleStyleSheet()
        style = styles["Normal"]

        # for i in range(100):
        #     bogustext = ("This is Paragraph number %s. " % i) * 20
        #     p = Paragraph(bogustext, style)
        #
        #     story.append(p)
        #     story.append(Spacer(1, 0.2 * inch))

        # 2000 -> 400

        story.append(Image("adm_chart.png", width=400, height=266.6))
        story.append(Image("adm_chart.png", width=400, height=266.6))
        story.append(Image("adm_chart.png", width=400, height=266.6))
        story.append(Image("adm_chart.png", width=400, height=266.6))
        story.append(Image("adm_chart.png", width=400, height=266.6))
        story.append(Image("adm_chart.png", width=400, height=266.6))


        table = [["Site", "Week Number", "RUTF Balance"]]

        for line in data["recent_stock_report"]:
            table.append([
                line["site"],
                "%s / %s"% (line["weeknum"], line["year"]) if line["weeknum"] else "No Data",
                line["balance"],
            ])

        story.append(Table(table))

        # Create a document starting with the list story, then on first page add Title and footer, following pages add footer.
        doc.build(story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)

        # in for loop - Make National, State and LGA level reports
        # after story.build for each report - send to all contacts based at that Site/Level


        email = EmailMessage(
            'this is the subject',
            'Body goes here',
            'imam_nigeria@gmail.com',
            ['assaye']
        )

        # email.attach_file("phello.pdf")
        email.send()