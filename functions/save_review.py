#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import sys
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests

def main(dict):

    databaseName = "reviews"
    data_dict = {}
    data_dict = dict["review"]
    #return {"result" : len(data_dict.keys())}
    if len(data_dict.keys()) > 0 :
        try:
            client = Cloudant.iam(
                    account_name=dict["COUCH_USERNAME"],
                    api_key=dict["IAM_API_KEY"],
                    connect=True,
                )
            my_database = client[databaseName] 
                
                # Create review document content data
            data = {
                'name': data_dict["name"],
                'dealership': data_dict["dealership"],
                "review": data_dict["review"],
                "purchase": data_dict["purchase"],
                "purchase_date": data_dict["purchase_date"],
                "car_make": data_dict["car_make"],
                "car_model": data_dict["car_model"],
                "car_year": data_dict["car_year"]
                }
            
            # Create a document using the Database API
            my_document = my_database.create_document(data)

            # Check that the document exists in the database
            if my_document.exists():
                print('SUCCESS!!')
                return({"status":200,"message": "Review added"})
        
        except CloudantException as ce:
            print("unable to connect")
            return {"error": ce}
        except (requests.exceptions.RequestException, ConnectionResetError) as err:
            print("connection error")
            return {"error": err}   
    else:
        return {"status":500,"message":"Error: missing name"}
    