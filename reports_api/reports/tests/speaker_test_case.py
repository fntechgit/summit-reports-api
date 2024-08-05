from django.test import TestCase
from graphene.test import Client

from reports_api.reports.models.constants import SelectionStatus, SubmissionStatus
from reports_api.schema import schema


class SpeakerTestCase(TestCase):

    databases = {'default', 'openstack_db'}

    def setUp(self):
        self.client = Client(schema)
        self.summit_id = 27

    def test_get_filtered_by_submission_plan(self):
        submission_plan = "Presentation Title 34"

        query = f'''
        {{
          reportData: speakers(summitId: {self.summit_id}, submissionPlan: "{submission_plan}") {{
            results: results(limit: 25) {{
              submissionPlan(summitId: {self.summit_id})
            }}
          }}
        }}
        '''

        executed = self.client.execute(query)

        report_data = executed.get('data', {}).get('reportData', {})
        results = report_data.get('results', [])

        self.assertTrue(results, "No results returned from the query")

        for result in results:
            submission_plan_found = result.get('submissionPlan')
            self.assertTrue(submission_plan in submission_plan_found)


    #Selection status tests
    def __test_get_filtered_by_selection_status(self, selection_status_filter, expected_status_list):
        query = f'''
        {{
          reportData: speakers(summitId: {self.summit_id}, selectionStatus: "{selection_status_filter}") {{
            results: results(limit: 25) {{
              selectionStatus(summitId: {self.summit_id}) {{
                status
              }}
            }}
            totalCount
          }}
        }}
        '''

        executed = self.client.execute(query)

        report_data = executed.get('data', {}).get('reportData', {})
        results = report_data.get('results', [])

        self.assertTrue(results, "No results returned from the query")

        total = report_data.get('totalCount')

        self.assertTrue(len(results), total)

        for result in results:
            selection_statuses = result.get('selectionStatus', [])
            self.assertTrue(selection_statuses, "No selection status found")
            for selection_status in selection_statuses:
                self.assertIn(selection_status['status'], expected_status_list)

    def test_get_filtered_by_selection_status_selected(self):
        self.__test_get_filtered_by_selection_status(
            SelectionStatus.SELECTED, [SelectionStatus.SELECTED, SelectionStatus.ACCEPTED, SelectionStatus.ALTERNATE])

    def test_get_filtered_by_selection_status_accepted(self):
        self.__test_get_filtered_by_selection_status(SelectionStatus.ACCEPTED, [SelectionStatus.ACCEPTED])

    def test_get_filtered_by_selection_status_alternate(self):
        self.__test_get_filtered_by_selection_status(SelectionStatus.ALTERNATE, [SelectionStatus.ALTERNATE])

    def test_get_filtered_by_selection_status_lightning_alternate(self):
        self.__test_get_filtered_by_selection_status(
            SelectionStatus.LIGHTNING_ALTERNATE,[SelectionStatus.LIGHTNING_ALTERNATE])

    def test_get_filtered_by_selection_status_rejected(self):
        self.__test_get_filtered_by_selection_status(
            SelectionStatus.REJECTED,[SelectionStatus.REJECTED])


    #Submission status tests
    def __test_get_filtered_by_submission_status(self, submission_status_filter):
        query = f'''
        {{
          reportData: speakers(publishedIn: {self.summit_id}, summitId: {self.summit_id}, submissionStatus: "{submission_status_filter}") {{
            results: results(limit: 25) {{
              submissionStatus(summitId: {self.summit_id}) {{
                status
              }}
            }}
            totalCount
          }}
        }}
        '''

        executed = self.client.execute(query)

        report_data = executed.get('data', {}).get('reportData', {})
        results = report_data.get('results', [])

        self.assertTrue(results, "No results returned from the query")

        total = report_data.get('totalCount')

        self.assertTrue(len(results), total)

        for result in results:
            submission_statuses = result.get('submissionStatus', [])
            self.assertTrue(submission_statuses, "No submission status found")
            for submission_status in submission_statuses:
                self.assertEqual(submission_status_filter, submission_status['status'])

    def test_get_filtered_by_submission_status_accepted(self):
        self.__test_get_filtered_by_submission_status(SubmissionStatus.ACCEPTED)

    def test_get_filtered_by_submission_status_received(self):
        self.__test_get_filtered_by_submission_status(SubmissionStatus.RECEIVED)

    def test_get_filtered_by_submission_status_non_received(self):
        self.__test_get_filtered_by_submission_status(SubmissionStatus.NON_RECEIVED)