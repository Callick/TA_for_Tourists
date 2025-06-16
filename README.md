# Translation Assistant for Tourists 🇵🇹➡️🌍
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
   **Windows:** Download then install following link - https://github.com/UB-Mannheim/tesseract/wiki<br>
   **MacOS:** ``` brew install tesseract ```
   **Linux (Debian/Ubuntu):** ``` sudo apt install tesseract-ocr ```
   
