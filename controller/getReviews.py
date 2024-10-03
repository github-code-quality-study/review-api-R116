from server_utils.route import route
from server_utils.request import Request
from server_utils.response import Response
from datetime import datetime
from repository.review import getReviewsByFilters
@route("/","GET")
def getReviews(req:Request):
    try:
        query = req.query
        locations=[]
        start_date = None
        end_date = None
        if "location" in query:
            locations = query["location"]
        # convert start_date and end_date to datetime, sample format: "2021-01-01"
        if "start_date" in query:
            start_date = query["start_date"][0]
        if "end_date" in query:
            end_date = query["end_date"][0]
        # get reviews from repository
        reviews = getReviewsByFilters({"location":locations,"start_date":start_date,"end_date":end_date})
        for review in reviews:
            sentiment = req.analyze_sentiment(review["ReviewBody"])
            review["sentiment"] = sentiment
        return Response(200,reviews)
    except Exception as e:
        return Response(500,{"error":str(e)})