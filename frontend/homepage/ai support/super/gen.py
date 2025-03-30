import google.generativeai as genai

genai.configure(api_key="AIzaSyDbS-NVjFAVroQTvOfKoMs8CtUvB1QKN2I")

def generate_event_post(event_name, date, location, theme, audience):
    prompt = (
        f"Generate an engaging social media post for an event named '{event_name}' happening on {date} at {location}. "
        f"The theme is '{theme}' and the target audience is {audience}. Include a catchy caption, hashtags, and a call to action."
    )
    
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    response = model.generate_content(prompt)
    
    return response.text

# Example usage
event_name = "AI Revolution Summit 2025"
date = "June 15, 2025"
location = "San Francisco, CA"
theme = "The Future of Artificial Intelligence"
audience = "Tech enthusiasts, developers, and AI researchers"

post_content = generate_event_post(event_name, date, location, theme, audience)
print(post_content)