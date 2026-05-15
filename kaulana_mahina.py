import datetime
import math
from ics import Calendar, Event

HAWAIIAN_MOON_PHASES = {
    1: {"name": "Hilo", "anahulu": "Hoʻonui", "type": "🌱 Planting", "desc": "First slim sliver. Excellent for planting roots (sweet potato). Fish hide in reefs."},
    2: {"name": "Hoaka", "anahulu": "Hoʻonui", "type": "🌱 Planting", "desc": "Crescent moon. Good planting day. Fish are easily frightened by shadows."},
    3: {"name": "Kūkahi", "anahulu": "Hoʻonui", "type": "🌱 Planting", "desc": "Good for planting things that grow straight up. Good reef fishing."},
    4: {"name": "Kūlua", "anahulu": "Hoʻonui", "type": "🌱 Planting", "desc": "Excellent farming day. Fish begin biting well."},
    5: {"name": "Kūkolu", "anahulu": "Hoʻonui", "type": "🐟 Fishing", "desc": "Reef and deep-sea fishing are excellent. Planting is average."},
    6: {"name": "Kūpau", "anahulu": "Hoʻonui", "type": "🌱 Planting", "desc": "End of the Ku days. Good for farming banana and taro root."},
    7: {"name": "ʻOlekūkahi", "anahulu": "Hoʻonui", "type": "🛑 Rest", "desc": "'Ole means unproductive. Rough seas. Clean gear; don't plant or fish."},
    8: {"name": "ʻOlekūlua", "anahulu": "Hoʻonui", "type": "🛑 Rest", "desc": "Unproductive day. Strong currents. Good for weeding fields."},
    9: {"name": "ʻOlekūkolu", "anahulu": "Hoʻonui", "type": "🛑 Rest", "desc": "Unproductive day. Sea is tempestuous. Finish household chores."},
    10: {"name": "ʻOlepau", "anahulu": "Hoʻonui", "type": "🌱 Planting", "desc": "Unproductive cycle ends. Evening is excellent for preparing soil."},
    11: {"name": "Huna", "anahulu": "Poepoe", "type": "🌱 Planting", "desc": "Huna means hidden. Root crops will grow large hidden in soil. Good fishing."},
    12: {"name": "Mōhalu", "anahulu": "Poepoe", "type": "🌱 Planting", "desc": "Flowers open up. Excellent for planting fruit-bearing plants. Sacred night."},
    13: {"name": "Hua", "anahulu": "Poepoe", "type": "🌱 Planting", "desc": "Hua means fruit/abundance. Highly productive for all farming and fishing."},
    14: {"name": "Akua", "anahulu": "Poepoe", "type": "🐟 Fishing", "desc": "Night of the gods. Abundant fishing; fish flock to the surface lights."},
    15: {"name": "Hoku", "anahulu": "Poepoe", "type": "🐟 Fishing", "desc": "The actual full moon. Highest tides. Excellent deep-sea fishing night."},
    16: {"name": "Māhealani", "anahulu": "Poepoe", "type": "🐟 Fishing", "desc": "Full moon begins to wane. Highly productive farming and night diving."},
    17: {"name": "Kulu", "anahulu": "Poepoe", "type": "🌱 Planting", "desc": "Kulu means dropping dew. Excellent for planting banana and damp crops."},
    18: {"name": "Lāʻaukūkahi", "anahulu": "Poepoe", "type": "🌱 Planting", "desc": "Lā'au means wood. Good for planting trees, medicine, and building frames."},
    19: {"name": "Lāʻaukūlua", "anahulu": "Poepoe", "type": "🌱 Planting", "desc": "Good for planting woody vines and trees. Fish are scattered."},
    20: {"name": "Lāʻaupau", "anahulu": "Poepoe", "type": "🌱 Planting", "desc": "End of woody moon cycle. Very productive farming afternoon."},
    21: {"name": "ʻOlekūkahi", "anahulu": "Emi", "type": "🛑 Rest", "desc": "Waning unproductive day. Sea conditions rough. Repair lines and nets."},
    22: {"name": "ʻOlekūlua", "anahulu": "Emi", "type": "🛑 Rest", "desc": "High winds and bad tides. Unproductive for field work."},
    23: {"name": "ʻOlepau", "anahulu": "Emi", "type": "🌱 Planting", "desc": "End of the unproductive cycle. Tide drops low; good for torch fishing."},
    24: {"name": "Kāloakūkahi", "anahulu": "Emi", "type": "🐟 Fishing", "desc": "Dedicated to Kanaloa (god of ocean). Excellent for catching octopus."},
    25: {"name": "Kāloakūlua", "anahulu": "Emi", "type": "🐟 Fishing", "desc": "Good day for ocean gathering and nearshore trap tracking."},
    26: {"name": "Kāloapau", "anahulu": "Emi", "type": "🐟 Fishing", "desc": "Cycle ends. Highly favorable for deep water angling and netting."},
    27: {"name": "Kāne", "anahulu": "Emi", "type": "🛑 Rest", "desc": "Dedicated to Kane (god of life/water). Sacred day; pray for water springs."},
    28: {"name": "Lono", "anahulu": "Emi", "type": "🌱 Planting", "desc": "Dedicated to Lono (god of rain). Plant sweet potatoes; pray for rain."},
    29: {"name": "Mauli", "anahulu": "Emi", "type": "🐟 Fishing", "desc": "Moon rises just before dawn. Excellent morning fishing and seaweed foraging."},
    30: {"name": "Muku", "anahulu": "Emi", "type": "🏰 Indoor Fort", "desc": "Dark moon. Low tides. Great for indoor fort building, family stories, resting."}
}

def calculate_lunar_age(target_date):
    baseline = datetime.datetime(2000, 1, 6, 18, 14)
    diff = target_date - baseline
    return (diff.total_seconds() / 86400) % 29.530588853

def generate_ical():
    c = Calendar()
    start_date = datetime.date.today()
    print("Processing 365 days of calendar entries...")
    
    for i in range(365):
        current_date = start_date + datetime.timedelta(days=i)
        age = calculate_lunar_age(datetime.datetime.combine(current_date, datetime.time(12, 0)))
        phase_day = math.ceil(age)
        if phase_day > 30: phase_day = 30
        if phase_day < 1: phase_day = 1
        
        phase = HAWAIIAN_MOON_PHASES[phase_day]
        e = Event()
        e.name = f"{phase['type']} - {phase['name']}"
        e.begin = current_date
        e.description = f"Anahulu: {phase['anahulu']}\nGuidance: {phase['desc']}"
        e.make_all_day()
        c.events.add(e)
        
    reminder = Event()
    reminder.name = "🔄 Refresh Kiwa's Lunar Calendar!"
    reminder.begin = start_date + datetime.timedelta(days=365)
    reminder.description = "Open your Chromebook Terminal and run: python3 kaulana_mahina.py"
    reminder.make_all_day()
    c.events.add(reminder)
        
    with open('hawaiian_lunar_calendar.ics', 'w', encoding='utf-8') as f:
        f.writelines(c.serialize_iter())
    print("Success! 365-day calendar file generated.")

if __name__ == "__main__":
    generate_ical()