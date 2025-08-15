from typing import List, Dict, Any

def recommend_plan(user_profile: Dict[str, Any]) -> str:
    """
    Recommends a membership plan based on a user's profile using a rule-based system.

    Args:
        user_profile: dictionary containing user data like 'goal' and 'activities'.

    Returns:
        name of the recommended plan as a string.
    """
    goal = user_profile.get('goal', '').lower()
    activities = [activity.lower() for activity in user_profile.get('activities', [])]

    # rule-based matching can be expanded if needed
    if goal == "lose weight" and "gym" in activities:
        return "Gold Plan"
    elif goal == "relax" and "yoga" in activities:
        return "Silver Plan"
    elif goal == "gain strength" and "football" in activities:
        return "Platinum Plan"
    
    # default fallback plan
    return "Standard Plan"
