from django.conf import settings

from celery import shared_task
from os.path import join
from subprocess import Popen, STDOUT, CalledProcessError, PIPE

from .models import Submission

import traceback


@shared_task
def run_code(sub_pk):
    submission = Submission.objects.get(pk=sub_pk)
    try:
        with Popen("python3 -u {} {}".format(
                join(settings.GRADER_DIRECTORY,
                     submission.lab.grader_filename),
                submission.code).split(), stdout=PIPE, stderr=STDOUT,
                cwd=settings.GRADER_DIRECTORY) as proc:
            for line in proc.stdout:
                if line.decode() == "\n":
                    continue
                submission.output += line.decode()
                submission.save()
        if proc.returncode != 0:
            raise CalledProcessError(
                proc.returncode, proc.args,
                output=proc.stdout,
                stderr=proc.stderr)
    except CalledProcessError as e:
        submission.output = e.output.read().decode()
    except Exception:
        submission.output = traceback.format_exc()
    submission.complete = True
    submission.save()
    return True
