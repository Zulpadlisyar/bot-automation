# TODO: Optimasi CI Workflow

## Langkah-langkah
- [x] 1. Analisis workflow CI saat ini
- [x] 2. Optimasi `.github/workflows/ci.yml`:
  - [x] Tambahkan `workflow_dispatch` untuk manual trigger
  - [x] Tambahkan `paths` filter agar CI hanya berjalan saat file relevan berubah
  - [x] Tambahkan `concurrency` untuk membatalkan run redundant
  - [x] Gunakan `cache: pip` bawaan `actions/setup-python` untuk simplifikasi
  - [x] Gabungkan install dependencies untuk mengurangi step count
  - [x] Tambahkan `if: !contains(github.event.head_commit.message, '[ci skip]')` untuk skip commit tertentu
- [x] 3. Verifikasi hasil edit

## Hasil
Workflow CI telah dioptimasi untuk mengurangi penggunaan GitHub Actions minutes.


