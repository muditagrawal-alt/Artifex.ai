Artifex.AI

Artifex.AI is a modular, Python-based generative AI application focused on text-to-image generation. The project is built as a clean, extensible system rather than a one-off demo, with emphasis on readable architecture, feature isolation, and future multimodal expansion.

The current implementation uses Stable Diffusion v1.5 and is deployed through a Gradio web interface with prompt history support.

🚀 Core Features
	•	Text-to-image generation using Stable Diffusion v1.5
	•	Interactive Gradio-based web UI
	•	Prompt history sidebar for reusing and tracking generations
	•	Modular Python codebase (each feature isolated)
	•	Local execution support
	•	Custom UI styling via CSS

🧠 Model Details
	•	Base Model: Stable Diffusion v1.5 (Stability AI)
	•	Task: Text-to-Image Generation
	•	Inference: Runs locally on CPU or GPU depending on setup

📁 Project Structure

Artifex.ai/
├── app.py               # Main Gradio application
├── sidebar_history.py   # Prompt history logic and sidebar UI
├── styles.css           # Custom UI styling
├── requirements.txt     # Python dependencies
├── LICENSE              # MIT License
├── README.md            # Project documentation

⚙️ Installation & Setup

1️⃣ Clone the repository

git clone https://github.com/your-username/Artifex.ai.git
cd Artifex.ai

2️⃣ Install dependencies

pip install -r requirements.txt

3️⃣ Run the application

python app.py

The Gradio interface will launch locally in your browser.

🎯 Design Philosophy

Artifex.AI is built with clarity over complexity:
	•	No unnecessary abstraction
	•	Easy-to-read Python files
	•	Features can be added or removed independently
	•	Designed as a foundation for future multimodal AI systems

🔮 Planned Extensions
	•	Audio generation (speech, sound effects, music)
	•	Video generation and editing pipelines
	•	3D asset generation
	•	Unified multimodal prompt handling
	•	Optional offline-first execution

📜 License

This project is licensed under the MIT License.

⚠️ Disclaimer

This project is intended for educational and experimental purposes. Model weights and outputs are subject to the original Stable Diffusion license and usage policies.

👤 Author

Mudit Agrawal
B.Tech CSE (AI/ML)
