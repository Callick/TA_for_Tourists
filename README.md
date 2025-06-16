# PortoLingua: Translation Assistant for Tourists 🇵🇹➡️🌍
This is an intelligent translation system designed to assist visitors in communicating in Porto, Portugal. Using OCR (Optical Character Recognition) technology and neural machine translation, it translates Portuguese text from street signs, menus, and information boards into a user's chosen language. It also recommends local attractions by recognising locations based on user input.
## 🔑 Key Features
**✅ Real-time Text Extraction:** Reads Portuguese text from images or camera input<br>
**✅ Format-Preserving Translation:** Maintains original layout during translation<br>
**✅ Location-Aware Recommendations:** Suggests closest attractions with distance markers<br>
**✅ Interactive Maps:** Shows mini-map thumbnails with expandable detailed views<br>
**✅ Multilingual Support:** Translates to English, French, German, and Italian<br>
**✅ Intelligent Address Detection:** Identifies Portuguese street names and locations
## 🛠 Technology Stack
  **1. AI/ML:** EasyOCR (CRNN model), Google Translate (via deep-translator) <br>
  **2. Backend:** Python 3.9, Streamlit <br>
  **3. Geospatial:** Folium, GeoPy, Nominatim <br>
  **4. Data Processing:** Pandas, NumPy <br>
  **5. Computer Vision:** Pillow (PIL) <br>
## ♻️ Workflow
 ![system_workflow](https://github.com/user-attachments/assets/51ea2fab-bb75-4292-acd1-9870eb6a86a8)

## ⚙️ Prerequisites
Before using this project, ensure the following:
  1. Python 3.9+
  2. Tesseract OCR engine
  3. Webcam (for live capture feature)
## 🚀 Installation & Setup
 **1. Clone the repository:**
```
    git clone https://github.com/Callick/TA_for_Tourists.git
    cd TA_for_Tourists
```
 **2. Install Python Dependencies**
```
    pip install streamlit numpy pillow easyocr pandas langdetect deep-translator geopy streamlit-folium
```
 **3. Install Tesseract OCR**
  - Windows: Download then install the following link - https://github.com/UB-Mannheim/tesseract/wiki
  - MacOS:
```
    brew install tesseract
```
  - Linux (Debian/Ubuntu):
```
    sudo apt install tesseract-ocr
```
 **4. Download Landmark Data**
 The project includes 'porto_landmarks.csv' with major Porto attractions. Just keep it on the same path.
## 🖥️ Running the Application
```![system_workflow](https://github.com/user-attachments/assets/0c40aa26-82ad-4844-a723-72f3221371a2)

    streamlit run TAforTourists.py
```
## 📂 Project Structure
Keep files as instructed below
```
    Translation Assistant for Tourists/
├── TAforTourists.py          # Main application
├── porto_landmarks.csv       # Landmark database with coordinates
├── assets/                   # Sample images for testing(optional)
```
## 🧪 Testing the System
Here you go to test the system. Under the folder 'properties', you will find sample images for testing the system. [N. B. If your machine doesn't support recommended GPU settings, the feature of suggested places won't be able to expand in a broad map view.]

## 🌟 Recommended Hardware
  **1. CPU:** Intel i5 or equivalent <br>
  **2. RAM:** 8GB+ <br>
  **3. Webcam:** 720p+ resolution <br>
  **4. GPU:** NVIDIA GPU with CUDA support (not required but recommended) <br>
  **5. Install CUDA-compatible PyTorch:**
```
    pip uninstall torch
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```
## ⚠️ Current Limitations
  1. Handwritten text recognition accuracy (~75%)
  2. Requires an internet connection for translation
  3. Address detection limited to Porto area
  4. Performance varies with image quality
  5. No offline translation mode
## 🔮 Future Improvements
  - Handwriting recognition with Vision Transformers
  - On-device translation models
  - Augmented reality integration
  - Offline mode support
  - Speech-to-text functionality
<div align="center">
  <img src="https://github.com/user-attachments/assets/ef756272-7699-4028-ade7-245a803b6c74" alt="Thanks for Explore" style="width:50%; height:50%;"><br/>
  <h2>END</h2>
</div>
