# Abhaas — Village Flood Risk Predictor

Village-level flood risk guidance, shelter information and community support for flood-prone regions of India, built for **VBYLD Hack for Social Cause 2026-27**.

Abhaas is a community-focused prototype designed to support flood awareness and preparedness in villages. It brings together village-level flood-risk estimates, weather information, safety updates, shelter guidance, and community help coordination in one web application.
Floods can disrupt homes, livelihoods, transport, and access to essential supplies. Abhaas aims to make preparedness information easier to access and help communities coordinate support when flooding is a concern

> **Prototype notice:** the flood-risk values shown in this prototype are **simulated**. Only the weather panel uses live data. Abhaas is a demonstration of the idea and **must not be used for real emergencies**. Always follow official warnings from IMD, NDMA and your local authorities.

## The problem

Village communities may face challenges accessing timely, understandable flood-risk information and coordinating help during emergencies. People may also need a simple way to share their safety status or communicate requests and offers of assistance.

## Proposed Solution

Abhaas brings several preparedness and community-support features together in a single application. The goal is to support awareness and coordination—not to replace official forecasts, emergency services, or local authorities.

## What Abhaas does today

- **Village search:** find any of 252 places across 29 states and union territories, by typing a name.
- **Risk level:** shows Low, Medium or High with a probability, from a small machine-learning model that uses rainfall, river level and elevation. *(Simulated data, see Limitations.)*
- **Shelter and contacts:** the nearest shelter, an address hint and emergency contact numbers.
- **What to do:** clear actions for each risk level.
- **SMS-ready alerts:** for High risk, a ready-to-copy text message to forward to people without internet access.
- **Active flood alerts page:** lists every High-risk village with its alert message.
- **Donation and Help Board:** neighbours can post needs or offer help.
- **Community Safety Board:** people can mark themselves safe, so family and volunteers can see who has been accounted for.
- **English and Hindi** interface.
- **Live weather** from OpenWeather. It shows the village's own weather when the place can be located, and the state's main city, with a note saying so, when it cannot.
- **"Use My Location"** suggests villages in the nearest state (approximate, state-level).

## How it works

1. The Flask app loads `village_data.csv` with pandas.
2. A lightweight logistic-regression model (`model_lite.py`, weights in `model_weights.json`) turns rainfall, river level and elevation into a flood probability.
3. The probability is mapped to Low (below 33%), Medium (33% to 66%) or High (above 66%).
4. The result page adds shelter details, recommended actions, live weather and, for High risk, an SMS-ready message.
5. Community posts and safety check-ins are saved in CSV files.

## Tech stack

- Python 3, Flask
- pandas, requests, python-dotenv
- HTML, CSS and a little JavaScript (Jinja templates)
- OpenWeather API for live weather
- CSV files for storage

## Getting started

Prerequisites: Python 3.11 or newer, and a free OpenWeather API key from openweathermap.org.

1. Clone the repository and open the folder:
   git clone https://github.com/riyagiri612/village-flood-risk-predictor.git
   cd village-flood-risk-predictor
2. Install the dependencies:
   python -m pip install -r requirements.txt
3. Create a file named .env in the project folder (next to app.py) with one line, using your own key:
   OPENWEATHER_API_KEY=your_key_here
4. Start the app:
   python app.py


## Project structure

```
app.py                 Flask app: routes, text in English and Hindi, shelters, actions
weather.py             Live weather and place lookup (OpenWeather)
model_lite.py          Lightweight flood-risk model
model_weights.json     Learned weights used by the model
village_data.csv       The 252 places and their (simulated) data
create_dataset.py      Script that generated village_data.csv
train_lite.py          Trains the lightweight model
train_model.py         Optional scikit-learn experiment (needs scikit-learn)
predict_risk.py        Optional command-line prediction with the scikit-learn model
donations.py           Donation and Help Board storage
safety.py              Community Safety Board storage
users.py               Account storage helpers (not used by the current login)
templates/             HTML pages
static/                Stylesheet
```


## Limitations

- **Risk values are simulated**, as described above. Only the weather panel is live.
- **The login is a demo.** The current sign-in stores the name and email in the session and **does not check passwords**.
- **CSV storage** is fine for a prototype, but it cannot handle many users at once, and it will not keep data on hosting platforms that have read-only or temporary storage.
- **Weather lookup by place name** can fail or match the wrong place for common names, in which case the app shows the state's main city with a note.
- **"Use My Location"** only finds the nearest state, not the nearest village.
- **Shelter details** were entered by hand for 10 places. Other villages show a generic placeholder and should be confirmed with the local Gram Panchayat.
- **Lack of more regional languages**


## Roadmap

1. **Real data:** replace the simulated table with forecast rainfall and river-flow data from public sources. 
2. **Pilot region:** start with a small set of flood-prone places in North Bengal. Live rainfall and river data was tested for 13 places there, and a simple rule that explains each rating ("heavy rain forecast", "river rising") was built in experiments.
3. **Trust and transparency:** show what each rating is based on and when the data was last updated, and link to official alerts such as NDMA's SACHET.
4. **Real accounts and a database** instead of session-only sign-in and CSV files.
5. **More languages** and a read-aloud option for people who cannot read easily.
