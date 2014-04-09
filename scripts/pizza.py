from competition.models import Competition, RegistrationQuestion


def run():
    print "Pizza Preferences"
    pizza = RegistrationQuestion.objects.get(question__contains="pizza")
    choices = pizza.question_choice_set.all()
    for c in pizza.competition_set.all():
        print "\n", c.name
        for choice in choices:
            rs = pizza.response_set.filter(registration__competition=c,
                                           registration__active=True,
                                           choices=choice)
            print "{}, {}".format(choice.choice, rs.count())
