import os

class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'd45g45iu3y4893n545rc398r2r28r'

    MONGODB_SETTINGS = {'db' : 'UTA_Enrollment',
        'host':'mongodb://localhost:27017/UTA_Enrollment'
    }