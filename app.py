from flask import Flask, render_template, request, redirect, session
import pickle
import pandas as pd
from donations import init_donations_file, add_post, get_all_posts

app = Flask(__name__)
app.secret_key = 'flood_app_secret_key'
init_donations_file()

with open("flood_model.pkl", "rb") as f:
    model = pickle.load(f)

village_df = pd.read_csv("village_data.csv")

SHELTERS = {
    "Rampur": {"name": "Rampur Govt. Primary School", "address": "Near Rampur Chowk", "contact": "1077"},
    "Sitapur": {"name": "Sitapur Community Hall", "address": "Main Road, Sitapur", "contact": "1077"},
    "Ganeshpur": {"name": "Ganeshpur Higher Secondary School", "address": "Ganeshpur Bazaar Road", "contact": "1077"},
    "Devgarh": {"name": "Devgarh Panchayat Bhawan", "address": "Village Center, Devgarh", "contact": "1077"},
    "Kishanpur": {"name": "Kishanpur Govt. School", "address": "Kishanpur Main Road", "contact": "1077"},
    "Lalganj": {"name": "Lalganj Relief Camp Ground", "address": "Near Lalganj Temple", "contact": "1077"},
    "Bhavpur": {"name": "Bhavpur Community Center", "address": "Bhavpur Market Road", "contact": "1077"},
    "Nandgaon": {"name": "Nandgaon Govt. School", "address": "Nandgaon Chowk", "contact": "1077"},
    "Shivpur": {"name": "Shivpur Panchayat Hall", "address": "Shivpur Main Street", "contact": "1077"},
    "Rajnagar": {"name": "Rajnagar Higher Secondary School", "address": "Rajnagar Bypass Road", "contact": "1077"},
    "Chandpur": {"name": "Chandpur Community Hall", "address": "Chandpur Village Center", "contact": "1077"},
    "Harigaon": {"name": "Harigaon Govt. School", "address": "Harigaon Main Road", "contact": "1077"},
    "Madhopur": {"name": "Madhopur Panchayat Bhawan", "address": "Madhopur Chowk", "contact": "1077"},
    "Ramnagar": {"name": "Ramnagar Relief Camp Ground", "address": "Near Ramnagar Bus Stand", "contact": "1077"},
    "Ashokpur": {"name": "Ashokpur Govt. School", "address": "Ashokpur Market Road", "contact": "1077"},
}

DEFAULT_SHELTER = {"name": "Nearest Government School / Panchayat Bhawan", "address": "Contact local administration for exact location", "contact": "1077"}

ACTIONS = {
    "Low": {
        "en": ["Stay alert and monitor local weather updates", "Keep emergency contact numbers handy", "No immediate action needed"],
        "hi": ["सतर्क रहें और मौसम की जानकारी पर नज़र रखें", "आपातकालीन नंबर पास रखें", "अभी कोई कार्रवाई ज़रूरी नहीं"]
    },
    "Medium": {
        "en": ["Move valuables and important documents to higher ground", "Keep an emergency bag ready (food, water, medicines)", "Stay in contact with neighbors and local authorities", "Be ready to evacuate if conditions worsen"],
        "hi": ["कीमती सामान और ज़रूरी कागज़ात ऊँची जगह पर रखें", "एक आपातकालीन बैग तैयार रखें (खाना, पानी, दवाइयाँ)", "पड़ोसियों और स्थानीय प्रशासन के संपर्क में रहें", "हालात बिगड़ने पर निकलने के लिए तैयार रहें"]
    },
    "High": {
        "en": ["Evacuate immediately to your nearest shelter", "Carry only essential items and important documents", "Help elderly, children, and disabled neighbors evacuate too", "Call the emergency helpline if you need rescue assistance"],
        "hi": ["तुरंत अपने नज़दीकी शेल्टर की ओर निकलें", "सिर्फ ज़रूरी सामान और कागज़ात साथ लें", "बुज़ुर्गों, बच्चों और दिव्यांग पड़ोसियों की मदद करें", "बचाव के लिए आपातकालीन हेल्पलाइन पर कॉल करें"]
    }
}

TEXT = {
    "en": {
        "home_title": "Village Flood Risk Predictor",
        "hero_subtitle": "Village-level flood risk, shelter guidance & community support — not just district averages.",
        "villages_monitored": "Villages Monitored", "high_risk_now": "High Risk Now", "community_posts": "Community Posts",
        "select_village": "Type or select your village:", "check_risk": "Check Flood Risk", "board_link": "Go to Donation & Help Board",
        "result_title": "Prediction Result", "village_label": "Village:", "risk_label": "Risk Level:",
        "prob_label": "Flood Probability:", "shelter_title": "Nearest Shelter",
        "contact_label": "Emergency Contact:", "actions_title": "What You Should Do",
        "try_another": "Try Another Village", "board_title": "Donation & Help Board",
        "post_title": "Post a Need or Donation", "want_to": "I want to:",
        "need_help": "Request Help", "offer_donate": "Offer Donation", "village_form": "Village:",
        "item_label": "Item (e.g. food, blankets, medicines):", "qty_label": "Quantity (e.g. \"20 people\" or \"50 blankets\"):",
        "contact_form": "Contact Number:", "post_btn": "Post", "current_posts": "Current Posts",
        "back_home": "Back to Home"
    },
    "hi": {
        "home_title": "गाँव बाढ़ जोखिम अनुमान",
        "hero_subtitle": "गाँव-स्तर पर बाढ़ का जोखिम, शेल्टर मार्गदर्शन और सामुदायिक सहायता — सिर्फ जिला औसत नहीं।",
        "villages_monitored": "निगरानी में गाँव", "high_risk_now": "अभी उच्च जोखिम", "community_posts": "सामुदायिक पोस्ट",
        "select_village": "अपना गाँव टाइप करें या चुनें:", "check_risk": "बाढ़ का जोखिम जांचें", "board_link": "दान और सहायता बोर्ड पर जाएँ",
        "result_title": "अनुमान परिणाम", "village_label": "गाँव:", "risk_label": "जोखिम स्तर:",
        "prob_label": "बाढ़ की संभावना:", "shelter_title": "नज़दीकी शेल्टर",
        "contact_label": "आपातकालीन संपर्क:", "actions_title": "आपको क्या करना चाहिए",
        "try_another": "दूसरा गाँव आज़माएँ", "board_title": "दान और सहायता बोर्ड",
        "post_title": "ज़रूरत या दान पोस्ट करें", "want_to": "मुझे करना है:",
        "need_help": "मदद माँगें", "offer_donate": "दान दें", "village_form": "गाँव:",
        "item_label": "वस्तु (जैसे खाना, कंबल, दवाइयाँ):", "qty_label": "मात्रा (जैसे \"20 लोग\" या \"50 कंबल\"):",
        "contact_form": "संपर्क नंबर:", "post_btn": "पोस्ट करें", "current_posts": "मौजूदा पोस्ट",
        "back_home": "होम पर वापस जाएँ"
    }
}

def predict_risk(rainfall_mm, river_level_m, elevation_m):
    input_data = [[rainfall_mm, river_level_m, elevation_m]]
    flood_probability = model.predict_proba(input_data)[0][1]
    if flood_probability < 0.33:
        risk = "Low"
    elif flood_probability < 0.66:
        risk = "Medium"
    else:
        risk = "High"
    return risk, round(flood_probability * 100, 1)

@app.route('/setlang/<lang>')
def setlang(lang):
    session['lang'] = lang
    return redirect(request.referrer or '/')

@app.route('/')
def home():
    lang = session.get('lang', 'en')
    villages = village_df['village'].tolist()
    high_count = 0
    for _, row in village_df.iterrows():
        risk, _ = predict_risk(row['rainfall_mm'], row['river_level_m'], row['elevation_m'])
        if risk == "High":
            high_count += 1
    posts_count = len(get_all_posts())
    return render_template('index.html', villages=villages, high_count=high_count,
                            total_villages=len(villages), posts_count=posts_count,
                            t=TEXT[lang], lang=lang)

@app.route('/predict', methods=['POST'])
def predict():
    return redirect(f"/risk/{request.form['village']}")

@app.route('/risk/<village>')
def risk_view(village):
    lang = session.get('lang', 'en')
    matches = village_df[village_df['village'] == village]
    if matches.empty:
        return redirect('/')
    row = matches.iloc[0]
    risk, confidence = predict_risk(row['rainfall_mm'], row['river_level_m'], row['elevation_m'])
    shelter = SHELTERS.get(village, DEFAULT_SHELTER)
    actions = ACTIONS[risk][lang]
    return render_template('result.html', risk=risk, confidence=confidence,
                            village=village, shelter=shelter, actions=actions,
                            t=TEXT[lang], lang=lang)

@app.route('/board')
def board():
    lang = session.get('lang', 'en')
    posts = get_all_posts()
    villages = village_df['village'].tolist()
    return render_template('board.html', posts=posts, villages=villages, t=TEXT[lang], lang=lang)

@app.route('/post', methods=['POST'])
def post():
    add_post(
        post_type=request.form['type'], village=request.form['village'],
        item=request.form['item'], quantity=request.form['quantity'],
        contact=request.form['contact']
    )
    return redirect('/board')

if __name__ == '__main__':
    app.run(debug=True)