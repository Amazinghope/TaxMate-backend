# import json
# from pathlib import Path

# MODE_RULES = json.loads(Path("prompt/mode_rules.json").read_text())

# def load_ruleset(persona: str) -> dict:
#     """Load the persona ruleset JSON file."""
#     return json.loads(Path(f"rulesets/2026/{persona}.json").read_text())

# def build_prompt(session: dict, user_msg: str) -> str:
#     """Build the full prompt for the AI using ruleset + mode + constraints."""
#     ruleset = load_ruleset(session["persona"])
#     mode = session["mode"]

#     return f"""
# You are TaxMate, a Nigerian tax explainer.

# Use ONLY the RULESET below. Do not hallucinate.

# RULESET:
# {json.dumps(ruleset, indent=2)}

# LANGUAGE MODE:
# {MODE_RULES[mode]}

# CONSTRAINTS:
# - Do not perform tax calculations
# - Do not provide filing guidance
# - Refuse anything outside scope

# QUESTION:
# {user_msg}
# """

#-----------

import json
from pathlib import Path

MODE_RULES = json.loads(Path("prompt/mode_rules.json").read_text())

PERSONA_INTROS = {
    "freelancer": "You are a freelancer working with multiple clients.",
    "salaried": "You are a salaried worker earning monthly income.",
    "business_owner": "You own a small business.",
    "first_timer": "You are paying tax for the first time."
}

def load_ruleset(persona):
    return json.loads(Path(f"rulesets/2026/{persona}.json").read_text())

def build_prompt(session, user_msg):
    persona = session["persona"]
    ruleset = load_ruleset(persona)
    intro = PERSONA_INTROS.get(persona, "")

    return f"""
You are TaxMate, a Nigerian tax explainer.

PERSONA:
{intro}

RULESET:
{json.dumps(ruleset, indent=2)}

LANGUAGE MODE:
{MODE_RULES[session["mode"]]}

CONSTRAINTS:
- No calculations
- No filing guidance
- Only answer from ruleset

QUESTION:
{user_msg}
"""
