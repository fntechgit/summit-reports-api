from django.test import TestCase
from graphene.test import Client

from reports_api.reports.models.constants import SelectionStatus, SubmissionStatus
from reports_api.schema import schema


class SpeakerTestCase(TestCase):

    databases = {'default', 'openstack_db'}

    def setUp(self):
        self.client = Client(schema)
        self.summit_id = 63

    def test_get_filtered_by_selection_plan_ids_in(self):
        selection_plan_ids = "48,49"

        query = f'''
        {{
          reportData: speakers(summitId: {self.summit_id}, selectionPlanIdIn: "{selection_plan_ids}") {{
            results: results(limit: 25) {{
              selectionPlan(summitId: {self.summit_id})
            }}
          }}
        }}
        '''

        executed = self.client.execute(query)

        report_data = executed.get('data', {}).get('reportData', {})
        results = report_data.get('results', [])

        self.assertTrue(results, "No results returned from the query")


    #Selection status tests
    def __test_get_filtered_by_selection_status(self, selection_status_filter, expected_status_list):
        query = f'''
        {{
          reportData: speakers(summitId: {self.summit_id}, selectionStatus: "{selection_status_filter}") {{
            results: results(limit: 300) {{
              id
              selectionStatus(summitId: {self.summit_id}) {{
                presentationId
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

        total = report_data.get('totalCount')

        self.assertGreaterEqual(total, len(results))

        for result in results:
            selection_statuses = result.get('selectionStatus', [])
            self.assertTrue(selection_statuses, "No selection status found")
            found_status = False
            for selection_status in selection_statuses:
                if expected_status_list.__contains__(selection_status.get('status')):
                    found_status = True
                    break
            self.assertTrue(found_status)

    def test_get_filtered_by_selection_status_selected(self):
        self.__test_get_filtered_by_selection_status(
            SelectionStatus.SELECTED.value, [SelectionStatus.SELECTED, SelectionStatus.ACCEPTED, SelectionStatus.ALTERNATE])

    def test_get_filtered_by_selection_status_accepted(self):
        self.__test_get_filtered_by_selection_status(SelectionStatus.ACCEPTED.value, [SelectionStatus.ACCEPTED])

    def test_get_filtered_by_selection_status_alternate(self):
        self.__test_get_filtered_by_selection_status(SelectionStatus.ALTERNATE.value, [SelectionStatus.ALTERNATE])

    def test_get_filtered_by_selection_status_lightning_accepted(self):
        self.__test_get_filtered_by_selection_status(
            SelectionStatus.LIGHTNING_ACCEPTED.value,[SelectionStatus.LIGHTNING_ACCEPTED])

    def test_get_filtered_by_selection_status_lightning_alternate(self):
        self.__test_get_filtered_by_selection_status(
            SelectionStatus.LIGHTNING_ALTERNATE.value,[SelectionStatus.LIGHTNING_ALTERNATE])

    def test_get_filtered_by_selection_status_rejected(self):
        self.__test_get_filtered_by_selection_status(
            SelectionStatus.REJECTED.value,[SelectionStatus.REJECTED])


    #Submission status tests
    def __test_get_filtered_by_submission_status(self, submission_status_filter):
        query = f'''
        {{
          reportData: speakers(summitId: {self.summit_id}, submissionStatus: "{submission_status_filter}") {{
            results: results(limit: 300) {{
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

        total = report_data.get('totalCount')

        self.assertGreaterEqual(total, len(results))

        for result in results:
            submission_statuses = result.get('submissionStatus', [])
            self.assertTrue(submission_statuses, "No submission status found")
            found_status = False
            for submission_status in submission_statuses:
                if submission_status_filter == submission_status.get('status'):
                    found_status = True
                    break
            self.assertTrue(found_status)

    def test_get_filtered_by_submission_status_accepted(self):
        self.__test_get_filtered_by_submission_status(SubmissionStatus.ACCEPTED.value)

    def test_get_filtered_by_submission_status_received(self):
        self.__test_get_filtered_by_submission_status(SubmissionStatus.RECEIVED.value)

    def test_get_filtered_by_submission_status_non_received(self):
        self.__test_get_filtered_by_submission_status(SubmissionStatus.NON_RECEIVED.value)