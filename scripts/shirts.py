from competition.models import Competition, RegistrationQuestion


def run():
    print "Shirt sizes"
    shirts = RegistrationQuestion.objects.get(question__contains="shirt")
    choices = shirts.question_choice_set.all()
    for c in shirts.competition_set.all():
        print "\n", c.name
        for choice in choices:
            rs = shirts.response_set.filter(registration__competition=c,
                                            registration__active=True,
                                            choices=choice)
            print "{}, {}".format(choice.choice, rs.count())
