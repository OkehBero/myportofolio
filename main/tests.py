from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Project
# Create your tests here.

class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")
        
class ProjectTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title="Aplikasi Manajemen Portofolio",
            description="Membangun website portofolio pribadi berbasis Django.",
            tech_stack="Django, HTML, CSS",
            project_url="https://github.com/example/repo"
        )

    def test_project_url_and_template(self):
        # 1. URL dapat diakses dan menggunakan template yang tepat
        response = self.client.get(reverse("main:show_project"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project.html")

    def test_project_data_rendered(self):
        # 2. Data model muncul di halaman HTML ketika ada data
        response = self.client.get(reverse("main:show_project"))
        self.assertContains(response, self.project.title)
        self.assertContains(response, self.project.description)
        self.assertContains(response, self.project.tech_stack)

    def test_empty_project_page(self):
        # 3. Halaman HTML menampilkan pesan kondisi kosong ketika belum ada data
        Project.objects.all().delete()
        response = self.client.get(reverse("main:show_project"))
        self.assertContains(response, "Belum ada proyek yang ditambahkan.")
        
class ExperienceCRUDTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )

    def test_show_experience_with_deserialization(self):
        """Memverifikasi show_experience berhasil merender data dari JSON deserialized."""
        response = self.client.get(reverse("main:show_experience"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, "Asisten Dosen PBP")

    def test_get_experience_json(self):
        """Memverifikasi endpoint API JSON mengembalikan data dalam format JSON."""
        response = self.client.get(reverse("main:get_experience_json"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        data = json.loads(response.content)
        self.assertTrue(len(data) >= 1)
        self.assertEqual(data[0]["fields"]["title"], "Asisten Dosen PBP")

    def test_create_experience_post(self):
        """Menguji penambahan data pengalaman via form POST."""
        post_data = {
            "title": "Software Engineer Intern",
            "description": "Bekerja pada backend microservices.",
            "category": "internship",
            "thumbnail": "",
            "ended_at": "",
        }
        response = self.client.post(reverse("main:create_experience"), data=post_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Experience.objects.filter(title="Software Engineer Intern").exists())

    def test_update_experience_post(self):
        """Menguji pembaruan data pengalaman via form POST."""
        update_data = {
            "title": "Lead Asisten Dosen PBP",
            "description": "Mengkoordinasikan tim asisten lab.",
            "category": "part-time",
            "thumbnail": "",
            "ended_at": "",
        }
        response = self.client.post(
            reverse("main:update_experience", args=[self.experience.id]),
            data=update_data
        )
        self.assertEqual(response.status_code, 302)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Lead Asisten Dosen PBP")

    def test_delete_experience_post(self):
        """Menguji penghapusan data pengalaman via POST."""
        response = self.client.post(
            reverse("main:delete_experience", args=[self.experience.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Experience.objects.filter(id=self.experience.id).exists())