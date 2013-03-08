from django.core.management.base import BaseCommand
from webserver.codemanagement.models import TeamClient

import os
import re
import tempfile
import subprocess


class Command(BaseCommand):
    help = 'Attempts to update all repositories by pulling from bases'

    def handle(self, *args, **options):

        # A list of tuples: (message, repo_directory, stderr)
        errors = []

        # A list of tuples: (team name, git-show output)
        successes = []

        for client in TeamClient.objects.all():
            directory = tempfile.mkdtemp(prefix='GRETA_UPDATE')
            repo_name = os.path.basename(client.repository.name)
            repo_name = repo_name.replace(".git", "")
            repo_directory = os.path.join(directory, repo_name)

            self.stdout.write("Updating {0}'s repo...\n".format(client.team.name))

            ####################
            # Clone
            ####################
            clone = subprocess.Popen(["git", "clone", client.repository.path],
                                     cwd=directory,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
            clone.wait()

            if clone.returncode != 0:
                errors.append(
                    ("Failed to clone {0}'s repo".format(client.team.name),
                     repo_directory,
                     clone.stdout.read() + clone.stderr.read())
                )
                continue

            ####################
            # Pull
            ####################
            # Use default merge-recursive strategy
            pull = subprocess.Popen(["git", "pull",
                                     client.base.repository.path],
                                    cwd=repo_directory,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            pull.wait()

            if pull.returncode != 0:
                errors.append(
                    ("Failed to pull into {0}'s repo".format(client.team.name),
                     repo_directory,
                     pull.stdout.read() + pull.stderr.read())
                )
                continue

            ####################
            # Push
            ####################
            push = subprocess.Popen(["git", "push"],
                                    cwd=repo_directory,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            push.wait()

            if push.returncode != 0:
                errors.append(
                    ("Failed to push to {0}'s repo".format(client.team.name),
                     repo_directory,
                     push.stdout.read() + push.stderr.read())
                )
                continue

            ####################
            # Show
            ####################
            show = subprocess.Popen(["git", "show"],
                                    cwd=repo_directory,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            show.wait()

            successes.append((client.team.name,
                              show.stdout.read() + show.stderr.read()))

        if successes:
            self.stdout.write("\n\nSuccessfully updated some team repos\n")
        for name, show in successes:
            self.stdout.write("\t - {0}\n".format(name))
            for line in show.splitlines():
                self.stdout.write("\t\t" + line + "\n")

        if errors:
            self.stdout.write("\n\nUnable to update some team repos\n")
        for name, directory, stderr in errors:
            self.stdout.write("\t - {0} ({1})\n".format(name, directory))
            for line in stderr.splitlines():
                self.stdout.write("\t\t" + line + "\n")

        if not errors and not successes:
            self.stdout.write("No team repos to update\n")
