import streamlit as st
import requests
import json
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configure Streamlit page
st.set_page_config(
    page_title="ISRO ChatBot Analytics",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #2c3e50, #34495e);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #3498db;
    }
    .chat-message {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 3px solid #3498db;
    }
    .sidebar-logo {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #3498db, #2980b9);
        border-radius: 10px;
        color: white;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Flask backend URL
FLASK_URL = "http://localhost:5000"

# Sidebar
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <h2>🚀 ISRO ChatBot</h2>
        <p>Analytics Dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Navigation")
    page = st.selectbox("Select Page", [
        "Dashboard", 
        "Chat Interface", 
        "Analytics", 
        "User Management",
        "ISRO Data Viewer"
    ])

# Main header
st.markdown("""
<div class="main-header">
    <h1>🚀 ISRO ChatBot Analytics Platform</h1>
    <p>Advanced analytics and management for your space exploration assistant</p>
</div>
""", unsafe_allow_html=True)

# Dashboard Page
if page == "Dashboard":
    st.header("📊 Dashboard Overview")
    
    # Create columns for metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Users",
            value="150",
            delta="12"
        )
    
    with col2:
        st.metric(
            label="Total Conversations",
            value="1,247",
            delta="89"
        )
    
    with col3:
        st.metric(
            label="Avg Session Time",
            value="8.5 min",
            delta="1.2 min"
        )
    
    with col4:
        st.metric(
            label="Satisfaction Rate",
            value="94.2%",
            delta="2.1%"
        )
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Daily Conversations")
        # Sample data for demo
        dates = pd.date_range('2024-01-01', periods=30, freq='D')
        conversations = [50 + i*2 + (i%7)*10 for i in range(30)]
        df = pd.DataFrame({'Date': dates, 'Conversations': conversations})
        
        fig = px.line(df, x='Date', y='Conversations', title="Daily Conversation Trends")
        fig.update_traces(line_color='#3498db')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Popular Topics")
        topics = ['ISRO Missions', 'Satellite Programs', 'Space Technology', 'Launch Vehicles', 'Research']
        counts = [85, 67, 45, 38, 25]
        
        fig = px.bar(x=topics, y=counts, title="Most Discussed Topics")
        fig.update_traces(marker_color='#e74c3c')
        st.plotly_chart(fig, use_container_width=True)

# Chat Interface Page
elif page == "Chat Interface":
    st.header("💬 Chat Interface")
    
    # Initialize session state for chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm your ISRO assistant. How can I help you learn about space exploration today?"}
        ]
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me about ISRO, space missions, or anything space-related..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate bot response (you can integrate with your Flask backend here)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Simulate API call to Flask backend
                try:
                    response = requests.post(f"{FLASK_URL}/chat", 
                                           json={"message": prompt},
                                           timeout=10)
                    if response.status_code == 200:
                        bot_response = response.json().get("response", "I'm sorry, I couldn't process that request.")
                    else:
                        bot_response = "I'm currently having trouble connecting to my knowledge base. Please try again later."
                except:
                    # Fallback response if Flask backend is not running
                    bot_response = generate_fallback_response(prompt)
                
                st.markdown(bot_response)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": bot_response})

# Analytics Page
elif page == "Analytics":
    st.header("📊 Advanced Analytics")
    
    tab1, tab2, tab3 = st.tabs(["User Behavior", "Content Analysis", "Performance Metrics"])
    
    with tab1:
        st.subheader("User Interaction Patterns")
        
        # Heatmap of user activity
        hours = list(range(24))
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        
        # Generate sample data
        import numpy as np
        activity_data = np.random.randint(10, 100, size=(7, 24))
        
        fig = go.Figure(data=go.Heatmap(
            z=activity_data,
            x=hours,
            y=days,
            colorscale='Blues',
            hoveremplate='Day: %{y}<br>Hour: %{x}<br>Activity: %{z}<extra></extra>'
        ))
        fig.update_layout(
            title="User Activity Heatmap (Hour vs Day)",
            xaxis_title="Hour of Day",
            yaxis_title="Day of Week"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Content & Query Analysis")
        
        # Query categories pie chart
        categories = ['Technical Questions', 'Mission Information', 'General Inquiries', 'Educational Content']
        values = [35, 30, 20, 15]
        
        fig = px.pie(values=values, names=categories, title="Query Categories Distribution")
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
        
        # Response time metrics
        st.subheader("Response Time Analysis")
        response_times = np.random.normal(1.2, 0.3, 1000)  # Sample data
        fig = px.histogram(x=response_times, title="Response Time Distribution", 
                          labels={'x': 'Response Time (seconds)', 'y': 'Frequency'})
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Performance Metrics")
        
        # System performance gauge
        col1, col2 = st.columns(2)
        
        with col1:
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = 94.2,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "User Satisfaction %"},
                delta = {'reference': 90},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "yellow"},
                        {'range': [80, 100], 'color': "green"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 95
                    }
                }
            ))
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = 98.7,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "System Uptime %"},
                delta = {'reference': 99},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "green"},
                    'steps': [
                        {'range': [0, 95], 'color': "lightgray"},
                        {'range': [95, 99], 'color': "yellow"},
                        {'range': [99, 100], 'color': "green"}
                    ]
                }
            ))
            st.plotly_chart(fig, use_container_width=True)

# User Management Page
elif page == "User Management":
    st.header("👥 User Management")
    
    # User statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Active Users", "89", "5")
    with col2:
        st.metric("New Users (30d)", "23", "12")
    with col3:
        st.metric("Returning Users", "127", "-3")
    
    # User table
    st.subheader("User Activity")
    
    # Sample user data
    users_data = {
        'Username': ['user1', 'user2', 'user3', 'user4', 'user5'],
        'Email': ['user1@email.com', 'user2@email.com', 'user3@email.com', 'user4@email.com', 'user5@email.com'],
        'Last Active': ['2024-01-15', '2024-01-14', '2024-01-13', '2024-01-12', '2024-01-11'],
        'Total Conversations': [45, 32, 67, 23, 89],
        'Status': ['Active', 'Active', 'Inactive', 'Active', 'Active']
    }
    
    df_users = pd.DataFrame(users_data)
    st.dataframe(df_users, use_container_width=True)

# ISRO Data Viewer Page
elif page == "ISRO Data Viewer":
    st.header("🚀 ISRO Mission Data")
    
    # Mission data
    missions_data = {
        'Mission': ['Chandrayaan-3', 'Mangalyaan', 'Aditya-L1', 'GSAT-30', 'RISAT-2B'],
        'Launch Date': ['2023-07-14', '2013-11-05', '2023-09-02', '2020-01-17', '2019-05-22'],
        'Status': ['Successful', 'Successful', 'Ongoing', 'Operational', 'Operational'],
        'Type': ['Lunar', 'Mars', 'Solar', 'Communication', 'Earth Observation'],
        'Cost (Crores)': [615, 450, 378, 500, 282]
    }
    
    df_missions = pd.DataFrame(missions_data)
    
    # Display mission data
    st.subheader("Recent ISRO Missions")
    st.dataframe(df_missions, use_container_width=True)
    
    # Mission cost visualization
    st.subheader("Mission Costs Comparison")
    fig = px.bar(df_missions, x='Mission', y='Cost (Crores)', 
                 color='Type', title="ISRO Mission Costs")
    st.plotly_chart(fig, use_container_width=True)
    
    # Launch timeline
    st.subheader("Launch Timeline")
    df_missions['Launch Date'] = pd.to_datetime(df_missions['Launch Date'])
    df_missions = df_missions.sort_values('Launch Date')
    
    fig = px.timeline(df_missions, x_start='Launch Date', x_end='Launch Date', 
                      y='Mission', color='Type', title="ISRO Mission Timeline")
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; padding: 1rem;">
    <p>🚀 ISRO ChatBot Analytics Platform | Built with Streamlit & Flask</p>
    <p>Empowering space exploration through intelligent conversation</p>
</div>
""", unsafe_allow_html=True)

# Helper function for fallback responses
def generate_fallback_response(prompt):
    """Generate fallback responses when Flask backend is not available"""
    prompt_lower = prompt.lower()
    
    if 'chandrayaan' in prompt_lower:
        return """🌙 **Chandrayaan Mission Series**
        
Chandrayaan is India's lunar exploration program by ISRO:

- **Chandrayaan-1** (2008): India's first lunar probe, discovered water molecules on the Moon
- **Chandrayaan-2** (2019): Included orbiter, lander, and rover; orbiter continues to operate
- **Chandrayaan-3** (2023): Successful soft landing near lunar south pole, making India the 4th country to achieve this

The missions have significantly contributed to our understanding of the Moon's composition and geology."""
    
    elif 'mangalyaan' in prompt_lower or 'mars' in prompt_lower:
        return """🔴 **Mars Orbiter Mission (Mangalyaan)**
        
Launched: November 5, 2013
Status: Mission completed successfully in 2022

Key Achievements:
- Made India the first country to reach Mars orbit in its first attempt
- Most cost-effective Mars mission ever ($74 million)
- Studied Martian atmosphere, surface features, and mineralogy
- Operated for 8 years (planned for 6 months)

This mission showcased India's space capabilities and cost-effective approach to planetary exploration."""
    
    elif 'isro' in prompt_lower:
        return """🚀 **Indian Space Research Organisation (ISRO)**
        
Established: 1969
Headquarters: Bangalore, India

Major Achievements:
- Over 400 satellite launches
- Successful Mars and Moon missions
- World's largest satellite constellation launch (104 satellites)
- Cost-effective space missions
- Indigenous launch vehicles (PSLV, GSLV)

ISRO is known for its frugal engineering and innovative approach to space exploration, making space technology accessible and affordable."""
    
    else:
        return """Thank you for your question about space exploration! 
        
I'd be happy to help you learn more about:
- ISRO missions and achievements
- Satellite programs and technology
- Launch vehicles (PSLV, GSLV)
- Space exploration history
- Future space missions

What specific aspect of space exploration interests you most?"""
