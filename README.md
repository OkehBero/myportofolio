Nama : Dave Wesley Tjoen

NPM : 2506656601

Kelas : PBP D

### Tugas 1

1. ...
2. ...
3. ...

### Tugas 2
1. Alur pemrosesan permintaan
   - Permintaan dari browser pertama kali diterima oleh proyek dan dipetakan melalui berkas 'portofolio/urls.py'.
   - Rute tersebut diteruskan oleh fungsi 'include' ke berkas 'main/urls.py' pada tingkat aplikasi untuk dicocokkan dengan rute rute 'project/' menuju view 'show_project'.
   - Fungsi view 'show_project' mengeksekusi query ORM Django untuk mengambil seluruh data dari model 'Project' di basis data.
   - View kemudian menyusun data tersebut ke dalam sebuah dictionary 'context' dan memanggil fungsi 'render()' bersama berkas 'project.html'.
   - Mesin template memproses data 'context' ke dalam tag HTML, mengevaluasi kondisi dan perulangan, lalu mengirimkan hasil render dokumen HTML sebagai respons kembali ke browser.

2. Alasan data disimpan pada model dan bukan ditulis statis di template
   - Penerapan prinsip pemisahan tanggung jawab (separation of concerns) memastikan template murni berfokus pada struktur tampilan antarmuka, sedangkan data dikelola secara mandiri oleh basis data melalui model.
   - Kemudahan pemeliharaan aplikasi meningkat karena penambahan, pembaruan, maupun penghapusan data tidak menuntut pengubahan kode HTML secara manual sehingga mencegah risiko rusaknya struktur antarmuka.
   - Skalabilitas dan reusabilitas aplikasi terjaga dengan baik karena data yang tersimpan di model dapat digunakan kembali untuk berbagai keperluan lain, seperti penyediaan API, fitur pencarian, pengurutan, hingga halaman detail tanpa adanya duplikasi kode.

3. Perbedaan 'makemigrations' dan 'migrate'
   - Perintah 'makemigrations' berfungsi mendeteksi perubahan skema pada 'models.py' dan membuat berkas skrip migrasi baru sebagai cetak biru instruksi tanpa memodifikasi basis data sesungguhnya.
   - Perintah 'migrate' bertugas mengeksekusi seluruh berkas migrasi yang belum terpasang ke dalam basis data agar struktur tabel dan kolom fisik benar-benar dibuat atau diperbarui.
   - Sebagai contoh, penambahan atribut baru seperti 'project_url = models.URLField(blank=True)' pada model 'Project' menuntut eksekusi 'makemigrations' untuk membuat berkas migrasi perubahan kolom, lalu dilanjutkan dengan 'migrate' agar kolom fisik tersebut tercipta di basis data.

4. AI Disclousure:
    - Aku menggunakan Gen AI (Google Gemini) dalam mengerjakan tugas ini. Bagian yang dibantu adalah:
        - Google Gemini membantu memberikan referensi struktur untuk model baru 'Project'.
        - Google Gemini membantu menyusun kerangka unit test.

### Tugas 3
1. Alasan penggunaan 'ModelForm' dan fungsi '{% csrf_token %}'
   - 'ModelForm' menerapkan prinsip DRY dengan memetakan form langsung ke model, sehingga validasi tipe data dan batasan field ditangani otomatis oleh Django.
   - Mempermudah penyimpanan ke basis data melalui 'form.save()' serta menyatukan pengaturan widget input dan label secara terpusat.
   - Tag '{% csrf_token %}' wajib disertakan untuk menghasilkan token keamanan unik guna mencegah serangan Cross-Site Request Forgery (CSRF) pada request POST.

2. Alasan JSON lebih disukai dibanding XML pada web modern
   - Sintaks JSON jauh lebih ringkas tanpa tag penutup berulang, sehingga ukuran data lebih ringan dan hemat bandwidth.
   - Didukung secara native oleh JavaScript pada browser modern, sehingga proses parsing data jauh lebih cepat tanpa beban tree XML DOM.
   - Struktur key-value dan array selaras dengan tipe data bahasa pemrograman modern serta arsitektur RESTful API.

3. Alur pengembalian data JSON dan pentingnya serialisasi
   - Alur: Klien mengakses URL API, View mengambil QuerySet dari database, QuerySet diubah ke teks JSON via 'serializers.serialize()', Dikembalikan via 'HttpResponse', View antarmuka mendeserialisasi kembali data tersebut untuk dirender ke template HTML.
   - Serialisasi wajib dilakukan karena objek QuerySet Django adalah objek kompleks Python di memori server yang tidak bisa dikirim langsung melalui protokol HTTP tanpa diubah ke format teks standar.

4. AI Disclosure:
   - Aku menggunakan Gen AI (Google Gemini) dalam mengerjakan tugas ini. Bagian yang dibantu adalah:
      - Membantu menyusun dan mendebug fungsi CRUD, serialisasi JSON, dan deserialisasi.
      - Membantu menyusun kerangka unit test.