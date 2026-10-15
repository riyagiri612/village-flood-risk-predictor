from flask import Flask, render_template, request, redirect, session, jsonify
from functools import wraps
import pandas as pd
from donations import init_donations_file, add_post, get_all_posts
from safety import init_safety_file, mark_safe, get_safety_records, get_safety_counts
from weather import get_live_weather, find_nearest_state
from model_lite import model

app = Flask(__name__)
app.secret_key = 'flood_app_secret_key'
init_donations_file()
init_safety_file()

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_email' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated

village_df = pd.read_csv("village_data.csv")

SHELTERS = {
    "Rampur": {"name": "Rampur Govt. Primary School", "address": "Near Rampur Chowk", "contact": "1077"},
    "Sitapur": {"name": "Sitapur Community Hall", "address": "Main Road, Sitapur", "contact": "1077"},
    "Chapra": {"name": "Chapra Govt. School", "address": "Chapra Main Road", "contact": "1077"},
    "Barpeta": {"name": "Barpeta Relief Camp Ground", "address": "Near Barpeta Chowk", "contact": "1077"},
    "Malda": {"name": "Malda Community Hall", "address": "Malda Bazaar Road", "contact": "1077"},
    "Alappuzha Rural": {"name": "Alappuzha Panchayat Bhawan", "address": "Alappuzha Rural Center", "contact": "1077"},
    "Bhadrak Rural": {"name": "Bhadrak Govt. School", "address": "Bhadrak Main Road", "contact": "1077"},
    "Karad": {"name": "Karad Community Hall", "address": "Karad Bypass Road", "contact": "1077"},
    "Valsad Rural": {"name": "Valsad Govt. School", "address": "Valsad Village Center", "contact": "1077"},
    "Kota Rural": {"name": "Kota Relief Camp Ground", "address": "Near Kota Bus Stand", "contact": "1077"},
}

DEFAULT_SHELTER_CONTACT = {"district": "1077", "state": "1070"}

def get_shelter(village):
    if village in SHELTERS:
        shelter = SHELTERS[village].copy()
        shelter["state_contact"] = DEFAULT_SHELTER_CONTACT["state"]
        return shelter
    return {
        "name": f"{village} Government Primary School",
        "address": "Confirm exact directions with your local Gram Panchayat office",
        "contact": DEFAULT_SHELTER_CONTACT["district"],
        "state_contact": DEFAULT_SHELTER_CONTACT["state"]
    }

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
        "home_title": "Abhaas — Village Flood Risk Predictor",
        "hero_subtitle": "Village-level flood risk, shelter guidance & community support — not just district averages.",
        "villages_monitored": "Villages Monitored", "high_risk_now": "High Risk Now", "community_posts": "Community Posts",
        "select_village": "Type or select your village:", "check_risk": "Check Flood Risk", "board_link": "Go to Donation & Help Board",
        "safety_link": "Community Safety Board", "alerts_link": "Active Flood Alerts",
        "result_title": "Prediction Result", "village_label": "Village:", "risk_label": "Risk Level:",
        "prob_label": "Flood Probability:", "shelter_title": "Nearest Shelter",
        "contact_label": "Emergency Contact:", "actions_title": "What You Should Do",
        "try_another": "Try Another Village", "board_title": "Donation & Help Board",
        "post_title": "Post a Need or Donation", "want_to": "I want to:",
        "need_help": "Request Help", "offer_donate": "Offer Donation", "village_form": "Village:",
        "item_label": "Item (e.g. food, blankets, medicines):", "qty_label": "Quantity (e.g. \"20 people\" or \"50 blankets\"):",
        "contact_form": "Contact Number:", "post_btn": "Post", "current_posts": "Current Posts",
        "back_home": "Back to Home", "sms_title": "SMS Alert (for non-smartphone users)",
        "sms_hint": "Copy this message and forward it via SMS to villagers without internet access.",
        "safety_title": "Community Safety Board", "mark_safe_title": "Mark Yourself Safe",
        "your_name": "Your Name:", "mark_safe_btn": "I Am Safe",
        "safety_records_title": "People Confirmed Safe", "no_safety_yet": "No one has marked safe yet.",
        "alerts_title": "Active Flood Alerts", "alerts_subtitle": "Villages currently at High risk — ready-to-send SMS alerts below.",
        "no_alerts": "No villages are currently at High risk.", "live_weather_title": "Live Weather"
    },
    "hi": {
        "home_title": "Abhaas — गाँव बाढ़ जोखिम अनुमान",
        "hero_subtitle": "गाँव-स्तर पर बाढ़ का जोखिम, शेल्टर मार्गदर्शन और सामुदायिक सहायता — सिर्फ जिला औसत नहीं।",
        "villages_monitored": "निगरानी में गाँव", "high_risk_now": "अभी उच्च जोखिम", "community_posts": "सामुदायिक पोस्ट",
        "select_village": "अपना गाँव टाइप करें या चुनें:", "check_risk": "बाढ़ का जोखिम जांचें", "board_link": "दान और सहायता बोर्ड पर जाएँ",
        "safety_link": "सामुदायिक सुरक्षा बोर्ड", "alerts_link": "सक्रिय बाढ़ चेतावनी",
        "result_title": "अनुमान परिणाम", "village_label": "गाँव:", "risk_label": "जोखिम स्तर:",
        "prob_label": "बाढ़ की संभावना:", "shelter_title": "नज़दीकी शेल्टर",
        "contact_label": "आपातकालीन संपर्क:", "actions_title": "आपको क्या करना चाहिए",
        "try_another": "दूसरा गाँव आज़माएँ", "board_title": "दान और सहायता बोर्ड",
        "post_title": "ज़रूरत या दान पोस्ट करें", "want_to": "मुझे करना है:",
        "need_help": "मदद माँगें", "offer_donate": "दान दें", "village_form": "गाँव:",
        "item_label": "वस्तु (जैसे खाना, कंबल, दवाइयाँ):", "qty_label": "मात्रा (जैसे \"20 लोग\" या \"50 कंबल\"):",
        "contact_form": "संपर्क नंबर:", "post_btn": "पोस्ट करें", "current_posts": "मौजूदा पोस्ट",
        "back_home": "होम पर वापस जाएँ", "sms_title": "SMS चेतावनी (बिना स्मार्टफोन वालों के लिए)",
        "sms_hint": "इस संदेश को कॉपी करें और बिना इंटरनेट वाले ग्रामीणों को SMS से भेजें।",
        "safety_title": "सामुदायिक सुरक्षा बोर्ड", "mark_safe_title": "खुद को सुरक्षित चिह्नित करें",
        "your_name": "आपका नाम:", "mark_safe_btn": "मैं सुरक्षित हूँ",
        "safety_records_title": "सुरक्षित पुष्टि किए गए लोग", "no_safety_yet": "अभी तक किसी ने सुरक्षित नहीं बताया है।",
        "alerts_title": "सक्रिय बाढ़ चेतावनी", "alerts_subtitle": "वर्तमान में उच्च जोखिम वाले गाँव — नीचे भेजने के लिए तैयार SMS चेतावनी।",
        "no_alerts": "फिलहाल कोई गाँव उच्च जोखिम में नहीं है।", "live_weather_title": "लाइव मौसम"
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

def get_all_village_risks():
    results = []
    for _, row in village_df.iterrows():
        risk, confidence = predict_risk(row['rainfall_mm'], row['river_level_m'], row['elevation_m'])
        results.append({"village": row['village'], "risk": risk, "confidence": confidence})
    return results

def generate_sms(village, shelter, lang):
    if lang == 'hi':
        return (f"🚨 बाढ़ चेतावनी: {village} में बाढ़ का उच्च खतरा है। "
                f"तुरंत {shelter['name']} ({shelter['address']}) पर जाएँ। "
                f"आपातकालीन नंबर: जिला {shelter['contact']}, राज्य {shelter['state_contact']}. - Abhaas")
    return (f"🚨 FLOOD ALERT: {village} is at HIGH risk of flooding. "
            f"Evacuate immediately to {shelter['name']} ({shelter['address']}). "
            f"Emergency contacts: District {shelter['contact']}, State {shelter['state_contact']}. - Abhaas")

@app.route('/login', methods=['GET', 'POST'])
def login():
    lang = session.get('lang', 'en')
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        if not name:
            name = email.split('@')[0] if email else 'Guest'
        session['user_name'] = name
        session['user_email'] = email or 'guest'
        return redirect('/')
    return render_template('login.html', t=TEXT[lang], lang=lang, error=None)

@app.route('/register')
def register():
    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('user_name', None)
    session.pop('user_email', None)
    return redirect('/login')

@app.route('/setlang/<lang>')
def setlang(lang):
    session['lang'] = lang
    return redirect(request.referrer or '/')

@app.route('/')
@login_required
def home():
    lang = session.get('lang', 'en')
    villages = village_df['village'].tolist()
    all_risks = get_all_village_risks()
    high_count = len([v for v in all_risks if v['risk'] == 'High'])
    posts_count = len(get_all_posts())
    return render_template('index.html', villages=villages, high_count=high_count,
                            total_villages=len(villages), posts_count=posts_count,
                            t=TEXT[lang], lang=lang, user_name=session.get('user_name'))

@app.route('/search-villages')
@login_required
def search_villages():
    query = request.args.get('q', '').strip().lower()
    if len(query) < 2:
        return jsonify([])
    matches = village_df[village_df['village'].str.lower().str.contains(query)]
    results = matches[['village', 'state']].head(8).to_dict('records')
    return jsonify(results)

@app.route('/nearest-state')
@login_required
def nearest_state():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    if lat is None or lon is None:
        return jsonify({"error": "no coordinates"}), 400
    state = find_nearest_state(lat, lon)
    matching_villages = village_df[village_df['state'] == state][['village', 'state']].to_dict('records')
    return jsonify({"state": state, "villages": matching_villages})

@app.route('/predict', methods=['POST'])
@login_required
def predict():
    return redirect(f"/risk/{request.form['village']}")

@app.route('/risk/<village>')
@login_required
def risk_view(village):
    lang = session.get('lang', 'en')
    matches = village_df[village_df['village'] == village]
    if matches.empty:
        return redirect('/')
    row = matches.iloc[0]
    risk, confidence = predict_risk(row['rainfall_mm'], row['river_level_m'], row['elevation_m'])
    shelter = get_shelter(village)
    actions = ACTIONS[risk][lang]
    sms_text = generate_sms(village, shelter, lang) if risk == "High" else None
    live_weather = get_live_weather(row['state'],village)
    return render_template('result.html', risk=risk, confidence=confidence,
                            village=village, shelter=shelter, actions=actions,
                            sms_text=sms_text, live_weather=live_weather,
                            t=TEXT[lang], lang=lang)

@app.route('/board')
@login_required
def board():
    lang = session.get('lang', 'en')
    posts = get_all_posts()
    villages = village_df['village'].tolist()
    return render_template('board.html', posts=posts, villages=villages, t=TEXT[lang], lang=lang)

@app.route('/post', methods=['POST'])
@login_required
def post():
    add_post(
        post_type=request.form['type'], village=request.form['village'],
        item=request.form['item'], quantity=request.form['quantity'],
        contact=request.form['contact']
    )
    return redirect('/board')

@app.route('/safety')
@login_required
def safety():
    lang = session.get('lang', 'en')
    villages = village_df['village'].tolist()
    records = get_safety_records()
    counts = get_safety_counts()
    return render_template('safety.html', villages=villages, records=records,
                            counts=counts, t=TEXT[lang], lang=lang)

@app.route('/mark-safe', methods=['POST'])
@login_required
def mark_safe_route():
    mark_safe(
        village=request.form['village'],
        name=request.form['name'],
        contact=request.form['contact']
    )
    return redirect('/safety')

@app.route('/alerts')
@login_required
def alerts():
    lang = session.get('lang', 'en')
    all_risks = get_all_village_risks()
    high_risk_villages = [v for v in all_risks if v['risk'] == 'High']
    alert_list = []
    for v in high_risk_villages:
        shelter = get_shelter(v['village'])
        sms_text = generate_sms(v['village'], shelter, lang)
        alert_list.append({"village": v['village'], "confidence": v['confidence'], "sms_text": sms_text})
    return render_template('alerts.html', alerts=alert_list, t=TEXT[lang], lang=lang)

if __name__ == '__main__':
    app.run(debug=True)