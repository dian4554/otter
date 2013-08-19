"""
Test to create and verify the created group in bobby.
"""
from test_repo.bobby.fixtures import BobbyFixture


class CreateGroupTest(BobbyFixture):

    """
    Verify create group in bobby.
    """

    def test_create_group_response_status_and_headers(self):
        """
        Create a group in bobby with a given group_id, notification
        and notification plan, and verify the headers and response code is 201.
        """
        create_group_response = self.bobby_client.create_group(
            group_id=self.group_id,
            notification=self.notification,
            notification_plan=self.notification_plan)
        self.assertEquals(create_group_response.status_code, 201,
                          msg='The response code for create  group in bobby '
                          'resulted in {0}'.format(create_group_response.status_code))
        self.validate_headers(create_group_response.headers)
        self.resources.add(self.group_id,
                           self.bobby_client.delete_group)

    def test_create_group_response(self):
        """
        Create a group in bobby with a given group_id, notification
        and notification plans, and verify the response object.
        """
        create_group = self.bobby_client.create_group(
            group_id=self.group_id,
            notification=self.notification,
            notification_plan=self.notification_plan).entity
        self.resources.add(self.group_id,
                           self.bobby_client.delete_group)
        self.assert_create_bobby_group_feilds(create_group)

    # def test_create_group_without_group_id(self):
    #     """
    #     Create a group in bobby without a group_id, and verify the
    #     response code is 400.
    #     """
    #     create_group_response = self.bobby_client.create_group(
    #         group_id=None,
    #         notification=self.notification,
    #         notification_plan=self.notification_plan)
    #     self.assertEquals(create_group_response.status_code, 400,
    #                       msg='The response code for create  group in bobby '
    #                       'resulted in {0}'.format(create_group_response.status_code))

    # def test_create_group_without_notification(self):
    #     """
    #     Create a group in bobby without a notification, and verify the
    #     response code is 400.
    #     """
    #     create_group_response = self.bobby_client.create_group(
    #         group_id=self.group_id,
    #         notification=None,
    #         notification_plan=self.notification_plan)
    #     self.assertEquals(create_group_response.status_code, 400,
    #                       msg='The response code for create  group in bobby '
    #                       'resulted in {0}'.format(create_group_response.status_code))
    #     self.resources.add(self.group_id,
    #                        self.bobby_client.delete_group)

    # def test_create_group_without_notification_plan(self):
    #     """
    #     Create a group in bobby without a notification plan, and verify the
    #     response code is 400.
    #     """
    #     create_group_response = self.bobby_client.create_group(
    #         group_id=self.group_id,
    #         notification=self.notification,
    #         notification_plan=None)
    #     self.assertEquals(create_group_response.status_code, 400,
    #                       msg='The response code for create  group in bobby '
    #                       'resulted in {0}'.format(create_group_response.status_code))
    #     self.resources.add(self.group_id,
    #                        self.bobby_client.delete_group)

    # def test_create_group_without_notification_notification_plans(self):
    #     """
    #     Create a group in bobby without a notification and notification plan,
    #     and verify the response code is 400.
    #     """
    #     create_group_response = self.bobby_client.create_group(
    #         group_id=self.group_id,
    #         notification=None,
    #         notification_plan=None)
    #     self.assertEquals(create_group_response.status_code, 400,
    #                       msg='The response code for create  group in bobby '
    #                       'resulted in {0}'.format(create_group_response.status_code))

    # def test_create_group_without_notification_plan_as_dict(self):
    #     """
    #     Create a group in bobby with a notification plan as a dict, and verify the
    #     response code is 400.
    #     """
    #     create_group_response = self.bobby_client.create_group(
    #         group_id=self.group_id,
    #         notification=self.notification,
    #         notification_plan={'label': 'TestNP', 'critical_state': ['test']})
    #     self.assertEquals(create_group_response.status_code, 400,
    #                       msg='The response code for create  group in bobby '
    #                       'resulted in {0}'.format(create_group_response.status_code))
    #     self.resources.add(self.group_id,
    #                        self.bobby_client.delete_group)