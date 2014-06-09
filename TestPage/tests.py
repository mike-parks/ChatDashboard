from django.test import TestCase
from django.test.client import RequestFactory
from mongoengine import connection, connect
import datetime
import urllib
import views


class MongoTestCase(TestCase):

    def __init__(self, methodName='runtest'):
        db_name = 'ourtestdb'
        connect(db_name)
        self.db = connection.get_db()
        super(MongoTestCase, self).__init__(methodName)

    def _post_teardown(self):
        super(MongoTestCase, self)._post_teardown()
        for collection in self.db.collection_names():
            if collection == 'system.indexes':
                continue
            self.db.drop_collection(collection)



class TestCase1Pt1(MongoTestCase):
    def setUp (self):
        self.factory = RequestFactory()
        
    def test_register(self):
        # registers user and then checks that user exists
        # create username with timestamp to make sure they are unique
        now = datetime.datetime.now()
        username = "TestUser-%d%d%d%d%d%d" % (now.year, now.month, now.day, now.hour, now.minute, now.second)
        
        # register user
        request = self.factory.post('/Register')
        request.POST['username'] = username
        request.POST['password'] = "Password1"
        request.POST['email'] = "testUser@email.com"
        response = views.send_message(request)
        self.assertEqual(response.status_code, 200, "Was unable to register user.")
        
        
        # attempt to register user a second time - should fail        
        response = views.send_message(request)
        self.assertNotEqual(response.status_code, 200, "Was able to register duplicate user.")
        
        
        #recreate username because the first one is already used
        now = datetime.datetime.now()
        username = "TestUser2-%d%d%d%d%d%d" % (now.year, now.month, now.day, now.hour, now.minute, now.second)
        
        # fail to register user with invalid password format - no number
        request = self.factory.post('/Register')
        request.POST['username'] = username
        request.POST['password'] = "Password"
        request.POST['email'] = "testUser@email.com"
        response = views.send_message(request)
        self.assertNotEqual(response.status_code, 200, "Was able to register user with invalid password format - no number.")
        
        # fail to register user with invalid password format- no uppercase
        request = self.factory.post('/Register')
        request.POST['username'] = username
        request.POST['password'] = "password1"
        request.POST['email'] = "testUser@email.com"
        response = views.send_message(request)
        self.assertNotEqual(response.status_code, 200, "Was able to register user with invalid password format - no uppercase.")
        
        # fail to register user with invalid password format - no lower case
        request = self.factory.post('/Register')
        request.POST['username'] = username
        request.POST['password'] = "PASSWORD1"
        request.POST['email'] = "testUser@email.com"
        response = views.send_message(request)
        self.assertNotEqual(response.status_code, 200, "Was able to register user with invalid password format - no lowercase.")
        
        # fail to register user with invalid email format
        request = self.factory.post('/Register')
        request.POST['username'] = username
        request.POST['password'] = "Password1"
        request.POST['email'] = "testUser"
        response = views.send_message(request)
        self.assertNotEqual(response.status_code, 200, "Was able to register user with invalid email format.")
        
        # fail to register user without email
        request = self.factory.post('/Register')
        request.POST['username'] = username
        request.POST['password'] = "Password1"
        request.POST['email'] = ""
        response = views.send_message(request)
        self.assertNotEqual(response.status_code, 200, "Was able to register user without email.")
        
        
        
class TestCase1Pt2(MongoTestCase):
    def setUp (self):
        self.factory = RequestFactory()
        
    def test_login(self):
        username = "TestUser"
        
        # log user in
        request = self.factory.post('/Login')
        request.POST['username'] = username
        request.POST['password'] = "Password1"
        response = views.send_message(request)
        self.assertEqual(response.status_code, 200, "Was unable to log user in.")
        
        # fail to log user in with wrong password
        request = self.factory.post('/Login')
        request.POST['username'] = username
        request.POST['password'] = "BadPassword"
        response = views.send_message(request)
        self.assertNotEqual(response.status_code, 200, "Was able to log user in with bad password.") 
        
        # fail to log user in with wrong username
        request = self.factory.post('/Login')
        request.POST['username'] = "BadTestUser"
        request.POST['password'] = "Password1"
        response = views.send_message(request)
        self.assertNotEqual(response.status_code, 200, "Was able to log user in with invalid username.") 
        
        
class TestCase1Pt3(MongoTestCase):
    def setUp (self):
        self.factory = RequestFactory()
        
    def test_logout(self):
        # log user in
        request = self.factory.post('/Logout')
        request.POST['username'] = username
        response = views.send_message(request)
        self.assertEqual(response.status_code, 200, "Was unable to log user out.")
        
        
class TestCase1Pt4(MongoTestCase):
    def setUp (self):
        self.factory = RequestFactory()
        
    def test_changePassword(self):
        username = "TestUser"
        
        # change password
        request = self.factory.post('/ChangePassword')
        request.POST['username'] = "TestUser"
        request.POST['CurrentPassword'] = "password"
        request.POST['NewPassword'] = "Password2"
        response = views.send_message(request)
        self.assertEqual(response.status_code, 200, "Was unable to change password.") 
        
        # fail change password - wrong current password        
        request = self.factory.post('/ChangePassword')
        request.POST['username'] = "TestUser"
        request.POST['CurrentPassword'] = "BadPassword"
        request.POST['NewPassword'] = "Password2"
        response = views.send_message(request)
        self.assertEqual(response.status_code, 200, "Was able to change password with invalid Current Password.") 
        
        #fail change password - wrong username        
        request = self.factory.post('/ChangePassword')
        request.POST['username'] = "BadTestUser"
        request.POST['CurrentPassword'] = "Password2"
        request.POST['NewPassword'] = "Password2"
        response = views.send_message(request)
        self.assertNotEqual(response.status_code, 200, "Was able to change password on BadTestUser.") 
        
        
        # fail on change password to password without number
        request = self.factory.post('/ChangePassword')
        request.POST['username'] = "TestUser"
        request.POST['CurrentPassword'] = "Password2"
        request.POST['NewPassword'] = "Password"
        response = views.send_message(request)
        self.assertNotEqual(response.status_code, 200, "Was able to change password to one without a number.") 
        
        # fail on change password to password without uppercase alpha
        request = self.factory.post('/ChangePassword')
        request.POST['username'] = "TestUser"
        request.POST['CurrentPassword'] = "Password2"
        request.POST['NewPassword'] = "password1"
        response = views.send_message(request)
        self.assertNotEqual(response.status_code, 200, "Was able to change password to one without an uppercase alpha.") 
        
        # fail on change password to password without lowercase alpha
        request = self.factory.post('/ChangePassword')
        request.POST['username'] = "TestUser"
        request.POST['CurrentPassword'] = "Password2"
        request.POST['NewPassword'] = "PASSWORD1"
        response = views.send_message(request)
        self.assertNotEqual(response.status_code, 200, "Was able to change password to one without a lowecase alpha.") 
    
        # change password back for next test
        request = self.factory.post('/ChangePassword')
        request.POST['username'] = "TestUser"
        request.POST['CurrentPassword'] = "Password2"
        request.POST['NewPassword'] = "Password1"
        response = views.send_message(request)
        self.assertEqual(response.status_code, 200, "Was unable to change password back to origional password.") 

class TestCase2Pt1(MongoTestCase):

    def test_connectivity(self):
        # urlopen returns 200 OK on success
        self.assertEqual(urllib.urlopen("localhost:8000/chat").getcode(), 200,
                         "Could not connect to localhost:8000/chat")
        self.assertEqual(urllib.urlopen("localhost:8000/chat2").getcode(), 200,
                         "Could not connect to localhost:8000/chat2")
        self.assertEqual(urllib.urlopen("localhost:8000/chat3").getcode(), 200,
                         "Could not connect to localhost:8000/chat3")


class TestCase4Pt1(MongoTestCase):

    def test_email(self):
        retval = views.email('tch161@psu.edu')
        self.assertEqual(retval,True,"Email Failed")


class TestCase5Pt5(MongoTestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_send_message(self):
        request = self.factory.post('/chat')
        request.POST['text'] = "test text"
        request.POST['username'] = "test user"
        request.POST['topic'] = "1"
        response = views.send_message(request)
        self.assertEqual(response.status_code, 200,
                         "Did not see 200 OK after first test message")

        # POSTing second request
        request.POST['text'] = "second test text"
        request.POST['username'] = "next test user"
        response = views.send_message(request)
        self.assertEqual(response.status_code, 200,
                         "Did not see 200 OK after second test message")
