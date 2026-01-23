import json
from pathlib import Path
from prompt.mode_renderer import render_standard, render_eli5, render_pidgin, render_hybrid

def load_ruleset(persona: str) -> dict:
    """Load persona JSON file safely from rulesets/2026."""
    path = Path(f"rulesets/2026/{persona}.json")
    if not path.exists():
        return {}
    return json.loads(path.read_text())

def generate_mock_reply(persona: str, mode: str, user_msg: str = "") -> str:
    """
    Generate a dynamic, persona-aware mock response respecting the language mode.
    - persona: freelancer, salaried, etc.
    - mode: standard, eli5, pidgin, hybrid
    - user_msg: optional, question asked by user
    """
    data = load_ruleset(persona)
    if not data:
        return f"No data found for persona '{persona}'."

    render_map = {
        "standard": render_standard,
        "eli5": render_eli5,
        "pidgin": render_pidgin,
        "hybrid": render_hybrid
    }

    renderer = render_map.get(mode.lower(), render_standard)
    response = renderer(data)

    if user_msg:
        response += f"\n\nQuestion asked: {user_msg}"

    return response

#--------

# import json
# from pathlib import Path
# from prompt.mode_renderer import render_standard, render_eli5, render_pidgin, render_hybrid

# def load_ruleset(persona: str) -> dict:
#     path = Path(f"rulesets/2026/{persona}.json")
#     if not path.exists():
#         return {}
#     return json.loads(path.read_text())

# def generate_mock_reply(persona: str, mode: str) -> str:
#     data = load_ruleset(persona)

#     render_map = {
#         "standard": render_standard,
#         "eli5": render_eli5,
#         "pidgin": render_pidgin,
#         "hybrid": render_hybrid
#     }

#     renderer = render_map.get(mode.lower(), render_standard)
#     return renderer(data)
# # Load persona ruleset
# def load_ruleset(persona: str) -> dict:
#     """Load the persona JSON file safely."""
#     path = Path(f"rulesets/2026/{persona}.json")
#     if not path.exists():
#         return {}
#     return json.loads(path.read_text())

# # Generate a mock AI reply
# def generate_mock_reply(persona: str, mode: str, user_msg: str) -> str:
#     """
#     Generate a detailed persona-aware mock response respecting the language mode.
#     """
#     ruleset = load_ruleset(persona)

#     # Basic intro
#     description = ruleset.get("description", "You are a taxpayer in Nigeria.")
#     taxes_apply = ", ".join(ruleset.get("taxes_apply", []))
#     taxes_not_apply = ", ".join(ruleset.get("taxes_not_apply", []))
#     changes = ", ".join(ruleset.get("what_changed_2026", []))
#     mistakes = ", ".join(ruleset.get("common_mistakes", []))
#     steps = ", ".join(ruleset.get("next_steps", []))

#     # Compose the full mock response
#     full_response = f"""
# {description}
# Taxes that apply to you: {taxes_apply or 'None'}
# Taxes that do not apply to you: {taxes_not_apply or 'None'}
# Recent changes in 2026: {changes or 'None'}
# Common mistakes: {mistakes or 'None'}
# Next steps: {steps or 'None'}
# Question asked: {user_msg}
# """

#     # Apply language mode
#     if mode.lower() == "eli5":
#         return f"[ELI5] Okay, kiddo! {full_response}"
#     elif mode.lower() == "pidgin":
#         return f"[Pidgin] Dis na wetin e mean: {full_response}"
#     elif mode.lower() == "hybrid":
#         return f"[Hybrid] Simple explain + Pidgin: {full_response}"
#     else:  # standard
#         return f"[Standard] {full_response}"


