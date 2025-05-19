import streamlit as st
import pandas as pd
import joblib
import io
import matplotlib.pyplot as plt

# Load model and scaler
model = joblib.load('xgb_model.pkl')
scaler = joblib.load('scaler.pkl')

# Required columns for validation
required_columns = [
    "Marital_status",
    "Application_mode",
    "Application_order",
    "Course",
    "Daytime_evening_attendance",
    "Previous_qualification",
    "Previous_qualification_grade",
    "Nacionality",
    "Mothers_qualification",
    "Fathers_qualification",
    "Mothers_occupation",
    "Fathers_occupation",
    "Admission_grade",
    "Displaced",
    "Educational_special_needs",
    "Debtor",
    "Tuition_fees_up_to_date",
    "Gender",
    "Scholarship_holder",
    "Age_at_enrollment",
    "International",
    "Curricular_units_1st_sem_credited",
    "Curricular_units_1st_sem_enrolled",
    "Curricular_units_1st_sem_evaluations",
    "Curricular_units_1st_sem_approved",
    "Curricular_units_1st_sem_grade",
    "Curricular_units_1st_sem_without_evaluations",
    "Curricular_units_2nd_sem_evaluations",
    "Curricular_units_2nd_sem_grade",
    "Curricular_units_2nd_sem_without_evaluations",
    "Unemployment_rate",
    "Inflation_rate",
    "GDP",
    "Status"
]

custom_columns = [
    "Previous_qualification_grade",
    "Admission_grade",
    "Age_at_enrollment",
    "Curricular_units_1st_sem_credited",
    "Curricular_units_1st_sem_enrolled",
    "Curricular_units_1st_sem_evaluations",
    "Curricular_units_1st_sem_approved",
    "Curricular_units_1st_sem_grade",
    "Curricular_units_1st_sem_without_evaluations",
    "Curricular_units_2nd_sem_evaluations",
    "Curricular_units_2nd_sem_grade",
    "Curricular_units_2nd_sem_without_evaluations",
    "Unemployment_rate",
    "Inflation_rate",
    "GDP",
    "Course_33",
    "Course_171",
    "Course_8014",
    "Course_9003",
    "Course_9070",
    "Course_9085",
    "Course_9119",
    "Course_9130",
    "Course_9147",
    "Course_9238",
    "Course_9254",
    "Course_9500",
    "Course_9556",
    "Course_9670",
    "Course_9773",
    "Course_9853",
    "Course_9991",
    "Marital_status_1",
    "Marital_status_2",
    "Marital_status_4",
    "Marital_status_5",
    "Marital_status_6",
    "Application_mode_1",
    "Application_mode_5",
    "Application_mode_7",
    "Application_mode_10",
    "Application_mode_15",
    "Application_mode_16",
    "Application_mode_17",
    "Application_mode_18",
    "Application_mode_39",
    "Application_mode_42",
    "Application_mode_43",
    "Application_mode_44",
    "Application_mode_51",
    "Application_mode_53",
    "Application_order_1",
    "Application_order_2",
    "Application_order_3",
    "Application_order_4",
    "Application_order_5",
    "Application_order_6",
    "Daytime_evening_attendance_0",
    "Previous_qualification_1",
    "Previous_qualification_2",
    "Previous_qualification_3",
    "Previous_qualification_4",
    "Previous_qualification_6",
    "Previous_qualification_9",
    "Previous_qualification_10",
    "Previous_qualification_12",
    "Previous_qualification_19",
    "Previous_qualification_38",
    "Previous_qualification_40",
    "Previous_qualification_43",
    "Nacionality_1",
    "Nacionality_6",
    "Nacionality_22",
    "Nacionality_24",
    "Nacionality_26",
    "Nacionality_41",
    "Mothers_qualification_1",
    "Mothers_qualification_2",
    "Mothers_qualification_3",
    "Mothers_qualification_4",
    "Mothers_qualification_5",
    "Mothers_qualification_6",
    "Mothers_qualification_9",
    "Mothers_qualification_12",
    "Mothers_qualification_19",
    "Mothers_qualification_34",
    "Mothers_qualification_37",
    "Mothers_qualification_38",
    "Mothers_qualification_39",
    "Mothers_qualification_40",
    "Mothers_qualification_41",
    "Mothers_qualification_42",
    "Fathers_qualification_1",
    "Fathers_qualification_2",
    "Fathers_qualification_3",
    "Fathers_qualification_4",
    "Fathers_qualification_5",
    "Fathers_qualification_9",
    "Fathers_qualification_11",
    "Fathers_qualification_12",
    "Fathers_qualification_14",
    "Fathers_qualification_19",
    "Fathers_qualification_22",
    "Fathers_qualification_34",
    "Fathers_qualification_36",
    "Fathers_qualification_37",
    "Fathers_qualification_38",
    "Fathers_qualification_39",
    "Fathers_qualification_40",
    "Mothers_occupation_0",
    "Mothers_occupation_1",
    "Mothers_occupation_2",
    "Mothers_occupation_3",
    "Mothers_occupation_4",
    "Mothers_occupation_5",
    "Mothers_occupation_6",
    "Mothers_occupation_7",
    "Mothers_occupation_8",
    "Mothers_occupation_9",
    "Mothers_occupation_90",
    "Mothers_occupation_99",
    "Mothers_occupation_123",
    "Mothers_occupation_141",
    "Mothers_occupation_144",
    "Mothers_occupation_191",
    "Mothers_occupation_193",
    "Mothers_occupation_194",
    "Fathers_occupation_0",
    "Fathers_occupation_1",
    "Fathers_occupation_2",
    "Fathers_occupation_3",
    "Fathers_occupation_4",
    "Fathers_occupation_5",
    "Fathers_occupation_6",
    "Fathers_occupation_7",
    "Fathers_occupation_8",
    "Fathers_occupation_9",
    "Fathers_occupation_10",
    "Fathers_occupation_90",
    "Fathers_occupation_99",
    "Fathers_occupation_144",
    "Fathers_occupation_192",
    "Fathers_occupation_193",
    "Displaced_0",
    "Educational_special_needs_0",
    "Debtor_0",
    "Tuition_fees_up_to_date_0",
    "Gender_0",
    "Scholarship_holder_0"
]

st.title("Dropout Prediction - Jaya Jaya Institute")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, delimiter=';')

    # Only keep enrolled students for prediction
    df = df[df['Status'] == 'Enrolled']

    # Validate presence of required columns
    if not all(col in df.columns for col in required_columns):
        st.error("CSV file must contain all required columns.")
    else:
        # Prepare features
        X = df.drop(columns=['Status'])

        # Identify text columns for one-hot encoding
        text_columns = list(X.select_dtypes(include=['object']).columns)
        label_columns = [
            'Course', 'Marital_status', 'Application_mode', 'Application_order',
            'Daytime_evening_attendance', 'Previous_qualification', 'Nacionality',
            'Mothers_qualification', 'Fathers_qualification', 'Mothers_occupation',
            'Fathers_occupation', 'Displaced', 'Educational_special_needs', 'Debtor',
            'Tuition_fees_up_to_date', 'Gender', 'Scholarship_holder', 'International'
        ]
        text_columns.extend(label_columns)

        for col in text_columns:
            dummies = pd.get_dummies(X[col].astype('object'), prefix=col).astype(int)
            X = pd.concat([X, dummies], axis=1)
            X.drop(columns=[col], inplace=True)

        # Ensure all custom columns exist
        for col in custom_columns:
            if col not in X.columns:
                X[col] = 0
        X = X[custom_columns]

        # Scale and predict
        X_scaled = scaler.transform(X)
        y_pred = model.predict(X_scaled)
        df['PredictedDropout'] = y_pred

        # Map prediction to labels
        df['Status'] = df['PredictedDropout'].apply(lambda x: 'Graduate' if x == 1 else 'Dropout')

        # Filter by status
        selected = st.selectbox('Filter Status', ['Dropout', 'Graduate'])
        df_filtered = df[df['Status'] == selected]

        # Metrics: dropout count, dropout rate, total students
        total = len(df)
        dropouts = int((df['Status'] == 'Dropout').sum())
        rate = (dropouts / total) * 100 if total > 0 else 0
        c1, c2, c3 = st.columns(3)
        c1.metric('Dropout Count', dropouts)
        c2.metric('Dropout Rate', f'{rate:.2f}%')
        c3.metric('Total Students', total)

        # Mapping dictionaries
        prev_map = {
            1: 'Secondary education',
            2: 'Higher education - bachelor\'s degree',
            3: 'Higher education - degree',
            4: 'Higher education - master\'s',
            5: 'Higher education - doctorate',
            6: 'Frequency of higher education',
            9: '12th year of schooling - not completed',
            10: '11th year of schooling - not completed',
            12: 'Other - 11th year of schooling',
            14: '10th year of schooling',
            15: '10th year of schooling - not completed',
            19: 'Basic education 3rd cycle (9th/10th/11th)',
            38: 'Basic education 2nd cycle (6th/7th/8th)',
            39: 'Technological specialization course',
            40: 'Higher education - degree (1st cycle)',
            42: 'Professional higher technical course',
            43: 'Higher education - master (2nd cycle)'
        }
        nat_map = {
            1: 'Portuguese', 2: 'German', 6: 'Spanish', 11: 'Italian',
            13: 'Dutch', 14: 'English', 17: 'Lithuanian', 21: 'Angolan', 22: 'Cape Verdean',
            24: 'Guinean', 25: 'Mozambican', 26: 'Santomean', 32: 'Turkish',
            41: 'Brazilian', 62: 'Romanian', 100: 'Moldova (Republic of)',
            101: 'Mexican', 103: 'Ukrainian', 105: 'Russian', 108: 'Cuban', 109: 'Colombian'
        }

        # Charts side by side
        col1, col2, col3 = st.columns(3)

        # Pie chart: Previous Qualification with "Others"
        with col1:
            df_filtered['PrevLabel'] = df_filtered['Previous_qualification'].map(prev_map)
            counts = df_filtered['PrevLabel'].value_counts()
            top3 = counts.nlargest(3)
            others = counts.sum() - top3.sum()
            display_counts = pd.concat([top3, pd.Series({'Others': others})])
            fig1, ax1 = plt.subplots()
            ax1.pie(display_counts, labels=None, autopct='%1.1f%%')
            ax1.set_title('Previous Qualification')
            ax1.legend(display_counts.index, loc='best')
            st.pyplot(fig1)

        # Histogram: Age at Enrollment by Gender
        with col2:
            male_ages = df_filtered[df_filtered['Gender'] == 1]['Age_at_enrollment']
            female_ages = df_filtered[df_filtered['Gender'] == 0]['Age_at_enrollment']
            fig2, ax2 = plt.subplots()
            ax2.hist([male_ages, female_ages], bins=8, label=['Male', 'Female'])
            ax2.set_xlabel('Age at Enrollment')
            ax2.set_ylabel('Count')
            ax2.legend()
            ax2.set_title('Age at Enrollment by Gender')
            st.pyplot(fig2)

        # Pie chart: Nationality with "Others"
        with col3:
            df_filtered['NatLabel'] = df_filtered['Nacionality'].map(nat_map)
            counts_n = df_filtered['NatLabel'].value_counts()
            top3_n = counts_n.nlargest(3)
            others_n = counts_n.sum() - top3_n.sum()
            display_counts_n = pd.concat([top3_n, pd.Series({'Others': others_n})])
            fig3, ax3 = plt.subplots()
            ax3.pie(display_counts_n, labels=None, autopct='%1.1f%%')
            ax3.set_title('Nationality')
            ax3.legend(display_counts_n.index, loc='best')
            st.pyplot(fig3)

        # Display filtered data and download
        st.dataframe(df_filtered)
        csv = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label='Download Prediction Result',
            data=csv,
            file_name='predicted_dropout.csv',
            mime='text/csv'
        )
