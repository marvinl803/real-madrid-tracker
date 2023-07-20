import os
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, render_template, request
from football_data import FootballDataClient
from news_data import NewsApiClient

load_dotenv()

# Fetch news information
news_api_key = "5b704ab1766847f7be25a5b261cb4780"
news_client = NewsApiClient(news_api_key)
query = "Real Madrid AND football"
news_articles = news_client.get_articles(query)

# Process news articles
news_articles_data = []
for article in news_articles:
    article_title = article["title"]
    article_description = article.get("description", "")  # Use a default value if 'description' is not present
    article_url = article["url"]
    article_image = article.get("image", "")  # Remove the 'image' field

    article_data = {
        "title": article_title,
        "description": article_description,
        "url": article_url,
    }

    news_articles_data.append(article_data)

# Fetch all match information from the football data API
client = FootballDataClient(os.getenv("FootballDataAPI"))
real_madrid_matches = client.get_matches(team_id=86)

matches_list = []
for match in real_madrid_matches:
    match_dict = {
        'match_id': match['id'],
        'competition': match['competition']['name'],
        'home_team': match['homeTeam']['name'],
        'home_team_id': match['homeTeam']['id'],
        'away_team': match['awayTeam']['name'],
        'away_team_id': match['awayTeam']['id'],
        'home_score': match['score']['fullTime']['homeTeam'],
        'away_score': match['score']['fullTime']['awayTeam'],
        'match_date': match['utcDate'],
        'status': match['status'],
        'referee': match['referees'][0]['name'] if match['referees'] else None
    }
    matches_list.append(match_dict)


def find_nearest_match(matches):
    today = datetime.now().date()
    sorted_matches = sorted(matches, key=lambda match: abs(datetime.strptime(match['match_date'], '%Y-%m-%dT%H:%M:%SZ').date() - today))
    return sorted_matches[0] if sorted_matches else None


def create_app():

    app = Flask(__name__)

    @app.route('/news')
    def news():
        return render_template('news.html', news_articles=news_articles_data)

    @app.route('/matches', methods=['GET', 'POST'])
    def matches():
        if request.method == 'POST':
            selected_date = request.form['date']
            filtered_matches = [match for match in matches_list if match['match_date'].startswith(selected_date)]
            if 'show_all' in request.form:
                return render_template('matches.html', matches_list=matches_list, news_articles=news_articles_data)
            elif filtered_matches:
                nearest_match = find_nearest_match(filtered_matches)
                return render_template('matches.html', nearest_match=nearest_match)
            else:
                return render_template('matches.html', no_matches=True)
        else:
            nearest_match = find_nearest_match(matches_list)
            return render_template('matches.html', nearest_match=nearest_match, news_articles=news_articles_data)

    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/matches/<match_id>')
    def match_details(match_id):
        match = next((match for match in matches_list if str(match['match_id']) == match_id), None)
        if match:
            return render_template('match_details.html', match=match)
        else:
            return "Match not found"

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
