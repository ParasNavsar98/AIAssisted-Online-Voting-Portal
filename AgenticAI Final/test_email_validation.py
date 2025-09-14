from ai_agent import is_email_valid



emails = [
    "paras123@gmail.com",
    "para.singh-99@outlook.com",
    "valid_user+test@yahoo.com",
    "imh$%^&@gmail.com",
    "Par543a$%^&s@gmail.com",
    "abc@@gmail.com",
    "navsarpa&^*ras@gmail.com",
    "user@domain",
    "justtext"
]

print("=== Email Validation Test ===")
for email in emails:
    result = "✅ Allowed" if is_email_valid(email) else "❌ Blocked"
    print(f"{email:35} -> {result}")
