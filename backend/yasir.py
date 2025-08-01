import os
import time
import requests
import json
from langchain_google_genai import ChatGoogleGenerativeAI

gemini_api_key = "xxxxxxxxxxxxxxxxxxxxxxxx"
qloo_api_key = "7ebTJkHD8CpDwojzvyCK1ir4ogIR0jbssb7Afz6tAMw"

os.environ["GOOGLE_API_KEY"] = gemini_api_key

qloo_hackathon_endpoint = "https://hackathon.api.qloo.com"

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)

headers = {
    "accept": "application/json",
    "X-Api-Key": qloo_api_key
}

def get_type(prompt):
    messages = [
        (
            "system",
            "Analyze the user's message and decide wheather we have to recommend a restaurant from his old visits or find a new place entirely. Only respond A for the first and B for second, and nothing else",
        ),
        (
            "user", prompt
        ),
    ]
    start_time = time.time()
    ai_msg = llm.invoke(messages)
    end_time = time.time() 

    print(f"Time taken: {end_time - start_time:.3f} seconds")
    print("Response from Gemini:")
    print(ai_msg.content)
    return ai_msg.content.strip().upper()

def get_keywords(prompt):
    messages = [
        (
            "system",
            "Identify and list only the most relevant keywords from the user's message that describe their preferences or requirements for a restaurant. Exclude any mention of location, generic terms like restaurant, place, food, or similar. Respond with a concise, comma-separated list of keywords that capture the user's specific interests, needs, or constraints for choosing a restaurant. Do not include any explanations or extra text.",
        ),
        (
            "user", prompt
        ),
    ]
    start_time = time.time()
    ai_msg = llm.invoke(messages)
    end_time = time.time() 

    print(f"Time taken: {end_time - start_time:.3f} seconds")
    print("Response from Gemini:")
    print(ai_msg.content)
    return ai_msg.content.strip()

def convert_to_urn(tag):
    # Convert tag to URN format
    return tag.replace(":", "%3A").replace(" ", "_")

def get_recommendation(entity, tags = "", operator = "union", take = 5):
    #tag --> urn:tag:genre:action ---> urn%3Atag%3Agenre%3Aaction
    #tags are comma separated
    #operator --> {union or intersection}

    url = f"{qloo_hackathon_endpoint}/recommendations?entity_ids={entity}&type=urn%3Aentity%3Aplace&bias.content_based=0.5&filter.entity_ids={tags}&filter.radius=10&filter.tags=&operator.filter.tags={operator}&page=1&sort_by=affinity&take={take}"

    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    
    with open("response_data.txt", "w") as file:
        json.dump(data, file, indent=2)
    print("Data saved to response_data.txt")
    
    return data

def get_insights(location, tags = "", operator="union", take = 5):

    url = f"{qloo_hackathon_endpoint}/v2/insights?filter.type=urn%3Aentity%3Aplace&filter.location.query={location}&filter.tags={tags}&operator.filter.tags={operator}&take={take}"

    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
        
    with open("response_data.txt", "w") as file:
        json.dump(data, file, indent=2)
    print("Data saved to response_data.txt")
    
    return data

def get_tags(query, take = 10):

    url = f"{qloo_hackathon_endpoint}/v2/tags?feature.typo_tolerance=true&filter.query={query}&take={take}"

    response = requests.get(url, headers=headers)
    data = json.loads(response.text)

    return data

#test the functions
x = get_tags("burger", take=5)
print("Tags:", x)
# t = convert_to_urn("urn:tag:specialty_dish:place:burger")
# data = get_insights("kolkata", tags=t, operator="union", take=5)
# print("Data:", data)
# res = json.dumps(data, indent=2)
# with open("response_data.txt", "w") as file:
#     file.write(res)
# print("Data saved to response_data.txt")
