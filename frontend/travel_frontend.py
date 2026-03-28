# travel_frontend.py
import streamlit as st
import requests
import datetime
from urllib.parse import quote_plus

API_URL = "https://ai-powered-travel-planner-g8j3.onrender.com/itinerary"
CITY_SEARCH_URL = "https://ai-powered-travel-planner-g8j3.onrender.com/city-search"

ITINERARY_TIMEOUT_SECONDS = 90

@st.cache_data(ttl=300, show_spinner=False)
def fetch_city_matches(query, limit=8):
    try:
        search_resp = requests.get(
            CITY_SEARCH_URL,
            params={"q": query.strip(), "limit": limit},
            timeout=8
        )
        if search_resp.status_code == 200:
            return search_resp.json().get("cities", [])
    except Exception:
        return None
    return []

def main():
    st.set_page_config(
        page_title="AI Travel Planner", 
        page_icon="🧭", 
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    if 'generate' not in st.session_state:
        st.session_state.generate = False
    if 'destination' not in st.session_state:
        st.session_state.destination = ""
    if 'days' not in st.session_state:
        st.session_state.days = 3
    if 'budget' not in st.session_state:
        st.session_state.budget = "Standard"
    if 'interests' not in st.session_state:
        st.session_state.interests = ["Culture", "Food"]
    if 'start_date' not in st.session_state:
        st.session_state.start_date = datetime.date.today()
    
    # Enhanced Custom CSS with gradients and modern design
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main Title Styling */
    h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 55px;
        white-space: pre-wrap;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 10px 10px 0px 0px;
        gap: 1px;
        padding: 12px 20px;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(135deg, #e0e7ff 0%, #cfd9ff 100%);
        transform: translateY(-2px);
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Card Styles with Gradients */
    .card {
        background: white;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        margin: 16px 0;
        border-left: 5px solid;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 32px rgba(0,0,0,0.12);
    }
    
    /* Food Card with Red Gradient */
    .food-card {
        border-left-color: #FF4B4B;
        background: linear-gradient(135deg, #ffffff 0%, #fff5f5 100%);
    }
    
    /* Landmark Card with Blue Gradient */
    .landmark-card {
        border-left-color: #1C83E1;
        background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%);
    }
    
    /* Day Card with Green Gradient */
    .day-card {
        border-left-color: #10b981;
        background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%);
        padding: 28px;
    }
    
    /* Weather Card with Sky Gradient */
    .weather-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 32px;
        border-radius: 20px;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    /* Trip Header with Animated Gradient */
    .trip-header {
        text-align: center;
        padding: 40px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-size: 200% 200%;
        animation: gradientShift 10s ease infinite;
        border-radius: 20px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
    }
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Summary Box */
    .summary-box {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 28px;
        border-radius: 16px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin: 20px 0;
    }
    .summary-box p {
        margin: 12px 0;
        font-size: 15px;
        line-height: 1.6;
    }
    
    /* Icon Styling */
    .icon-wrapper {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 48px;
        height: 48px;
        border-radius: 12px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 24px;
        margin-right: 16px;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    /* Activity Icons */
    .activity-row {
        display: flex;
        align-items: center;
        margin: 16px 0;
        padding: 16px;
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        border-radius: 12px;
        border-left: 4px solid;
    }
    .activity-row.morning { border-left-color: #fbbf24; }
    .activity-row.lunch { border-left-color: #ef4444; }
    .activity-row.afternoon { border-left-color: #3b82f6; }
    .activity-row.evening { border-left-color: #8b5cf6; }
    
    /* Image Styling */
    .destination-image {
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        overflow: hidden;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 28px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Metric Card */
    .metric-value {
        font-size: 32px;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Specialty Tags */
    .specialty-tag {
        display: inline-block;
        padding: 8px 16px;
        margin: 6px;
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        color: #92400e;
        border-radius: 20px;
        font-weight: 600;
        font-size: 14px;
        box-shadow: 0 2px 8px rgba(252, 211, 77, 0.3);
    }
    
    /* Landmark Tags */
    .landmark-tag {
        display: inline-block;
        padding: 8px 16px;
        margin: 6px;
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        color: #1e40af;
        border-radius: 20px;
        font-weight: 600;
        font-size: 14px;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
    }
    
    /* Tips Card */
    .tip-card {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        padding: 24px;
        border-radius: 16px;
        border-left: 5px solid #f59e0b;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.2);
    }
    
    /* Price Badge */
    .price-badge {
        display: inline-block;
        padding: 4px 12px;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border-radius: 12px;
        font-weight: 600;
        font-size: 13px;
        margin-right: 8px;
    }
    
    /* Rating Badge */
    .rating-badge {
        display: inline-block;
        padding: 4px 12px;
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
        color: white;
        border-radius: 12px;
        font-weight: 600;
        font-size: 13px;
    }
    
    /* Welcome Card */
    .welcome-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    
    
    # Sidebar with enhanced styling
    with st.sidebar:
        st.markdown('<div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin-bottom: 20px;"><h2 style="color: white; margin: 0;">🧳 Trip Details</h2></div>', unsafe_allow_html=True)
        
        destination = st.text_input(
            "🧭 Destination:", 
            value=st.session_state.destination,
            placeholder="Type any city name (e.g., Hyderabad, Paris, Tokyo)"
        )

        selected_city_payload = None
        if destination and len(destination.strip()) >= 2:
            city_matches = fetch_city_matches(destination)
            if city_matches is None:
                st.caption("City search API is unavailable. Continuing with typed destination.")
            elif city_matches:
                city_labels = [c.get("display_name", c.get("city", "")) for c in city_matches]
                selected_label = st.selectbox(
                    "📌 Select matching city:",
                    options=city_labels,
                    index=0,
                    help="Pick the exact city from API suggestions."
                )
                for c in city_matches:
                    if c.get("display_name") == selected_label:
                        selected_city_payload = c
                        break
            else:
                st.caption("No exact city suggestions found. You can still search with your typed value.")
        
        days = st.slider(
            "📅 Trip Duration (Days):", 
            min_value=1, 
            max_value=30, 
            value=st.session_state.days
        )
        
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input(
                "📆 Start Date:", 
                value=st.session_state.start_date
            )
        with col2:
            budget = st.selectbox(
                "💰 Budget:", 
                ["Economy", "Standard", "Luxury"],
                index=["Economy", "Standard", "Luxury"].index(st.session_state.budget) 
                if st.session_state.budget in ["Economy", "Standard", "Luxury"] else 1
            )
        
        interests = st.multiselect(
            "🧩 Your Interests:", 
            ["Food", "Adventure", "Culture", "Nature", "Shopping", "History", "Relaxation"],
            default=st.session_state.interests
        )
        
        if st.button("🗂️ Generate Itinerary", type="primary", use_container_width=True):
            if destination and destination.strip():
                st.session_state.generate = True
                if selected_city_payload:
                    st.session_state.destination = selected_city_payload.get("display_name", destination.strip())
                else:
                    st.session_state.destination = destination.strip()
                st.session_state.days = days
                st.session_state.budget = budget
                st.session_state.interests = interests
                st.session_state.start_date = start_date
                st.experimental_rerun()
            else:
                st.warning("⚠️ Please enter a destination")
    
    # Main content
    if st.session_state.generate and st.session_state.destination:
        destination = st.session_state.destination
        days = st.session_state.days
        budget = st.session_state.budget
        interests = st.session_state.interests
        start_date = st.session_state.start_date
        
        with st.spinner("⏳ Creating your itinerary..."):
            try:
                response = requests.post(
                    API_URL, 
                    json={
                        "city": destination,
                        "days": days,
                        "budget": budget,
                        "interests": interests
                    }, 
                    timeout=ITINERARY_TIMEOUT_SECONDS
                )
                
                if response.status_code == 200:
                    data = response.json()
                    display_destination = data.get("resolved_city", destination)
                    city_corrected = data.get("city_corrected", False)
                    input_city = data.get("input_city", destination)
                    city_key = display_destination.lower()
                    location_images = data.get("location_images", [])
                    food_images_api = data.get("food_images", [])

                    if city_corrected and city_key != input_city.lower():
                        st.info(f"Showing results for **{display_destination}** (searched: `{input_city}`).")

                    # Enhanced trip header with gradient animation
                    st.markdown(
                        f"""
                        <div class="trip-header">
                            <h1 style="color: #ffffff; -webkit-text-fill-color: #ffffff; background: none; -webkit-background-clip: initial; font-size: 42px; font-weight: 700; text-shadow: 0 4px 12px rgba(0, 0, 0, 0.35);">
                                🧳 Your {days}-Day Travel Plan to {display_destination}
                            </h1>
                            <p style="color: #ffffff; font-size: 18px; text-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);">
                                {start_date.strftime('%B %d, %Y')} → {(start_date + datetime.timedelta(days=days - 1)).strftime('%B %d, %Y')}
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    
                    # Main content columns
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        # Enhanced Weather Card
                        weather = data.get("weather", {})
                        temp = weather.get('temperature', 25)
                        conditions = weather.get('conditions', 'Sunny')
                        humidity = weather.get('humidity', 60)
                        
                        st.markdown(f"""
                        <div class="weather-card">
                            <div style="display: flex; align-items: center; justify-content: space-between;">
                                <div>
                                    <h2 style="margin: 0; color: white; font-size: 28px;">🌡️ Weather in {display_destination}</h2>
                                    <p style="margin: 10px 0 0 0; opacity: 0.9; font-size: 16px;">{conditions}</p>
                                </div>
                                <div style="text-align: right;">
                                    <div style="color: white; font-size: 56px; line-height: 1; font-weight: 700;">{temp}°C</div>
                                    <p style="margin: 5px 0 0 0; opacity: 0.9;">Humidity: {humidity}%</p>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # City description with icon
                        st.markdown(f"""
                        <div class="card" style="border-left-color: #667eea;">
                            <div style="display: flex; align-items: start;">
                                <div class="icon-wrapper">📌</div>
                                <div style="flex: 1;">
                                    <h3 style="margin: 0 0 12px 0; color: #1f2937;">About {display_destination}</h3>
                                    <p style="color: #4b5563; line-height: 1.8; margin: 0;">{data.get('description', f'{display_destination} is a beautiful destination with rich culture and history.')}</p>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Daily Itinerary with enhanced icons
                        st.markdown('<h2 style="margin-top: 40px; margin-bottom: 20px;">📅 Day-by-Day Itinerary</h2>', unsafe_allow_html=True)
                        
                        itinerary = data.get("itinerary", [])
                        for day_plan in itinerary:
                            day_num = day_plan.get('day', 1)
                            current_date = start_date + datetime.timedelta(days=day_num-1)
                            
                            morning_text = day_plan.get('morning', 'Morning activity')
                            lunch_text = day_plan.get('lunch', 'Lunch recommendation')
                            afternoon_text = day_plan.get('afternoon', 'Afternoon activity')
                            evening_text = day_plan.get('evening', 'Evening activity')
                            
                            st.markdown(f"""
                            <div class="day-card">
                                <div style="display: flex; align-items: center; margin-bottom: 20px;">
                                    <div class="icon-wrapper" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);">📅</div>
                                    <div>
                                        <h3 style="margin: 0; color: #1f2937;">Day {day_num} - {current_date.strftime('%A, %B %d')}</h3>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            # Morning activity
                            st.markdown(f"""
                                <div class="activity-row morning">
                                    <span style="font-size: 24px; margin-right: 12px;">🕘</span>
                                    <div>
                                        <strong style="color: #92400e; font-size: 14px; text-transform: uppercase;">Morning</strong>
                                        <p style="margin: 4px 0 0 0; color: #1f2937;">{morning_text}</p>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            # Lunch activity
                            st.markdown(f"""
                                <div class="activity-row lunch">
                                    <span style="font-size: 24px; margin-right: 12px;">🍴</span>
                                    <div>
                                        <strong style="color: #991b1b; font-size: 14px; text-transform: uppercase;">Lunch</strong>
                                        <p style="margin: 4px 0 0 0; color: #1f2937;">{lunch_text}</p>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            # Afternoon activity
                            st.markdown(f"""
                                <div class="activity-row afternoon">
                                    <span style="font-size: 24px; margin-right: 12px;">🕒</span>
                                    <div>
                                        <strong style="color: #1e40af; font-size: 14px; text-transform: uppercase;">Afternoon</strong>
                                        <p style="margin: 4px 0 0 0; color: #1f2937;">{afternoon_text}</p>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            # Evening activity
                            st.markdown(f"""
                                <div class="activity-row evening">
                                    <span style="font-size: 24px; margin-right: 12px;">🌆</span>
                                    <div>
                                        <strong style="color: #6b21a8; font-size: 14px; text-transform: uppercase;">Evening</strong>
                                        <p style="margin: 4px 0 0 0; color: #1f2937;">{evening_text}</p>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Enhanced Tabs for Restaurants and Attractions
                        st.markdown('<h2 style="margin-top: 40px; margin-bottom: 20px;">📌 Recommendations</h2>', unsafe_allow_html=True)
                        tab1, tab2 = st.tabs(["🍴 Restaurants", "🏛️ Attractions"])
                        
                        with tab1:
                            restaurants = data.get("restaurants", [])
                            if restaurants:
                                for i, restaurant in enumerate(restaurants[:8], 1):
                                    name = restaurant.get('name', 'Restaurant')
                                    address = restaurant.get('address', restaurant.get('address_line2', destination))
                                    price_range = restaurant.get('price_range', '$$')
                                    specialty = restaurant.get('specialty', 'Local cuisine')
                                    rating = restaurant.get('rating', 4.0)
                                    
                                    st.markdown(f"""
                                    <div class="card food-card">
                                        <div style="display: flex; align-items: start; justify-content: space-between;">
                                            <div style="display: flex; align-items: start; flex: 1;">
                                                <div style="background: linear-gradient(135deg, #FF4B4B 0%, #dc2626 100%); color: white; width: 42px; height: 42px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-weight: 700; margin-right: 16px; box-shadow: 0 4px 12px rgba(255, 75, 75, 0.3);">{i}</div>
                                                <div style="flex: 1;">
                                                    <h4 style="margin: 0 0 8px 0; color: #1f2937; font-size: 18px;">{name}</h4>
                                                    <p style="margin: 6px 0; color: #6b7280; font-size: 14px;"><span style="margin-right: 8px;">📌</span>{address}</p>
                                                    <div style="margin-top: 10px;">
                                                        <span class="price-badge">{price_range}</span>
                                                        <span style="color: #4b5563; font-size: 14px;">🍽️ {specialty}</span>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="rating-badge">⭐ {rating}</div>
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)
                            else:
                                st.info(f"🔍 Explore local restaurants in {display_destination} for authentic dining experiences.")
                        
                        with tab2:
                            attractions = data.get("attractions", [])
                            if attractions:
                                for i, attraction in enumerate(attractions[:10], 1):
                                    name = attraction.get('name', 'Attraction')
                                    address = attraction.get('address_line2', attraction.get('formatted', destination))
                                    category = attraction.get('categories', {}).get('name', 'Attraction')
                                    
                                    st.markdown(f"""
                                    <div class="card landmark-card">
                                        <div style="display: flex; align-items: start;">
                                            <div style="background: linear-gradient(135deg, #1C83E1 0%, #1e40af 100%); color: white; width: 42px; height: 42px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-weight: 700; margin-right: 16px; box-shadow: 0 4px 12px rgba(28, 131, 225, 0.3);">{i}</div>
                                            <div style="flex: 1;">
                                                <h4 style="margin: 0 0 8px 0; color: #1f2937; font-size: 18px;">{name}</h4>
                                                <p style="margin: 6px 0; color: #6b7280; font-size: 14px;"><span style="margin-right: 8px;">📌</span>{address}</p>
                                                <div style="margin-top: 10px;">
                                                    <span style="background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); color: #1e40af; padding: 4px 12px; border-radius: 12px; font-weight: 600; font-size: 13px;">🏷️ {category}</span>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)
                            else:
                                st.info(f"🔍 Discover amazing attractions and landmarks in {display_destination}.")
                    
                    with col2:
                        # Enhanced Destination Image with dynamic location-specific images
                        try:
                            # Use the first location image from API, or fallback to a dynamic search-based image
                            if location_images and len(location_images) > 0:
                                image_url = location_images[0]
                            else:
                                # Fallback to a dynamic Unsplash image based on destination
                                image_url = f"https://source.unsplash.com/1200x800/?{quote_plus(display_destination)},city"
                            
                            st.image(image_url, caption=f"🖼️ {display_destination}")
                        except Exception:
                            # Fallback image - generic but not Paris-specific
                            st.image("https://images.pexels.com/photos/1482182/pexels-photo-1482182.jpeg?auto=compress&cs=tinysrgb&w=800", 
                                    caption=f"🖼️ {display_destination}")
                        
                        # Enhanced Trip Summary
                        st.markdown(f"""
                        <div class="summary-box">
                            <h3 style="margin: 0 0 20px 0; color: #1f2937; text-align: center;">📋 Trip Summary</h3>
                            <p><span style="font-size: 20px; margin-right: 8px;">📌</span><strong>Destination:</strong> {display_destination}</p>
                            <p><span style="font-size: 20px; margin-right: 8px;">📅</span><strong>Duration:</strong> {days} days</p>
                            <p><span style="font-size: 20px; margin-right: 8px;">💰</span><strong>Budget:</strong> {budget}</p>
                            <p><span style="font-size: 20px; margin-right: 8px;">🧩</span><strong>Interests:</strong> {', '.join(interests) if interests else 'Not specified'}</p>
                            <p><span style="font-size: 20px; margin-right: 8px;">📆</span><strong>Dates:</strong> {start_date.strftime('%b %d')} - {(start_date + datetime.timedelta(days=days-1)).strftime('%b %d, %Y')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Local Specialties with enhanced tags
                        st.markdown('<h3 style="margin-top: 30px; margin-bottom: 15px; color: #1f2937;">🍴 Local Specialties</h3>', unsafe_allow_html=True)
                        specialties = data.get("local_specialties", [])
                        specialty_html = '<div style="margin: 10px 0;">'
                        for food in specialties[:5]:
                            specialty_html += f'<span class="specialty-tag">🍽️ {food}</span>'
                        specialty_html += '</div>'
                        st.markdown(specialty_html, unsafe_allow_html=True)
                        
                        # Famous Landmarks with enhanced tags
                        st.markdown('<h3 style="margin-top: 30px; margin-bottom: 15px; color: #1f2937;">🏛️ Iconic Landmarks</h3>', unsafe_allow_html=True)
                        landmarks = data.get("famous_landmarks", [])
                        landmark_html = '<div style="margin: 10px 0;">'
                        for landmark in landmarks[:5]:
                            landmark_html += f'<span class="landmark-tag">🏛️ {landmark}</span>'
                        landmark_html += '</div>'
                        st.markdown(landmark_html, unsafe_allow_html=True)
                        
                        # Additional destination image - Food
                        try:
                            if food_images_api and len(food_images_api) > 0:
                                food_img = food_images_api[0]
                            else:
                                food_img = f"https://source.unsplash.com/1200x800/?{quote_plus(display_destination)},food"
                            st.image(food_img, caption=f"🍴 Cuisine of {display_destination}")
                        except Exception:
                            pass

                        # Mini gallery from place + food APIs
                        st.markdown('<h3 style="margin-top: 20px; margin-bottom: 10px; color: #1f2937;">🖼️ City Gallery</h3>', unsafe_allow_html=True)
                        # Show dynamic gallery images if available
                        gallery_images = []
                        if location_images:
                            gallery_images.extend(location_images[1:4])
                        if food_images_api:
                            gallery_images.extend(food_images_api[1:3])
                        
                        if gallery_images:
                            for idx, url in enumerate(gallery_images[:5], 1):
                                try:
                                    st.image(url, caption=f"{display_destination} Gallery {idx}")
                                except Exception:
                                    pass
                        else:
                            st.caption(f"More images of {display_destination} will appear here.")
                    
                    # Enhanced Travel Tips
                    st.markdown('<h2 style="margin-top: 50px; margin-bottom: 25px;">💡 Smart Travel Tips</h2>', unsafe_allow_html=True)
                    tips_col1, tips_col2, tips_col3 = st.columns(3)
                    
                    with tips_col1:
                        st.markdown("""
                        <div class="tip-card">
                            <h4 style="margin: 0 0 15px 0; color: #92400e;">📱 Essential Apps</h4>
                            <ul style="margin: 0; padding-left: 20px; color: #78350f; line-height: 1.8;">
                                <li>Google Maps for navigation</li>
                                <li>Local transport apps</li>
                                <li>Translation tools</li>
                                <li>Currency converter</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with tips_col2:
                        st.markdown("""
                        <div class="tip-card" style="background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); border-left-color: #10b981;">
                            <h4 style="margin: 0 0 15px 0; color: #065f46;">💰 Budget Smart</h4>
                            <ul style="margin: 0; padding-left: 20px; color: #064e3b; line-height: 1.8;">
                                <li>Visit free attractions</li>
                                <li>Use public transport</li>
                                <li>Try street food</li>
                                <li>Book in advance</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with tips_col3:
                        st.markdown(f"""
                        <div class="tip-card" style="background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); border-left-color: #3b82f6;">
                            <h4 style="margin: 0 0 15px 0; color: #1e40af;">🌡️ Weather Ready</h4>
                            <ul style="margin: 0; padding-left: 20px; color: #1e3a8a; line-height: 1.8;">
                                <li>Pack for {weather.get('conditions', 'variable weather')}</li>
                                <li>Dress in layers</li>
                                <li>Stay hydrated</li>
                                <li>Sun protection</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                    
                else:
                    st.error(f"❌ Failed to fetch itinerary. Status: {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to the server. Make sure Flask is running!")
                st.markdown("""
                <div class="card" style="border-left-color: #ef4444;">
                    <h4>🔧 Quick Fix:</h4>
                    <ol style="line-height: 2;">
                        <li>Open terminal in your project folder</li>
                        <li>Run: <code>python travel_itinerary1.py</code></li>
                        <li>Keep terminal open</li>
                        <li>Refresh this page</li>
                    </ol>
                </div>
                """, unsafe_allow_html=True)
            except requests.exceptions.ReadTimeout:
                st.error(
                    f"❌ Itinerary generation is taking too long (>{ITINERARY_TIMEOUT_SECONDS}s). "
                    "Please try again with fewer trip days or retry in a moment."
                )
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
        
        # Back button
        st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)
        if st.button("← Plan Another Trip", type="secondary", use_container_width=True):
            st.session_state.generate = False
            st.experimental_rerun()
    
    else:
        # Enhanced Welcome screen
        st.markdown("""
        <div class="welcome-card">
            <h1 style="text-align: center; margin-bottom: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
                🧭 Welcome to AI Travel Planner
            </h1>
            <p style="text-align: center; font-size: 18px; color: #4b5563; margin-bottom: 30px;">
                Plan your perfect trip with AI-powered itineraries. Get personalized recommendations 
                for attractions, restaurants, and activities based on your preferences.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown("""
            <div class="card" style="border-left-color: #667eea;">
                <h3 style="margin-top: 0; color: #1f2937;">✅ Premium Features</h3>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;">
                    <div>
                        <h4 style="color: #667eea; margin: 0 0 8px 0;">🗺️ Smart Planning</h4>
                        <p style="color: #6b7280; margin: 0; font-size: 14px;">AI-generated itineraries tailored to your interests and schedule</p>
                    </div>
                    <div>
                        <h4 style="color: #667eea; margin: 0 0 8px 0;">🍴 Food Discovery</h4>
                        <p style="color: #6b7280; margin: 0; font-size: 14px;">Find must-try local specialties and top-rated restaurants</p>
                    </div>
                    <div>
                        <h4 style="color: #667eea; margin: 0 0 8px 0;">🏛️ Hidden Gems</h4>
                        <p style="color: #6b7280; margin: 0; font-size: 14px;">Discover famous landmarks and secret attractions</p>
                    </div>
                    <div>
                        <h4 style="color: #667eea; margin: 0 0 8px 0;">🌡️ Live Weather</h4>
                        <p style="color: #6b7280; margin: 0; font-size: 14px;">Current weather conditions for perfect planning</p>
                    </div>
                    <div>
                        <h4 style="color: #667eea; margin: 0 0 8px 0;">💰 Budget Options</h4>
                        <p style="color: #6b7280; margin: 0; font-size: 14px;">Plans for Economy, Standard, and Luxury budgets</p>
                    </div>
                    <div>
                        <h4 style="color: #667eea; margin: 0 0 8px 0;">⏱️ Day Planning</h4>
                        <p style="color: #6b7280; margin: 0; font-size: 14px;">Detailed morning, lunch, afternoon, and evening activities</p>
                    </div>
                </div>
                <div style="margin-top: 30px; padding: 20px; background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border-radius: 12px; border-left: 4px solid #f59e0b;">
                    <p style="margin: 0; color: #92400e; font-weight: 600; font-size: 16px;">
                        ℹ️ Fill in your trip details in the sidebar and click "Generate Itinerary" to get started!
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.image(
    "https://images.pexels.com/photos/338515/pexels-photo-338515.jpeg?auto=compress&cs=tinysrgb&w=800"
)

            st.image(
    "https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?auto=compress&cs=tinysrgb&w=800"
)
        
        # Quick start examples with enhanced styling
        st.markdown('<h2 style="margin-top: 50px; margin-bottom: 25px; text-align: center;">▶️ Quick Start Examples</h2>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        def select_example(city, days_val, budget_val, interests_val):
            st.session_state.generate = True
            st.session_state.destination = city
            st.session_state.days = days_val
            st.session_state.budget = budget_val
            st.session_state.interests = interests_val
            st.session_state.start_date = datetime.date.today()
            st.experimental_rerun()
        
        with col1:
            if st.button("Paris Adventure\n3 days • Culture & Food", use_container_width=True, key="paris"):
                select_example("Paris", 3, "Standard", ["Culture", "Food", "History"])
        
        with col2:
            if st.button("Tokyo Experience\n4 days • Food & Culture", use_container_width=True, key="tokyo"):
                select_example("Tokyo", 4, "Standard", ["Food", "Culture", "Shopping"])
        
        with col3:
            if st.button("Goa Getaway\n5 days • Nature & Relax", use_container_width=True, key="goa"):
                select_example("Goa", 5, "Economy", ["Nature", "Relaxation", "Food"])
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col4, col5, col6 = st.columns(3)
        
        with col4:
            if st.button("London Historic\n4 days • History & Culture", use_container_width=True, key="london"):
                select_example("London", 4, "Luxury", ["History", "Culture", "Shopping"])
        
        with col5:
            if st.button("Dubai Luxury\n3 days • Food & Adventure", use_container_width=True, key="dubai"):
                select_example("Dubai", 3, "Luxury", ["Shopping", "Adventure", "Food"])
        
        with col6:
            if st.button("Jaipur Heritage\n4 days • History & Culture", use_container_width=True, key="jaipur"):
                select_example("Jaipur", 4, "Standard", ["History", "Culture", "Food"])

if __name__ == "__main__":
    main()