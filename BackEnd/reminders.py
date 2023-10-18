import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from jinja2 import Template
import time
from database import db
from models import Order, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

remainder_time_to_get_mail = datetime.now().replace( #setting the time to send the mail
    hour=17, minute=26, second=0, microsecond=0)

def remainder_send_to_the_user(to_address, subject, message): #remainder send to the user daily sent at a particular time 
    msg = MIMEMultipart()
    msg['To'] = to_address
    msg['From'] = 'ushasrigudikandula456@gmail.com'
    msg['Subject'] = subject

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'ushasrigudikandula456@gmail.com'
    smtp_password = 'trmfjwllrhewpjdq'
    msg.attach(MIMEText(message, 'html'))
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
    return "email sent successfully"
    
 

db.init_app(app)

if __name__ == '__main__':
    seconds = 10
    with app.app_context():
        flag=1 #using infinite loop and setting the time to send the remainder daly if todays remainder expires then calcualte the next remainder and set the job for it
        while flag==1:
            current_time_of_day = datetime.now()
            time_remained_for_the_remainder = remainder_time_to_get_mail - current_time_of_day

            if time_remained_for_the_remainder.total_seconds() < 0:
                time_remained_for_the_remainder += timedelta(days=1)

            print(
                f" Delaying and waiting {time_remained_for_the_remainder.seconds} seconds for the remainder to be sent as an email")
            time.sleep(time_remained_for_the_remainder.seconds)
            
            with open('./templates/daily_remainder.html', 'r') as f:
                template = Template(f.read())
            
            users = User.query.filter_by(role="user").all()
            
            for user in users:
                today = datetime.today().date()
                print(today)
                user_orders_today = Order.query.filter_by(user_id=user.id).filter(
                    Order.ordered_at >= today).all()
                print(user_orders_today)

                if not user_orders_today:
                    message="You havent visited so far today .please do visit sir/Madam"
                    remainder_send_to_the_user(user.email, 'RemainderToVisitOurStore', template.render(user=user.username,message=message))
                else:
                    print(f"The user took something no need of sending remainders so just send thanks{user.username}")
                    message="Thanks do visit again .Hoping Feedback from you"
                    remainder_send_to_the_user(user.email, 'VoteOfThanks', template.render(user=user.username ,message=message))
