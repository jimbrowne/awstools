Handy AWS tools from Jim Browne and 42Lines
===========================================

* server-certificate-check - Check server certificates in IAM for expiration and other issues.  Example output:

```
Certificate subject is C=US, ST=California, L=San Francisco, O=Example Corporation, OU=IT, CN=page.example.com
+ 508 days left before expiration (2013-10-26 23:59:59+00:00)
Chain certificate subject is C=US, O=VeriSign, Inc., OU=VeriSign Trust Network, OU=Terms of use at https://www.verisign.com/rpa (c)10, CN=VeriSign Class 3 International Server CA - G3
+ Certificate issuer matches chain subject

Certificate subject is C=US, ST=California, L=San Francisco, O=Example Corporation, OU=IT, CN=bonham.example.com
- Key length less than 2048 bits!
- Certificate is expired! 2012-02-22 23:59:59+00:00
Chain certificate subject is O=VeriSign Trust Network, OU=VeriSign, Inc., OU=VeriSign International Server CA - Class 3, OU=www.verisign.com/CPS Incorp.by Ref. LIABILITY LTD.(c)97 VeriSign
+ Certificate issuer matches chain subject

Certificate subject is C=US, ST=California, L=San Francisco, O=Example Corporation, OU=IT, CN=*.dev.example.com
+ 3 days left before expiration (2012-06-08 23:59:59+00:00)
Chain certificate subject is C=US, O=VeriSign, Inc., OU=VeriSign Trust Network, OU=Terms of use at https://www.verisign.com/rpa (c)10, CN=VeriSign Class 3 Secure Server CA - G3
+ Certificate issuer matches chain subject
```

* reserved-instances-check - Examine all running instances and current reserved instance purchases.  Suggest changes based on current data.  Optionally print detail about running instances and reserved instances.  Example output:

```
jbrowne@foo:~/awstools$ ./reserved-instances-check --quiet --itag=hostname --rdays=300

Advice based on current data:

1 candidate(s) for a reservation purchase in account main region us-east-1 zone us-east-1a
id i-deadbeef start 2011-12-16T02:58 (rockstar.dev.example.com)

1 unused reservation(s) in account main region us-east-1 zone us-east-1d
Use --rdetail to see reservation details

1 reservations(s) about to expire in account main region us-east-1 zone us-east-1d
id deadbeef-f000-baaa-dead-baaaaaaaaaaaa state active region RegionInfo:us-east-1 place us-east-1d type c1.xlarge count 1 start 2011-09-19T21:58 duration 365 elapsed 267 left 98

jbrowne@foo:~/awstools$ ./reserved-instances-check --itag=hostname
Account: main

Zone: us-east-1c
  Type m1.large Reservations 12 Instances 13 Delta 1

Zone: us-east-1a
  Type m1.large Reservations 93 Instances 100 Delta 7

Zone: us-east-1b
  Type c1.xlarge Reservations 21 Instances 20 Delta -1

[snipped advice section]

jbrowne@aauadmin02:~/awstools$ ~/boto-dev/bin/python ./reserved-instances-check --itag=hostname --rdetail
Account: main

Zone: us-east-1c
  Type m1.large Reservations 12 Instances 13 Delta 1
    Reservations:
      count 11 start 2011-09-19T22:15 duration 365 elapsed 266 left 99,
      count 1 start 2011-09-19T22:15 duration 1095 elapsed 266 left 829

Zone: us-east-1a
  Type m1.large Reservations 93 Instances 100 Delta 7
    Reservations:
      count 92 start 2011-09-19T22:11 duration 365 elapsed 267 left 98,
      count 1 start 2011-09-19T22:14 duration 1095 elapsed 266 left 829

Zone: us-east-1b
  Type c1.xlarge Reservations 21 Instances 20 Delta -1
    Reservations:
      count 21 start 2011-09-19T21:58 duration 365 elapsed 267 left 98

```
