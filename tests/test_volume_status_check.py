from datetime import datetime
from unittest import TestCase
from unittest.mock import patch  # Python 3

import botocore.session
from botocore.stub import Stubber, ANY
import pynagios

from volume_status_check import VolumeEventsCheck


class TestInstanceEvents(TestCase):
    def test_whole(self):
        describe_volumes_response = {
            "Volumes": [{
                "Attachments": [{
                    "AttachTime": "2017-03-09T08:45:51+00:00",
                    "Device": "/dev/sda1",
                    "InstanceId": "i-e8121e57783be97d",
                    "State": "attached",
                    "VolumeId": "vol-7e640bfda981b0cd599737d83b5a715c",
                    "DeleteOnTermination": True
                }],
                "AvailabilityZone": "us-east-1d",
                "CreateTime": "2017-03-09T08:45:51.735000+00:00",
                "Encrypted": False,
                "Size": 8,
                "SnapshotId": "snap-36f7cbe89a7f6041",
                "State": "in-use",
                "VolumeId": "vol-7e640bfda981b0cd599737d83b5a715c",
                "Iops": 100,
                "Tags": [],
                "VolumeType": "gp2",
                "MultiAttachEnabled": False
            }, {
                "Attachments": [{
                    "AttachTime": "2018-02-07T19:21:13+00:00",
                    "Device": "/dev/sda1",
                    "InstanceId": "i-a2dd316aad503999",
                    "State": "attached",
                    "VolumeId": "vol-98c679207680100da032523f0006bdcf",
                    "DeleteOnTermination": True
                }],
                "AvailabilityZone": "us-east-1d",
                "CreateTime": "2018-02-07T19:21:13.018000+00:00",
                "Encrypted": False,
                "Size": 30,
                "SnapshotId": "snap-81645b243521b82c",
                "State": "in-use",
                "VolumeId": "vol-98c679207680100da032523f0006bdcf",
                "Iops": 100,
                "Tags": [],
                "VolumeType": "gp2",
                "MultiAttachEnabled": False
            }]
        }

        describe_volume_status_response = {
            "VolumeStatuses": [{
                "Actions": [],
                "AvailabilityZone":
                "us-east-1d",
                "Events": [{
                    "EventType": "io-performance:degraded",
                    'Description': "Volume performance degraded",
                    'EventId': "id-abcedef",
                    'NotAfter': "2030-01-01T06:00:00.000Z",
                    'NotBefore': "2020-01-01T06:00:00.000Z",
                    'InstanceId': "i-e8121e57783be97d"
                }],
                "VolumeId": "vol-7e640bfda981b0cd599737d83b5a715c",
                "VolumeStatus": {
                    "Details": [{
                        "Name": "io-enabled",
                        "Status": "passed"
                    }, {
                        "Name": "io-performance",
                        "Status": "not-applicable"
                    }],
                    "Status": "ok"
                }
            }, {
                "Actions": [{
                    "Code": "code-test",
                    "Description": "Description of code-test",
                    "EventId": "id-fedcba",
                    "EventType": "event type"
                }],
                "AvailabilityZone": "us-east-1d",
                "Events": [],
                "VolumeId": "vol-98c679207680100da032523f0006bdcf",
                "VolumeStatus": {
                    "Details": [{
                        "Name": "io-enabled",
                        "Status": "passed"
                    }, {
                        "Name": "io-performance",
                        "Status": "not-applicable"
                    }],
                    "Status":
                    "ok"
                }
            }, {
                "Actions": [],
                "AvailabilityZone":
                "us-east-1d",
                "Events": [{
                    "EventType": "io-performance:degraded",
                    'Description': "Volume performance degraded",
                    'EventId': "id-abcedeffff",
                    'NotAfter': "2001-01-01T06:00:00.000Z",
                    'NotBefore': "2000-01-01T06:00:00.000Z",
                    'InstanceId': "i-e8121e57783be97d"
                }],
                "VolumeId":
                "vol-40a3b690a823989a",
                "VolumeStatus": {
                    "Details": [{
                        "Name": "io-enabled",
                        "Status": "passed"
                    }, {
                        "Name": "io-performance",
                        "Status": "not-applicable"
                    }],
                    "Status":
                    "ok"
                }
            }, {
                "Actions": [],
                "AvailabilityZone":
                "us-east-1d",
                "Events": [{
                    "EventType": "io-performance:degraded",
                    'Description': "Volume performance degraded",
                    'EventId': "id-abcedeffff",
                    'NotAfter': "2030-01-01T06:00:00.000Z",
                    'NotBefore': "2020-01-01T06:00:00.000Z",
                    'InstanceId': ""
                }],
                "VolumeId":
                "vol-13972a2f5a00e40b",
                "VolumeStatus": {
                    "Details": [{
                        "Name": "io-enabled",
                        "Status": "passed"
                    }, {
                        "Name": "io-performance",
                        "Status": "not-applicable"
                    }],
                    "Status":
                    "ok"
                }
            }, {
                "Actions": [{
                    "Code": "code-test",
                    "Description": "Description of code-test",
                    "EventId": "id-fedcba",
                    "EventType": "event type"
                }],
                "AvailabilityZone":
                "us-east-1d",
                "Events": [],
                "VolumeId":
                "vol-dcf1ea968ab3ad8c",
                "VolumeStatus": {
                    "Details": [{
                        "Name": "io-enabled",
                        "Status": "passed"
                    }, {
                        "Name": "io-performance",
                        "Status": "not-applicable"
                    }],
                    "Status":
                    "ok"
                }
            }]
        }

        check = VolumeEventsCheck()
        client = botocore.session.get_session().create_client('ec2')
        check.ec2_client = client
        stubber = Stubber(client)
        stubber.add_response('describe_volume_status',
                             describe_volume_status_response, {})

        # Each describe volumes *should* respect the VolumeId filter, but not harmless
        # if extra volumes are included in the response and greatly simplifies test setup.
        stubber.add_response('describe_volumes', describe_volumes_response, {
            'VolumeIds': ANY
        })
        stubber.add_response('describe_volumes', describe_volumes_response, {
            'VolumeIds': ANY
        })
        stubber.add_response('describe_volumes', describe_volumes_response, {
            'VolumeIds': ANY
        })
        stubber.add_response('describe_volumes', describe_volumes_response, {
            'VolumeIds': ANY
        })
        stubber.add_response('describe_volumes', describe_volumes_response, {
            'VolumeIds': ANY
        })

        with stubber:
            check.regioncheck('us-east-1')

        # One volume with Event in the past
        self.assertIn('degraded', check.infos[0])

        # One unattached volume with pending Event
        self.assertIn('degraded', check.warns[0])

        # One unattached volume with an Action
        self.assertIn('code-test', check.warns[1])

        # One attached volume with current/pending Event
        self.assertIn('degraded', check.criticals[0])

        # One attached volume with an Action
        self.assertIn('code-test', check.criticals[1])
