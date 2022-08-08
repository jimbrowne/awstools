from unittest import TestCase

import botocore.session
from botocore.stub import Stubber

from availability_zones_check import AvailabilityZonesCheck


class TestInstanceEvents(TestCase):
    def test_whole(self):
        describe_az_response = {
            "AvailabilityZones": [
                {
                    "State": "impaired",
                    "OptInStatus": "opt-in-not-required",
                    "Messages": [],
                    "RegionName": "us-east-1",
                    "ZoneName": "us-east-1a",
                    "GroupName": "us-east-1",
                    "NetworkBorderGroup": "us-east-1",
                    "ZoneType": "availability-zone"
                },
                {
                    "State": "available",
                    "OptInStatus": "opt-in-not-required",
                    "Messages": [],
                    "RegionName": "us-east-1",
                    "ZoneName": "us-east-1b",
                    "GroupName": "us-east-1",
                    "NetworkBorderGroup": "us-east-1",
                    "ZoneType": "availability-zone"
                },
                ]
        }

        check = AvailabilityZonesCheck()
        client = botocore.session.get_session().create_client('ec2')
        check.ec2_client = client
        stubber = Stubber(client)
        stubber.add_response('describe_availability_zones', describe_az_response,
                             {})
        with stubber:
            check.regioncheck('us-east-1')

        self.assertEqual(check.responses[0], 'us-east-1:us-east-1a state impaired')
