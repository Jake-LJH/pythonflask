import os

class Settings:
    secretKey = '6w2hj*2nk4nfa089ym35\)anm52845-sreva124@$)(*17'

    #Dev
    #host='localhost'
    #database='furniture'
    #user='root'
    #password='root'

    #Staging on heroku
    host=os.environ['HOST']
    database=os.environ['DATABASE']
    user=os.environ['USERNAME']
    password=os.environ['PASSWORD']
