from itsdangerous import URLSafeTimedSerializer , SignatureExpired
import random
from key import secret_key , salt

serializer=URLSafeTimedSerializer(secret_key)

#fuction to generate otp
def gen_otp(length=6):
    return ''.join([str(random.randint(0,9))for _ in range(length)])
    

#function to create token

def create_token(result,salt):
    token=serializer.dumps(result,salt=salt)
    return token

# function to verify created tokens

def verify_token(token,salt,expire=300):
    try:
        token_data=serializer.loads(token,salt=salt,max_age=expire)
        return token_data
    except SignatureExpired:
        print('token expired')
        return None
    
if __name__=='__main__':
    result={'username':'Gopikrishna','email':'ramtharaknadhalla@gmail.com',}
    #token=create_token(result,salt=salt)
    tokens='eyJ1c2VybmFtZSI6IkdvcGlrcmlzaG5hIiwiZW1haWwiOiJyYW10aGFyYWtuYWRoYWxsYUBnbWFpbC5jb20ifQ.ZfKWtA.6anMllYtqt84svDcMEqJX5q5WNQ'
    print('encrypted token',tokens)
    token_data=verify_token(tokens,salt=salt)
    print('decrypted data',token_data)