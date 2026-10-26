
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
📊The dataset used in this project is the Paris treated traffic GeoJSON dataset (2023) (Paris_AADT_AAWT_2023.geojson).   It was sourced directly from the open-source GitHub repository traffic-volume-data-EU-cities maintained by XavB64. This dataset contains standardized street-segment traffic metrics for Paris, including Annual Average Daily Traffic (AADT), Annual Average Weekly Traffic (AAWT), OpenStreetMap road types (osm_type), speed limits, and lane counts.
Github URL : https://github.com/XavB64/traffic-volume-data-EU-cities/tree/main/France/Paris/treated
Automatic Download: Both the notebook.ipynb and train.py automatically pull this dataset via its raw GitHub link, so no manual downloading is required.
🛠️ Models & Validation SummaryBaseline Model: Linear RegressionFinal Model: Random Forest Regressor (max_depth=10, min_samples_leaf=10, n_estimators=100)Evaluation Metric: Root Mean Squared Error (RMSE)Final Test Performance: Test RMSE of ~7,437
🚀 Instructions on How to Run the Project1. Install DependenciesClone the repository and install the required packages:Bashpip install -r requirements.txt
2. Train the Model (Optional)To re-run the training pipeline and generate a fresh model_paris_traffic.bin:Bashpython train.py
3. Run the Flask Application LocallyStart the prediction server:Bashpython predict.py
The server will run on http://localhost:9696.4. Test the Local EndpointIn a separate terminal, test a prediction request using PowerShell:PowerShell$body = @{
    raw_oneway = 1
    osm_oneway = 1
    osm_lanes = 3.0
    osm_maxspeed = 30.0
    osm_type_motorway = 0
    osm_type_motorway_link = 0
    osm_type_primary = 1
    osm_type_primary_link = 0
    osm_type_residential = 0
    osm_type_secondary = 0
    osm_type_secondary_link = 0
    osm_type_tertiary = 0
    osm_type_trunk = 0
    osm_type_trunk_link = 0
    osm_type_unclassified = 0
    osm_type_unknown = 0
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:9696/predict" -Method Post -Body $body -ContentType "application/json"
-- Running with Docker (Deployment)To ensure complete environment reproducibility, you can containerize and run the application using Docker.
1. Build the Docker ImageMake sure Docker Desktop is running, then build the image:Bashdocker build -t paris-traffic-model .
2. Run the ContainerBashdocker run -it --rm -p 9696:9696 paris-traffic-model
-- Deployment Interaction ProofHere is the interaction screenshot showing the Flask API running locally inside the Docker container and responding successfully to incoming prediction requests:
