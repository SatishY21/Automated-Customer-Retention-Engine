import streamlit as st
import pandas as pd
import joblib
import requests  # <-- Import the requests library
import io

# --- n8n Webhook Configuration ---
# IMPORTANT: Replace this with the Test URL from your n8n Webhook node
N8N_WEBHOOK_URL = "https://your-n8n-instance.com/webhook-test/your-unique-path"

# Function to load the model
@st.cache_resource
def load_model():
    try:
        model = joblib.load('churn_model.joblib')
        return model
    except FileNotFoundError:
        st.error("Model file ('churn_model.joblib') not found. Please ensure it's in the same directory.")
        return None

# Function to trigger the n8n retention workflow
def trigger_retention_workflow(customer_email):
    """Sends the customer's email to the n8n webhook."""
    st.info(f"Triggering retention workflow for {customer_email}...")
    
    # The data payload to send. n8n will receive this as JSON.
    payload = {'email': customer_email}
    
    try:
        response = requests.post(N8N_WEBHOOK_URL, json=payload)
        
        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            st.success(f"Successfully sent retention signal for {customer_email}!")
            st.balloons()
        else:
            st.error(f"Failed to trigger workflow. Status code: {response.status_code}")
            st.code(response.text) # Show error details from n8n if any
            
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while trying to contact the n8n webhook.")
        st.code(str(e))


# --- Streamlit App UI ---
st.set_page_config(layout="wide", page_title="Customer Churn Predictor")
st.title("🚀 Customer Churn Prediction & Retention")
st.write("Upload a CSV file with customer data to predict churn. For customers likely to churn, you can trigger an automated retention email workflow via n8n.")

model = load_model()

if model:
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            # Read the uploaded file into a DataFrame
            customers_df = pd.read_csv(uploaded_file)
            st.write("Uploaded Data Preview:")
            st.dataframe(customers_df.head())

            # Ensure the required columns are present
            required_features = model.named_steps['preprocessor'].feature_names_in_
            
            # Check if an 'email' column exists for the retention workflow
            has_email_column = 'email' in customers_df.columns
            if not has_email_column:
                st.warning("The uploaded CSV does not contain an 'email' column. The retention feature will be disabled.")
            
            # Make predictions
            predictions = model.predict(customers_df)
            prediction_proba = model.predict_proba(customers_df)[:, 1]

            # Create results DataFrame
            results_df = customers_df.copy()
            results_df['Churn Prediction'] = ['Yes' if p == 1 else 'No' for p in predictions]
            results_df['Churn Probability (%)'] = [f"{p*100:.2f}%" for p in prediction_proba]
            
            st.subheader("Prediction Results")
            st.dataframe(results_df)

            # Display retention options for churners
            churners = results_df[results_df['Churn Prediction'] == 'Yes']
            if not churners.empty:
                st.subheader("⚠️ High-Risk Customers Identified")
                st.write("The following customers are likely to churn. You can trigger a retention email workflow for them.")
                
                for index, row in churners.iterrows():
                    # Use a unique key for each button based on the row index
                    button_key = f"button_{index}"
                    
                    if has_email_column:
                        customer_email = row.get('email', 'N/A')
                        if pd.notna(customer_email):
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.write(f"**Customer Email:** {customer_email} (**Probability:** {row['Churn Probability (%)']})")
                            with col2:
                                if st.button(f"Send Retention Email", key=button_key):
                                    trigger_retention_workflow(customer_email)
                        else:
                            st.write(f"Customer at index {index} has no email address provided.")
                    else:
                        st.write(f"Customer at index {index} (No email column in source file)")

        except Exception as e:
            st.error(f"An error occurred while processing the file: {e}")

