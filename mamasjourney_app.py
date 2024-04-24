import streamlit as st
from streamlit_timeline import st_timeline
import pandas as pd
from datetime import datetime, timedelta, date

# Page Configuration
st.set_page_config(page_title="mamasjourney", page_icon=':ship:', layout="wide",)

# Titel-Darstellung
st.title("mamasjourney :ship:")

# Funktion zur Berechnung des Geburtstermins
def calculate_due_date(last_period_date):
    gestation_period = timedelta(days=280)
    due_date = last_period_date + gestation_period
    return due_date

# Geburtstermin berechnen


# Timeline Darstellung und Berechnung der SSW
last_period_date = st.date_input('Letzter Menstruationszyklus' , format="YYYY/MM/DD")
if last_period_date:
    due_date = calculate_due_date(last_period_date)
    st.write("Voraussichtlicher Geburtstermin:", due_date)
    
if isinstance(last_period_date, date):
    week = timedelta(days=7)
    ssw2 = last_period_date + week
    ssw3 = ssw2 + week
    ssw4= ssw3 + week
    ssw5= ssw4 + week
    ssw6= ssw5 + week
    ssw7= ssw6 + week
    ssw8= ssw7 + week
    ssw9= ssw8 + week
    ssw10= ssw9 + week
    ssw11= ssw10 + week
    ssw12= ssw11 + week
    ssw13 = ssw12 + week
    ssw14= ssw13 + week
    ssw15= ssw14 + week
    ssw16= ssw15 + week
    ssw17= ssw16 + week
    ssw18= ssw17 + week
    ssw19= ssw18 + week
    ssw20= ssw19 + week
    ssw21= ssw20 + week
    ssw22= ssw21 + week
    ssw23= ssw22 + week
    ssw24= ssw23 + week
    ssw25= ssw24 + week
    ssw26= ssw25 + week
    ssw27= ssw26 + week
    ssw28= ssw27 + week
    ssw29= ssw28 + week
    ssw30= ssw29 + week
    ssw31= ssw30 + week
    ssw32= ssw31 + week
    ssw33= ssw32 + week
    ssw34= ssw33 + week
    ssw35= ssw34 + week
    ssw36= ssw35 + week
    ssw37= ssw36 + week
    ssw38= ssw37 + week
    ssw39= ssw38 + week
    ssw40= ssw39 + week
    ssw41= ssw40 + week
    ssw42= ssw41 + week
else:
    st.write("Bitte wählen Sie ein Datum aus.")

items = [
    {
        "id": "a",
        "content": "1.Trimester",
        "start": str(last_period_date),
        "end": str(ssw13),
        "type": "background"
    },
    {"id": 1, "content": "SSW1", "start": str(last_period_date)},
    {"id": 2, "content": "SSW2", "start": str(ssw2)},
    {"id": 3, "content": "SSW3", "start": str(ssw3)},
    {"id": 4, "content": "SSW4", "start": str(ssw4)},
    {"id": 5, "content": "SSW5", "start": str(ssw5)},
    {"id": 6, "content": "SSW6", "start": str(ssw6)},
    {"id": 7, "content": "SSW7", "start": str(ssw7)},
    {"id": 8, "content": "SSW8", "start": str(ssw8)},
    {"id": 9, "content": "SSW9", "start": str(ssw9)},
    {"id": 10, "content": "SSW10", "start": str(ssw10)},
    {"id": 11, "content": "SSW11", "start": str(ssw11)},
    {"id": 12, "content": "SSW12", "start": str(ssw12)},
    {"id": 13, "content": "SSW13", "start": str(ssw13)},
    {"id": 14, "content": "SSW14", "start": str(ssw14)},
    {"id": 15, "content": "SSW15", "start": str(ssw15)},
    {"id": 16, "content": "SSW16", "start": str(ssw16)},
    {"id": 17, "content": "SSW17", "start": str(ssw17)},
    {"id": 18, "content": "SSW18", "start": str(ssw18)},
    {"id": 19, "content": "SSW19", "start": str(ssw19)},
    {"id": 20, "content": "SSW20", "start": str(ssw20)},
    {"id": 21, "content": "SSW21", "start": str(ssw21)},
    {"id": 22, "content": "SSW22", "start": str(ssw22)},
    {"id": 23, "content": "SSW23", "start": str(ssw23)},
    {"id": 24, "content": "SSW24", "start": str(ssw24)},
    {"id": 25, "content": "SSW25", "start": str(ssw25)},
    {"id": 26, "content": "SSW26", "start": str(ssw26)},
    {"id": 27, "content": "SSW27", "start": str(ssw27)},
    {"id": 28, "content": "SSW28", "start": str(ssw28)},
    {"id": 29, "content": "SSW29", "start": str(ssw29)},
    {"id": 30, "content": "SSW30", "start": str(ssw30)},
    {"id": 31, "content": "SSW31", "start": str(ssw31)},
    {"id": 32, "content": "SSW32", "start": str(ssw32)},
    {"id": 33, "content": "SSW33", "start": str(ssw33)}
]

timeline = st_timeline(items, groups=[],options={},height= '250px')
st.subheader('Ausgewählte Woche')
st.write(timeline)

# Dummy-Daten für den DataFrame
data = {
    'Bauelement': ['Baby', 'Mama', 'Notizen'],
    'Gewicht': [57, 60, 62],
    'Blutwerte': ['Normal', 'Erhöht', 'Normal']
}

# DataFrame erstellen
df = pd.DataFrame(data)

# Eingabefeld für das Datum des letzten Menstruationszyklus
last_period_date = st.date_input("Datum des letzten Menstruationszyklus:")

# Übersicht über Bauelemente, Gewicht und Blutwerte
st.header('Übersicht')
st.write('Schwangerschaftsbauelemente, Gewicht und Blutwerte')
st.write(df)


st.subheader('Mamas Tagebuch')
st.text_area('Notieren Sie ihre Erkenntnisse', value='Hier tippen')
