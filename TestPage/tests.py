from django.test import TestCase
from django.test.client import RequestFactory
import urllib
import views

class TestCase2Pt1(TestCase):

    def test_connectivity(self):
        # urlopen returns 200 OK on success
        self.assertEqual(urllib.urlopen("localhost:8000/chat").getcode(), 200,
                         "Could not connect to localhost:8000/chat")
        self.assertEqual(urllib.urlopen("localhost:8000/chat2").getcode(), 200,
                         "Could not connect to localhost:8000/chat2")
        self.assertEqual(urllib.urlopen("localhost:8000/chat3").getcode(), 200,
                         "Could not connect to localhost:8000/chat3")


class TestCase4Pt1(TestCase):

    def test_email(self):
        retval = views.email('tch161@psu.edu')
        self.assertEqual(retval,True,"Email Failed")


class TestCase5Pt5(TestCase):

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
