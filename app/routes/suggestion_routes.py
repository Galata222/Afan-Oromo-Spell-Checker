# Import necessary modules
from flask import jsonify, Blueprint, request
from app.suggestion_ranking.suggestion_ranking import SuggestionRanking

# Create a Blueprint for suggestion ranking routes
suggestion_ranking_routes = Blueprint('suggestion_ranking_routes', __name__)

# Create an instance of the SuggestionRanking class
suggestion_ranker = SuggestionRanking('app/knowledge_base/resources/dictionary.aff')  # Pass the .aff file path to SuggestionRanking

# Route for ranking suggestions
@suggestion_ranking_routes.route('/rank_suggestions', methods=['POST'])
def rank_suggestions():
    # print("Received request for ranking suggestions.")
    
    data = request.get_json()
    suggestions = data.get('suggestions', [])
    misspelled_word = data.get('errors', "")
    print(f"Received suggestions: {suggestions}")
    print(f"Received misspeltword: {misspelled_word}")
    # Use the SuggestionRanking class to rank suggestions
    ranked_suggestions = suggestion_ranker.rank_suggestions(suggestions, misspelled_word)

    print(f"Returning ranked suggestions: {ranked_suggestions}")
    return jsonify({'ranked_suggestions': ranked_suggestions})
