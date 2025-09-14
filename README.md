# AIAssisted-Online-Voting-Portal

🗳 AgenticAI – AI-Powered Online Voting Portal
📌 Overview

AgenticAI is a secure and intelligent online voting system that leverages Artificial Intelligence and Blockchain-ready architecture to ensure transparency, security, and efficiency in elections. The portal allows voters to cast their votes digitally, while an AI chatbot guides them through the process, explains candidate details, and promotes election transparency.

✨ Key Features

🔐 Secure Login – Voter authentication via unique credentials (ID, DOB, Name, Email).

🗳 One Voter, One Vote – Prevents duplicate/multiple voting attempts.

📊 Real-Time Results – Votes are counted instantly with live result visualization.

🎨 Interactive UI – Candidate cards, voting dashboard, and election slogans.

🗄 Database Support – Uses SQLite for secure storage of registered voters and votes.

🤝 Hackathon-Ready – Designed for scalability with potential blockchain integration.

🛠 Tech Stack

Backend: Flask (Python)

Frontend: HTML, CSS, Jinja2 templates

Database: SQLite (preregistered.db)

AI/ML: Custom-trained model (agent_model.pkl)

Testing: Python unit tests

📂 Project Structure
AgenticAI Final/
│── app.py                 # Main application entry point  
│── ai_agent.py            # AI logic  
│── train_model.py         # Model training script  
│── agent_model.pkl        # Trained AI model  
│── preregistered.db       # SQLite database  
│── schema.sql             # Database schema  
│── users.csv              # Sample voter dataset  
│── templates/             # HTML templates (login, voting, results, etc.)  
│── static/images/         # Candidate images  
│── test_agent.py          # AI test  
│── test_email_validation.py # Email validation test  
│── .env                   # Environment variables  
│── .gitignore             # Git ignore file  

🔮 Future Enhancements

🔗 Blockchain integration for tamper-proof vote recording.

🌍 Scalability for large-scale elections.

📱 Mobile-friendly responsive design.

🧑‍💻 Multi-language AI chatbot for inclusivity.
