# 🚦 ROAD//SAFE — Road Accident Severity Classification

> **RoadSafe Analytics** is a machine-learning web application for exploring historical road-accident records and classifying the severity category associated with a user-described accident scenario.

<p align="center">
  <strong>SEE THE SIGNAL. READ THE ROAD.</strong>
</p>

---

## 📌 Project Overview

RoadSafe Analytics combines statistical data analysis with a supervised classification model in an interactive Streamlit application. Users can explore historical accident patterns, select road and accident conditions, and receive a predicted severity category from the trained model.

The project was developed as an academic Statistical Inference / Machine Learning project. It demonstrates a workflow that includes data preparation, exploratory analysis, classification, and deployment of a user-facing application.

### What RoadSafe can do

- **Classify an accident scenario:** Submit the available accident and road-condition inputs to receive the model's predicted severity category.
- **Explore historical patterns:** View summaries and charts based on the supplied dataset.
- **Inspect selected conditions:** Explore distributions for factors such as weather, road-surface conditions, lighting, and day of the week when those columns are available.
- **Use a browser-based interface:** Interact with the app without running notebook cells.

### Important limitation

RoadSafe predicts a **severity label for an input record**. It does **not** predict whether an accident will happen, provide emergency advice, or guarantee a real-world outcome. Model outputs are estimates based on patterns in historical data and should not be used as a substitute for professional road-safety assessment.

---

## ✨ Application Pages

| Page | Description |
|---|---|
| **Home** | Overview of the project, dataset summary, and severity-category distribution. |
| **Classify Severity** | Form for entering accident-related conditions and receiving a classification result. |
| **Road Safety Insights** | Interactive exploration of severity and selected categorical variables. |
| **About** | Project purpose, scope, data notes, and limitations. |

> The application is designed for end users. Technical model-comparison tables and detailed evaluation outputs are kept in the project notebook rather than the main app interface.

---

## 🧠 Machine-Learning Workflow

1. Load the road-accident dataset.
2. Clean and prepare the data.
3. Select the input features and the target column.
4. Split the data into training and testing sets.
5. Train and evaluate candidate classification models in the notebook.
6. Select the model to use in the application.
7. Save the trained model and its preprocessing pipeline as a Joblib artifact.
8. Load the saved artifact in Streamlit to classify user-provided inputs.

The target column used by the current app defaults to `Accident_severity`. The exact model, features, preprocessing, and target should match the saved model artifact created by the notebook.

---

## 🗂️ Repository Structure

A typical deployment-ready repository should look like this:

```text
RoadSafe-Analytics/
├── app.py
├── requirements.txt
├── road_accident_severity_classifier.joblib
├── Road.csv                         # Include only if permitted and needed by the app
└── README.md
```

If your notebook is part of the repository, you can also include it:

```text
├── Riddhi_Road_Accident_Classification_Project_Updated.ipynb
```

### Files

- **`app.py`** — Streamlit user interface.
- **`requirements.txt`** — Python packages required to run the application.
- **`road_accident_severity_classifier.joblib`** — Saved model artifact loaded by the app. It must contain the keys and structure expected by `app.py`, including the trained model and feature names.
- **`Road.csv`** — Dataset used to show historical summaries and populate the form's category choices. Include it only if you are permitted to share it and the app requires it.
- **Notebook (`.ipynb`)** — Data preparation, statistical analysis, model training, and export steps.

---

## 🛠️ Technology Stack

- **Python** — Application and analysis language
- **Streamlit** — Interactive web application
- **Pandas** — Data loading and manipulation
- **NumPy** — Numerical operations
- **Scikit-learn** — Machine-learning preprocessing, model training, and prediction
- **Joblib** — Saving and loading the trained model
- **Matplotlib / Seaborn** — Data visualization where used
- **Requests / BeautifulSoup** — Web-scraping demonstration where used in the notebook

---

## ⚙️ Run Locally

### 1. Install Python

Use a supported Python 3 version compatible with the versions of the libraries used to train and save the model. If deployment reports package compatibility issues, use a Python version supported by all required dependencies.

Check your installation:

```bash
python --version
```

On Windows, if `python` points to an older installation, try:

```powershell
python3 --version
```

### 2. Clone the repository

```bash
git clone https://github.com/<your-username>/RoadSafe-Analytics.git
cd RoadSafe-Analytics
```

Replace `<your-username>` with your GitHub username.

### 3. Create and activate a virtual environment (recommended)

**Windows PowerShell:**

```powershell
python3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If `python3` is not available, use a Python 3 launcher installed on your machine.

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 5. Add the required files

Place the model artifact next to `app.py`:

```text
road_accident_severity_classifier.joblib
```

Also place `Road.csv` beside `app.py` if you want the historical insights and dataset-based dropdown options to work.

**Important:** The saved artifact must match the current app's expected structure. The current app expects a dictionary containing at least:
- `model` — the fitted prediction pipeline/model
- `features` — the input feature names in the correct order

It may also contain `model_name`, `target`, `feature_options`, and `class_labels`.

### 6. Start Streamlit

```bash
python -m streamlit run app.py
```

On Windows, if Streamlit was installed using `python3`, you can also run:

```powershell
python3 -m streamlit run app.py
```

Streamlit will print a local URL, usually `http://localhost:8501`, which you can open in your browser.

---

## ☁️ Deploy to Streamlit Community Cloud

1. Push the application files to a GitHub repository.
2. Open [Streamlit Community Cloud](https://share.streamlit.io/).
3. Sign in with GitHub and choose **Create app**.
4. Select your repository and branch.
5. Set the main file path to `app.py`.
6. Deploy the app and inspect the deployment logs if an error occurs.

### Deployment checklist

- [ ] `app.py` is in the repository root, or the main-file path points to its location.
- [ ] `requirements.txt` lists the necessary packages.
- [ ] The model artifact exists at the path expected by `app.py`.
- [ ] The artifact was saved with a compatible Python / scikit-learn environment.
- [ ] `Road.csv` is included only if permitted and needed.
- [ ] The app works after a fresh restart.
- [ ] Input values are passed to the model in the same representation used during training.

**Large model files:** GitHub's regular upload interface has file-size limits. For large artifacts, use an appropriate Git LFS or external artifact-storage approach, and update the application to load the artifact from that location. Do not commit credentials or private tokens.

---

## 📊 Data and Interpretation

The app uses `Road.csv` as its working analysis dataset when that file is available beside `app.py`. The notebook may also demonstrate scraping from an official public data catalogue as a separate data-acquisition exercise.

Do not describe the scraped catalogue as the source of every row in `Road.csv` unless the data provenance actually confirms that. Include the source, licence, and attribution required by the dataset provider.

Before interpreting results:
- Check for missing values and duplicate records.
- Review the distribution of the target classes.
- Consider class imbalance when interpreting accuracy.
- Evaluate class-wise precision, recall, and F1-score in the notebook.
- Avoid interpreting associations as proof of causation.
- Make sure the test data was not used to train or tune the model.

---

## 🔒 Privacy and Responsible Use

- Do not commit personal, confidential, or restricted data.
- Do not include secrets, API keys, passwords, or access tokens in the repository.
- If publishing the repository, check whether the dataset licence permits redistribution.
- Predictions are educational estimates and may be wrong.
- Do not use this application to make emergency decisions or to claim that a specific condition caused an accident.

---

## 🧪 Troubleshooting

### `ModuleNotFoundError`
Install the dependencies from the project directory:

```bash
python -m pip install -r requirements.txt
```

### Streamlit command not found
Run Streamlit through Python:

```bash
python -m streamlit run app.py
```

### Model file not found
Ensure `road_accident_severity_classifier.joblib` is in the same directory as `app.py` and that the filename matches exactly.

### Prediction input error
The saved model and the app must use the same feature names, feature order, data types, category labels, and preprocessing steps as training. If the model was trained on encoded numeric categories, ensure the app encodes user selections using the same mappings or, preferably, loads a pipeline that performs preprocessing internally.

### Insights or dropdown options are missing
Ensure `Road.csv` is in the same directory as `app.py`, and verify that the expected columns exist in the dataset.

### Deployment fails
Open the hosting platform's logs and check the first traceback. A common cause is a mismatch between Python, scikit-learn, and the versions used to serialize the model.

---

## 🔮 Possible Future Improvements

- More accessible category labels and explanations on prediction results.
- Clearer visual explanations for the model output.
- Improved handling of encoded categories using saved preprocessing mappings.
- Dataset filters and additional historical visualizations.
- Model monitoring and version tracking.
- Automated tests for preprocessing and prediction inputs.

---

## 👩‍💻 Academic Project

**Project:** RoadSafe Analytics — Road Accident Severity Classification  
**Domain:** Statistical Inference, Data Analysis, and Machine Learning  
**Interface:** Streamlit  
**Prediction task:** Classification of recorded accident severity

Created for educational and academic demonstration.

---

## 📄 License

Add a license before publishing the repository. If you do not intend to grant reuse rights, do not add an open-source license without considering the implications. The dataset may have a separate licence from the source code.
