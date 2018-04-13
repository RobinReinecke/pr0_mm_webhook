"""
Mini pr0gramm.com API in Python 3 by Robinatus.
"""

import json
import requests

class Api:
    """
    API Class for Requests
    """
    def __init__(self, EnableSFW, EnableNSFW, EnableNSFL, EnableTop):
        """
        Initialize the API Class.

        If all Filters are disabled, the SFW Filter auto-enables.    
        
        Arguments:
            EnableSFW {bool} -- Enable SFW Filter
            EnableNSFW {bool} -- Enable NSFW Filter
            EnableNSFL {bool} -- Enable NSFL Filter
            EnableTop {bool} -- Enable Top
        """

        self._api_url = "http://pr0gramm.com/api/"
        self.SFW = EnableSFW
        self.NSFW = EnableNSFW
        self.NSFL = EnableNSFL
        self.Top = EnableTop 

    @property
    def _flags(self):
        """
        Flags for Request
        
        Returns:
            int -- Flags value
        """
        flags = int(self.SFW) * 1 + int(self.NSFW) * 2 + int(self.NSFL) * 4
        return flags  if flags > 0 else 1

    def get(self):
        """
        Get newest items.

        Returns:
            dict -- Items
        """

        # Set up the arguments for request
        args = ({
            'flags': self._flags,
            'promoted': int(self.Top),
        })
        
        # Make request and verify success
        response = requests.get(self._api_url + 'items/get', params= args)
        response.raise_for_status()
        # Return items
        return response.json()["items"]

    def info(self, id):
        """Load informations for an item
        
        Arguments:
            id {int} -- Item ID
        
        Returns:
            dict -- Item Informations
        """

        # Set up the arguments for request 
        args = ({
             'itemId': id
        })

        response = requests.get(self._api_url + 'items/info', params= args)
        response.raise_for_status()
        return response.json()
