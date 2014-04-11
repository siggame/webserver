from competition.models import (Competition, RegistrationQuestion,
                                RegistrationQuestionResponse)

import csv
import StringIO


def run():
    shirt = RegistrationQuestion.objects.filter(question__contains="shirt")
    for c in Competition.objects.all().order_by('start_time'):
        print c.name
        csv_content = StringIO.StringIO()
        writer = csv.writer(csv_content)
        for r in c.registration_set.filter(active=True).order_by('signup_date'):
            try:
                size = r.response_set.get(question=shirt).choices.get().choice
            except RegistrationQuestionResponse.DoesNotExist:
                size = None
            writer.writerow([r.signup_date,
                             r.user.username,
                             r.user.get_full_name(),
                             r.user.email,
                             size])
        print csv_content.getvalue()
