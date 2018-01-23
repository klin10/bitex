"""Bitstamp REST API backend.

Documentation available here:
    https://www.bitstamp.net/api/
"""
# Import Built-ins
import logging
import hashlib

# Import Third-Party

# Import Homebrew
from bitex.api.REST import RESTAPI

# Init Logging Facilities
log = logging.getLogger(__name__)


class OKCoinREST(RESTAPI):
    """OKCoin REST API class."""

    def __init__(self, key=None, secret=None, version=None, config=None,
                 addr=None, timeout=5):
        """Initialize the class instance."""
        version = 'v1' if not version else version
        addr = 'https://www.okcoin.com/api' if not addr else addr
        super(OKCoinREST, self).__init__(addr=addr, version=version,
                                         key=key, secret=secret, config=config,
                                         timeout=timeout)

    def sign_request_kwargs(self, endpoint, **kwargs):
        """Sign the request.

        OKCoin requires the parameters in the signature string and url to
        be appended in alphabetical order. This means we cannot rely on urllib's
        encode() method and need to do this ourselves.
        """
        req_kwargs = super(OKCoinREST, self).sign_request_kwargs(endpoint,
                                                                 **kwargs)
        # Prepare payload arguments
        payload = req_kwargs.pop('params', {})
        payload['api_key'] = self.key

        # Create the signature from payload and add it to params
        encoded_params = '&'.join([k + '=' + str(payload[k]) for k in sorted(payload.keys())])
        sign = encoded_params + '&secret_key=' + self.secret
        hash_sign = hashlib.md5(sign.encode('utf-8')).hexdigest().upper()
        payload['sign'] = hash_sign
        req_kwargs['data'] = payload
        if kwargs['method'] == 'POST':
            req_kwargs['headers'] = {"Content-Type": 'application/x-www-form-urlencoded'}
            req_kwargs['data'] = encoded_params

        req_kwargs['url'] = self.generate_url(self.generate_uri(endpoint))
        return req_kwargs
