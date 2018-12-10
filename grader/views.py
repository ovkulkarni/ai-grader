from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from .forms import SubmissionForm

from os.path import join
from subprocess import check_output, STDOUT, CalledProcessError
import tempfile
import traceback

# Create your views here.


@login_required
def upload_view(request):
    submissions = request.user.submission_set.all().order_by('-upload_time')
    if request.method == "POST":
        if ('code' not in request.FILES and
            'code_input' in request.POST and
                len(request.POST['code_input']) > 0):
            tmp = tempfile.NamedTemporaryFile()
            tmp.write(request.POST['code_input'].encode())
            request.FILES['code'] = InMemoryUploadedFile(
                tmp, 'code', 'textInputFile', 'text/x-python-script',
                len(request.POST['code_input']),
                'utf-8')
        form = SubmissionForm(request.POST, request.FILES)
        if not form.is_valid():
            form.fields['code'].required = False
            return render(request, "upload.html", {'form': form,
                                                   'submissions': submissions})
        submission = form.save(commit=False)
        submission.user = request.user
        submission.save()
        try:
            status = check_output("python3 {} {}".format(
                join(settings.GRADER_DIRECTORY,
                     submission.lab.grader_filename),
                submission.code).split(), stderr=STDOUT).decode()
            submission.output = status
        except CalledProcessError as e:
            submission.output = str(e.output)
        except Exception:
            submission.output = traceback.format_exc()
        submission.save()
        return redirect("index")
    form = SubmissionForm()
    form.fields['code'].required = False
    return render(request, "upload.html", {'form': form,
                                           'submissions': submissions})


def login_view(request):
    return render(request, "login.html", {})


def logout_view(request):
    logout(request)
    return redirect("index")
