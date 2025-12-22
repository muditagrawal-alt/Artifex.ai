from datetime import datetime #Real-time timestamps for when the prompt was made
import pytz #Allows access to a vide range of time zones world-wide
import base64

history_data = []

#Function for adding the time zone to the prompt in history
def add_to_history(prompt, image_path):
    ist = pytz.timezone("Asia/Kolkata")
    timestamp = datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S")
    history_data.append({
        "prompt": prompt,
        "image": image_path,
        "timestamp": timestamp
    })

#Function for history data
def render_history():
    if not history_data:
        return "<p>No history yet.</p>"

    html = "<div style='max-height: 400px; overflow-y: auto;'>"
    for idx, entry in enumerate(history_data):
        try:
            with open(entry["image"], "rb") as f:
                encoded = base64.b64encode(f.read()).decode("utf-8")
                img_data = f"data:image/jpeg;base64,{encoded}"
        except Exception as e:
            img_data = ""

        html += f"""
        <div style='margin-bottom: 10px; border-bottom: 1px solid #ccc; padding-bottom: 10px;'>
            <p><b>{idx + 1}. {entry['prompt']}</b> <br> <small>{entry['timestamp']}</small></p>
            <img src="{img_data}" style="width: 100px; height: auto; border-radius: 6px;" />
        </div>
        """
    html += "</div>"
    return html



