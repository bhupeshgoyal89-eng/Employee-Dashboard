# Employee Dashboard - AI-Powered Performance Command Center

A high-performance fintech-inspired employee dashboard built with Streamlit. This is a prototype featuring mocked data and session state management.

## Features

### 📊 Overview Dashboard
- KPI cards: Actual vs AOP, Performance Score, Health Index, Social Score, 360 Sentiment
- Monthly performance trends (line chart)
- KRA performance breakdown (bar chart)
- Active projects & initiatives tracker

### 💚 Health & Wellness
- Weekly self-assessment (stress, sleep, energy, satisfaction)
- Health Index gauge visualization
- 8-week wellness trend tracking
- AI-powered wellness insights

### 📈 Performance Management
- KRA tracking with target vs actual
- Active projects with progress bars
- MIS (Monthly Intelligence Sheet) upload simulation
- Performance summary insights

### 🤝 360 Feedback System
- Submit feedback for colleagues
- View received feedback with sentiment analysis
- Sentiment score distribution (pie chart)
- Mocked NLP sentiment scoring

### 👥 Social Score & Collaboration
- Composite social score metrics
- Email response time tracking
- Meeting participation metrics
- Collaboration & mentorship scoring
- Interactive radar chart for collaboration profile

### 🤖 AI Quarterly Appraisal Assistant
- Automated promotion readiness calculation
- Strength identification
- Risk area detection
- Increment band recommendations
- Role trajectory suggestions
- Manager sharing capability

## Tech Stack

- **Framework**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly
- **State Management**: Streamlit Session State

## Installation & Setup

```bash
# Clone or navigate to project directory
cd Employee-Dashboard

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running the App

```bash
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`

## Architecture

### File Structure
```
app.py              # Single-file Streamlit application
requirements.txt    # Python dependencies
README.md          # Documentation
```

### Key Components

1. **Mock Data Generation**: Generates realistic employee performance data, health history, and feedback
2. **Session State Management**: Persists user inputs and selections across page navigation
3. **Utility Functions**: Styling helpers, color logic, status badges
4. **Page Functions**: Modular page implementations (one per feature)
5. **AI Logic**: Rule-based appraisal recommendations based on multiple metrics

## Design Philosophy

- **Dark Mode Theme**: Modern, fintech-inspired aesthetic
- **Minimal & Clean**: Data-rich without clutter
- **Color Coded**: Green (on-track), Yellow (moderate risk), Red (attention needed)
- **Executive-Grade**: Stripe dashboard meets McKinsey performance tracker

## Color System

- **Primary**: #00d4ff (Cyan) - Main accent
- **Success**: #00ff88 (Green) - On track
- **Warning**: #ffa500 (Orange) - Moderate risk
- **Danger**: #ff4757 (Red) - Attention needed
- **Backgrounds**: #0f1419 (Dark), #1a1f2e (Card)

## Mocked Data Notes

- All employee data is simulated and resets on app reload
- No database or backend required
- Perfect for demo/prototype purposes
- Easily replaceable with real API calls

## Next Steps for Production

1. Connect to real employee database/HRIS
2. Integrate actual NLP for sentiment analysis
3. Implement proper file upload handling
4. Add authentication & authorization
5. Connect to email/collaboration systems
6. Add data persistence (PostgreSQL, etc.)
7. Implement real AI/ML for appraisal logic
8. Add email notifications

## Demo Data

- Employee: Alex Morgan (Quantitative Trading)
- 6 months of performance history
- 8 weeks of health tracking
- 5 360-feedback entries
- 4 KRAs tracked
- 3 active projects
- 2 key initiatives

---

**Version**: 0.1 (Prototype)  
**Status**: Ready for Demo  
**Last Updated**: February 2026
