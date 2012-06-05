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
