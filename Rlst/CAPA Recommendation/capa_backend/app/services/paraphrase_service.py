import random
import re


SYNONYMS = {

    "checked": ["verified", "examined", "inspected", "reviewed"],
    "verified": ["confirmed", "validated", "checked"],
    "observed": ["noticed", "identified", "detected"],
    "detected": ["found", "identified", "noticed"],
    "found": ["identified", "observed", "detected"],

    "fixed": ["repaired", "corrected", "resolved", "rectified"],
    "repaired": ["fixed", "restored", "serviced"],
    "resolved": ["corrected", "fixed", "addressed"],
    "corrected": ["rectified", "resolved", "fixed"],

    "installed": ["mounted", "fitted", "assembled"],
    "removed": ["detached", "eliminated", "taken out"],
    "adjusted": ["aligned", "calibrated", "modified"],
    "calibrated": ["adjusted", "configured", "aligned"],

    "tightened": ["secured", "fastened", "locked"],
    "loosened": ["released", "slackened"],
    "opened": ["unlocked", "unsealed"],
    "closed": ["sealed", "shut"],

    "lubricated": ["greased", "oiled"],
    "greased": ["lubricated", "oiled"],
    "washed": ["cleaned", "rinsed"],
    "sanitized": ["disinfected", "sterilized"],

    "damaged": ["broken", "faulty", "defective"],
    "broken": ["damaged", "cracked", "fractured"],
    "cracked": ["split", "fractured"],
    "bent": ["deformed", "warped"],
    "worn": ["eroded", "deteriorated"],

    "leaking": ["dripping", "seeping", "leakage"],
    "overflow": ["spillage", "overflowing"],
    "blocked": ["clogged", "jammed", "obstructed"],
    "clogged": ["blocked", "choked"],

    "overheated": ["too hot", "high temperature"],
    "cooled": ["temperature reduced", "chilled"],
    "vibration": ["shaking", "oscillation"],
    "noise": ["sound", "abnormal sound"],

    "running": ["operating", "working"],
    "stopped": ["halted", "shut down"],
    "started": ["initiated", "activated"],
    "shutdown": ["power off", "turned off"],

    "unsafe": ["hazardous", "dangerous"],
    "safe": ["secured", "protected"],
    "risk": ["hazard", "danger"],
    "warning": ["alert", "caution"],

    "machine": ["equipment", "device", "unit"],
    "motor": ["drive", "electric motor"],
    "pump": ["transfer pump", "circulation pump"],
    "valve": ["control valve", "gate valve"],
    "pipe": ["pipeline", "tube"],
    "filter": ["strainer", "screen"],
    "fan": ["blower", "ventilator"],
    "compressor": ["air compressor"],
    "generator": ["genset", "power generator"],

    "electrical": ["electric", "power"],
    "mechanical": ["machine related"],
    "hydraulic": ["fluid powered"],
    "pneumatic": ["air powered"],

    "temperature": ["heat", "thermal condition"],
    "pressure": ["system pressure", "operating pressure"],
    "voltage": ["electric potential"],
    "current": ["electric current"],
    "battery": ["power cell"],
    "sensor": ["detector", "probe"],

    "maintenance": ["servicing", "upkeep"],
    "inspection": ["audit", "assessment", "checking"],
    "service": ["maintenance", "repair"],
    "operation": ["functioning", "working"],
    "production": ["manufacturing", "processing"],

    "pass": ["approved", "accepted"],
    "fail": ["rejected", "unsuccessful"],
    "good": ["excellent", "satisfactory"],
    "poor": ["bad", "unsatisfactory"],
    "normal": ["standard", "acceptable"],
    "abnormal": ["unusual", "irregular"],

    "replace": ["renew", "change"],
    "repair": ["fix", "restore"],
    "inspect": ["check", "verify"],
    "monitor": ["observe", "track"],
    "measure": ["calculate", "record"],
    "record": ["log", "document"],
    "report": ["document", "submit"],

    "dust": ["powder", "dirt"],
    "water": ["liquid", "moisture"],
    "oil": ["lubricant"],
    "grease": ["lubricant"],
    "rust": ["corrosion", "oxidation"],
    "corrosion": ["rust", "oxidation"],

    "emergency": ["urgent", "critical"],
    "critical": ["high priority", "severe"],
    "minor": ["low priority", "small"],
    "major": ["serious", "significant"]
}

def paraphrase_text(text):

    words = re.findall(
        r'\w+|\S',
        text
    )

    new_words = []

    for word in words:

        clean_word = word.lower()

        if clean_word in SYNONYMS:

            replacement = random.choice(
                SYNONYMS[clean_word]
            )

            # preserve capitalization
            if word[0].isupper():

                replacement = replacement.capitalize()

            new_words.append(
                replacement
            )

        else:

            new_words.append(word)

    return " ".join(new_words)


