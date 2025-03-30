import google.generativeai as genai

genai.configure(api_key="AIzaSyDbS-NVjFAVroQTvOfKoMs8CtUvB1QKN2I")
models = genai.list_models()

for model in models:
    print(model.name)
