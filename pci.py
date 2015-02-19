import copy
from requests import ConnectionError
import tortilla
from requests.auth import _basic_auth_str

class PCI_API(object):
    """ PCI wrapper over tortilla wrapper
        over requests wrapper over API HTTP calls!
    """

    tortilla_defaults = {
        'parent': None,
        'params': {},            # query string params that need to be passed always
        'headers': {},           # headers
        'debug': None,
        'silent': False,
        'extension': None,
        'format': None,
        'cache_lifetime': None,
        'cache': None,
        'delay': 0.
    }

    api_defaults = {
        'base_endpoint': 'http://api3.openpolis.it'
    }

    def __init__(self, **args):
        defaults = dict(self.api_defaults.items() + self.tortilla_defaults.items())
        defaults.update(args)

        self.__dict__.update(copy.deepcopy(defaults))

        self.api = self.__tortilla_api()


    def __str__(self):
        return str(self.__url()+'/'+self.api_version)

    def __getattr__(self, key):
        return self.api.__call__(key)

    def get_url(self):
        url = '{self.base_endpoint}'.format(self=self)
        return url

    def get_api_version(self):
        return self.api_version

    def is_online(self):
        try:
            # protocol ping
            self.api.get()
        except ConnectionError, e:
            return False
        else:
            return True

    def __tortilla_api(self):
        url = self.get_url()
        if 'api_key' in self.__dict__:
            self.headers.update({'apikey': self.api_key})
        elif 'user' in self.__dict__ and 'password' in self.__dict__:
            self.headers.update({
                'Authentication': _basic_auth_str(
                    self.user, self.password
                )
            })
        else:
            pass

        args = {}
        for a in self.tortilla_defaults.keys():
            args[a] = self.__dict__[a]
        return tortilla.wrap(url, **args)



class Popit(PCI_API):

    api_defaults = {
        'instance': 'openpolistest',
        'host': 'popit.mysociety.org',
        'version': 'v0.1',
        'user': None,
        'password': None,
        'api_key': None,
    }

    def get_url(self):
        url = 'http://{self.instance}.{self.host}/api/{self.version}'.format(self=self)
        return url


class Mapit(PCI_API):
    api_defaults = {
        'base_endpoint': 'http://global.mapit.mysociety.org/',
    }

    def is_online(self):
        try:
            # the list of generations
            # is the closest thing to a protocol ping
            # for the Mapit API
            self.api.generations.get()
        except ConnectionError, e:
            return False
        else:
            return True

