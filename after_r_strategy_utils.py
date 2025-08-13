from recommendation_utils import handle_recommendation_and_selection

def after_r_strategy(driver):
    """
    Handles post R-Strategy update actions: clicks Recommendations & Selections tab, waits, then clicks Next.
    """
    handle_recommendation_and_selection(driver)
