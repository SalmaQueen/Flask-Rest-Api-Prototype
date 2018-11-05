from tests.base_test_case import BaseTestCase


class TestMisc(BaseTestCase):

    def setUp(self):
        # Test that https is enforced on production
        super(TestMisc, self).setUp()
        self.app.debug = False

    def test_redirect_http(self):
        resp = self.client.get('/api/v1/books')
        self.assertEqual(301, resp.status_code)
