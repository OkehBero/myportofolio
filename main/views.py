from django.shortcuts import get_object_or_404, redirect, render
from main.models import Experience, Project
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from main.forms import ProjectForm, ExperienceForm

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

def get_experience_json(request):
    """Mengembalikan data seluruh pengalaman dalam format JSON."""
    experiences = Experience.objects.all()
    data = serializers.serialize("json", experiences)
    return HttpResponse(data, content_type="application/json")

def show_experience(request):
    """Menampilkan daftar pengalaman setelah mengambil JSON dan melakukan deserialisasi."""
    json_response = get_experience_json(request)
    deserialized_data = serializers.deserialize("json", json_response.content.decode("utf-8"))
    experience_list = [item.object for item in deserialized_data]
    
    context = {
        "name": "Dave",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def create_experience(request):
    """Membuat data pengalaman baru menggunakan ExperienceForm."""
    form = ExperienceForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman baru berhasil ditambahkan!")
        return redirect("main:show_experience")
        
    context = {
        "name": "Dave",
        "form": form,
        "page_title": "Tambah Pengalaman Baru",
        "submit_label": "Simpan Pengalaman",
    }
    return render(request, "experience_form.html", context)

def update_experience(request, experience_id):
    """Mengubah data pengalaman yang sudah ada berdasarkan ID."""
    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman berhasil diperbarui!")
        return redirect("main:show_experience")
        
    context = {
        "name": "Dave",
        "form": form,
        "page_title": "Ubah Pengalaman",
        "submit_label": "Simpan Perubahan",
    }
    return render(request, "experience_form.html", context)

def delete_experience(request, experience_id):
    """Menghapus data pengalaman berdasarkan ID."""
    experience = get_object_or_404(Experience, pk=experience_id)
    if request.method == "POST":
        experience.delete()
        messages.success(request, "Pengalaman berhasil dihapus!")
    return redirect("main:show_experience")

### ======== BAGIAN PROJECT ========  

def get_projects_json(request):
    """Mengembalikan data proyek dalam format JSON dengan dukungan filter judul."""
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()
    if title_query:
        projects = projects.filter(title__icontains=title_query)
    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

def show_projects(request):
    """Menampilkan daftar proyek setelah mengambil JSON dan melakukan deserialisasi."""
    json_response = get_projects_json(request)
    projects = serializers.deserialize("json", json_response.content.decode("utf-8"))
    projects_list = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()
    
    context = {
        "name": "Dave",
        "project_list": projects_list,
        "title_query": title_query,
    }
    return render(request, "project.html", context)

def create_project(request):
    """Menambahkan proyek baru menggunakan ProjectForm."""
    form = ProjectForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")
    context = {
        "name": "Dave",
        "form": form,
    }
    return render(request, "projects_form.html", context)

def delete_project(request, project_id):
    """Menghapus proyek berdasarkan ID."""
    project = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
    return redirect("main:show_projects")