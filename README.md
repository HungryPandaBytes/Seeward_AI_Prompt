# Cybersecurity Insights Assistant

A Streamlit application for analyzing and visualizing cybersecurity vulnerability data with AI-powered insights.

Live Demo: [https://seewardaiprompt-gqw2zhx5ffxhycyvg6f5vw.streamlit.app/]

## Features

- **User Authentication**: Secure login and registration system
- **AI-Powered Analysis**: Leverages OpenAI's GPT models to analyze vulnerability data
- **80/20 Principle Focus**: Prioritizes critical vulnerabilities that pose the highest risk
- **Role-Based Dashboards**: Customized views for different security roles:
  - CISO
  - IT Manager
  - Security Analyst
  - Developer
- **Data Visualization**: Embedded Looker Studio reports for comprehensive security metrics

## Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
4. Ensure you have `config.yaml` for user authentication or the application will create a default one

## Usage

1. Run the application:
   ```
   streamlit run app.py
   ```
2. Register a new account or login with existing credentials
3. Upload vulnerability scanner CSV data
4. Choose between quick analysis (80/20 principle) or custom analysis
5. View role-specific dashboards for different security perspectives

## Requirements

- Python 3.7+
- Streamlit
- OpenAI API key
- pandas
- PyYAML
- streamlit-authenticator
- python-dotenv

## Project Structure

- `app.py`: Main application file
- `config.yaml`: User authentication configuration
- `images/`: Directory containing application images (including logo)
- `.env`: Environment variables file (not tracked in git)

## Dashboard Integration

The application integrates with Looker Studio for visualization of security metrics with specialized dashboards for different security roles.
