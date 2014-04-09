from competition.models import Competition, RegistrationQuestion


def run():
    print "ACM Members"
    acm = RegistrationQuestion.objects.get(question__contains="ACM")
    yes = acm.question_choice_set.get(choice="Yes")
    for c in acm.competition_set.all():
        print "\n", c.name
        rs = acm.response_set.filter(registration__competition=c,
                                     registration__active=True,
                                     choices=yes)
        for r in rs:
            u = r.registration.user
            print "{}, {}, {}".format(u.email, u.username, u.get_full_name())
