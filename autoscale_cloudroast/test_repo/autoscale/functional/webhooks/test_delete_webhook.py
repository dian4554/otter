"""
Test to verify a webhok can be deleted successfully.
"""
from test_repo.autoscale.fixtures import ScalingGroupWebhookFixture


class DeleteWebhook(ScalingGroupWebhookFixture):

    """
    verify delete webhook call's response code, headers.
    """

    def test_delete_webhook(self):
        """
        Test delete webhook returns 204 when successful
        """
        self.assertEquals(self.create_webhook_response.status_code, 201,
                          msg='Create webhook for a policy failed with {0} for group'
                          '{1}'.format(self.create_webhook_response.status_code,
                                       self.group.id))
        self.validate_headers(self.create_webhook_response.headers)
        delete_webhook_resp = self.autoscale_client.delete_webhook(
            group_id=self.group.id,
            policy_id=self.policy['id'],
            webhook_id=self.webhook['id'])
        self.assertEquals(delete_webhook_resp.status_code, 204,
                          msg='Delete webhook failed with {0} for group '
                          '{1}'.format(delete_webhook_resp.status_code, self.group.id))
        self.validate_headers(delete_webhook_resp.headers)
