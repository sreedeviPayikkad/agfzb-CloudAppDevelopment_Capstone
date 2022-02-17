import requests
import json
from .models import CarMake, CarModel, CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("returned status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


def get_request_with_key(url, api_key, **kwargs):
    try:
        params = dict()
        params["text"] = kwargs["text"]
        params["version"] = kwargs["version"]
        params["features"] = kwargs["features"]
        params["return_analyzed_text"] = kwargs["return_analyzed_text"]

        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                params=params, auth=HTTPBasicAuth('apikey', api_key))
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)

def post_request(url, json_payload, **kwargs):
    try:
        # Call post method of requests library with URL and parameters
        #response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
        response = requests.post(url, params=kwargs, json=json_payload)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    json_data = json.loads(response.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        dealers = json_result["allDealerships"]

        # For each dealer object
        for dealer in dealers:
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):

def get_dealer_by_id_from_cf(url, dealerId):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerID=dealerId)
    if json_result:
        dealers = json_result["Docs"]

        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            #dealer_doc = dealer["doc"]
            dealer_doc = dealer

            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


def get_dealer_by_state_from_cf(url, dealerState):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, state=dealerState)
    if json_result:
        dealers = json_result["allDealershipsByState"]

        # For each dealer object
        for dealer in dealers:
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerID=dealerId)
    if json_result:
        reviews = json_result["Docs"]

        # For each dealer object
        for review in reviews:
            review_doc = review
            # Create a DealerReview object with values in `doc` object
            review_obj = DealerReview(dealership=review_doc["dealership"], name=review_doc["name"], purchase=review_doc["purchase"],
                                      review=review_doc["review"], purchase_date=review_doc[
                                          "purchase_date"], car_make=review_doc["car_make"],
                                      car_model=review_doc["car_model"],
                                      car_year=review_doc["car_year"], sentiment="")

            # Getting the sentiment
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)

            results.append(review_obj)

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):

    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/9d2f2eff-6c78-4403-9f5f-174865d0e65a/v1/analyze?version=2019-07-12"
    api_key = "RsUUjVAxkhwlFH0NWHxCXZ4v1pcbn-LqC-wuYYBIjhbS"
    version = "2020-08-01"
    feature = "sentiment"
    return_analyzed_text = True

    result_json = get_request_with_key(url, text=text, api_key=api_key, version=version, features=feature,
                                       return_analyzed_text=return_analyzed_text)

    try:
        sentiment = result_json['sentiment']['document']['label']
    except:
        sentiment = "neutral"

    return(sentiment)
