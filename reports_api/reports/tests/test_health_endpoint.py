from django.test import SimpleTestCase
from django.urls import reverse


class HealthEndpointTests(SimpleTestCase):
    # SimpleTestCase forbids database queries, which proves the view never touches the database
    def test_health_returns_200_ok_without_access_token(self):
        response = self.client.get(reverse('health'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'ok')
        self.assertTrue(response['Content-Type'].startswith('text/plain'))

    def test_health_url(self):
        self.assertEqual(reverse('health'), '/api/public/v1/health')

    def test_reports_still_requires_access_token(self):
        self.assertEqual(self.client.get('/reports').status_code, 403)
