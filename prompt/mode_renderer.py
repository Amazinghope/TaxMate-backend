def render_standard(data: dict) -> str:
    """Render persona data in professional English with detailed explanation."""
    description = data.get("description", "You are a taxpayer in Nigeria.")
    taxes_apply = ", ".join(data.get("taxes_apply", [])) or "None"
    taxes_not_apply = ", ".join(data.get("taxes_not_apply", [])) or "None"
    changes = ", ".join(data.get("what_changed_2026", [])) or "None"
    mistakes = ", ".join(data.get("common_mistakes", [])) or "None"
    steps = ", ".join(data.get("next_steps", [])) or "None"

    return (
        f"{description}\n\n"
        f"Taxes that apply to you: {taxes_apply}. These are the taxes you are legally required to pay based on your income and activities.\n"
        f"Taxes that do not apply to you: {taxes_not_apply}. You are exempt from these taxes.\n"
        f"Recent changes in 2026: {changes}. Make sure to understand these updates to remain compliant.\n"
        f"Common mistakes people like you make: {mistakes}. Avoid these to prevent penalties.\n"
        f"Recommended next steps: {steps}. Following these steps will help you stay organized and compliant.\n"
    )

def render_eli5(data: dict) -> str:
    """Render persona data like explaining to a 5-year-old."""
    return (
        f"Hey little buddy! {data.get('description', 'You are a taxpayer in Nigeria.')}\n\n"
        f"Taxes you gotta pay: {', '.join(data.get('taxes_apply', [])) or 'None'}. These are like rules for money you earn.\n"
        f"Taxes you no need pay: {', '.join(data.get('taxes_not_apply', [])) or 'None'}.\n"
        f"New things for 2026: {', '.join(data.get('what_changed_2026', [])) or 'None'}. Just know they changed some rules.\n"
        f"Things people often do wrong: {', '.join(data.get('common_mistakes', [])) or 'None'}. Don't do these!\n"
        f"What you fit do next: {', '.join(data.get('next_steps', [])) or 'None'}. Follow these to stay safe.\n"
    )

def render_pidgin(data: dict) -> str:
    """Render persona data in Nigerian Pidgin with more explanation."""
    return (
        f"Dis na about you: {data.get('description','You be taxpayer for Nigeria.')}\n\n"
        f"Taxes wey you gats pay: {', '.join(data.get('taxes_apply', [])) or 'None'}. Na wetin government dey expect make you pay.\n"
        f"Taxes wey no concern you: {', '.join(data.get('taxes_not_apply', [])) or 'None'}. No worry about these.\n"
        f"Wetin don change for 2026: {', '.join(data.get('what_changed_2026', [])) or 'None'}. Make sure say you sabi dis.\n"
        f"Common wahala wey people dey make: {', '.join(data.get('common_mistakes', [])) or 'None'}. No make the same mistake.\n"
        f"Wetin you suppose do next: {', '.join(data.get('next_steps', [])) or 'None'}. Follow am make your tax waka smooth.\n"
    )

def render_hybrid(data: dict) -> str:
    """Render persona data mixing English and Pidgin with detailed explanation."""
    return (
        f"{data.get('description','You are a taxpayer in Nigeria.')}\n\n"
        f"Taxes wey apply to you: {', '.join(data.get('taxes_apply', [])) or 'None'}. These ones you need to pay so government go dey happy.\n"
        f"Taxes wey no concern you: {', '.join(data.get('taxes_not_apply', [])) or 'None'}.\n"
        f"Changes for 2026: {', '.join(data.get('what_changed_2026', [])) or 'None'}. Make sure say you sabi dis info.\n"
        f"Common mistakes wey people dey make: {', '.join(data.get('common_mistakes', [])) or 'None'}.\n"
        f"Next steps: {', '.join(data.get('next_steps', [])) or 'None'}. Follow these steps to dey correct.\n"
    )
