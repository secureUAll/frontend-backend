# Certificates for SSL



As our VM is not exposed to the outside of the UA network, we can't generate a free SSL certificate with Let's Encrypt (as it can not validate that our server exists). As the solution is a paid certificate, while the project is in development we are going to use a certificate signed by a CA created by us.

> Followed the tutorial on https://www.ibm.com/docs/en/runbook-automation?topic=deployment-generate-install-signed-rba-server-certificate



## Install the Root CA Certificate on your browser

As we created a custom CA it is not expected for browsers to trust it. To bypass this problem, just add the root CA certificate as a trusted CA on your browser settings.

<u>It's location is `<frontend-backend-repo>/ssl/internalca/rootCACert.pem`</u>.

Tutorials for:

- [Firefox](https://portswigger.net/burp/documentation/desktop/getting-started/proxy-setup/certificate/firefox)
- [Chrome](https://support.securly.com/hc/en-us/articles/206081828-How-to-manually-install-the-Securly-SSL-certificate-in-Chrome)
- [Opera](https://wiki.wmtransfer.com/projects/webmoney/wiki/Installing_root_certificate_in_Opera)

