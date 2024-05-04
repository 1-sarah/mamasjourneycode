import yaml
import streamlit as st
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities.exceptions import (CredentialsError,
                                                          ForgotError,
                                                          LoginError,
                                                          RegisterError,
                                                          ResetError,
                                                          UpdateError) 
from streamlit_timeline import timeline
import pandas as pd
from datetime import datetime, timedelta, date
from github_contents import GithubContents

# Page Configuration
st.set_page_config(page_title="mamasjourney", page_icon=':ship:', layout="wide",)

# Verbindung zu GitHub initialisieren
github = GithubContents("ratnasha", "FirstApp-data", "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")

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login()
if authentication_status:
    authenticator.logout('Logout', 'main')
    if username == 'mama1':
        st.write(f'Welcome *{name}*')
        # Funktion zum Laden des Datums aus der JSON-Datei
        def load_last_period_date():
            try:
                data = github.read_json("last_period_date.json")
                last_period_date = pd.to_datetime(data["last_period_date"])
            except:
                last_period_date = None
            return last_period_date

        # Funktion zum Speichern des Datums in der JSON-Datei
        def save_last_period_date(date):
            github.write_json("last_period_date.json", {"last_period_date": date.strftime("%Y-%m-%d")}, "Save last period date")

        # Funktion zur Berechnung des Geburtstermins
        def calculate_due_date(last_period_date):
            gestation_period = timedelta(days=280)
            due_date = last_period_date + gestation_period
            return due_date

        # Funktion zur Erstellung der Timeline-Items
        def create_timeline_items(last_period_date):
            items = []
            week = timedelta(days=7)
            for i in range(1, 41):
                ssw = last_period_date + i * week
                items.append({"id": i, "content": f"SSW {i}", "start": str(ssw)})
            return items

        # Titel-Darstellung
        st.title("mamasjourney :ship:")

        # Laden des letzten Menstruationszyklus-Datums aus der JSON-Datei
        last_period_date = load_last_period_date()

        # Eingabefeld für das Datum des letzten Menstruationszyklus
        if last_period_date is not None:
            last_period_date = st.date_input('Letzter Menstruationszyklus', value=last_period_date, format="YYYY/MM/DD")
        else:
            last_period_date = st.date_input('Letzter Menstruationszyklus', format="YYYY/MM/DD")

        # Geburtstermin berechnen und Timeline erstellen
        if last_period_date:
            due_date = calculate_due_date(last_period_date)
            st.write("Voraussichtlicher Geburtstermin:", due_date)
            timeline_items = create_timeline_items(last_period_date)
            st.subheader('Schwangerschafts-Timeline')
            timeline(timeline_items, height='250')
        st.header('Mama')
        st.write('Gewicht')
        mama_weight_date = st.date_input("Datum", value=datetime.today(), min_value=last_period_date, max_value=datetime.today(), format="YYYY/MM/DD")
        mama_weight = st.number_input("Gewicht (kg)", min_value=0.0)
        if st.button("Gewicht speichern"):
            # Neuer DataFrame für das aktuelle Gewicht erstellen
            new_row = pd.DataFrame({"Date": [mama_weight_date], "Weight": [mama_weight]})
            if github.file_exists("mama_weights.csv"):
                # CSV-Datei existiert bereits, lade sie und füge die neue Zeile hinzu
                mama_weights_df = github.read_df("mama_weights.csv")
                mama_weights_df = pd.concat([mama_weights_df, new_row], ignore_index=True)
            else:
                # CSV-Datei existiert nicht, erstelle eine neue mit der neuen Zeile
                mama_weights_df = new_row.copy()

            # Speichere den aktualisierten DataFrame in der CSV-Datei
            github.write_df("mama_weights.csv", mama_weights_df, "Save mama weight")

        st.subheader('Mama Gewichtsdaten')
        if github.file_exists("mama_weights.csv"):
            mama_weights_df = github.read_df("mama_weights.csv")
            st.write(mama_weights_df)
        else:
            st.write("Noch keine Gewichtsdaten vorhanden.")

        st.write('Blutwert')

        blutwerte_text = st.text_area("Blutwerte")
        if st.button("Blutwert speichern"):
            # Neuer DataFrame für das aktuelle Blutwert erstellen
            new_row = pd.DataFrame({"Date": [mama_weight_date], "Blutwert": [blutwerte_text]})
            if github.file_exists("mama_blutwert.csv"):
                # CSV-Datei existiert bereits, lade sie und füge die neue Zeile hinzu
                mama_blutwert_df = github.read_df("mama_blutwert.csv")
                mama_blutwert_df = pd.concat([mama_blutwert_df, new_row], ignore_index=True)
            else:
                # CSV-Datei existiert nicht, erstelle eine neue mit der neuen Zeile
                mama_blutwert_df = new_row.copy()

            # Speichere den aktualisierten DataFrame in der CSV-Datei
            github.write_df("mama_blutwert.csv", mama_blutwert_df, "Save mama Blutwert")

        st.subheader('Mama Blutwert')
        if github.file_exists("mama_blutwert.csv"):
            mama_blutwert_df = github.read_df("mama_blutwert.csv")
            st.write(mama_blutwert_df)
        else:
            st.write("Noch keine Blutwerte vorhanden.")

        st.header('Baby')
        st.write('Ideen Name')

        baby_name_text = st.text_area("Babyname")
        if st.button("Name speichern"):
            # Neuer DataFrame für das aktuelle Blutwert erstellen
            new_row = pd.DataFrame({"Date": [mama_weight_date], "Babyname": [baby_name_text]})
            if github.file_exists("baby_name.csv"):
                # CSV-Datei existiert bereits, lade sie und füge die neue Zeile hinzu
                mama_babyname_df = github.read_df("baby_name.csv")
                mama_babyname_df = pd.concat([mama_babyname_df, new_row], ignore_index=True)
            else:
                # CSV-Datei existiert nicht, erstelle eine neue mit der neuen Zeile
                mama_babyname_df = new_row.copy()

            # Speichere den aktualisierten DataFrame in der CSV-Datei
            github.write_df("baby_name.csv", mama_babyname_df, "Save mama Blutwert")

        st.subheader('Baby Name')
        if github.file_exists("baby_name.csv"):
            mama_babyname_df = github.read_df("baby_name.csv")
            st.write(mama_babyname_df)
        else:
            st.write("Noch keine Blutwerte vorhanden.")

        st.header('Tagebuch')

        tagebuch_text = st.text_area("Tagebuch")
        if st.button("Eintrag speichern"):
            # Neuer DataFrame für das aktuelle Blutwert erstellen
            new_row = pd.DataFrame({"Date": [mama_weight_date], "Tagebuch": [tagebuch_text]})
            if github.file_exists("tagebuch.csv"):
                # CSV-Datei existiert bereits, lade sie und füge die neue Zeile hinzu
                tagebuch_df = github.read_df("tagebuch.csv")
                tagebuch_df = pd.concat([tagebuch_df, new_row], ignore_index=True)
            else:
                # CSV-Datei existiert nicht, erstelle eine neue mit der neuen Zeile
                tagebuch_df = new_row.copy()

            # Speichere den aktualisierten DataFrame in der CSV-Datei
            github.write_df("tagebuch.csv", tagebuch_df, "Save mama Blutwert")

        st.subheader('Tagebuch')
        if github.file_exists("tagebuch.csv"):
            tagebuch_df = github.read_df("tagebuch.csv")
            st.write(tagebuch_df)
        else:
            st.write("Noch keine Blutwerte vorhanden.")
    elif username == 'mama2':
        st.write(f'Welcome *{name}*')
        # Funktion zum Laden des Datums aus der JSON-Datei
        def load_last_period_date_mama2():
            try:
                data = github.read_json("last_period_date_mama2.json")
                last_period_date_mama2 = pd.to_datetime(data["last_period_date"])
            except:
                last_period_date_mama2 = None
            return last_period_date_mama2

        # Funktion zum Speichern des Datums in der JSON-Datei
        def save_last_period_date_mama2(date):
            github.write_json("last_period_date_mama2.json", {"last_period_date": date.strftime("%Y-%m-%d")}, "Save last period date")

        # Funktion zur Berechnung des Geburtstermins
        def calculate_due_date_mama2(last_period_date_mama2):
            gestation_period = timedelta(days=280)
            due_date_mama2 = last_period_date_mama2 + gestation_period
            return due_date_mama2

        # Funktion zur Erstellung der Timeline-Items
        def create_timeline_items_mama2(last_period_date_mama2):
            items_mama2 = []
            week = timedelta(days=7)
            for i in range(1, 41):
                ssw = last_period_date_mama2 + i * week
                items_mama2.append({"id": i, "content": f"SSW {i}", "start": str(ssw)})
            return items_mama2

        # Titel-Darstellung
        st.title("mamasjourney :ship:")

        # Laden des letzten Menstruationszyklus-Datums aus der JSON-Datei
        last_period_date_mama2 = load_last_period_date_mama2()

        # Eingabefeld für das Datum des letzten Menstruationszyklus
        if last_period_date_mama2 is not None:
            last_period_date_mama2 = st.date_input('Letzter Menstruationszyklus', value=last_period_date_mama2, format="YYYY/MM/DD")
        else:
            last_period_date_mama2 = st.date_input('Letzter Menstruationszyklus', format="YYYY/MM/DD")

        # Geburtstermin berechnen und Timeline erstellen
        if last_period_date_mama2:
            due_date_mama2 = calculate_due_date_mama2(last_period_date_mama2)
            st.write("Voraussichtlicher Geburtstermin:", due_date_mama2)
            timeline_items = create_timeline_items_mama2(last_period_date_mama2)
            st.subheader('Schwangerschafts-Timeline')
            timeline = timeline(timeline_items, height='250')
            st.subheader('Ausgewählte Woche')
            st.write(timeline)
        st.header('Mama')
        st.write('Gewicht')
        mama_weight_date = st.date_input("Datum", value=datetime.today(), min_value=last_period_date_mama2, max_value=datetime.today(), format="YYYY/MM/DD")
        mama_weight = st.number_input("Gewicht (kg)", min_value=0.0)
        if st.button("Gewicht speichern"):
            # Neuer DataFrame für das aktuelle Gewicht erstellen
            new_row = pd.DataFrame({"Date": [mama_weight_date], "Weight": [mama_weight]})
            if github.file_exists("mama_weights_mama2.csv"):
                # CSV-Datei existiert bereits, lade sie und füge die neue Zeile hinzu
                mama_weights_df = github.read_df("mama_weights_mama2.csv")
                mama_weights_df = pd.concat([mama_weights_df, new_row], ignore_index=True)
            else:
                # CSV-Datei existiert nicht, erstelle eine neue mit der neuen Zeile
                mama_weights_df = new_row.copy()

            # Speichere den aktualisierten DataFrame in der CSV-Datei
            github.write_df("mama_weights_mama2.csv", mama_weights_df, "Save mama weight")

        st.subheader('Mama Gewichtsdaten')
        if github.file_exists("mama_weights_mama2.csv"):
            mama_weights_df = github.read_df("mama_weights_mama2.csv")
            st.write(mama_weights_df)
        else:
            st.write("Noch keine Gewichtsdaten vorhanden.")

        st.write('Blutwert')

        blutwerte_text = st.text_area("Blutwerte")
        if st.button("Blutwert speichern"):
            # Neuer DataFrame für das aktuelle Blutwert erstellen
            new_row = pd.DataFrame({"Date": [mama_weight_date], "Blutwert": [blutwerte_text]})
            if github.file_exists("mama_blutwert_mama2.csv"):
                # CSV-Datei existiert bereits, lade sie und füge die neue Zeile hinzu
                mama_blutwert_df = github.read_df("mama_blutwert_mama2.csv")
                mama_blutwert_df = pd.concat([mama_blutwert_df, new_row], ignore_index=True)
            else:
                # CSV-Datei existiert nicht, erstelle eine neue mit der neuen Zeile
                mama_blutwert_df = new_row.copy()

            # Speichere den aktualisierten DataFrame in der CSV-Datei
            github.write_df("mama_blutwert_mama2.csv", mama_blutwert_df, "Save mama Blutwert")

        st.subheader('Mama Blutwert')
        if github.file_exists("mama_blutwert_mama2.csv"):
            mama_blutwert_df = github.read_df("mama_blutwert_mama2.csv")
            st.write(mama_blutwert_df)
        else:
            st.write("Noch keine Blutwerte vorhanden.")

        st.header('Baby')
        st.write('Ideen Name')

        baby_name_text = st.text_area("Babyname")
        if st.button("Name speichern"):
            # Neuer DataFrame für das aktuelle Blutwert erstellen
            new_row = pd.DataFrame({"Date": [mama_weight_date], "Babyname": [baby_name_text]})
            if github.file_exists("baby_name_mama2.csv"):
                # CSV-Datei existiert bereits, lade sie und füge die neue Zeile hinzu
                mama_babyname_df = github.read_df("baby_name_mama2.csv")
                mama_babyname_df = pd.concat([mama_babyname_df, new_row], ignore_index=True)
            else:
                # CSV-Datei existiert nicht, erstelle eine neue mit der neuen Zeile
                mama_babyname_df = new_row.copy()

            # Speichere den aktualisierten DataFrame in der CSV-Datei
            github.write_df("baby_name_mama2.csv", mama_babyname_df, "Save mama Blutwert")

        st.subheader('Baby Name')
        if github.file_exists("baby_name_mama2.csv"):
            mama_babyname_df = github.read_df("baby_name_mama2.csv")
            st.write(mama_babyname_df)
        else:
            st.write("Noch keine Blutwerte vorhanden.")

        st.header('Tagebuch')

        tagebuch_text = st.text_area("Tagebuch")
        if st.button("Eintrag speichern"):
            # Neuer DataFrame für das aktuelle Blutwert erstellen
            new_row = pd.DataFrame({"Date": [mama_weight_date], "Tagebuch": [tagebuch_text]})
            if github.file_exists("tagebuch_mama2.csv"):
                # CSV-Datei existiert bereits, lade sie und füge die neue Zeile hinzu
                tagebuch_df = github.read_df("tagebuch_mama2.csv")
                tagebuch_df = pd.concat([tagebuch_df, new_row], ignore_index=True)
            else:
                # CSV-Datei existiert nicht, erstelle eine neue mit der neuen Zeile
                tagebuch_df = new_row.copy()

            # Speichere den aktualisierten DataFrame in der CSV-Datei
            github.write_df("tagebuch_mama2.csv", tagebuch_df, "Save mama Blutwert")

        st.subheader('Tagebuch')
        if github.file_exists("tagebuch_mama2.csv"):
            tagebuch_df = github.read_df("tagebuch_mama2.csv")
            st.write(tagebuch_df)
        else:
            st.write("Noch keine Blutwerte vorhanden.")
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
