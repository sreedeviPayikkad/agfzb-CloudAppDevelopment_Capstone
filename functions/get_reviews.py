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

    #if dict["dealerID"]:
       
    print(dict['dealerID'])
    
    databaseName = "reviews"

    #return({"Docs": int(dict['dealerID'])})

    try:
        client = Cloudant.iam(
            account_name=dict["COUCH_USERNAME"],
            api_key=dict["IAM_API_KEY"],
            connect=True,
        )
        #print("Databases: {0}".format(client.all_dbs()))

        my_database = client[databaseName] 
        
        #selector = {'id ': dict["dealerID"]} 
        selector = {'dealership': {'$eq': int(dict['dealerID'])}}
        result_by_filter = my_database.get_query_result(selector,raw_result=True,limit=100) 

        reviews = result_by_filter["docs"]
        
        return({"Docs": reviews})
        

    except CloudantException as ce:
        print("unable to connect")
        return {"error": ce}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    return {"dbs": client.all_dbs()}