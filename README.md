
**Machine Learning Zoomcamp - Midterm Project**

##  Description of the Problem
Predicting urban traffic volume is crucial for city planning, reducing congestion, and optimizing public transit routes. This project builds an end-to-end Machine Learning web service to predict Annual Average Daily Traffic (`AADT`) for street segments in Paris. Using geographic and road attribute features (such as number of lanes, maximum speed, and OpenStreetMap road types), the model accurately estimates traffic density.


---

## 🗂️ Project Structure
```text
ZoomcampMidtermproject/
├── notebook.ipynb            # Exploratory Data Analysis, feature engineering, and model tuning
├── train.py                  # Training script that builds the final model and saves it
├── predict.py                # Flask web service for local/containerized inference
├── model_paris_traffic.bin   # Serialized final Random Forest model (Pickle)
├── Dockerfile                # Containerization configuration
├── requirements.txt          # Python dependencies
├── deployment_screenshot.png # Evidence of local Docker deployment & interaction
└── README.md                 # Project documentation
```
## 📑 Table of Contents

- [Dataset](#-dataset)
- [Models & Validation](#-models--validation)
- [Getting Started](#-getting-started)
- [Testing the API](#-testing-the-api)
- [Running with Docker](#-running-with-docker)
- [Deployment Proof](#-deployment-proof)

---

## 📊 Dataset

The project uses the **Paris treated traffic GeoJSON dataset (2023)** (`Paris_AADT_AAWT_2023.geojson`), sourced from the open-source [traffic-volume-data-EU-cities](https://github.com/XavB64/traffic-volume-data-EU-cities/tree/main/France/Paris/treated) repository maintained by [XavB64](https://github.com/XavB64).

**Contents:** standardized street-segment traffic metrics for Paris, including:

- **AADT**: Annual Average Daily Traffic
- **AAWT**: Annual Average Weekly Traffic
- **`osm_type`**: OpenStreetMap road type
- **Speed limits**
- **Lane counts**

**Automatic download:** both `notebook.ipynb` and `train.py` pull the dataset directly from its raw GitHub link, so no manual download is needed.

---

## 🤖 Models & Validation

| Item | Details |
|------|---------|
| **Baseline model** | Linear Regression |
| **Final model** | Random Forest Regressor |
| **Hyperparameters** | `max_depth=10`, `min_samples_leaf=10`, `n_estimators=100` |
| **Evaluation metric** | Root Mean Squared Error (RMSE) |
| **Final test performance** | Test RMSE ≈ **7,437** |

---

## 🚀 Getting Started

### 1. Install dependencies

Clone the repository and install the required packages:

```bash
pip install -r requirements.txt
```

### 2. Train the model (optional)

To re-run the training pipeline and generate a fresh `model_paris_traffic.bin`:

```bash
python train.py
```

### 3. Run the Flask application locally

Start the prediction server:

```bash
python predict.py
```

The server runs at **http://localhost:9696**.

---

## 🧪 Testing the API

In a separate terminal, send a test prediction request using PowerShell:

```powershell
$body = @{
    raw_oneway                = 1
    osm_oneway                = 1
    osm_lanes                 = 3.0
    osm_maxspeed              = 30.0
    osm_type_motorway         = 0
    osm_type_motorway_link    = 0
    osm_type_primary          = 1
    osm_type_primary_link     = 0
    osm_type_residential      = 0
    osm_type_secondary        = 0
    osm_type_secondary_link   = 0
    osm_type_tertiary         = 0
    osm_type_trunk            = 0
    osm_type_trunk_link       = 0
    osm_type_unclassified     = 0
    osm_type_unknown          = 0
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:9696/predict" -Method Post -Body $body -ContentType "application/json"
```

---

## 🐳 Running with Docker

Containerizing the app ensures a fully reproducible environment.

### Build the image

Make sure Docker Desktop is running, then build the image:

```bash
docker build -t paris-traffic-model .
```

### Run the container

```bash
docker run -it --rm -p 9696:9696 paris-traffic-model
```

The API is then available at **http://localhost:9696**.

---

## 📸 Deployment Proof

The screenshot below shows the Flask API running inside the Docker container and successfully responding to prediction requests:

<!-- Replace with the path to your screenshot -->
![Docker deployment screenshot](ML-Zoomcamp-MidtermProject-Paris-Traffic-Prediction/deployment_screenshot.png)

---

## 🛠️ Tech Stack

- **Python** (scikit-learn, Flask)
- **Jupyter Notebook** (EDA and experimentation)
- **Docker** (deployment)
