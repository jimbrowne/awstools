from unittest import TestCase
from unittest.mock import patch  # Python 3

import botocore.session
from botocore.stub import Stubber
import pynagios

from instance_events_check import InstanceEventsCheck


class TestInstanceEvents(TestCase):
    @patch('instance_events_check.InstanceEventsCheck.fetch_instance_info')
    def test_whole(self, mock_fetch_instance):
        mock_fetch_instance.return_value = {
            'i-a5084746c687f663': {
                'info': '',
                'tags': {
                    'Name': 'machine1.example.com',
                    'customer': 'ACME',
                    'function': 'Coyote',
                    }
                },
            'i-f8ca35f013ebf7bb': {
                'info': '',
                'tags': {
                    'Name': 'machine2.example.com',
                    'customer': 'Weyland Yutani',
                    'function': 'Terraforming',
                    }
            }
        }

        describe_instance_status_response = {
            "InstanceStatuses": [{
                "AvailabilityZone": "us-east-1d",
                "InstanceId": "i-a5084746c687f663",
                'Events': [
                    {
                        'InstanceEventId': 'ident',
                        # 'instance-reboot'|'system-reboot'|'system-maintenance'|
                        # 'instance-retirement'|'instance-stop'
                        'Code'	    : 'system-reboot',
                        'Description': 'scheduled reboot',
                        'NotAfter': '2022-05-24T06:00:00.000Z',
                        'NotBefore': '2022-05-20T06:00:00.000Z',
                        'NotBeforeDeadline': '2022-05-23T06:00:00.000Z',
                    },
                ],
                "InstanceState": {
                    "Code": 16,
                    "Name": "running"
                },
                "InstanceStatus": {
                    "Details": [{
                        "Name": "reachability",
                        "Status": "passed"
                    }],
                    "Status": "ok"
                },
                "SystemStatus": {
                    "Details": [{
                        "Name": "reachability",
                        "Status": "passed"
                    }],
                    "Status": "ok"
                }
            }, {
                "AvailabilityZone": "us-east-1d",
                "InstanceId": "i-f8ca35f013ebf7bb",
                'Events': [
                    {
                        'InstanceEventId': 'ident',
                        # 'instance-reboot'|'system-reboot'|'system-maintenance'|
                        # 'instance-retirement'|'instance-stop'
                        'Code'	    : 'instance-stop',
                        'Description': 'Completed The instance is running on degraded hardware',
                        'NotAfter': '2022-05-24T06:00:00.000Z',
                        'NotBefore': '2022-05-20T06:00:00.000Z',
                        'NotBeforeDeadline': '2022-05-23T06:00:00.000Z',
                    },
                ],
                "InstanceState": {
                    "Code": 16,
                    "Name": "running"
                },
                "InstanceStatus": {
                    "Details": [{
                        "Name": "reachability",
                        "Status": "passed"
                    }],
                    "Status": "ok"
                },
                "SystemStatus": {
                    "Details": [{
                        "Name": "reachability",
                        "Status": "passed"
                    }],
                    "Status": "ok"
                }
            }]
        }

        check = InstanceEventsCheck()
        client = botocore.session.get_session().create_client('ec2')
        check.ec2_client = client
        stubber = Stubber(client)
        stubber.add_response('describe_instance_status', describe_instance_status_response,
                             {})
        with stubber:
            with patch('sys.argv', ['--tags', 'Name']):
                check.regioncheck('us-east-1')

        self.assertEqual(check.responses[0].status, pynagios.WARNING)
        self.assertIn('scheduled reboot', check.responses[0].message)


    @patch('instance_events_check.InstanceEventsCheck.fetch_instance_info')
    def test_no_instances(self, mock_fetch_instance):
        mock_fetch_instance.return_value = {}

        check = InstanceEventsCheck()
        check.regioncheck('us-east-1')

        self.assertEqual(check.responses, [])
