# 🛡️ ACRE Automated-Customer-Retention-Engine

[![Python Version](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30.0-ff69b4.svg)](https://streamlit.io)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.6.1-orange.svg)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**ACRE** is an end-to-end application that leverages machine learning to predict customer churn and automates the retention process. This tool provides an interactive interface to identify high-risk customers and triggers an intelligent workflow to proactively engage them with retention offers.

---

### ✨ Live Demo

> **[🚀 Access the live application here!](https://automated-customer-retention-engine-dtampjuzmwhjek9elakblf.streamlit.app/)** > 

## Key Features

- **🔮 Predictive Analytics:** Utilizes a trained Logistic Regression model to accurately predict the likelihood of a customer churning based on their service history and usage patterns.
- **💻 Interactive UI:** A user-friendly web interface built with Streamlit that allows for easy batch prediction by simply uploading a CSV file.
- **🤖 Automated Retention Workflow:** For customers identified as high-risk, the app can trigger an n8n webhook, initiating a custom workflow that can automatically send personalized retention emails, special offers, or create support tickets.
- **✅ High Performance:** The model is built on a robust Scikit-learn pipeline, ensuring efficient data preprocessing and reliable predictions.

- ## 🛠️ Tech Stack

- **Backend & Model:** Python, Scikit-learn, Pandas, Joblib
- **Frontend:** Streamlit
- **Automation:** n8n (via Webhooks)
- **Dataset:** [Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) from Kaggle.

## 📄 License

This project is licensed under the MIT License.

## ⚙️ System Workflow

```mermaid
graph TD
    A[User uploads CSV of customers] --> B{Streamlit UI};
    B --> C[Load Scikit-learn Model];
    C --> D{Predict Churn Likelihood};
    D -- If Churn is 'Yes' --> E[Display 'Send Retention Email' Button];
    D -- If Churn is 'No' --> F[Display 'No Action Needed'];
    E -- On Click --> G[Trigger n8n Webhook];
    G --> H(n8n Automation Engine);
    H --> I[Generate Personalized Email via AI];
    I --> J[Send Email to Customer];



