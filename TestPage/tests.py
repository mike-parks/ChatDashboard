from django.test import TestCase
from django.test.client import RequestFactory
from mongoengine import connection, connect
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
