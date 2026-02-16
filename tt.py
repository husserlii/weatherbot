import os
import requests
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
print("Script démarré")
# === CONFIGURATION ===
import os
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")

if not TELEGRAM_TOKEN:
    raise ValueError("BOT_TOKEN non défini dans les variables d'environnement")

# === WILAYAS 1-58 ===
WILAYAS = {
    1: ('Adrar', 27.8743, -0.2939), 2: ('Chlef', 36.1653, 1.3345), 3: ('Laghouat', 33.8, 2.865),
    4: ('Oum El Bouaghi', 35.8754, 7.1135), 5: ('Batna', 35.5559, 6.1741), 6: ('Béjaïa', 36.7509, 5.0567),
    7: ('Biskra', 34.851, 5.728), 8: ('Béchar', 31.6167, -2.2167), 9: ('Blida', 36.47, 2.8287),
    10: ('Bouira', 36.3749, 3.902), 11: ('Tamanrasset', 22.785, 5.5228), 12: ('Tébessa', 35.4042, 8.1246),
    13: ('Tlemcen', 34.8783, -1.315), 14: ('Tiaret', 35.37, 1.32), 15: ('Tizi Ouzou', 36.7169, 4.0497),
    16: ('Alger', 36.7538, 3.0588), 17: ('Djelfa', 34.67, 3.25), 18: ('Jijel', 36.82, 5.76),
    19: ('Sétif', 36.19, 5.41), 20: ('Saïda', 34.83, 0.15), 21: ('Skikda', 36.8667, 6.9),
    22: ('Sidi Bel Abbès', 35.19, -0.63), 23: ('Annaba', 36.9, 7.76), 24: ('Guelma', 36.46, 7.43),
    25: ('Constantine', 36.365, 6.6147), 26: ('Médéa', 36.26, 2.75), 27: ('Mostaganem', 35.94, 0.09),
    28: ('M’Sila', 35.7, 4.55), 29: ('Mascara', 35.4, 0.14), 30: ('Ouargla', 31.95, 5.32),
    31: ('Oran', 35.6971, -0.6308), 32: ('El Bayadh', 33.68, 1.02), 33: ('Illizi', 26.4833, 8.4667),
    34: ('Bordj Bou Arréridj', 36.0732, 4.7611), 35: ('Boumerdès', 36.76, 3.47), 36: ('El Tarf', 36.77, 8.31),
    37: ('Tindouf', 27.67, -8.15), 38: ('Tissemsilt', 35.61, 1.81), 39: ('El Oued', 33.37, 6.87),
    40: ('Khenchela', 35.43, 7.14), 41: ('Souk Ahras', 36.28, 7.95), 42: ('Tipaza', 36.59, 2.45),
    43: ('Mila', 36.45, 6.27), 44: ('Aïn Defla', 36.26, 1.97), 45: ('Naâma', 33.26, -0.31),
    46: ('Aïn Témouchent', 35.3, -1.14), 47: ('Ghardaïa', 32.49, 3.67), 48: ('Relizane', 35.74, 0.55),
    49: ('Timimoun', 29.26, 0.23), 50: ('Bordj Badji Mokhtar', 21.33, 0.95), 51: ('Ouled Djellal', 34.42, 5.07),
    52: ('Béni Abbès', 30.13, -2.16), 53: ('In Salah', 27.2, 2.47), 54: ('In Guezzam', 19.57, 5.77),
    55: ('Touggourt', 33.1, 6.06), 56: ('Djanet', 24.55, 9.48), 57: ('El M’Ghair', 33.95, 5.92), 58: ('El Meniaa', 30.58, 2.88)
}

# === MÉTÉO ===
def get_weather(lat, lon):
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&"
            "current_weather=true&"
            "daily=temperature_2m_max,temperature_2m_min,precipitation_sum&"
            "timezone=Africa/Algiers"
        )
        response = requests.get(url).json()
        current = response.get("current_weather", {})
        daily = response.get("daily", {})

        return (
            f"🌤 Météo actuelle : {current.get('temperature', 'N/A')}°C\n"
            f"💨 Vent : {current.get('windspeed', 'N/A')} km/h\n"
            f"📈 Max : {daily.get('temperature_2m_max', ['N/A'])[0]}°C\n"
            f"📉 Min : {daily.get('temperature_2m_min', ['N/A'])[0]}°C\n"
            f"🌧 Pluie : {daily.get('precipitation_sum', ['N/A'])[0]} mm"
        )
    except:
        return "Impossible de récupérer la météo."

# === PRIÈRE ===
def get_prayer(lat, lon):
    try:
        params = {"latitude": lat, "longitude": lon, "method": 2}
        response = requests.get(PRAYER_API_URL, params=params).json()
        timings = response["data"]["timings"]
        return "\n".join([f"🕌 {k}: {v}" for k, v in timings.items()])
    except:
        return "Impossible de récupérer les horaires."

# === HANDLERS ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "Bonjour 🌙\nChoisissez votre wilaya (1-58) :\n"
    for num, (name, _, _) in WILAYAS.items():
        message += f"{num}: {name}\n"
    await update.message.reply_text(message)

async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if not text.isdigit() or int(text) not in WILAYAS:
        await update.message.reply_text("❌ Entrez un numéro valide entre 1 et 58.")
        return

    choice = int(text)
    name, lat, lon = WILAYAS[choice]

    weather = get_weather(lat, lon)
    prayer = get_prayer(lat, lon)

    await update.message.reply_text(f"✅ Wilaya : {name}\n\n{weather}\n\n{prayer}")

# === LANCEMENT ===
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_choice))




