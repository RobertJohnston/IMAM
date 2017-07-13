import os
import json
import numpy as np
from datetime import date, timedelta
from isoweek import Week

from django.core.management.base import BaseCommand
from django.db.models import Q
from home.utilities import exception_to_sentry
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from django.core.mail import EmailMessage

from home.views import json_for_charts
from home.models import Second_admin, Registration, Site, Program, Stock
from home.utilities import iso_year_start, iso_to_gregorian, weeks_for_year


PAGE_HEIGHT = defaultPageSize[1]
PAGE_WIDTH = defaultPageSize[0]


def generate_adm_chart(data):
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
            "max": len(data["categories"]) - 1,
            # length -1 is used because the counts are 1 to x and the data are 0 to x

            "crosshair": True,
            "title": {
                "text": 'Week Number'
            },
        }],
        "credits": {
            "enabled": False
        },
        "yAxis": [{  # Primary yAxis
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
        }, {  # Secondary yAxis
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
        "series": [{
            "name": "Admissions",
            "type": 'column',
            "data": data["adm_by_week"],
            "yAxis": 0,
            "color": '#ffcccc',
            "findNearestPointBy": 'x',
            "tooltip": {
                "valueSuffix": ' cases'
            }
        }, {
            "name": 'Default Rate',
            "type": 'line',
            "yAxis": 1,
            "data": data["defu_rate_by_week"],
            "color": '#000000',
            "marker": {"enabled": True},
            "findNearestPointBy": 'x',
            "tooltip": {
                "pointFormat": '<span style="color:{point.color}">\u25CF</span> {series.name}: <b>{point.y:,.1f}</b> %<br/>'
            }
        }, {
            "name": 'Transfer Rate',
            "type": 'line',
            "yAxis": 1,
            "data": data["tout_rate_by_week"],
            "dashStyle": 'shortdot',
            "color": '#FFA500',
            "marker": {"enabled": False},
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
            "marker": {"enabled": False},
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
        "chart": {"renderTo": "admissions-chart"},
    }

    #FIXME extract function from generate_adm_chart and generate_stock_chart
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

    open("adm_chart.json", "w").write(json.dumps(adm_chart, indent=4).replace('"REPLACE_ME"', formatting_function))

    # javascript highcharts export is run in the shell instead as python command
    os.system("highcharts-export-server -infile adm_chart.json -outfile adm_chart.png -width 2000 -type png > /dev/null")

    return "adm_chart.png"



def generate_stock_chart(data):
    stock_chart = {
        "title": {
            "text": data["title"] + "<br>Stock Balance by Week"
        },
        "subtitle": {
            "text": 'IMAM Nigeria ' + data["date"],
            "align": 'right',
            "verticalAlign": 'bottom',
            "x": -50,
            "y": 10
        },
        "chart": {
            "type": 'column',
            "renderTo": "stock-chart"
        },
        "credits": {
            "enabled": False
        },
        "tooltip": {
             "shared": True,
             "xDateFormat": '%e %b %Y'
        },
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
        },
        "xAxis": [{
            "labels": {
                "formatter": "REPLACE_ME"
            },
            "type": 'datetime',
            "categories": data["categories"],
            "min": 0,
            "max": len(data["categories"]) - 1,
            "crosshair": True,
            "title": {
                "text": 'Week Number'
            },
        }],
        "plotOptions": {
            "column": {
                "dataLabels": {
                    "enabled": True,
                    "useHTML": True,
                    "formatter": "REPLACE_ME2",
                }
            },
        },
        "yAxis": {
            "title": {
                "text": 'Cartons'
            },
        },
        "series": [{
            "name": "RUTF",
            "type": 'column',
            "data": data["stock_by_week"],
            "color": '#72639B',
            "findNearestPointBy": 'x',
            "tooltip": {
                "valueSuffix": ' cartons'
                }
        }, {
            "name": 'Two week margin',
            "type": 'line',
            "data": data["two_weeks_margin"],
            "dashStyle": 'shortdot',
            "color": '#8A9861',
            "marker": {"enabled": False},
            "findNearestPointBy": 'x',
            "tooltip": {
                "pointFormat": '<span style="color:{point.color}">\u25CF</span> {series.name}: <b>{point.y:,.0f}</b>'
                }
        }],
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

    red_splash_function = """function() {
        if (this.y < 1) {
           return '<div><img src="https://image.ibb.co/dbbekv/red_splash_vs.png"></div></div>';
        }
    }"""

    open("stock_chart.json", "w").write(json.dumps(stock_chart, indent=4).replace('"REPLACE_ME"', formatting_function).replace('"REPLACE_ME2"', red_splash_function))

    os.system("highcharts-export-server -infile stock_chart.json -outfile stock_chart.png -width 2000 -type png > /dev/null")

    return "stock_chart.png"




class Command(BaseCommand):
    help = 'Generates PDF reports'

    # A command must define handle
    @exception_to_sentry
    def handle(self, *args, **options):

        # data = json_for_charts(2017, "National", None, "All")

        # generate_adm_chart(data)

        # # Warning: this is a beta version of this website, you can't consider the data here to be final
        #
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
            c.drawCentredString(PAGE_WIDTH / 2.0, PAGE_HEIGHT - 30, "Warning: this is a beta version of this report")
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
            canvas.drawString(inch, 0.75 * inch, "First Page")
            canvas.drawRightString(PAGE_WIDTH - inch, 0.75 * inch, "%s" % data['date'])

            canvas.restoreState()

        def myLaterPages(canvas, doc):
            canvas.saveState()

            warning(canvas, doc)

            canvas.setFont('Times-Roman', 9)
            canvas.drawString(inch, 0.75 * inch, "Page %d " % (doc.page))
            canvas.drawRightString(PAGE_WIDTH - inch, 0.75 * inch, "%s" % data['date'])

            canvas.restoreState()
        #
        # doc = SimpleDocTemplate("phello.pdf")
        # story = [Spacer(1, 2 * inch)]
        #
        # styles = getSampleStyleSheet()
        # style = styles["Normal"]
        #
        # # for i in range(100):
        # #     bogustext = ("This is Paragraph number %s. " % i) * 20
        # #     p = Paragraph(bogustext, style)
        # #
        # #     story.append(p)
        # #     story.append(Spacer(1, 0.2 * inch))
        #
        # # 2000 -> 400
        #
        # story.append(Image("adm_chart.png", width=400, height=266.6))
        # story.append(Image("adm_chart.png", width=400, height=266.6))
        # story.append(Image("adm_chart.png", width=400, height=266.6))
        # story.append(Image("adm_chart.png", width=400, height=266.6))
        # story.append(Image("adm_chart.png", width=400, height=266.6))
        # story.append(Image("adm_chart.png", width=400, height=266.6))
        #
        #
        # table = [["Site", "Week Number", "RUTF Balance"]]
        #
        # for line in data["recent_stock_report"]:
        #     table.append([
        #         line["site"],
        #         "%s / %s"% (line["weeknum"], line["year"]) if line["weeknum"] else "No Data",
        #         line["balance"],
        #     ])
        #
        # story.append(Table(table))
        #
        # # Create a document starting with the list story, then on first page add Title and footer, following pages add footer.
        # doc.build(story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
        #
        # # in for loop - Make National, State and LGA level reports
        # # after story.build for each report - send to all contacts based at that Site/Level
        #
        #
        # email = EmailMessage(
        #     'this is the subject',
        #     'Body goes here',
        #     'imamnigeria@gmail.com',
        #     ['assaye']
        # )
        #
        # # email.attach_file("phello.pdf")
        # email.send()

        if not os.path.exists("sent_reports"):
            os.makedirs("sent_reports")

        for second_admin in Second_admin.objects.filter(Q(site__sc=True) | Q(site__otp=True)):
            pdf_file_name = "sent_reports/%s-%s.pdf" % (second_admin.lga.replace("/", "-").encode("utf-8"), second_admin.lga_num)
            doc = SimpleDocTemplate(pdf_file_name)

            # add date

            styles = getSampleStyleSheet()
            style = styles["Normal"]

            print("Generating report %s-%s.pdf" % (second_admin.lga.replace("/", "-").encode("utf-8"), second_admin.lga_num))

            # XXX change 2017 to current year
            data = json_for_charts(2017, "lga", str(second_admin.lga_num), "All")

            story = [Spacer(1, 2 * inch)]

            # story.append(Paragraph("Active sites: %s   Inactive sites: %s" % (data["number_of_active_sites"], data["number_of_inactive_sites"]), style))
            story.append(Spacer(1, 0.2 * inch))

            # chart_file_name = generate_adm_chart(data)
            # story.append(Image(chart_file_name, width=400, height=266.6))
            story.append(Spacer(1, 0.2 * inch))

            # story.append(Paragraph("Program report rate: %s %%" % data["program_report_rate"], style))
            story.append(Spacer(1, 0.2 * inch))

            story.append(Paragraph("Stock Reports", style))
            story.append(Spacer(1, 0.2 * inch))

            # chart_file_name = generate_stock_chart(data)
            # story.append(Image(chart_file_name, width=400, height=266.6))
            story.append(Spacer(1, 0.2 * inch))

            # story.append(Paragraph("Stock report rate: %s %%" % data["stock_report_rate"], style))
            story.append(Spacer(1, 0.2 * inch))

            #story.append(Paragraph("Recent Stock Reports", style))
            story.append(Spacer(1, 0.2 * inch))

            # table is list of lists with these column titles
            table = [["Site", "Week Number", "RUTF Balance"]]
            #
            # for line in data["recent_stock_report"]:
            #     table.append([
            #         line["site"],
            #         "%s / %s"% (line["weeknum"], line["year"]) if line["weeknum"] else "No Data",
            #         line["balance"],
            #     ])

            story.append(Table(table))

            variables_to_tests = [
                ["Program", [("amar", "Admissions"), ("beg", "Begigigi"), ("dcur", "Curred people"), ("dead", "Dead")]],
                ["Stock", [("rutf_out", "Consumed cartons"), ("rutf_in", "Received cartons"), ("rutf_bal", "Balance of cartons")]],
            ]

            # duplicate from views.py
            today_year, today_week, _ = date.today().isocalendar()
            _8_weeks_ago = Week(today_year, today_week) - 8
            year_start = iso_year_start(_8_weeks_ago.year)
            _8_weeks_ago = year_start + timedelta(days=0, weeks=_8_weeks_ago.week - 1)

            # PRESENT ACTIONABLE INFORMATION
            # loop over sites in LGA
            # present data errors by site
            for site in Site.objects.filter(Q(sc=True) | Q(otp=True)).filter(lga_num=second_admin.lga_num,\
                                                                             latest_communication_datetime__gte=_8_weeks_ago):
                site_types = []
                if site.otp:
                    site_types.append("OTP")
                if site.sc:
                    site_types.append("SC")

                print "Site: %s (%s) " % (site.sitename.strip(), ", ".join(site_types))
                story.append(Paragraph("Site: %s (%s)" % (site.sitename.strip(), ", ".join(site_types)), style))
                problem = False


                for model, variables in variables_to_tests:
                    for site_type in site_types:
                        for variable, variable_name in variables:
                            print model, variable
                            medians, values = outliers(site.siteid, variable, kind=model, site_type=site_type)

                            if not medians:
                                continue

                            for median, value in zip(medians, values):
                                # print median
                                if median and value > adm_cutoff(float(median)):
                                    problem = True
                                    # print("%s ERROR (%s) \t\t median=%s, value=%s, cut=%s" % (variable_name, site_type, median, value, int(adm_cutoff(float(median)))))
                                    story.append(Paragraph("%s ERROR (%s) \t median=%s, value=%s, cut=%s" % (
                                        variable_name, site_type, median, value, int(adm_cutoff(float(median)))), style))

                if problem:
                    for contact in Registration.objects.filter(siteid=site.siteid):
                        story.append(Paragraph("%s (%s) - Phone number %s" % (contact.name, contact.post, contact.urn), style))

                    story.append(Spacer(1, 0.2 * inch))
                else:
                    print "No issues identified - Congrats"
                    story.append(Paragraph("No issues identified - Congrats", style))
                    story.append(Spacer(1, 0.2 * inch))


            doc.build(story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)

            # emails = set()
            # for contact in Registration.objects.filter(mail__isnull=False).filter(lga_num=second_admin.lga_num):
            #     emails.add(contact.mail)

            # for mail in emails:
            #     email = EmailMessage(
            #         'this is the subject',
            #         'Body goes here',
            #         'imamnigeria@gmail.com',
            #         [mail]
            #     )
            #
            #     email.attach_file(pdf_file_name)
            #     email.send()

            # To send email only to IMAM Admin email account
            email = EmailMessage(
                'this is the subject',
                'Body goes here',
                'imamnigeria@gmail.com',  # Email is from
                ['imamnigeria@gmail.com'] # Email is sent to: email addresses must be in list
                #['imamnigeria@gmail.com', 'robertfjohnston@gmail.com']
            )

            email.attach_file(pdf_file_name)
            # email.send()

            # FIXME remove break to continue loop
            # break


def outliers(siteid, var, site_type, kind="Program"):
    since_x_weeks = {}

    year, weeknum, _ = date.today().isocalendar()
    current_week = Week(year, weeknum)

    if kind == "Program":
        model = Program
    elif kind == "Stock":
        model = Stock
    else:
        raise Exception("Unsupported kind, supported kinds are 'Stock' or 'Program'")

    for i in model.objects.filter(siteid=siteid, type=site_type).order_by('year', 'weeknum'):
        weeks_since_today = current_week - Week(i.year, i.weeknum)
        since_x_weeks[weeks_since_today] = i

    medians_list = []

    for j in sorted(since_x_weeks.keys()):
        # Median centred on current week with 3 weeks from past and 4 from future.  More responsive to change.
        lower, upper = j - 3, j + 4

        values_to_medianize = []

        window = range(lower, upper + 1)
        for item in window:  # include +1 because range is from start up to not including end.
            if item in since_x_weeks and getattr(since_x_weeks[item], var) is not None:
                values_to_medianize.append(getattr(since_x_weeks[item], var))

        if getattr(since_x_weeks[j], var) is None:
            continue

        medians_list.append((
            max(since_x_weeks.keys()) - j,  # the index for the x-axis graph but inverted to be chronological order
            np.median(values_to_medianize),  # the median
            getattr(since_x_weeks[j], var),  # the value named in var ("amar" for example)
        ))

    if not medians_list:
        return False, False

    weeks, medians, var_values = zip(
        *list(reversed(medians_list)))  # zip(* ) allows the lists to be translated to format

    if np.median(medians) == 0:
        return None, None

    # diff = map(lambda x: int(100 * (abs(x[0] - x[1]) / np.median(medians))), zip(medians, var_values))

    return medians, var_values # list of medians and list of values of input variable.


def adm_cutoff(x):
    result = float((49.594 * x ** -0.674) * x)

    if result < x + 25:  # this happens at 150
        result = x + 25

    # median of admissions is <40.  only 6 sites have median between 50 and 80.
    return result

