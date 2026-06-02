# Workflow-CI: Heart Disease Model Training with MLflow

Repository ini merupakan implementasi **Kriteria 3** dari submission Machine Learning Terapan untuk mendemonstrasikan workflow CI/CD menggunakan MLflow Project dan GitHub Actions.

## 📋 Deskripsi

Project ini mengimplementasikan pipeline otomatis untuk:
- 🤖 Training model RandomForestClassifier untuk prediksi penyakit jantung
- 📊 Tracking eksperimen dengan MLflow
- 🔄 CI/CD automation dengan GitHub Actions
- 🐳 Docker Image deployment ke Docker Hub
- 💾 Penyimpanan artifacts di GitHub Repository

## 📁 Struktur Folder

```
Workflow-CI/
├── .github/
│   └── workflows/
│       └── ci.yml                          # GitHub Actions workflow
├── MLProject/
│   ├── modelling.py                        # Script training model
│   ├── conda.yaml                          # Dependency environment
│   ├── MLProject                           # MLflow Project config (tanpa ekstensi)
│   ├── heart-disease_preprocessing.csv     # Dataset
│   ├── mlruns/                            # MLflow tracking artifacts (auto-generated)
│   └── docker_hub_link.txt                # Link Docker Hub image (auto-generated)
└── README.md
```

## 🚀 Fitur Utama

### ✅ Level Advance (4 Points)

1. **MLflow Project Setup**
   - Konfigurasi MLProject dengan parameterized entry points
   - Conda environment untuk reproducibility
   - Local tracking dengan MLflow

2. **GitHub Actions CI/CD**
   - Trigger otomatis pada push ke branch `main`
   - Manual trigger dengan `workflow_dispatch`
   - Training model otomatis menggunakan `mlflow run`

3. **Artifact Management (Skilled)**
   - Upload artifacts ke GitHub Actions
   - Commit `mlruns/` ke repository untuk persistensi
   - Retention artifacts selama 30 hari

4. **Docker Deployment (Advance)**
   - Build Docker image dengan `mlflow models build-docker`
   - Push ke Docker Hub otomatis
   - Versioning dengan latest tag

## 🛠️ Setup

### Prerequisites

- Python 3.9+
- MLflow 2.9.2+
- GitHub Repository
- Docker Hub Account

### Setup Local

```bash
# Clone repository
git clone https://github.com/<USERNAME>/Workflow-CI.git
cd Workflow-CI

# Install MLflow
pip install mlflow scikit-learn pandas numpy

# Run MLflow Project
cd MLProject
mlflow run . --env-manager=local

# View results
mlflow ui
```

### Setup GitHub Actions

1. **Buat GitHub Repository** bernama `Workflow-CI`

2. **Setup GitHub Secrets**
   
   Pergi ke `Settings > Secrets and variables > Actions` dan tambahkan:
   - `DOCKERHUB_USERNAME`: Username Docker Hub Anda
   - `DOCKERHUB_TOKEN`: Access token dari Docker Hub

3. **Push ke GitHub**
   ```bash
   git add .
   git commit -m "Initial commit - MLflow CI/CD setup"
   git branch -M main
   git remote add origin https://github.com/<USERNAME>/Workflow-CI.git
   git push -u origin main
   ```

### Mendapatkan Docker Hub Token

1. Login ke [Docker Hub](https://hub.docker.com/)
2. Klik profile > Account Settings
3. Security > New Access Token
4. Beri nama token (misal: `github-actions`)
5. Copy token dan simpan sebagai GitHub Secret

## 📊 Parameter MLflow Project

File `MLProject` mendukung parameter berikut:

| Parameter      | Type  | Default                              | Deskripsi                    |
|----------------|-------|--------------------------------------|------------------------------|
| `data_path`    | str   | `heart-disease_preprocessing.csv`    | Path ke dataset              |
| `n_estimators` | int   | 100                                  | Jumlah trees di Random Forest|
| `random_state` | int   | 42                                   | Seed untuk reproducibility   |
| `test_size`    | float | 0.2                                  | Proporsi data test           |

### Contoh Custom Run

```bash
mlflow run . --env-manager=local \
  -P n_estimators=200 \
  -P test_size=0.25
```

## 🐳 Docker Image

Docker image yang dihasilkan dapat diakses di:
- **Repository**: `<DOCKERHUB_USERNAME>/heart-disease-model`
- **Tag**: `latest`
- **Link**: Cek file `MLProject/docker_hub_link.txt` setelah CI/CD selesai

### Menggunakan Docker Image

```bash
# Pull image
docker pull <DOCKERHUB_USERNAME>/heart-disease-model:latest

# Run model server
docker run -p 5000:8080 <DOCKERHUB_USERNAME>/heart-disease-model:latest

# Test prediction
curl -X POST http://localhost:5000/invocations \
  -H 'Content-Type: application/json' \
  -d '{"dataframe_split": {"columns": ["age", "sex", "cp", ...], "data": [[63, 1, 1, ...]]}}'
```

## 📈 Workflow CI/CD

### Trigger

Workflow akan berjalan otomatis ketika:
- Ada push ke branch `main`
- Manual trigger via GitHub Actions UI

### Steps

1. ✅ Checkout repository
2. ✅ Setup Python 3.9
3. ✅ Install dependencies (MLflow, scikit-learn, pandas, numpy)
4. ✅ Run MLflow Project training
5. ✅ Extract Run ID dari MLflow
6. ✅ Upload artifacts ke GitHub Actions
7. ✅ Commit `mlruns/` ke repository
8. ✅ Setup Docker Buildx
9. ✅ Login ke Docker Hub
10. ✅ Build Docker image dengan MLflow
11. ✅ Push image ke Docker Hub
12. ✅ Save Docker Hub link
13. ✅ Commit Docker Hub link ke repository

## 📝 Kriteria Penilaian

| Level      | Poin | Status | Deskripsi                                          |
|------------|------|--------|----------------------------------------------------|
| Reject     | 0    | ❌     | Tidak ada folder MLProject atau workflow CI        |
| Basic      | 2    | ✅     | MLProject + CI yang bisa melatih model             |
| Skilled    | 3    | ✅     | Basic + menyimpan artifacts ke repository          |
| **Advance**| **4**| **✅** | **Skilled + Docker image ke Docker Hub**           |

## 🔍 Verifikasi

### Cek Artifacts di GitHub

1. Pergi ke `Actions` tab di GitHub
2. Klik workflow run terbaru
3. Scroll ke bawah, lihat section "Artifacts"
4. Download `mlflow-artifacts` untuk melihat hasil training

### Cek Docker Image di Docker Hub

1. Login ke [Docker Hub](https://hub.docker.com/)
2. Pergi ke repository `<USERNAME>/heart-disease-model`
3. Lihat image dengan tag `latest`
4. Cek file `MLProject/docker_hub_link.txt` di repository

### Cek MLflow Tracking

Setelah CI/CD selesai, folder `MLProject/mlruns/` akan otomatis ter-commit ke repository dengan hasil tracking lengkap.

## 🎯 Hasil Eksperimen

Model yang dilatih:
- **Algorithm**: Random Forest Classifier
- **Dataset**: Heart Disease (303 samples, 13 features)
- **Metrics**: Accuracy, Precision, Recall, F1-Score
- **Tracking**: MLflow dengan autolog
- **Artifacts**: Model pickle, metrics, parameters

## 📚 Teknologi

- **MLflow**: Experiment tracking & model registry
- **Scikit-learn**: Machine learning library
- **GitHub Actions**: CI/CD automation
- **Docker**: Containerization
- **Docker Hub**: Image registry

## 👨‍💻 Author

**Nama**: [Raditya Putra Farma]  
**Program**: Dicoding x IBM - Membangun Sistem Machine Learning  
**Kriteria**: 3 - Membuat Workflow CI  
**Target**: Advance (4 points)

## 📄 License

Project ini dibuat untuk keperluan submission program Dicoding x IBM.

---

**Last Updated**: June 3, 2026
