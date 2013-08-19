"""
Test delete group in bobby
"""
from test_repo.bobby.fixtures import BobbyGroupFixture
from cloudcafe.common.tools.datagen import rand_name


class GetGroupTest(BobbyGroupFixture):

    """
    Tests for delete group in bobby
    """

    @classmethod
    def setUpClass(cls):
        """
        Creates a group with the given group id
        """
        cls.group_id_temp = rand_name('012345678-2222-4543-85bc-')
        super(GetGroupTest, cls).setUpClass(group_id=cls.group_id_temp)

    def test_delete_group(self):
        """
        Delete the group and verify the response code is 204.
        """
        delete_response = self.bobby_client.delete_group(self.group_id_temp)
        self.asserEquals(delete_response.status_code, 204,
            msg='Deleteing a group resulted in {0} as against 204'.format(
                delete_response.status_code))