from django.shortcuts import get_object_or_404, redirect, render
from main.models import Experience, Project
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from main.forms import ProjectForm

def show_main(request):
    context = {
        "name": "Dave",
        "npm": "2506656601",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Mahasiswa Ilmu Komputer Universitas Indonesia yang tertarik "
            "pada pengembangan kecerdasan artifisial dan keamanan siber."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Dave",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_project(request):
    context = {
        "name": "Dave",  
        "project_list": Project.objects.all(),
    }
    return render(request, "project.html", context)

def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_project")

    context = {
        "name": "Dave",
        "form": form,
    }
    return render(request, "projects_form.html", context)