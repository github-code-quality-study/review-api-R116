from models.review import Review
from typing import List
from datetime import datetime
import csv
def getAllReviews()->List[Review]:
    reviews=[]
    with open('data/reviews.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            # Unpack the row dictionary directly into the Review constructor
            review = Review(**row)
            reviews.append(review)
    return reviews

def addReview(review:Review)->bool:
    reviews = getAllReviews()
    foundLocation = False
    for r in reviews:
        if r["Location"] == review["Location"]:
            foundLocation = True
            break
    return foundLocation


def getFilter(query:dict,review:Review)->bool:
    condition = True
    if "location" in query and query["location"] is not None and len(query["location"])>0:
        condition = condition and review["Location"] in query["location"]
    if "start_date" in query and query["start_date"] is not None:
        condition = condition and datetime.strptime(review["Timestamp"], "%Y-%m-%d %H:%M:%S") >= datetime.strptime(query["start_date"], "%Y-%m-%d")
    if "end_date" in query and query["end_date"] is not None:
        condition = condition and datetime.strptime(review["Timestamp"], "%Y-%m-%d %H:%M:%S") <= datetime.strptime(query["end_date"], "%Y-%m-%d")
    return condition
def getReviewsByFilters(filters:dict)->List[Review]:
    reviews = getAllReviews()
    filtered_reviews = [review for review in reviews if getFilter(filters,review)]    
    return filtered_reviews
