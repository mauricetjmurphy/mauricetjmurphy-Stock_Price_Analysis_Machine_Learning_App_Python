from flask import Flask, jsonify, request, session
import unittest
from app import app
from app import db
from dotenv import load_dotenv

load_dotenv()


class TestCase(unittest.TestCase):

    def test_login_page(self):
        # This test checks the login page for a HTTP 200 OK response
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)


    def test_login_page_content(self):
        #  This test checks if "Login" is in the response data that we get from the login route
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertTrue(b"Login" in response.data)


    def test_data_page(self):
        with app.test_request_context():
        # This test checks the data page
            user = db.users.find_one({'email': 'test@test.com'})
            session['logged_in'] = True
            session['user'] = user
            tester = app.test_client(self)
            response = tester.get('/data', content_type='html/text')
            self.assertEqual(response.status_code, 302)
    

    def test_regression_page(self):
        with app.test_request_context():
        # This test checks the regression route
            user = db.users.find_one({'email': 'test@test.com'})
            session['logged_in'] = True
            session['user'] = user
            tester = app.test_client(self)
            response = tester.get('/regression', content_type='html/text')
            self.assertEqual(response.status_code, 302)

    
    def test_sentiment_page(self):
        with app.test_request_context():
        # This test checks the sentiment route
            user = db.users.find_one({'email': 'test@test.com'})
            session['logged_in'] = True
            session['user'] = user
            tester = app.test_client(self)
            response = tester.get('/sentiment', content_type='html/text')
            self.assertEqual(response.status_code, 302)
    

   

if __name__ == '__main__':
    unittest.main()