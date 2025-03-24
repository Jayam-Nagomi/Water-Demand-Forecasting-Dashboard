
# Water Demand Prediction Using LSTM

## Overview
This project implements a Long Short-Term Memory (LSTM) model to predict water demand based on historical data of **reservoir levels, groundwater levels, and rainfall** in the **Cauvery Basin** for the year 2023. The model forecasts future demand and provides insights through an interactive **Streamlit dashboard**.

## Features
- **LSTM-based Prediction Model**: A sequential deep learning model trained on time-series data.
- **Data Processing**: Includes exploratory data analysis (EDA) and preprocessing steps.
- **Evaluation Metrics**: Uses **Mean Squared Error (MSE), Root Mean Squared Error (RMSE), and Mean Absolute Error (MAE)**.
- **Interactive Dashboard**: Built with **Streamlit**, displaying visualizations and key insights.
- **Deployment**: Hosted on **Streamlit Community Cloud**.

## Project Structure
```
📂 project_root/
│── 📁 .streamlit/          # Streamlit configuration files
│── 📁 pages/               # Additional pages for the Streamlit app
│── 📄 source_code.ipynb    # Contains model implementation, preprocessing, EDA, prediction, and testing scripts
│── 📄 Data.csv             # Dataset containing water-related data
│── 📄 Home.py              # Main script for launching the Streamlit app
│── 📄 model.keras          # Trained LSTM model file
│── 📄 requirements.txt     # Dependencies for running the project
│── 📄 README.md            # Project documentation
```

## Installation
1. **Clone the repository:**
   ```sh
   git clone https://github.com/Jayam-Nagomi/Water-Demand-Forecasting-Dashboard
   cd Water-Demand-Forecasting-Dashboard
   ```
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Run the Streamlit dashboard:**
   ```sh
   streamlit run app.py
   ```

## Model Architecture
```python
model = Sequential([
    LSTM(64, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])),
    LSTM(32, return_sequences=False),
    Dense(y_train.shape[1])
])
```
- **Optimizer**: Adam
- **Loss Function**: MSE
- **Regularization**: Early stopping & checkpointing
- **Training Data Split**: Training & validation sets

## Deployment
The Streamlit app is deployed on **Streamlit Community Cloud**. If inactive, it may go to sleep but wakes up when accessed.

[Click here to access the app](https://water-demand-forecasting.streamlit.app/)
