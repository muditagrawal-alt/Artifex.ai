#Importing the necessary python libraries
import gradio as gr #For UI
import uuid #Provides a powerful and flexible way to generate Universally Unique Identifiers (UUID)
import os #Enables working with File System
import requests #Used to make HTTP requests 
import base64 #Decodes the Base 64 encoded image data retrieved by the Stability API key
from PIL import Image #Imports the image module from the Pillow(Enables opening, manipulating, and saving images) package
from io import BytesIO #Treats raw Binary Data
from sidebar_history import add_to_history, render_history, history_data #Imports key components from sidebar_history.py

#Image generation function which calls Stablity API key
def generate_image_from_prompt(prompt):
    api_key = os.getenv("STABILITY_API_KEY")
    if not api_key:
        raise RuntimeError("❌ STABILITY_API_KEY not found in environment.")

    engine_id = "stable-diffusion-xl-1024-v1-0"
    url = f"https://api.stability.ai/v1/generation/{engine_id}/text-to-image"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "text_prompts": [{"text": prompt}],
        "aspect_ratio": "1:1"
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        print("❌ API Error:", response.status_code, response.text)
        raise RuntimeError("Image generation failed.")

    result = response.json()
    if "artifacts" not in result or not result["artifacts"]:
        raise RuntimeError("No image returned in API response.")

    image_data = base64.b64decode(result["artifacts"][0]["base64"])
    image = Image.open(BytesIO(image_data)).convert("RGB")

    os.makedirs("/tmp/images", exist_ok=True)
    filename = f"/tmp/images/{uuid.uuid4().hex}.jpeg"
    image.save(filename, format="JPEG", quality=95)

    return filename

#Function to generate prompt
def generate(prompt):
    image_path = generate_image_from_prompt(prompt)
    add_to_history(prompt, image_path)
    return image_path, render_history()

#Function to delete prompt one prompt via index
def delete_prompt(index):
    try:
        index = int(str(index).strip())
        if 1 <= index <= len(history_data):
            del history_data[index - 1]
    except:
        pass
    return render_history()

#Function to delete all the prompts in history
def delete_all():
    history_data.clear()
    return render_history()
    
#Gradio UI Layout
with gr.Blocks(css="styles.css") as demo:
    sidebar_visible = gr.State(False)

    gr.HTML("<style>" + open("styles.css", "r").read() + "</style>")


    toggle_sidebar = gr.Button("☰", elem_id="history-toggle-button")

    # Title
    gr.Markdown("## Artifex.AI: Generating Images from Text Prompts")

    # Main prompt input row
    with gr.Row():
        prompt = gr.Textbox(
            placeholder="Enter your prompt and press Enter...",
            show_label=False,
            elem_id="prompt-box"
        )

        generate_btn = gr.Button("Generate", elem_id="generate-btn")

    # Output image
    output_image = gr.Image(
        label="Generated Image",
        interactive=False,
        elem_id="generated-image"
    )

    #Index for prompt deletion
    with gr.Column(visible=False, elem_id="sidebar") as history_sidebar:
        history_gallery = gr.HTML()

        with gr.Row():
            with gr.Column(scale=7):
                delete_index = gr.Textbox(
                    label="Index",
                    placeholder="Enter index (e.g. 1)",
                    lines=1
                )
            with gr.Column(scale=3):
                delete_btn = gr.Button("Delete Prompt")

        clear_btn = gr.Button("Clear All History")

    #Connects frontend to the backend defining how the app behaves when a user interacts with it
    def toggle(visible):
        return not visible, gr.update(visible=not visible)

    toggle_sidebar.click(toggle, inputs=[sidebar_visible], outputs=[sidebar_visible, history_sidebar])
    generate_btn.click(generate, inputs=[prompt], outputs=[output_image, history_gallery])
    prompt.submit(generate, inputs=[prompt], outputs=[output_image, history_gallery])
    delete_btn.click(delete_prompt, inputs=[delete_index], outputs=[history_gallery])
    delete_index.submit(delete_prompt, inputs=[delete_index], outputs=[history_gallery])
    clear_btn.click(delete_all, outputs=[history_gallery])

#Launches the App
if __name__ == "__main__":
    demo.launch()