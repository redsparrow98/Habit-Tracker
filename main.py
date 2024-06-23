import requests
from dotenv import find_dotenv, load_dotenv
import os

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

* Documentation (https://docs.pixe.la/entry/post-pixel) specifys how to configurate the data for the pixel.
Two requiered keys are:
- date (representing the date on which you with to enter the data in the format of: YYYYMMDD)
- quantity (Specify the quantity to be registered on the specified date )

* This post requires the Token to be passed in the header for authentication before the post is allowed, since this was
used in step 2 as well this part will reuse the 'header' dictionary contain the authentication token for the PixelaAPI

"""

# This endpoint is to post a pixel to a specific graph - format (/v1/users/<username>/graphs/<graphID>)
pixel_creation_endpoint = f"{pixela_endpoint}/{PIXELA_USERNAME}/graphs/graph1"

# Requiered parameters to create the pixel on the graph (date(yyyymmdd), quantity: Float [0-9].[0-9])
pixel_conf = {
    "date": "20240622",
    "quantity": "2.0",
}

# Request for the pixel creation passing on the pixel_par to be saved on the graph
pixel_creation = requests.post(url=pixel_creation_endpoint, json=pixel_conf, headers=headers)
print(pixel_creation.text)
