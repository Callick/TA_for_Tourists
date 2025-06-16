# Import required libraries
import streamlit as st
import numpy as np
from PIL import Image
import easyocr
import pandas as pd
from langdetect import detect, LangDetectException
from math import radians, sin, cos, sqrt, atan2
from deep_translator import GoogleTranslator
import os
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import time

# Initialize OCR reader for Portuguese
reader = easyocr.Reader(['pt'])

# Configure Streamlit page
st.set_page_config(page_title="Porto Translator Guide", layout="centered")
st.title("Translation Assistant for Tourists 🇵🇹➡️🌍")

# ======================================
# OCR Text Ordering Functions
# ======================================
def sort_text_regions(results):
    """Sort detected text regions from top to bottom, left to right"""
    return sorted(results, key=lambda x: (x[0][0][1], x[0][0][0]))

def group_text_lines(sorted_results, y_threshold=20):
    """Group text into lines based on Y-coordinate proximity"""
    if not sorted_results:
        return []
    
    lines = []
    current_line = [sorted_results[0]]
    
    for result in sorted_results[1:]:
        y_prev = current_line[-1][0][0][1]
        y_curr = result[0][0][1]
        
        if abs(y_curr - y_prev) < y_threshold:
            current_line.append(result)
        else:
            lines.append(current_line)
            current_line = [result]
    
    lines.append(current_line)
    return lines

def format_ordered_text(results):
    """Organize OCR results into properly ordered text"""
    sorted_results = sort_text_regions(results)
    lines = group_text_lines(sorted_results)
    
    ordered_text = []
    for line in lines:
        # Sort words in line left-to-right
        line_sorted = sorted(line, key=lambda x: x[0][0][0])
        line_text = " ".join([res[1] for res in line_sorted])
        ordered_text.append(line_text)
    
    return "\n".join(ordered_text)

# ======================================
# Load Landmarks Data from CSV
# ======================================
LANDMARKS = None
LANDMARKS_PATH = "porto_landmarks.csv"

try:
    if os.path.exists(LANDMARKS_PATH):
        LANDMARKS = pd.read_csv(LANDMARKS_PATH)
        required_columns = ['name', 'latitude', 'longitude', 'description']
        if not all(col in LANDMARKS.columns for col in required_columns):
            st.error(f"⚠️ CSV file missing required columns: {required_columns}")
            LANDMARKS = None
    else:
        st.error(f"⚠️ Landmarks file not found: {LANDMARKS_PATH}")
except Exception as e:
    st.error(f"⚠️ Error loading landmarks: {str(e)}")
    LANDMARKS = None

# ======================================
# Geocoding Functions
# ======================================
def geocode_address(address):
    """Convert address text to coordinates"""
    try:
        geolocator = Nominatim(user_agent="porto_translator")
        location = geolocator.geocode(address + ", Porto, Portugal")
        return (location.latitude, location.longitude) if location else None
    except:
        return None

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two coordinates in km"""
    R = 6371  # Earth radius in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = (sin(dlat/2) ** 2 + cos(radians(lat1))) * \
        cos(radians(lat2)) * sin(dlon/2) ** 2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))

def create_mini_map(lat, lon, name):
    """Create a thumbnail map for a location"""
    m = folium.Map(location=[lat, lon], zoom_start=15, 
                  width=200, height=150, control_scale=False)
    folium.Marker([lat, lon], tooltip=name, 
                 icon=folium.Icon(color='red', icon='info-sign')).add_to(m)
    return m

# ======================================
# Image Input Section
# ======================================
st.header("Step 1: Choose Input Method")
input_choice = st.radio(
    "Select your preferred input:",
    options=["📁 Upload Image", "📸 Use Webcam"],
    index=0
)

img_file = None
if input_choice == "📸 Use Webcam":
    img_file = st.camera_input("Take photo of text:")
else:
    img_file = st.file_uploader("Upload image:", type=["jpg", "png"])

# ======================================
# Image Processing & OCR
# ======================================
if img_file:
    col_preview, col_processing = st.columns([1, 3])
    
    with col_preview:
        st.markdown("""
            <div style='border:2px solid #e0e0e0; 
                        border-radius:10px; 
                        padding:10px;
                        margin-bottom:20px;
                        text-align:center'>
                <h4 style='color:#666666; margin:0 0 10px 0;'>Image Preview</h4>
        """, unsafe_allow_html=True)
        image = Image.open(img_file)
        st.image(image, use_container_width=True, output_format="JPEG")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col_processing:
        with st.spinner("🔍 Analyzing image..."):
            try:
                img_np = np.array(image.convert('RGB'))
                results = reader.readtext(img_np)
                
                # Get properly ordered text
                extracted_text = format_ordered_text(results).strip()
                
                if not extracted_text:
                    st.error("❌ No text found in image")
                    st.stop()
                
                # Display ordered text with line numbers
                st.subheader("Extracted Portuguese Text:")
                st.markdown("```text\n" + extracted_text + "\n```")
                
            except Exception as e:
                st.error(f"❌ OCR Error: {str(e)}")
                st.stop()

        # ======================================
        # Language Handling
        # ======================================
        st.subheader("🌐 Language Settings")
        
        col_lang1, col_lang2 = st.columns(2)
        with col_lang1:
            try:
                detected_lang = detect(extracted_text)
                lang_status = (
                    f"⚠️ Detected: {detected_lang.upper()} (Expected PT)"
                    if detected_lang != 'pt' else "✅ Confirmed: Portuguese"
                )
                st.markdown(lang_status)
            except LangDetectException:
                st.warning("⚠️ Language detection failed")

        with col_lang2:
            target_lang = st.selectbox(
                "Translate to:",
                ["English", "French", "Deutsch", "Italian"],
                index=0
            )

        # Line-by-line translation
        with st.spinner(f"🌍 Translating to {target_lang}..."):
            try:
                # Split into lines and translate individually
                translated_lines = []
                for line in extracted_text.split('\n'):
                    translated = GoogleTranslator(
                        source='auto',
                        target=target_lang.lower()[:2]
                    ).translate(line)
                    translated_lines.append(translated)
                
                translated_text = "\n".join(translated_lines)
                
                # Display formatted translation
                st.subheader(f"Translated Text ({target_lang}):")
                st.markdown("```text\n" + translated_text + "\n```")
                
            except Exception as e:
                st.error(f"❌ Translation failed: {str(e)}")
                st.stop()

        # ======================================
        # Location Features (Enhanced)
        # ======================================
        st.header("📍 Nearby Attractions")
        address_keywords = ['rua', 'avenida', 'praça', 'largo', 'número', 'travessa']
        is_address = any(kw in extracted_text.lower() for kw in address_keywords)
        
        if is_address and LANDMARKS is not None:
            # Geocode detected address
            with st.spinner("🗺️ Locating address..."):
                address_coords = geocode_address(extracted_text)
                
            if address_coords:
                st.success(f"📍 Detected location: {address_coords[0]:.4f}, {address_coords[1]:.4f}")
                
                # Calculate distances
                LANDMARKS['distance'] = LANDMARKS.apply(
                    lambda row: calculate_distance(
                        address_coords[0], address_coords[1],
                        row['latitude'], row['longitude']
                    ), axis=1
                )
                
                # Get top 3 closest landmarks
                closest_landmarks = LANDMARKS.sort_values('distance').head(3)
                
                # Display each recommendation with map thumbnail
                st.subheader("Top Recommendations Nearby:")
                for _, row in closest_landmarks.iterrows():
                    with st.container():
                        col1, col2 = st.columns([1, 2])
                        with col1:
                            # Create and display mini map
                            mini_map = create_mini_map(row['latitude'], row['longitude'], row['name'])
                            st_folium(mini_map, width=150, height=150)
                            
                        with col2:
                            st.markdown(f"""
                                <div style='padding:10px;'>
                                    <h4 style='color:#2e86c1; margin-top:0;'>{row['name']}</h4>
                                    <p>📏 <strong>{row['distance']:.2f} km</strong> away</p>
                                    <p>{row['description']}</p>
                                </div>
                            """, unsafe_allow_html=True)
                        
                        # Add expandable detailed map
                        with st.expander("🗺️ View on map", expanded=False):
                            detail_map = folium.Map(location=[row['latitude'], row['longitude']], 
                                                  zoom_start=15)
                            folium.Marker(
                                [address_coords[0], address_coords[1]],
                                tooltip="Your Location",
                                icon=folium.Icon(color='blue', icon='user')
                            ).add_to(detail_map)
                            folium.Marker(
                                [row['latitude'], row['longitude']],
                                tooltip=row['name'],
                                icon=folium.Icon(color='red', icon='info-sign')
                            ).add_to(detail_map)
                            folium.PolyLine(
                                locations=[address_coords, [row['latitude'], row['longitude']]],
                                color='green',
                                weight=2
                            ).add_to(detail_map)
                            st_folium(detail_map, width=700, height=400)
                        
                        st.markdown("---")
            else:
                st.warning("⚠️ Could not locate address. Showing city center attractions.")
                # Fallback to city center
                PORTO_CENTER = (41.1579, -8.6291)
                LANDMARKS['distance'] = LANDMARKS.apply(
                    lambda row: calculate_distance(
                        PORTO_CENTER[0], PORTO_CENTER[1],
                        row['latitude'], row['longitude']
                    ), axis=1
                )
                for _, row in LANDMARKS.sort_values('distance').head(3).iterrows():
                    st.markdown(f"""
                        <div style='padding:15px;
                                    background:#f8f9fa;
                                    border-radius:8px;
                                    margin:15px 0;
                                    box-shadow:0 2px 4px rgba(0,0,0,0.1)'>
                            <h4 style='color:#2e86c1; margin-top:0;'>{row['name']}</h4>
                            📍 <strong>{row['distance']:.1f} km</strong> from city center<br>
                            {row['description']}
                        </div>
                    """, unsafe_allow_html=True)
        
        elif not is_address:
            st.info("ℹ️ No address detected - try a street sign or restaurant menu!")
        else:
            st.warning("⚠️ Landmark data not available")

else:
    st.info("👆 Please upload an image or enable webcam to get started")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align:center; color:#666; margin-top:30px;'>
        Built with ❤️ for Porto visitors | 
        <a href='#' style='color:#2e86c1; text-decoration:none;'>GitHub Repo</a>
    </div>
""", unsafe_allow_html=True)