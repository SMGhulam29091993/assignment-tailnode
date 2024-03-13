import requests
from pymongo import MongoClient

# Function to fetch users data from the API and store it in the database
def fetch_and_store_users(api_key, users_collection):
    url = "https://dummyapi.io/data/v1/user"
    headers = {"app-id": api_key}
    response = requests.get(url, headers=headers)
    users_data = response.json()["data"]
    
    for user in users_data:
        print(user)  # Print the user dictionary
        user_id = user["id"]
        first_name = user["firstName"]
        last_name = user["lastName"]
        # Check if the 'email' key exists in the user dictionary before accessing it
        email = user.get("email")
        if email is not None:
            # Insert user data into the database
            users_collection.insert_one({
                "user_id": user_id,
                "first_name": first_name,
                "last_name": last_name,
                "email": email
            })

# Function to fetch posts data for each user from the API and store it in the database
def fetch_and_store_posts(api_key, collection):
    users = collection.find()
    
    for user in users:
        url = f"https://dummyapi.io/data/v1/user/{user['_id']}/post"
        headers = {"app-id": api_key}
        response = requests.get(url, headers=headers)
        posts_data = response.json()["data"]
        
        for post in posts_data:
            post_data = {
                "_id": post["id"],
                "user_id": user["_id"],
                "text": post["text"]
                # Add other post data as required
            }
            # Insert post data into the collection
            collection.insert_one(post_data)

# Main function to execute the script
def main():
    # Connect to the MongoDB server
    client = MongoClient("mongodb://127.0.0.1:27017/")
    
    # Select or create a database
    db = client["dummy_db"]
    
    # Select or create a collection for users
    users_collection = db["users"]
    
    # Select or create a collection for posts
    posts_collection = db["posts"]
    
    # Replace 'your_api_key' with your actual API key obtained after login
    api_key = '65f1dec92d8e5b4fc6534749'
    
    # Fetch and store users data
    fetch_and_store_users(api_key, users_collection)
    
    # Fetch and store posts data
    fetch_and_store_posts(api_key, posts_collection)
    
    # Close the MongoDB connection
    client.close()

if __name__ == "__main__":
    main()
