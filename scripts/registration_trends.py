from competition.models import Competition

import collections
import csv
import datetime
import itertools
import json
import StringIO


def daterange(start_date, end_date):
    num_days = int((end_date - start_date).days) + 1
    for n in range(num_days + 1):
        yield start_date + datetime.timedelta(days=n)


def accumulate(registrations):
    dates = [x.signup_date for x in registrations]
    result = collections.OrderedDict()
    for day in daterange(min(dates), max(dates)):
        key = day.strftime("%m-%d-%Y")
        result[key] = registrations.filter(signup_date__lt=day).count()
    return result


def run():
    for competition in Competition.objects.all():
        registrations = competition.registration_set.filter(active=True)

        csv_content = StringIO.StringIO()
        writer = csv.writer(csv_content)

        print "\n", competition.name
        for date, count in accumulate(registrations).iteritems():
            writer.writerow([date, count])

        print csv_content.getvalue()
