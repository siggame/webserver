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
            self.stdout.write("\tCloning...\n")
            clone = subprocess.Popen(["git", "clone", client.repository.path],
                                     cwd=directory,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
            out, err = clone.communicate()

            if clone.returncode != 0:
                errors.append(
                    ("Failed to clone {0}'s repo".format(client.team.name),
                     repo_directory,
                     out + err)
                )
                continue

            ####################
            # Pull
            ####################
            self.stdout.write("\tPulling...\n")
            # Use default merge-recursive strategy
            pull = subprocess.Popen(["git", "pull",
                                     client.base.repository.path],
                                    cwd=repo_directory,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            out, err = pull.communicate()

            if pull.returncode != 0:
                errors.append(
                    ("Failed to pull into {0}'s repo".format(client.team.name),
                     repo_directory,
                     out + err)
                )
                continue

            ####################
            # Push
            ####################
            self.stdout.write("\tPushing...\n")
            push = subprocess.Popen(["git", "push"],
                                    cwd=repo_directory,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            out, err = push.communicate()

            if push.returncode != 0:
                errors.append(
                    ("Failed to push to {0}'s repo".format(client.team.name),
                     repo_directory,
                     out + err)
                )
                continue

            ####################
            # Show
            ####################
            self.stdout.write("\tGetting show...\n")
            show = subprocess.Popen(["git", "show"],
                                    cwd=repo_directory,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            out, err = show.communicate()

            successes.append((client.team.name, out + err))

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
