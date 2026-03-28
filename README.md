
# 🧭 AI-Powered Travel Planner  
*A Full-Stack AI Web Application for Personalized Travel Itineraries*

---

## 📌 Overview
**AI-Powered Travel Planner** is a full-stack web application that generates **intelligent, personalized, and day-by-day travel itineraries** based on user preferences such as destination, travel duration, budget, and interests.

The application is built using a **Streamlit-based frontend** and a **Flask REST API backend**, integrates multiple real-world third-party APIs, and is deployed on modern cloud platforms following **production-ready and secure development practices**.

---

## 🌐 Live Application
- **Frontend (Streamlit Cloud):** [*(Click Here)*](https://travelfrontendpy-d6arskq56f3umxydntjqse.streamlit.app/)
- **Backend API (Render):** [*(link)*](https://ai-powered-travel-planner-g8j3.onrender.com)

---

## 🚀 Key Capabilities
- Intelligent **city search with autocomplete**
- AI-driven **daily travel itinerary generation**
- **Live weather insights** for destinations
- **Restaurant and local cuisine recommendations**
- **Attractions and landmark discovery**
- Personalized planning based on:
  - Budget (Economy, Standard, Luxury)
  - Interests (Food, Culture, Nature, Adventure, etc.)
- Responsive and modern UI with custom styling
- Secure handling of third-party API credentials

---

## 🏗️ System Architecture

**Frontend**
- Built using **Streamlit**
- Handles user input, data visualization, and UI rendering
- Communicates with backend via REST API calls

**Backend**
- Built using **Flask**
- Exposes RESTful endpoints for:
  - City search
  - Weather retrieval
  - Places & restaurants discovery
  - Itinerary generation logic
- Integrates multiple external APIs
- Deployed as a standalone backend service

---

## 🧰 Technology Stack

### Frontend
- Streamlit
- Python
- Custom CSS for enhanced UI/UX

### Backend
- Flask (REST API)
- Flask-CORS
- Requests

### External APIs
- **OpenWeather API** – Weather & geocoding
- **Geoapify API** – Attractions & places
- **Spoonacular API** – Food & cuisine data
- **Wikipedia API** – Images & landmarks

### Deployment & DevOps
- Render (Backend hosting)
- Streamlit Cloud (Frontend hosting)
- Environment variables for secrets management

---

## 📁 Repository Structure     
```

AI-powered-travel-planner/   
├── travel_frontend.py      # Streamlit frontend application   
├── travel_itinerary1.py    # Flask backend REST API   
├── requirements.txt        # Project dependencies    
└── README.md     

```

---

## ⚙️ Application Workflow
1. User submits travel preferences via the frontend
2. Frontend sends a request to the Flask backend
3. Backend:
   - Resolves city and coordinates
   - Fetches real-time weather data
   - Retrieves attractions and restaurants
   - Generates a structured daily itinerary
4. Frontend renders results in an intuitive, user-friendly interface

---

## 🔐 Security & Configuration
- API keys are **never hardcoded**
- Secrets are managed using **environment variables**
- `.env` file is used only for local development and excluded via `.gitignore`
- Production secrets are configured securely on Render

### Required Environment Variables
```

OPENWEATHER_API_KEY
GEOAPIFY_API_KEY
SPOONACULAR_API_KEY

````

✔️ Follows industry-standard security practices.

---

## 🧪 Local Setup (Optional)

### Install dependencies
```bash
pip install -r requirements.txt
````

### Run backend

```bash
python travel_itinerary1.py
```

### Run frontend

```bash
streamlit run travel_frontend.py
```

---


## 🎓 Learning Outcomes

* Full-stack application design
* REST API development with Flask
* Integration of real-world APIs
* Cloud deployment and service separation
* Secure credential management
* UI/UX design with Streamlit

---  

## 🔮 Future Enhancements

* User authentication and profiles
* Downloadable itineraries (PDF)
* Interactive maps
* Multi-language support
* Mobile-first UI improvements

---

## 👩‍💻 Author

**Madhuri**
🔗 GitHub: [https://github.com/Madhuri-0607](https://github.com/Madhuri-0607)

---

⭐ If you find this project useful, feel free to give it a star!


