# 🏠 Karachi House Price Predictor

**A Machine Learning-powered web application that estimates apartment prices in Karachi based on real-time market data.**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://[https://share.streamlit.io/user/muhammad-mujtaba-git])

### 🚀 Try the Live App
Click the badge above or visit: **[https://karachi-house-price-predictor-reva3zn2gqez2ij5ftt5et.streamlit.app/]**

---

### 🧐 Project Overview
Predicting real estate prices in Karachi is difficult due to extreme variance in neighborhoods (e.g., DHA vs. Surjani Town) and messy data formats. This project solves that using a **Ridge Regression** model trained on property listings. It features a custom-built cleaning pipeline that handles local currency units (`Lakh`, `Crore`) and extracts granular location data (Phases, Blocks, Precincts) for high precision.

### ✨ Key Features
* **Smart Location Parsing:** Automatically extracts specific "Phases", "Blocks", or "Precincts" from addresses to distinguish between luxury and standard areas (e.g., differentiating *DHA Phase 6* from *DHA Phase 1*).
* **Currency Normalization:** Custom logic to parse and convert mixed text inputs like "1 Crore 50 Lakh" into usable integers.
* **Outlier Removal:** Implemented strict filtering to remove "garbage data" (prices < 1 Lakh) that was causing negative predictions in earlier iterations.
* **Interactive Web UI:** Built with **Streamlit** to allow users to input their own criteria and get instant price estimates.

### 📊 Model Performance
* **Algorithm:** Ridge Regression (L2 Regularization)
* **Training MAE:** ~20.4 Lakhs PKR
* **Test MAE:** ~20.9 Lakhs PKR
* **Accuracy:** The close gap between Training and Test error indicates a robust model with minimal overfitting. It significantly outperforms the baseline error of ~1.37 Crore.

### 🛠️ Tech Stack
* **Python 3.9**
* **Scikit-Learn** (Model & Pipeline)
* **Pandas & NumPy** (Data Manipulation)
* **Streamlit** (Frontend Deployment)
* **Category Encoders** (OneHotEncoding for neighborhoods)

### ⚙️ How to Run Locally

1. **Clone the repo:**
   ```bash
   git clone [https://github.com/](https://github.com/)[Muhammad-Mujtaba-Git]/[Karachi-House-Price-Predictor].git
   cd [Karachi-House-Price-Predictor]