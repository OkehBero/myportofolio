from django.shortcuts import render

from main.models import Experience


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