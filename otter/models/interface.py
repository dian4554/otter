"""
Interface to be used by the scaling groups engine
"""

from zope.interface import Interface, Attribute


class NoSuchScalingGroupError(Exception):
    """
    Error to be raised when attempting operations on a scaling group that
    does not exist.
    """
    def __init__(self, tenant_id, group_id):
        super(NoSuchScalingGroupError, self).__init__(
            "No such scaling group {uuid!s} for tenant {tenant!s}".format(
                tenant=tenant_id, uuid=group_id))


class NoSuchEntityError(Exception):
    """
    Error to be raised when attempting operations on an entity that does not
    exist.
    """
    pass


class NoSuchPolicyError(Exception):
    """
    Error to be raised when attempting operations on an policy that does not
    exist.
    """
    pass


class IScalingGroup(Interface):
    """
    Scaling group record
    """
    uuid = Attribute("UUID of the scaling group - immutable.")

    def view_manifest():
        """
        The manifest contains everything required to configure this scaling:
        the config, the launch config, and all the scaling policies.

        :return: a dictionary with 3 keys: ``groupConfiguration`` containing
            the group configuration dictionary, ``launchConfiguration``
            containing the launch configuration dictionary, and
            ``scalingPolicies`` containing a dictionary of the scaling policies
            mapped to their UUIDs
        :rtype: ``dict``
        """
        pass

    def view_config():
        """
        :return: a view of the config, as specified by
            :data:`otter.json_schema.scaling_group.config`
        :rtype: a :class:`twisted.internet.defer.Deferred` that fires with
            ``dict``
        """
        pass

    def view_launch_config():
        """
        :return: a view of the launch config, as specified by
            :data:`otter.json_schema.scaling_group.launch_config`
        :rtype: a :class:`twisted.internet.defer.Deferred` that fires with
            ``dict``
        """
        pass

    def view_state():
        """
        The state of the scaling group consists of a mapping of entity id's to
        entity links for the current entities in the scaling group, a mapping
        of entity id's to entity links for the pending entities in the scaling
        group, the desired steady state number of entities, and a boolean
        specifying whether scaling is currently paused.

        The entity links are in JSON link format.

        :return: a view of the state of the scaling group in the form::

        {
          "active": {
            "{instanceId1}": [
              {
                "href": "https://dfw.servers.api.rackspacecloud.com/v2/010101/servers/{instanceId1}",
                "rel": "self"
              },
              {
                "href": "https://dfw.servers.api.rackspacecloud.com/v2/010101/servers/{instanceId1}",
                "rel": "bookmark"
              }
            ],
            "{instanceId2}": [
              {
                "href": "https://dfw.servers.api.rackspacecloud.com/v2/010101/servers/{instanceId2},
                "rel": "self"
              },
              {
                "href": "https://dfw.servers.api.rackspacecloud.com/v2/010101/servers/{instanceId2}"
                "rel": "bookmark"
              }
            ]
          },
          "pending": {
            "{instanceId3}": [
              {
                "href": "https://dfw.servers.api.rackspacecloud.com/v2/010101/servers/{instanceId3},
                "rel": "self"
              },
              {
                "href": "https://dfw.servers.api.rackspacecloud.com/v2/010101/servers/{instanceId3}"
                "rel": "bookmark"
              }
            ]
          },
          "steadyState": 3,
          "paused": false
        }

        :rtype: a :class:`twisted.internet.defer.Deferred` that fires with
            ``dict``
        """
        pass

    def update_config(config):
        """
        Update the scaling group configuration paramaters based on the
        attributes in ``config``.  This can update the already-existing values,
        or just overwrite them - it is up to the implementation.

        :param config: Configuration data in JSON format, as specified by
            :data:`otter.json_schema.scaling_group.config`
        :type config: ``dict``

        :return: a :class:`twisted.internet.defer.Deferred` that fires with None
        """
        pass

    def update_launch_config(launch_config):
        """
        Update the scaling group launch configuration parameters based on the
        attributes in ``launch_config``.  This can update the already-existing
        values, or just overwrite them - it is up to the implementation.

        :param launch_config: launch config data in JSON format, as specified
            by :data:`otter.json_schema.scaling_group.launch_config`
        :type launch_config: ``dict``

        :return: a :class:`twisted.internet.defer.Deferred` that fires with None
        """
        pass

    def set_steady_state(steady_state):
        """
        The steady state represents the number of entities - defaults to the
        minimum. This number represents how many entities _should_ be
        currently in the system to handle the current load. Its value is
        constrained to be between ``min_entities`` and ``max_entities``,
        inclusive.

        :param steady_state: The new value for the desired number of entities
            in steady state.  If this value is greater than ``max_entities``,
            the value will be set to ``max_entities``.  Similarly, if this
            value is less than ``min_entities``, the value will be set to
            ``min_entities``.
        :type steady_state: ``int``

        :return: a :class:`twisted.internet.defer.Deferred` that fires with None
        """
        pass

    def bounce_entity(entity_id):
        """
        Rebuilds an entity given by the entity ID.  This essentially deletes
        the given entity and a new one will be rebuilt in its place.

        :param entity_id: the uuid of the entity to delete
        :type entity_id: ``str``

        :return: a :class:`twisted.internet.defer.Deferred` that fires with None

        :raises: NoSuchEntityError if the entity is not a member of the scaling
            group
        """
        pass

    def create_policy(data):
        """
        Create a set of new scaling policies.

        :param data: the details of the scaling policy in JSON format
        :type data: ``dict`` of ``dict``

        :return: the UUID and full details of the newly created scaling policies
            as specified by :data:`otter.json_schema.scaling_group.policy_list`
        """
        pass

    def update_policy(policy_id, data):
        """
        Updates an existing policy with the data given.

        :param policy_id: the uuid of the entity to update
        :type policy_id: ``str``

        :param data: the details of the scaling policy in JSON format
        :type data: ``dict``

        :return: a UUID with policy, as specified by
            :data:`otter.json_schema.scaling_group.policy_list`
        :rtype: a :class:`twisted.internet.defer.Deferred` that fires with
            ``dict``
        """
        pass

    def list_policies():
        """
        :return: a dict of the policies, as specified by
            :data:`otter.json_schema.scaling_group.policy_list`
        :rtype: a :class:`twisted.internet.defer.Deferred` that fires with
            ``dict``
        """
        pass

    def get_policy(policy_id):
        """
        :return: a policy, as specified by
            :data:`otter.json_schema.scaling_group.policy`
        :rtype: a :class:`twisted.internet.defer.Deferred` that fires with
            ``dict``
        """
        pass

    def delete_policy(policy_id):
        """
        Delete the scaling policy

        :param policy_id: the uuid of the policy to be deleted
        :type policy_id: ``str``

        :return: a :class:`twisted.internet.defer.Deferred` that fires with None

        :raises: :class:`NoSuchPolicyError` if the policy id does not exist
        """
        pass


class IScalingGroupCollection(Interface):
    """
    Collection of scaling groups
    """
    def create_scaling_group(tenant_id, config, launch, policies=None):
        """
        Create scaling group based on the tenant id, the configuration
        paramaters, the launch config, and optional scaling policies.

        Validation of the config, launch config, and policies should have
        already happened by this point (whether they refer to real other
        entities, that the config's ``maxEntities`` should be greater than or
        equal to ``minEntities``, etc.).

        On successful creation, of a scaling group, the minimum entities
        parameter should immediately be enforced.  Therefore, if the minimum
        is greater than zero, that number of entities should be created after
        scaling group creation.

        :param tenant_id: the tenant ID of the tenant the scaling group
            belongs to
        :type tenant_id: ``str``

        :param config: scaling group configuration options in JSON format, as
            specified by :data:`otter.json_schema.scaling_group.config`
        :type data: ``dict``

        :param launch: scaling group launch configuration options in JSON
            format, as specified by
            :data:`otter.json_schema.scaling_group.launch_config`
        :type data: ``dict``

        :param policies: list of scaling group policies, each one given as a
            JSON blob as specified by
            :data:`otter.json_schema.scaling_group.scaling_policy`
        :type data: ``list`` of ``dict``

        :return: uuid of the newly created scaling group
        :rtype: a :class:`twisted.internet.defer.Deferred` that fires with `str`
        """
        pass

    def delete_scaling_group(tenant_id, scaling_group_id):
        """
        Delete the scaling group

        :param tenant_id: the tenant ID of the scaling groups
        :type tenant_id: ``str``

        :param scaling_group_id: the uuid of the scaling group to delete
        :type scaling_group_id: ``str``

        :return: a :class:`twisted.internet.defer.Deferred` that fires with None

        :raises: :class:`NoSuchScalingGroupError` if the scaling group id
            doesn't exist for this tenant id
        """
        pass

    def list_scaling_groups(tenant_id):
        """
        List the scaling groups for this tenant ID

        :param tenant_id: the tenant ID of the scaling groups
        :type tenant_id: ``str``

        :return: a list of scaling groups
        :rtype: a :class:`twisted.internet.defer.Deferred` that fires with a
            ``list`` of :class:`IScalingGroup` providers
        """
        pass

    def get_scaling_group(tenant_id, scaling_group_id):
        """
        Get a scaling group model

        Will return a scaling group even if the ID doesn't exist,
        but the scaling group will throw exceptions when you try to do things
        with it.

        :param tenant_id: the tenant ID of the scaling groups
        :type tenant_id: ``str``

        :return: scaling group model object
        :rtype: :class:`IScalingGroup` provider (no
            :class:`twisted.internet.defer.Deferred`)
        """
        pass
