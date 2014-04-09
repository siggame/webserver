from competition.models import Competition


def run():
    print "Ineligible Teams"
    for c in Competition.objects.all():
        print "\n", c.name
        for t in c.team_set.filter(eligible_to_win=False):
            print t.name 
