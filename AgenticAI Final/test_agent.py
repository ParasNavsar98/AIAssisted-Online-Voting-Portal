from ai_agent import load_agent, verify_user

agent_model = load_agent()

test_users = [
    ("aaravsharma101@gmail.com", "12345"),    # valid in dataset
    ("hacker@@evil.com", "$$$$$$"),           # invalid email & special chars
    ("admin@random.com", "admin"),            # weak password
    ("strangeuser@gmail.com", "!@#$%^")      # only special chars
]

for email, password in test_users:
    if verify_user(email, password, agent_model):
        print(f"✅ Login allowed for {email}")
    else:
        print(f"⚠️ Suspicious login detected for {email}")
