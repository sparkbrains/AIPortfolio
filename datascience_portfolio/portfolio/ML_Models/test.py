import requests

app_id = '3471473083142359'
app_secret = 'ad25aa12f6f2939ce28be9bdd4604604'

# Generate access token
def generate_access_token(app_id, app_secret):
    url = f'https://graph.facebook.com/oauth/access_token?client_id={app_id}&client_secret={app_secret}&grant_type=client_credentials'
    response = requests.get(url)
    response_json = response.json()
    access_token = response_json['access_token']
    return access_token

access_token = generate_access_token(app_id, app_secret)

user_id = '103961672729659'
# url = f'https://graph.facebook.com/{user_id}?fields=first_name,last_name&access_token={access_token}'
# response = requests.get(url)
# response_json = response.json()
# first_name = response_json['first_name']
# last_name = response_json['last_name']
# print(first_name,"???????????????????")
# print(last_name,"???????????????????")

url = f'https://graph.facebook.com/{user_id}/accounts?access_token={access_token}'

response = requests.get(url)
response_json = response.json()
print(response_json)
# post_id = 104047409387752
# def get_likes_and_comments(post_id, access_token):
#     # Retrieve likes
#     likes_url = f"https://graph.facebook.com/v12.0/{post_id}/likes"
#     likes_params = {
#         "access_token": access_token
#     }
#     likes_response = requests.get(likes_url, params=likes_params)
#     likes_data = likes_response.json()

#     # Retrieve comments
#     comments_url = f"https://graph.facebook.com/v12.0/{post_id}/comments"
#     comments_params = {
#         "access_token": access_token
#     }
#     comments_response = requests.get(comments_url, params=comments_params)
#     comments_data = comments_response.json()

#     return likes_data, comments_data

# # Replace with your post ID and access token
# post_id = "your_post_id"
# access_token = "your_access_token"

# likes, comments = get_likes_and_comments(post_id, access_token)
# print(likes,"????????")
# # print("Likes:")
# # for like in likes['data']:
# #     print(like['name'])

# # print("\nComments:")
# # for comment in comments['data']:
# #     print(f"{comment['from']['name']}: {comment['message']}")



# import facebook




# app_id = '3471473083142359'
# app_secret = 'ad25aa12f6f2939ce28be9bdd4604604'


# # Set the permissions you need
# permissions = ['user_posts']

# # Generate a login URL to get the user's permission
# oauth_url = facebook.GraphAPI().get_auth_url(app_id, app_secret, permissions)
# print("Please visit the following URL and grant permission:")
# print(oauth_url)
# print()

# # After the user grants permission, obtain the access token
# access_token = input("Enter the access token generated after granting permission: ")

# # Create a Facebook Graph API instance
# graph = facebook.GraphAPI(access_token)

# # Get the user's posts
# user_posts = graph.get_connections('me', 'posts')

# print("Post IDs:")
# for post in user_posts['data']:
#     print(post['id'])



# Set your app credentials



# Set the permissions you need
# permissions = ['user_likes', 'user_posts']

# # Generate a login URL to get the user's permission
# oauth_url = facebook.GraphAPI().get_auth_url(app_id, app_secret, permissions)
# print("Please visit the following URL and grant permission:")
# print(oauth_url)
# print()

# # After the user grants permission, obtain the access token
# access_token = input("Enter the access token generated after granting permission: ")

# # Create a Facebook Graph API instance
# graph = facebook.GraphAPI(access_token)

# # Get likes and comments for a post
# post_id = '104047409387752'

# likes = graph.get_connections(post_id, 'likes')
# comments = graph.get_connections(post_id, 'comments')

# print("Likes:")
# for like in likes['data']:
#     print(like['name'])

# print("\nComments:")
# for comment in comments['data']:
#     print(f"{comment['from']['name']}: {comment['message']}")
