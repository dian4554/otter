"""
Contains the actual Klein app and base route handlers for the REST service.
"""
import json

from twisted.web.server import Request

from otter.rest.otterapp import OtterApp
from otter.rest.groups import OtterGroups
from otter.rest.webhooks import OtterExecute
from otter.rest.limits import OtterLimits
from otter.rest.history import OtterHistory

Request.defaultContentType = 'application/json'


class Otter(object):
    """
    Otter holds the Klein app and routes for the REST service.
    """
    app = OtterApp()

    def __init__(self, store, health_check_function=None):
        self.store = store
        self.health_check_function = health_check_function

    @app.route('/')
    def base(self, request):
        """
        base root route.

        :returns: Empty string
        """
        return ''

    @app.route('/v1.0/<string:tenant_id>/groups/', branch=True)
    def groups(self, request, tenant_id):
        """
        group routes delegated to OtterGroups.
        """
        return OtterGroups(self.store, tenant_id).app.resource()

    @app.route('/v1.0/execute/<string:capability_version>/<string:capability_hash>/')
    def execute(self, request, capability_version, capability_hash):
        """
        execute route handled by OtterExecute
        """
        return OtterExecute(self.store, capability_version,
                            capability_hash).app.resource()

    @app.route('/v1.0/<string:tenant_id>/limits')
    def limits(self, request, tenant_id):
        """
        return group limit maximums
        """
        return OtterLimits(self.store, tenant_id).app.resource()

    @app.route('/v1.0/<string:tenant_id>/history')
    def history(self, request, tenant_id):
        """
        return audit history
        """
        return OtterHistory(self.store, tenant_id).app.resource()

    @app.route('/health', methods=['GET'])
    def health_check(self, request):
        """
        Return whether health checks succeeded
        """
        request.setHeader('X-Response-Id', 'health_check')
        if self.health_check_function:
            return self.health_check_function().addCallback(json.dumps)

        return json.dumps({'healthy': True})
