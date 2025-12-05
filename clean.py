import os
import json
from openai import OpenAI

API_KEY = "sk-roTlKyXXDUcOI3EsnNuniF41aoCF0czrHzHDfXUdsyT6tmLH"
BASE_URL = "https://gpt.api.zhangyichi.cn/v1" 
MODEL_NAME = "gemini-2.5-flash"     
TEMPERATURE = 0.1

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

def call_llm_api(prompt):
    try:
        print(f"Calling API ({MODEL_NAME})...")
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=TEMPERATURE
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"API Calling Error: {e}")
        return ""

def clean_json_string(text):
    if not text:
        return ""
    cleaned = text.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    elif cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
        
    return cleaned.strip()

def main():
    input_file = "input.txt"
    template_file = "prompt_clean.md"
    output_file = "content.json"

    if not os.path.exists(input_file):
        print(f"Input File {input_file} Not Found")
        return
    if not os.path.exists(template_file):
        print(f"Prompt File {template_file} Not Found")
        return

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            input_content = f.read()
        with open(template_file, 'r', encoding='utf-8') as f:
            prompt_template = f.read()

        final_prompt = prompt_template.replace("{Input_text}", input_content)
        raw_response = call_llm_api(final_prompt)
        
        if not raw_response:
            print("Error: API returned nothing")
            return

        cleaned_response = clean_json_string(raw_response)
        
        try:
            json_data = json.loads(cleaned_response)
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)
            print(f"Succeeded. JSON saved to {output_file}")
            
        except json.JSONDecodeError:
            print("Warning: Invalid JON")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(cleaned_response)
            print(f"JSON saved to {output_file}")

    except Exception as e:
        print(f"Unknown Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()