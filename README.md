# Air Quality Monitoring System

This repository contains the implementation of an Air Quality Monitoring System that tracks air pollution data through backend processes and visualizes this data both as digital maps and within a 3D model environment using Azure Digital Twins. The system uses Azure Functions for automating data retrieval, pollution analysis, and sending notifications concerning air quality dangers to end users.

## Project Structure

```

.

|____server.py # Backend server to provide APIs for frontend views

|____DTDL_models # Contains Digital Twins Definition Language models

|____README.md # Project documentation

|____azure_functions

| |____host.json # Configuration file for Azure Functions

| |____requirements.txt # Python dependencies for Azure Functions

| |____function_app.py # Azure Functions app for periodical data fetching and analysis

|____templates

| |____map.html # HTML template showing the map visualization of air quality data

|____3D_model

| |____general_scene.gltf # 3D model for Azure Digital Twins visualization

```

## Features

- **Live Air Quality Mapping**: Visualization of current air quality data on a digital map.

- **3D Visualization**: Uses Azure Digital Twins to model and visualize air quality in a 3D interactive environment.

- **Automated Data Handling**: Azure Functions automatically fetch air quality data, analyze pollution levels, and notify users if thresholds are exceeded.

## Getting Started

### Prerequisites

- Python 3.8+

- Azure account with an active subscription

- Azure CLI or Azure portal access

- Node.js and npm (for any frontend package management)

### Installation

1. **Clone the repository:**

 ```bash
 git clone https://github.com/yourgithubusername/air-quality-monitoring.git
 cd air-quality-monitoring
 ```

2. **Set up a virtual environment (optional but recommended):**

 ```bash
 python -m venv venv
 source venv/bin/activate # On Windows use `.\venv\Scripts\activate`
 ```

3. **Install requirements:**

 ```bash
 pip install -r azure_functions/requirements.txt
 ```

4. **Local settings for Azure Functions:**

 Navigate to the `azure_functions` directory and rename the `local.settings.json.example` to `local.settings.json`, then update it with your Azure credentials.

5. **Run the server:**

 ```bash
 python server.py
 ```

## Usage

To see the air quality mapping:

- Open your web browser and navigate to `http://localhost:<port>/map.html` (replace `<port>` with the port number server.py is running on, usually printed to the console on startup).

To interact with the 3D digital twins model:

- Ensure your Azure Digital Twins instance is properly set up and that the `general_scene.gltf` is correctly configured in the Azure Digital Twins Explorer.

### Interacting with Azure Functions

Azure Functions are set to trigger at scheduled intervals, but you can trigger them manually from the Azure portal for testing purposes.

## Screenshots

![Air Quality Map](https://github.com/Miracle-Aligner/air_quality_dt/blob/main/screenshots/01.jpeg)

**Description:** This screenshot demonstrates the 3D models hat represent Digital Twins of 10 air sensors, City App Server and end-user phone.

![Air Quality Map](https://github.com/Miracle-Aligner/air_quality_dt/blob/main/screenshots/02.jpeg)

**Description:** This screenshot demonstrates Twin Graph from Azure Digital Twin Service.

![Air Quality Map](https://github.com/Miracle-Aligner/air_quality_dt/blob/main/screenshots/03.jpeg)

**Description:** This screenshot demonstrates Model Graph from Azure Digital Twin Service.

![Air Quality Map](https://github.com/Miracle-Aligner/air_quality_dt/blob/main/screenshots/04.jpeg)

**Description:** This screenshot demonstrates the air quality map rendered from `map.html`.

## Final Presentation

For a comprehensive overview, including the scope of work, please see our [final project presentation](https://docs.google.com/presentation/d/1nRTD9RVssoOtlGSgyX_Dwp-qhCw_sd8cUWrZeDK_aGY/edit?usp=sharing).