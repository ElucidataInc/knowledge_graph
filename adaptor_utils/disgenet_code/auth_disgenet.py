import requests
import sys

def authenticate_user(cui_identifier, email, password):

    auth_params = {"email":email,"password":password}

    api_host = "https://www.disgenet.org/api"

    api_key = None
    s = requests.Session()
    try:
        r = s.post(api_host+'/auth/', data=auth_params)
        if(r.status_code == 200):
            #Lets store the api key in a new variable and use it again in new requests
            print('You have been authenticated\n')
            json_response = r.json()
            api_key = json_response.get("token")

        else:
            print(r.status_code)
            sys.exit('Couldn\'t authenticate')

    except requests.exceptions.RequestException as req_ex:
        print(req_ex)
        print("Something went wrong with the request.")

    if api_key:
        #Add the api key to the requests headers of the requests Session object in order to use the restricted endpoints.
        s.headers.update({"Authorization": "Bearer %s" % api_key}) 
        #Get disease-gene associations for a disease for ALL sources in TSV (to change format use ?format=json)
        gda_response = s.get(api_host+f'/gda/disease/{cui_identifier}?source=ALL&type=disease&format=tsv')
        if(gda_response.status_code == 200):
            print('Query Successful')
            return(gda_response)
        else:
            sys.exit('Unable to fetch contents for query, Try Again')

    if s:
        s.close()