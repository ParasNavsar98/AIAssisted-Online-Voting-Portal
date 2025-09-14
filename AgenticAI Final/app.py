from flask import Flask, render_template, request, redirect, session, flash
import sqlite3, smtplib, random
from email.message import EmailMessage   
from ai_agent import is_email_valid, verify_user, load_agent
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

agent_model = load_agent()
VOTE_HIDE_DURATION = timedelta(minutes=5)

load_dotenv()  # loads environment variables from .env

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-key")



# -----------------------------
# Database helper
# -----------------------------
def get_db_connection():
    return sqlite3.connect(r"C:\Users\DELL\OneDrive\Desktop\DataBase\vote.db")

# -----------------------------
# Register / Create account
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def Creatacc():
    if request.method == "POST":
        Username = request.form["name"].strip()
        Email = request.form["email"].strip()
        Password = request.form["passkey"].strip()
        Cpassword = request.form["cpasskey"].strip()

        session["username"] = Username
        session["email"] = Email
        session["passkey"] = Password

        if Password != Cpassword:
            flash("Passwords do not match!")
            return render_template("creatacc.html")

        # Check if email already exists
        conn = get_db_connection()
        curs = conn.cursor()
        curs.execute("SELECT * FROM votes WHERE email = ?", (Email,))
        if curs.fetchone():
            conn.close()
            flash("Email already registered! Please login.")
            return redirect("/login")

        # Generate OTP
        otp = random.randrange(100000, 1000000)
        session["OTP"] = otp
        print(f"Generated OTP: {otp}")  # debug log

        # Send OTP via Gmail
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login("parasexp541@gmail.com", "fthb vxci ufzt muuf")  # app password
            msg = EmailMessage()
            msg["Subject"] = "OTP Verification"
            msg["From"] = "parasexp541@gmail.com"
            msg["To"] = Email
            msg.set_content(f"Your OTP is {otp}")
            server.send_message(msg)
            server.quit()
        except Exception as e:
            print("Error sending email:", e)
            flash("Could not send OTP. Check email settings.")
            return render_template("creatacc.html")

        # Insert user into DB
        curs.execute(
            "INSERT INTO votes (name, email, password, cpassword) VALUES (?, ?, ?, ?)",
            (Username, Email, Password, Cpassword),
        )
        conn.commit()
        conn.close()

        flash("Account created! Please login with OTP.")
        return redirect("/login")

    return render_template("creatacc.html")


# -----------------------------
# Login
# -----------------------------
@app.route("/login", methods=["POST", "GET"])
def Login():
    if request.method == "POST":
        Password = request.form["passkey"].strip()
        Cotp = request.form["otp"].strip()

        # Fetch session values set during registration
        ctp = session.get("OTP")
        saved_passkey = session.get("passkey")
        saved_email = session.get("email")

        if not is_email_valid(saved_email):
            flash("❌ Invalid email format. Please try again.")
            return render_template("login.html")

        # OTP expired
        if ctp is None:
            flash("Session expired. Please register again.")
            return redirect("/")

        # OTP or credentials wrong
        if int(Cotp) != ctp or saved_passkey != Password:
            flash("Login Failed: Incorrect OTP or Credentials")
            return render_template("login.html")

        # 🔒 AI Agent verification
        if not verify_user(saved_email, Password, agent_model):
            flash("⚠️ Suspicious login detected! Access denied.")
            return render_template("login.html")

        # Fetch email from DB (using saved email from session)
        conn = get_db_connection()
        curs = conn.cursor()
        curs.execute("SELECT email FROM votes WHERE email = ?", (saved_email,))
        row = curs.fetchone()
        conn.close()

        if row:
            session["email"] = row[0]
        else:
            flash("User email not found. Please register again.")
            return redirect("/")

        # Login success
        session["hasvoted"] = False
        flash("✅ Login Successful!")
        return redirect("/vote")

    return render_template("login.html")

# -----------------------------
# Voting Route
# -----------------------------
@app.route("/vote", methods=["GET", "POST"])
def vote():
    if "email" not in session:
        flash("Please login first!")
        return redirect("/login")

    conn = get_db_connection()
    curs = conn.cursor()

    # Check if user already voted
    curs.execute("SELECT votecast FROM votes WHERE email = ?", (session["email"],))
    row = curs.fetchone()
    user_vote = row[0] if row else None

    # Candidate mapping (ID → Name)
    candidates = {
        "can1": "Harry",
        "can2": "Alice",
        "can3": "Hiroshi",
        "can4": "Emma"
    }

    if request.method == "POST" and not user_vote:
        chosen_id = request.form.get("Candidate")
        chosen_name = candidates.get(chosen_id)

        if chosen_name:
            curs.execute(
                "UPDATE votes SET votecast = ?, vote_time = CURRENT_TIMESTAMP WHERE email = ?",
                (chosen_name, session["email"])
            )
            conn.commit()
            flash("Vote successfully registered!")
            user_vote = chosen_name
            conn.close()
            return redirect("/result")
        else:
            flash("Invalid candidate selected.")

    conn.close()
    return render_template("voting.html", user_vote=user_vote)

# -----------------------------
# Result Route
# -----------------------------
@app.route("/result")
def result():   
    if "email" not in session:
        flash("Please login first!")
        return redirect("/login")

    conn = get_db_connection()
    curs = conn.cursor()

    # Get latest vote timestamp
    curs.execute("SELECT MAX(vote_time) FROM votes")
    last_vote_row = curs.fetchone()
    last_vote_time = last_vote_row[0] if last_vote_row else None

    show_results = False
    results = {}
    winner = None

    if last_vote_time:
        try:
            last_vote_time = datetime.strptime(last_vote_time.split(".")[0], "%Y-%m-%d %H:%M:%S")
        except Exception as e:
            print("Error parsing datetime:", e)

        if datetime.now() - last_vote_time >= VOTE_HIDE_DURATION:
            show_results = True

    # Fetch candidate votes (directly by name stored in DB)
    if show_results:
        curs.execute("SELECT votecast, COUNT(*) FROM votes WHERE votecast IS NOT NULL GROUP BY votecast")
        rows = curs.fetchall()
        for row in rows:
            results[row[0]] = row[1]

        if results:
            max_votes = max(results.values())   
            top_candidates = [c for c, v in results.items() if v == max_votes]

            if len(top_candidates) == 1:
                winner = top_candidates[0]
            else:
                winner = top_candidates

    conn.close()
    return render_template("result.html", results=results, show_results=show_results, winner=winner)

# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
