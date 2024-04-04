import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ctoken import gen_otp

sender_email = 'kgk6575@gmail.com'
password = 'lisg itts kfkr stsg'


def send_email(receiver_email,subject,body,sender=sender_email,password=password):
    try:
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = receiver_email
        msg['Subject'] = subject

         # Attach the Plain Body
        msg.attach(MIMEText(body,'plain'))

        # Attach the HTML Body
        #msg.attach(MIMEText(body,'html'))
        
        # Connecting to mail server

        server=smtplib.SMTP_SSL('smtp.gmail.com',465)
        server.login(sender,password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print('error in sending email',e)
        return False

'''if __name__=='__main__':
    otp=gen_otp()
    subject='verify your to signup'
    #body=f'dera user,\n please yur one time password to complete verification process\n{otp}'
    body=f'''
"""<!DOCTYPE html>
<html>

<head>
<title>email sending</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f4f4f4;
            background-image:url('./img/header.jpg');
        }}

        .container {{
            max-width: 600px;
            margin: auto;
            background-color: #fff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}

        .header {{
            font-size: 24px;
            color: #333;
            text-align: center;
            padding-bottom: 20px;
        }}

        .content {{
            font-size: 16px;
            color: #666;
            line-height: 1.5;
        }}

        .otp {{
            font-size: 20px;
            font-weight: bold;
            color: #333;
            text-align: center;
            margin: 20px 0;
        }}

        .footer {{
            text-align: center;
            padding-top: 20px;
            font-size: 14px;
            color: #aaa;
        }}
    </style>
</head>

<body>
    <div class="container">
        <div class="header">
            Your OTP for Verification
        </div>
        <div class="content">
            <p>Dear User,</p>
            <p>Please use the following One Time Password (OTP) to complete your verification process:</p>
            <div class="otp">
                {otp}
            </div>
            <p>This OTP is valid for the next 10 minutes. Do not share this OTP with anyone for security reasons.</p>
        </div>
        <div class="footer">
            &copy; 2024 Your Company Name. All rights reserved.
        </div>
    </div>
</body>

</html>'''
    reciever_email='ramtharaknadhalla@gmail.com'
    send_email(receiver_email=reciever_email,subject=subject,body=body)
    print('emial sent')'''"""