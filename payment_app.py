from flask import Flask, request, render_template_string
import logging

app = Flask(__name__)

# Configure auth.log file to log security and authentication events
logging.basicConfig(filename='auth.log', level=logging.WARNING, format='%(asctime)s - %(message)s')

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Secure Payment Gateway</title>
    <style>
        body { font-family: sans-serif; background-color: #2c3e50; color: white; text-align: center; padding-top: 50px; }
        .login-box { background: #34495e; padding: 30px; border-radius: 10px; width: 300px; margin: auto; box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
        input { width: 90%; padding: 10px; margin: 10px 0; border: none; border-radius: 5px; }
        button { width: 100%; padding: 10px; background: #e74c3c; color: white; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #c0392b; }
    </style>
</head>
<body>
    <h2>🔒 AIOps Secure Payment Gateway</h2>
    <div class="login-box">
        <form method="POST">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login & Pay</button>
        </form>
        <p style="color: #e74c3c;">{{ error_msg }}</p>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def login():
    error_msg = ""
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        
        # Correct password is 'secret123'; all failed attempts will be logged
        if user == 'admin' and pwd == 'secret123':
            return "<h3 style='color:#2ecc71;'>✅ Payment Successful!</h3>"
        else:
            error_msg = "❌ Invalid Credentials!"
            client_ip = request.remote_addr
            # Log failed login attempts to the security log file
            logging.warning(f"CRITICAL: FAILED LOGIN ATTEMPT - User: {user} - IP: {client_ip} - Reason: Invalid Password")
            
    return render_template_string(HTML_PAGE, error_msg=error_msg)

if __name__ == '__main__':
    # Run the payment service on port 5000
    app.run(host='0.0.0.0', port=5000)