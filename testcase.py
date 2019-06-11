
import unittest
from server import app
from flask import session


class Testcase(unittest.TestCase):
    
    # =================================================+
    # Unittest for Auth Blueprint
    # =================================================+

    # -------------------------------------------------+
    # Display Testcase
    # -------------------------------------------------+

    def test_index_statuscode(self):
        """ Test Index / Endpoint Redirect Function """
        tester = app.test_client(self)
        self.assertEqual( tester.get('/').status_code , 302)

    def test_index2_statuscode(self):
        """ Test Index /index Endpoint Redirect Function """
        tester = app.test_client(self)
        self.assertEqual(tester.get('/index').status_code, 302)

    def test_index_content(self):
        """ Test Index Endpoint Redirect Function on no session found"""
        tester = app.test_client(self)
        self.assertTrue(b"You should be redirected automatically to target URL" in tester.get('/index').data)

    def test_login_statuscode(self):
        """ Test Login Endpoint Redirect Function """
        tester = app.test_client(self)
        self.assertEqual( tester.get('/login').status_code , 200)

    def test_login_content(self):
        """ Test Login Endpoint Redirect Function """
        tester = app.test_client(self)
        self.assertTrue(b"Login to start your session" in tester.get('/login').data)

    def test_register_statuscode(self):
        """ Test Register Endpoint Redirect Function """
        tester = app.test_client(self)
        self.assertEqual(tester.get('/register').status_code, 200)

    def test_register_content(self):
        """ Test Register Endpoint Redirect Function """
        tester = app.test_client(self)
        self.assertTrue(b"Register to join the game" in tester.get('/register').data)

    # -------------------------------------------------+
    # Respond Engine Testcase
    # -------------------------------------------------+

    def test_dashboard_injectSession(self):
        """ Injectd with exisiting username """
        tester = app.test_client(self)
        with tester.session_transaction() as session:
            session['username'] = "accalina"
        self.assertTrue( b"accalina" in tester.get("/").data )

    # -------------------------------------------------+
    # Negative Testcase
    # -------------------------------------------------+

    def test_negative_dashboard_injectSession_statuscode(self):
        """ Injected with non existing username """
        tester = app.test_client(self)
        with tester.session_transaction() as session:
            session['username'] = "notfound"
        self.assertEqual(tester.get("/").status_code, 403)

    def test_negative_dashboard_injectSession_content(self):
        """ Injected with non existing username """
        tester = app.test_client(self)
        with tester.session_transaction() as session:
            session['username'] = "notfound"
        self.assertTrue(b"BAD USERNAME" in tester.get("/").data)

    def test_negative_members_injectSession_statuscode(self):
        """ Injected with non existing username """
        tester = app.test_client(self)
        with tester.session_transaction() as session:
            session['username'] = "notfound"
        self.assertEqual(tester.get("/members").status_code, 403)

    def test_negative_members_injectSession_content(self):
        """ Injected with non existing username """
        tester = app.test_client(self)
        with tester.session_transaction() as session:
            session['username'] = "accalina"
        self.assertTrue(tester.get("/members").data)

    def test_negative_market_injectSession_statuscode(self):
        """ Injected with non existing username """
        tester = app.test_client(self)
        with tester.session_transaction() as session:
            session['username'] = "notfound"
        self.assertEqual(tester.get("/market").status_code, 403)

    def test_negative_market_injectSession_content(self):
        """ Injected with non existing username """
        tester = app.test_client(self)
        with tester.session_transaction() as session:
            session['username'] = "accalina"
        self.assertTrue(tester.get("/market").data)

    def test_negative_operations_injectSession_statuscode(self):
        """ Injected with non existing username """
        tester = app.test_client(self)
        with tester.session_transaction() as session:
            session['username'] = "notfound"
        self.assertEqual(tester.get("/operations").status_code, 403)

    def test_negative_operations_injectSession_content(self):
        """ Injected with non existing username """
        tester = app.test_client(self)
        with tester.session_transaction() as session:
            session['username'] = "accalina"
        self.assertTrue(tester.get("/operations").data)

if __name__ == "__main__":
    unittest.main()
