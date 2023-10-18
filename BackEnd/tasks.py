from celery import Celery
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from jinja2 import Template
import time
from io import StringIO
import csv
import os
from celery.schedules import crontab
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template
from models import Product,User,Category,Order
from database import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

celery = Celery(__name__, broker='redis://localhost:6379/0',
                backend='redis://localhost:6379/0')
  
celery.conf.beat_schedule = { #beat scheduer using crontab used to call the celery tasks 
    'run-every-minute': {
        'task': 'tasks.month_report',   
        'schedule': crontab(hour='17',minute='26'),   
    },
}



celery.conf.timezone = 'Asia/Kolkata'
celery.conf.update(app.config)

@celery.task
def month_report(): #used to generate the monthly reports and send the template mail to the users end 
    with app.app_context():
        month = datetime.now().strftime('%B')
        year = datetime.now().year
        day = datetime.now().day
        active_users = User.query.filter_by(role='user').all()
        count=0
    
        for user in active_users:
            orders = Order.query.filter_by(user_id=user.id).all()
            user_name=user.username
            ordersList=[]
            expenditure=0
            length=0
            if orders :
                for i in orders:
                    ordersList.append({"product_name":i.name,"rate":i.price,"quantity":i.quantity,"amount":i.amount})
                    expenditure+=i.amount
                length=len(ordersList)

        
            with open('./templates/monthly_report.html', 'r') as f:
                template = Template(f.read())

            send_email2(user.email, 'welcome', template.render(user_name= user_name,month=month,year=year,day=day,order_list=ordersList,expenditure=expenditure,length=length))
            count+=1
        return  count

def send_email2(to_address, subject, message): #send mail to the user using smtp protocol
    msg = MIMEMultipart()
    msg['To'] = to_address
    msg['From']= 'ushasrigudikandula456@gmail.com'
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
    return "email sent successfully to the user"

@celery.task
def export_csv(created_user_id): #csv celery task triggers on getting clciked by the manager downlaod option
    with app.app_context():
        products = Product.query.filter_by(store_manager_id=created_user_id).all()

        
        csv_buffer = StringIO()
        csv_writer = csv.writer(csv_buffer)
        csv_writer.writerow(["Name", "category_id",
                            "mandate", "Price", "Units", "Quantity","No_sold_items"])
        

        for product in products:
            order_product_ids = Order.query.filter_by(product_id = product.product_id).all()
            sold_out = 0
            if(order_product_ids):
                for i in order_product_ids:
                    sold_out+=i.quantity
            csv_writer.writerow([
                product.product_name,
                str(product.category_id),
                str(product.created_at),
                str(product.rate),
                str(product.units),
                str(product.quantity),
                str(sold_out)
            ])
        print(csv_writer)
 
        base_dir = os.path.abspath(os.path.dirname(__file__))
        csv_file_path = os.path.join(base_dir, "csv/product_report.csv")
        with open(csv_file_path, 'w') as csv_file:
            csv_file.write(csv_buffer.getvalue())
        print("Hello Anil")

        return csv_buffer.getvalue()
    
db.init_app(app) #to avoid the initalizaion error or multiple instance error