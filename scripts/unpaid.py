from competition.models import Competition


def run():
    print "Unpaid Teams"
    for c in Competition.objects.filter(cost__gt=0):
        print "\n", c.name
        for t in c.team_set.filter(paid=False):
            print t.name
            for member in t.members.all():
                print "\t" + member.username
