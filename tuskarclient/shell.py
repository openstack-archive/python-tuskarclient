#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Command-line interface to the Heat API.
"""

from __future__ import print_function

import logging
import logging.handlers
import sys
import tuskarclient.v1.argparsers

logger = logging.getLogger(__name__)


class TuskarShell(object):

    def __init__(self, raw_args):
        self.raw_args = raw_args

    def run(self):
        parser = tuskarclient.v1.argparsers.create_top_parser()
        args = parser.parse_args(self.raw_args)

        if args.help or not self.raw_args:
            parser.print_help()
            return 0

        self._ensure_auth_info(args)

    def _ensure_auth_info(self, args):
        '''Ensure that authentication information is provided. Two variants
        of authentication are supported:
        - provide username, password, tenant and auth url
        - provide token and tuskar url (or auth url instead of tuskar url)
        '''
        if not args.os_auth_token:
            if not args.os_username:
                raise UsageError("You must provide username via either "
                                 "--os-username or env[OS_USERNAME]")

            if not args.os_password:
                raise UsageError("You must provide password via either "
                                 "--os-password or env[OS_PASSWORD]")

            if not args.os_tenant_id and not args.os_tenant_name:
                raise UsageError("You must provide tenant via either "
                                 "--os-tenant-name or --os-tenant-id or "
                                 "env[OS_TENANT_NAME] or env[OS_TENANT_ID]")

            if not args.os_auth_url:
                raise UsageError("You must provide auth URL via either "
                                 "--os-auth-url or env[OS_AUTH_URL]")
        else:
            if not args.tuskar_url and not args.os_auth_url:
                raise UsageError("You must provide either "
                                 "--tuskar_url or --os_auth_url or "
                                 "env[TUSKAR_URL] or env[OS_AUTH_URL]")


class UsageError(Exception):
    pass


def main():
    logger.addHandler(logging.StreamHandler(sys.stderr))
    try:
        TuskarShell(sys.argv[1:]).run()
    except UsageError as e:
        print(e.message, file=sys.stderr)
    except Exception as e:
        logger.exception("Exiting due to an error:")
        sys.exit(1)


if __name__ == '__main__':
    main()
