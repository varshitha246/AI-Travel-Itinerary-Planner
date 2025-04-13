# AI-Travel-Itinerary-Planner

Overview

The AI Travel Itinerary Planner is a web application that generates personalized travel itineraries based on user preferences. It combines weather data, local attractions, restaurant recommendations, and cultural insights to create comprehensive travel plans.

Features

    Dynamic Itinerary Generation: Creates day-by-day plans with morning, afternoon, and evening activities

    Multi-City Support: Includes famous global and Indian destinations (Paris, Tokyo, Delhi, Mumbai, etc.)

    Personalization Options:

        Trip duration (1-30 days)

        Budget levels (Economy, Standard, Luxury)

        Interest-based filtering (Food, Adventure, Culture, Nature, etc.)

    Comprehensive Destination Info:

        Weather forecasts

        Wikipedia descriptions and images

        Local specialties and famous landmarks

        Restaurant recommendations with price ranges

        Attraction listings with categories

Technical Stack

    Backend:
        Flask (Python) with REST API endpoints

    Frontend:
        Streamlit for interactive web interface

    APIs Integrated:

        OpenWeatherMap (weather data)

        Spoonacular (restaurant data)

        Geoapify (place/attraction data)

        Wikipedia (descriptions and images)

Setup Instructions

    Install dependencies:
   
        pip install flask flask_cors requests streamlit

    Run the backend server:
    
        python travel_itinerary1.py

    Run the frontend application:
    
        streamlit run travel_frontend.py

    Access the application in your browser at http://localhost:8501

Usage

    Select or enter a destination city

    Choose trip duration and start date

    Set your budget level

    Select your travel interests

    Click "Generate Itinerary" to create your personalized travel plan

Example Output

The application provides:

    Weather information for your destination

    Cultural description and image

    Must-try local foods

    Famous landmarks

    Daily itinerary with activities

    Recommended restaurants

    Must-visit attractions

Note

API keys included in the code are for demonstration purposes. For production use, replace with your own keys and secure them properly.
