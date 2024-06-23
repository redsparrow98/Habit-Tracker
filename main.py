import requests
from dotenv import find_dotenv, load_dotenv
import os
from datetime import datetime

# ----------------------------------------------------------------------------------------------------------------------
# ================= #
#   dotenv set-up   #
# ================= #

# Find the .env file automatically by walking up directories until its found
dotenv_path = find_dotenv()

# Load up the entries in the .env file as environment variables
load_dotenv(dotenv_path)

# ----------------------------------------------------------------------------------------------------------------------
# ================= #
#     CONSTANTS     #
# ================= #

PIXELA_USER_TOKEN = os.getenv("PIXELA_USER_TOKEN")
PIXELA_USERNAME = os.getenv("PIXELA_USERNAME")


# ----------------------------------------------------------------------------------------------------------------------
# ================= #
# pixela API SET UP #
# ================= #

"""
https://pixe.la/

* To use pixela we must create a user on the API by setting up the user parameters:
    - token (special identifier almost like a password)
    - username (special identifier for the user)
    - agreeTermsOfService (yes to agreeing to the terms of the API)
    - notMinor (yes to confirm that the user is not a minor)

* These parameters then get passed to the API by using a HTTP Post request using the
    - url (endpoint of the API)
    - json (User params are passed to the API in JSON format to be processed and a user created)

* Once the user is created the request can be commented out since there will be no more need to create the same user 
with same information
"""

# endpoint for pixela API tracking and graphs
pixela_endpoint = "https://pixe.la/v1/users"

# ----------------------------------------------------------------------------------------------------------------------
# 1st STEP CREATE USER (using http post-request)

# Required parameters to Create a new Pixela user on API, token and username are special identifiers for the new user.
user_params = {
    "token": PIXELA_USER_TOKEN,
    "username": PIXELA_USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes",
}

""" 
This code was sued to initially create a user it's no longer necessary but will keep for sake of understanding 
the process explained in the comment block above.
"""
# response = requests.post(url=pixela_endpoint, json=user_params)
# print(response.text)

# ----------------------------------------------------------------------------------------------------------------------
# 2nd STEP CREATE GRAPH DEFINITION

"""
To create a graph first there must be a user registered by following and completing step 1.

* To create a graph it uses a different endpoint 'graph_endpoint' in which 
    - <username> (put in the username of the created user in step 1 or if one exists already)
    - /graphs (extension to access the graph options)

* In order for us to validate the user we would also need to pass on the TOKEN (password) and this API request this to
    be done via HEADERS. We pass this information by creating a Dictionary that contains the requiered key for the 
    header which is usually in the documentation.
    - X-USER-TOKEN (Key that will validate if the value is the token for the user)

The requiered parameters for this post requests are configurations for the graph

* All this information is passed to the API by using a POST request and passing the:
- url   (ENDPOINT)
- json  (CONFIGURATIONS/PARAMETERS)
- headers   (HEADER TOKEN AUTHENTICATION)

* Once the graph is created it can be accessed via https://pixe.la/v1/users/a-know/graphs/test-graph.html
- a-kwon    (put your username)
- test-graph    (put the 'id' of your graph created above)

* Finally the creating the graph POST method can be commented out in order to avoid error messaged if the graph was 
created successfully
"""

# Create a graph endpoint of this format ( https://pixe.la/v1/users/<username>/graphs )
create_graph_endpoint = f"{pixela_endpoint}/{PIXELA_USERNAME}/graphs"


# The token is passed to the request by providing an HTTP header containing the specific key and the token that was used
# to create the suer in the 1st step
headers = {
    "X-USER-TOKEN": PIXELA_USER_TOKEN,
}

# Parameters that we want to send to the API to be used for Graph configuration
graph_config = {
    "id": "graph1",
    "name": "Coding Graph",
    "unit": "hours",
    "type": "float",
    "color": "ajisai"
}

# # To pass on the token credentials, it uses the 'headers=' Kwarg(key word argument)
# graph_request = requests.post(url=create_graph_endpoint, json=graph_config, headers=headers)
# print(graph_request.text)
#
# # To view the graph online, search https://pixe.la/v1/users/a-know/graphs/test-graph.html
# # (a-kwon = put your username(redsparrow98) / test-graph = put the 'id' of your graph created above(graph1))

# ----------------------------------------------------------------------------------------------------------------------
# 3rd STEP CREATING A PIXEL IN THE GRAPH

"""
* This step is to add a pixel of data on a created graph in step 2 (for this case its tracking hours spent coding)

* First the endpoint is slightly different to the one used to create the graph at the end of the endpoint the final 
path is the GraphID that was provided in the graph_config dictionary under the 'id' key.

* Documentation (https://docs.pixe.la/entry/post-pixel) specify how to configurate the data for the pixel.
Two requiered keys are:
- date (representing the date on which you with to enter the data in the format of: YYYYMMDD)
- quantity (Specify the quantity to be registered on the specified date)
(0.1 of an hour is 6min so 2h30min = 2.5 / 2h40min = 2.66 etc)

* In order for the date to automatically be detected for the day of use the program uses datetime module and formats the
now() result by using the strftime() Method (https://www.w3schools.com/python/python_datetime.asp)
creating the requiered inout of the date yyyymmdd to be passed in to the POST request.

- Or if we want to backdate and input a different date the we can create a specific date object like this:
date = datetime(year=2024, month=6, day=22)
then the date gets formated using the date.strftime("%Y%m%d") and passed in to the request


* This post requires the Token to be passed in the header for authentication before the post is allowed, since this was
used in step 2 as well this part will reuse the 'header' dictionary contain the authentication token for the PixelaAPI

* For the purposes of step 4 and 5 updating and deleting the pixel the create pixel request will be commented out
"""

# The graph ID that will be used to CREATE, UPDATE & DELETE pixels of the graph for this program
graph_id = graph_config["id"]

# This endpoint is to post a pixel to a specific graph - format (/v1/users/<username>/graphs/<graphID>)
pixel_creation_endpoint = f"{pixela_endpoint}/{PIXELA_USERNAME}/graphs/{graph_id}"

# For the date to be filled out automatically for every day to save manual input use date time.
# To format the date to fit the PixelaAPI 'date' key format requirements use the strftime() method
# (https://www.w3schools.com/python/python_datetime.asp)
date = datetime.now()
formated_date = date.strftime("%Y%m%d")

# Requiered parameters to create the pixel on the graph (date(yyyymmdd), quantity: Float [0-9].[0-9])
pixel_conf = {
    "date": formated_date,
    "quantity": "3",
}

# # Post request for the pixel creation passing on the pixel_par to be saved on the graph
# pixel_creation = requests.post(url=pixel_creation_endpoint, json=pixel_conf, headers=headers)
# print(pixel_creation.text)

# ----------------------------------------------------------------------------------------------------------------------
# 4th STEP UPDATING A PIXEL ON THE GRAPH

"""
* To update the data in a pixel the request uses the PUT method.

* Each pixel has a unique key identifying it in the DB(database) for this API it is the date.
- To update a pixel we must know what date we want to update in the graph, so the endpoint for updating is the
Pixela endpoint/ username/ graphs/ graph_id / date of teh pixel we want to update.

* The parameters that are being passed is the 'quantity' which will update the already existing quantity value with the
new value being passed in the PUT request

* The request is commented out once action is complete to avoid errors
"""

# Date if the pixel you wish to update
update_date = "20240620"

# Endpoint for the updating an existing pixel on a graph
update_pixel_endpoint = f"{pixela_endpoint}/{PIXELA_USERNAME}/graphs/{graph_id}/{update_date}"

# New quantity to replace/update the original data in the pixel DB(database)
update_params = {
    "quantity": "3.8"
}

# # Put request to update an existing pixel with different data. Each pixel has a special date that identifies them
# update_response = requests.put(url=update_pixel_endpoint, json=update_params, headers=headers)
# print(update_response.text)


# ----------------------------------------------------------------------------------------------------------------------
# 5th STEP DELETING AN EXISTING PIXEL FROM THE GRAPH ENTIRELY

"""
* To delete a pixel from the DB(database) we use the DELETE request.

* Same as in step 4 to access a specific pixel we need the unique key which is the date. This way the program and server 
knows exactly which entry we want to delete. So the endpoint is the same as updating a pixel since we need access to a
specific pixel in the DB.

* To delete the pixel we simply use the DELETE request and pass in the endpoint with the graph id and the pixel key as 
well as the header to authenticate the user. This will delete the pixel if one exists with such a date key.

* The delete request is commented out after action is complete to avoid errors.
"""

# # Delete request to delete a pixel from the DB(database) fully
# delete_pixel_response = requests.delete(url=update_pixel_endpoint, headers=headers)
# print(delete_pixel_response.text)
