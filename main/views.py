from django.shortcuts import get_object_or_404, redirect, render
from main.models import Experience, Project
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, JsonResponse
from main.forms import ProjectForm, ExperienceForm
from django.views.decorators.http import require_POST

### ====== Tutorial 4 ====== ###
import datetime

def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": "Dave",
        "npm": "2506656601",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Mahasiswa Ilmu Komputer Universitas Indonesia yang tertarik "
            "pada pengembangan kecerdasan artifisial dan keamanan siber."
        ),
        "last_login" : last_login,
    }
    return render(request, "index.html", context)

def get_experience_json(request):
    """Mengembalikan data seluruh pengalaman dalam format JSON."""
    experiences = Experience.objects.all()
    data = serializers.serialize("json", experiences, use_natural_foreign_keys=True)
    return HttpResponse(data, content_type="application/json")

def is_editor_user(user):
    """Memeriksa apakah akun pengguna tergabung ke dalam grup Editor."""
    return user.is_authenticated and user.groups.filter(name='Editor').exists()

def show_experience(request):
    """Menampilkan daftar pengalaman setelah mengambil JSON dan melakukan deserialisasi."""
    json_response = get_experience_json(request)
    deserialized_data = serializers.deserialize("json", json_response.content.decode("utf-8"))
    experience_list = [item.object for item in deserialized_data]
    is_editor = request.user.is_authenticated and request.user.groups.filter(name='Editor').exists()
    
    context = {
        "name": "Dave",
        "experience_list": Experience.objects.all(),
        "is_editor": is_editor,
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

@login_required(login_url="/login/") # 1. Alihkan pengunjung yang belum login ke /login/
def update_experience(request, experience_id):
    """Mengubah data pengalaman yang sudah ada berdasarkan ID (hanya Superuser & Editor)."""
    # 2. Cek apakah user adalah superuser atau tergabung dalam grup Editor
    is_editor = request.user.groups.filter(name='Editor').exists()
    if not (request.user.is_superuser or is_editor):
        raise PermissionDenied # Tolak user biasa dengan HTTP 403 Forbidden

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

@login_required(login_url="/login/")
def delete_experience(request, experience_id):
    """Hanya superuser yang diizinkan menghapus pengalaman."""
    if not request.user.is_superuser:
        raise PermissionDenied

    experience = get_object_or_404(Experience, pk=experience_id)
    if request.method == "POST":
        experience.delete()
        messages.success(request, "Pengalaman berhasil dihapus!")
        return redirect("main:show_experience")
    return redirect("main:show_experience")

### ======== BAGIAN PROJECT ========  

def get_projects_json(request):
    """Mengembalikan data proyek dalam format JSON dengan dukungan filter judul."""
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.prefetch_related('starred_by').all()
    
    if title_query:
        projects = projects.filter(title__icontains=title_query)
    
    data = []
    for project in projects:
        starred_users = project.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(project.id),
            "fields": {
                "title": project.title,
                "description": project.description,
                "tech_stack": project.tech_stack,
                "project_url": project.project_url,
                "project_image_url": project.project_image_url,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)


def show_projects(request):
    title_query = request.GET.get("title", "").strip()
    
    context = {
        "name": "Dave",
        "title_query": title_query,
        "form": ProjectForm(),
    }
    return render(request, "project.html", context)



@login_required(login_url="/login/")
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    
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

@login_required(login_url="/login/")
def delete_project(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    """Menghapus proyek berdasarkan ID."""
    project = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
    return redirect("main:show_projects")

### ====== TUTORIAL 4 ====== ###
def register(request):
    form = UserCreationForm(request.POST or None)
    
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")
    
    context = {
        "name" : "Dave",
        "form" : form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)
    
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response
    
    context = {
        "name" : "Dave",
        "form" : form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

# Tanpa cek is_superuser: semua akun yang sudah login boleh memberi star
@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        # Kalau akun ini sudah pernah memberi star, batalkan star-nya.
        # Kalau belum, tambahkan star.
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_projects")

### ====== Tugas 4 ====== ###
@login_required(login_url="/login/")
def toggle_star_experience(request, experience_id):
    """Mengaktifkan atau membatalkan star pada objek Experience tertentu."""
    experience = get_object_or_404(Experience, pk=experience_id)
    if request.method == "POST":
        if request.user in experience.starred_by.all():
            experience.starred_by.remove(request.user)
            messages.info(request, f"Batal menyukai {experience.title}.")
        else:
            experience.starred_by.add(request.user)
            messages.success(request, f"Menyukai {experience.title}!")
    return redirect("main:show_experience")

### ====== Tutorial 5 ====== ###
@require_POST
def create_project_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan proyek."},
            status=403,
        )

    form = ProjectForm(request.POST)
    if form.is_valid():
        project = form.save()
        return JsonResponse(
            {"message": "Proyek berhasil ditambahkan.", "pk": str(project.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)