from server_utils.route import route
from server_utils.request import Request
from server_utils.response import Response
from repository.review import addReview as addReviewRepo
from models.review import Review
from datetime import datetime
from uuid import uuid4
@route("/","POST")
def addReview(req:Request):
    try:
        review:Review = {}
        #check if req body is same as the Review model
        if "ReviewBody" not in req.body or "Location" not in req.body:
            return Response(400,{"error":"ReviewBody and Location are required"})
        review["Timestamp"] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        review["ReviewBody"] = req.body["ReviewBody"][0]
        review["Location"] = req.body["Location"][0]
        review["ReviewId"] = str(uuid4())
        valid = addReviewRepo(review)
        if not valid:
            return Response(400,{"error":"Invalid Location"})
        return Response(201,review)
    except Exception as e:
        return Response(500,{"error":str(e)})