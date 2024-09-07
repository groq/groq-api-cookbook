import gradio as gr
import base64
from PIL import Image
import io
import requests
from groq import Groq

# Groq API settings
LLAVA_MODEL = "llava-v1.5-7b-4096-preview"
LLAMA_GUARD_MODEL = "llama-guard-3-8b"

def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def analyze_image(image, prompt, api_key, is_url=False):
    client = Groq(api_key=api_key)
    
    if is_url:
        image_content = {"type": "image_url", "image_url": {"url": image}}
    else:
        base64_image = encode_image(image)
        image_content = {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        image_content,
                    ],
                }
            ],
            model=LLAVA_MODEL,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def check_content_safety(image_description, api_key):
    client = Groq(api_key=api_key)
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a content safety classifier. Analyze the given text and determine if it contains any unsafe or inappropriate content."},
                {"role": "user", "content": f"Please analyze this image description for any unsafe or inappropriate content: {image_description}"}
            ],
            model=LLAMA_GUARD_MODEL,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def process_image(image, url, prompt, api_key):
    if image is not None:
        return analyze_image(image, prompt, api_key), check_content_safety(analyze_image(image, prompt, api_key), api_key)
    elif url:
        try:
            response = requests.get(url)
            image = Image.open(io.BytesIO(response.content))
            return analyze_image(url, prompt, api_key, is_url=True), check_content_safety(analyze_image(url, prompt, api_key, is_url=True), api_key)
        except:
            return "Invalid image URL. Please provide a direct link to an image.", ""
    else:
        return "Please provide an image to analyze.", ""

def launch():
    with gr.Blocks() as demo:
        gr.Markdown("# Image Analysis with Groq API")
        
        with gr.Row():
            with gr.Column():
                api_key = gr.Textbox(label="Enter your Groq API Key:", type="password")
                image_input = gr.Image(type="pil", label="Upload Image")
                url_input = gr.Textbox(label="Or paste image URL")
                prompt = gr.Textbox(label="Enter a prompt for image analysis:", value="Describe the contents of this image in detail.")
                analyze_button = gr.Button("Analyze Image")
            
            with gr.Column():
                analysis_output = gr.Textbox(label="Analysis Result")
                safety_output = gr.Textbox(label="Content Safety Check")
        
        analyze_button.click(
            fn=process_image,
            inputs=[image_input, url_input, prompt, api_key],
            outputs=[analysis_output, safety_output]
        )
    
    demo.launch()

if __name__ == "__main__":
    launch()