import pandas as pd
import random

random.seed(42)

states_villages = {
    "Uttar Pradesh": ["Rampur", "Sitapur", "Deoria", "Basti", "Gonda", "Bahraich", "Azamgarh", "Ballia", "Kushinagar", "Mau"],
    "Bihar": ["Chapra", "Siwan", "Gopalganj", "Vaishali", "Samastipur", "Madhubani", "Darbhanga", "Purnia", "Katihar", "Saharsa"],
    "Assam": ["Barpeta", "Nalbari", "Dhubri", "Goalpara", "Morigaon", "Nagaon", "Golaghat", "Sivasagar", "Jorhat", "Lakhimpur"],
    "West Bengal": ["Malda", "Murshidabad", "Nadia Rural", "Hooghly Rural", "Howrah Rural", "Bankura", "Purulia", "Birbhum", "Cooch Behar", "Jalpaiguri"],
    "Kerala": ["Alappuzha Rural", "Kuttanad", "Chengannur", "Pathanamthitta Rural", "Cherthala", "Thrissur Rural", "Kottayam Rural", "Ernakulam Rural", "Palakkad Rural", "Wayanad"],
    "Odisha": ["Bhadrak Rural", "Kendrapara", "Jagatsinghpur Rural", "Puri Rural", "Balasore", "Cuttack Rural", "Ganjam Rural", "Mayurbhanj", "Keonjhar", "Bhubaneswar Rural"],
    "Maharashtra": ["Karad", "Sangli Rural", "Kolhapur Rural", "Ratnagiri Rural", "Wardha", "Chiplun", "Wai", "Satara Rural", "Solapur Rural", "Nashik Rural"],
    "Gujarat": ["Valsad Rural", "Navsari Rural", "Bharuch Rural", "Junagadh Rural", "Surendranagar", "Bhavnagar Rural", "Anand Rural", "Vadodara Rural", "Kutch Rural", "Rajkot Rural"],
    "Rajasthan": ["Kota Rural", "Bharatpur Rural", "Alwar Rural", "Sawai Madhopur", "Baran", "Dholpur", "Karauli", "Jhalawar", "Tonk", "Bundi"],
    "Madhya Pradesh": ["Hoshangabad Rural", "Mandla", "Balaghat", "Betul", "Chhindwara Rural", "Seoni", "Sehore", "Raisen", "Harda", "Narsinghpur"],
    "Tamil Nadu": ["Cuddalore Rural", "Nagapattinam Rural", "Thanjavur Rural", "Tiruvarur", "Villupuram Rural", "Pudukkottai", "Ramanathapuram", "Sivaganga", "Dindigul Rural", "Erode Rural"],
    "Karnataka": ["Raichur Rural", "Belagavi Rural", "Bagalkot", "Yadgir", "Kalaburagi Rural", "Koppal", "Vijayapura Rural", "Gadag", "Haveri", "Dharwad Rural"],
    "Andhra Pradesh": ["East Godavari Rural", "West Godavari Rural", "Krishna Rural", "Vizianagaram", "Nellore Rural", "Guntur Rural", "Prakasam Rural", "Srikakulam", "Chittoor Rural", "Kadapa Rural"],
    "Punjab": ["Gurdaspur Rural", "Ferozepur Rural", "Ropar", "Hoshiarpur Rural", "Patiala Rural", "Amritsar Rural", "Sangrur", "Bathinda Rural", "Moga", "Faridkot"],
    "Himachal Pradesh": ["Kullu Rural", "Mandi Rural", "Kangra Rural", "Chamba Rural", "Solan Rural", "Bilaspur HP", "Una", "Hamirpur HP", "Sirmaur", "Kinnaur"],
    "Jharkhand": ["Sahibganj", "Godda", "Dumka", "Pakur", "East Singhbhum Rural", "West Singhbhum", "Hazaribagh Rural", "Giridih", "Deoghar", "Ranchi Rural"],
    "Chhattisgarh": ["Bastar", "Raigarh Rural", "Bilaspur CG Rural", "Rajnandgaon", "Durg Rural", "Kanker", "Dhamtari", "Mahasamund", "Korba Rural", "Jashpur"],
    "Uttarakhand": ["Haridwar Rural", "Udham Singh Nagar", "Nainital Rural", "Pauri", "Tehri", "Almora", "Bageshwar", "Champawat", "Rudraprayag", "Chamoli"],
    "Telangana": ["Khammam Rural", "Warangal Rural", "Nizamabad Rural", "Karimnagar Rural", "Adilabad Rural", "Mahbubnagar Rural", "Nalgonda Rural", "Medak", "Suryapet", "Jagtial"],
    "Tripura": ["Sepahijala", "Gomati", "Dhalai", "Unakoti", "Khowai", "West Tripura Rural", "South Tripura Rural", "North Tripura Rural"],
    "Haryana": ["Kurukshetra Rural", "Karnal Rural", "Panipat Rural", "Sonipat Rural", "Jind", "Kaithal", "Yamunanagar Rural", "Ambala Rural", "Fatehabad", "Sirsa"],
    "Goa": ["Bicholim", "Sanguem", "Canacona", "Quepem", "Ponda Rural"],
    "Jammu and Kashmir": ["Anantnag Rural", "Pulwama Rural", "Baramulla Rural", "Kupwara", "Budgam Rural", "Kathua Rural", "Udhampur Rural", "Rajouri", "Poonch", "Doda"],
    "Manipur": ["Bishnupur", "Thoubal", "Imphal Rural", "Churachandpur", "Senapati"],
    "Meghalaya": ["Ri-Bhoi", "Jaintia Hills", "West Garo Hills", "East Khasi Hills Rural", "South Garo Hills"],
    "Mizoram": ["Aizawl Rural", "Lunglei Rural", "Champhai", "Kolasib", "Serchhip"],
    "Nagaland": ["Dimapur Rural", "Kohima Rural", "Mokokchung", "Wokha", "Zunheboto"],
    "Sikkim": ["Gangtok Rural", "Namchi", "Mangan", "Gyalshing"],
    "Arunachal Pradesh": ["Itanagar Rural", "Pasighat", "Ziro", "Along", "Tezu"],
}

data = {"village": [], "state": [], "rainfall_mm": [], "river_level_m": [], "elevation_m": [], "flooded_before": []}

for state, villages in states_villages.items():
    for v in villages:
        rainfall = random.randint(30, 350)
        river_level = round(random.uniform(2.0, 10.5), 1)
        elevation = random.randint(20, 200)
        flood_score = (rainfall / 350) + (river_level / 10.5) + (1 - elevation / 200)
        flooded = 1 if flood_score > 1.6 else 0

        data["village"].append(v)
        data["state"].append(state)
        data["rainfall_mm"].append(rainfall)
        data["river_level_m"].append(river_level)
        data["elevation_m"].append(elevation)
        data["flooded_before"].append(flooded)

df = pd.DataFrame(data)
df.to_csv("village_data.csv", index=False)
print(f"Dataset created with {len(df)} places across {len(states_villages)} states/UTs!")
print(df.head(10))