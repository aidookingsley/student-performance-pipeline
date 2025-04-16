# 🎓 Student Performance Data Engineering Project

Welcome to the **Student Performance Pipeline**, a complete data engineering and visualization project built around the UCI Student Performance dataset. This project demonstrates the full lifecycle of data from ingestion to insights using modern data tooling.

---

## 🚀 Getting Started

### 1. **Clone the Repository**
```bash
git clone https://github.com/aidookingsley/student-performance-pipeline.git
cd student-performance-pipeline
```

### 2. **Set Up the Environment (Optional)**
```bash
python -m venv venv
source venv/bin/activate  # For Mac/Linux
venv\Scripts\activate  # For Windows
```

### 3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 4. **Run the ETL Pipeline**
```bash
python scripts/extract.py
python scripts/transform.py
python scripts/load.py
```

---

## 🧪 Data Engineering Workflow

### **1. Data Extraction**
- Downloads data from the [UCI ML Repository](https://archive.ics.uci.edu/ml/datasets/Student+Performance).
- Two datasets: `student-mat.csv` and `student-por.csv`.

### **2. Data Transformation**
- Merge datasets
- Add derived features (e.g., average grades, pass/fail)
- Clean and preprocess

### **3. Data Loading**
- Save transformed data as CSV or Parquet
- Upload to AWS S3 and Azure Blob Storage

---

## ⏱️ Orchestrating the Pipeline with Airflow

Airflow DAGs automate the data pipeline:
- Scheduled extractions and transformations
- Upload to cloud storage

Access the Airflow UI:
```bash
http://localhost:8081
```

---

## 📊 Streamlit Dashboard

Visualize trends and interact with the data using a lightweight Streamlit app.

### Features:
- Filter by age, gender, and address
- Grade distribution and correlation charts
- Download datasets
- ML predictions (if included)

Access the app:
```bash
http://localhost:8501
```

---

## 🐳 Dockerized Setup

To run everything together:
```bash
docker-compose up --build
```

This spins up:
- Apache Airflow
- PostgreSQL & Redis (for Airflow backend)
- Streamlit Dashboard

---

## 🧰 Tools & Tech Stack

| Purpose             | Tools                           |
|---------------------|----------------------------------|
| Language            | Python                          |
| Data Orchestration | Apache Airflow                  |
| Dashboard           | Streamlit                       |
| Cloud Storage       | AWS S3, Azure Blob              |
| Containerization    | Docker, Docker Compose          |
| CI/CD               | GitHub Actions                  |
| Database            | PostgreSQL                      |

---

## 🧪 Testing
Run tests :
```bash
pytest
```

---

## 📝 Future Enhancements
- Add model training + evaluation
- Schedule Streamlit refresh with Airflow
- Include CI notifications
- Expand DAGs to include downstream ML workflows

---

## 💬 Contributing

Contributions welcome! Fork the repo and submit a pull request 💡

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 📬 Contact

**Kingsley Mensah Aidoo**  
📧 aidookingsleymensah@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/youkingsley-m-aidoo)
