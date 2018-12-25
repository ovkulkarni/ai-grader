from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import Http404, JsonResponse, HttpResponse
from django.contrib import messages

from .forms import SubmissionForm
from .models import Submission, Lab
from .tasks import run_code

import tempfile

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
        run_code.delay(submission.pk)
        submissions = request.user.submission_set.all().order_by(
            '-upload_time')
        form.fields['code'].required = False
        messages.success(
            request, "Successfully submitted lab for grading! Please check below for the grader's output.")
        return render(request, "upload.html", {'form': form,
                                               'submissions': submissions,
                                               'inp': request.POST['code_input']
                                               })
    form = SubmissionForm()
    form.fields['code'].required = False
    return render(request, "upload.html", {'form': form,
                                           'submissions': submissions})


@login_required
def get_description_view(request):
    if request.GET.get('id', '').isdigit():
        lab = get_object_or_404(Lab, id=int(request.GET.get('id')))
        return HttpResponse(lab.detailed_description)
    raise Http404


@login_required
def view_submission_output(request, pk):
    submission = get_object_or_404(Submission, pk=pk)
    if submission.user != request.user and not request.user.is_superuser:
        raise Http404
    deets = {'complete': submission.complete, 'output': submission.output}
    return JsonResponse(deets)


def login_view(request):
    return render(request, "login.html", {})


def logout_view(request):
    logout(request)
    return redirect("index")


def about_view(request):
    return render(request, "about.html", {})
