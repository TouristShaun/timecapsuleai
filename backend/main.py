from flask import Flask, jsonify, request, abort, send_from_directory
from models import db, init_app, Paper, Insight, BusinessInsight, CuratedList, Trend
from user_auth import init_app, load_user, register_user, login_user, logout_user

app = Flask(__name__)

# Initialize the database
init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/papers', methods=['GET'])
def get_papers():
    try:
        papers = Paper.query.all()
        if papers:
            return jsonify({"papers": [paper.serialize() for paper in papers]}), 200
        else:
            return jsonify({"error": "No papers found"}), 404
    except:
        abort(500)  # Internal Server Error

@app.route('/insights', methods=['GET'])
def get_insights():
    try:
        insights = Insight.query.all()
        if insights:
            return jsonify({"insights": [insight.serialize() for insight in insights]}), 200
        else:
            return jsonify({"error": "No insights found"}), 404
    except:
        abort(500)

@app.route('/trends', methods=['GET'])
def get_trends():
    try:
        trends = Trend.query.all()
        if trends:
            return jsonify({"trends": [trend.serialize() for trend in trends]}), 200
        else:
            return jsonify({"error": "No trends found"}), 404
    except:
        abort(500)

@app.route('/business_insights', methods=['GET'])
def get_business_insights():
    try:
        business_insights_data = BusinessInsight.query.all()
        if business_insights_data:
            return jsonify({"business_insights": [bi.serialize() for bi in business_insights_data]}), 200
        else:
            return jsonify({"error": "No business insights found"}), 404
    except:
        abort(500)

@app.route('/curated_lists', methods=['GET'])
def get_curated_lists():
    try:
        lists = CuratedList.query.all()
        if lists:
            return jsonify({"curated_lists": [clist.serialize() for clist in lists]}), 200
        else:
            return jsonify({"error": "No curated lists found"}), 404
    except:
        abort(500)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return send_from_directory('frontend/build', 'index.html')


if __name__ == "__main__":
    app.run()
