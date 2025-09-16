from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re

app = Flask(__name__)

# --- CONFIGURE THESE ---
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = 'joshua8john199@gmail.com'  # Replace with your email
SMTP_PASS = 'ksrmidtyzidnkdma'      # Replace with your app password (not your main password)
FROM_EMAIL = SMTP_USER
SUBJECT = 'Job Alert Confirmation'

@app.route('/send-alert', methods=['POST'])
def send_alert():
    data = request.get_json()
    email = data.get('email')
    if not email or not re.match(r'^\S+@\S+\.\S+$', email):
        return jsonify({'success': False, 'error': 'Invalid email'}), 400
    try:
        # Compose email
        msg = MIMEMultipart()
        msg['From'] = FROM_EMAIL
        msg['To'] = email
        msg['Subject'] = SUBJECT
        body = f"""
        <h2>Job Alert Enabled!</h2>
        <p>Thank you for subscribing to job alerts. You will receive notifications for new or similar jobs.</p>
        <p>If you did not request this, please ignore this email.</p>
        """
        msg.attach(MIMEText(body, 'html'))
        # Send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(FROM_EMAIL, email, msg.as_string())
        server.quit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
