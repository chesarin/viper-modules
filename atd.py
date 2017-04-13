try:
    import requests
    HAVE_REQUESTS = True
except ImportError:
    HAVE_REQUESTS = False

import base64
from viper.common.abstracts import Module
from viper.core.session import __sessions__


class Atd(Module):
    cmd = 'atd'
    description = 'This module allow interaction with McAfee ATD'
    authors = ['Antonio Cesar Vargas']

    def __init__(self):
        super(Atd, self).__init__()
        self.parser.add_argument(
            '-H', '--host', default='localhost', help='Specify a host. Default: localhost')
        self.parser.add_argument(
            '-u', '--username', default='admin', help='Specify a user name. Default: admin')
        self.parser.add_argument(
            '-p', '--password', default='password', help='Specify a password. Default: password')

    def run(self):
        super(Atd, self).run()
        if self.args is None:
            return

        if not __sessions__.is_set():
            self.log('error', "No sessions opened")
            return
        headers = {'Accept': 'application/vnd.ve.v1.0+json',
                   'Content-Type': 'application/json'}

        host = self.args.host
        username = self.args.username
        password = self.args.password

        def atd_connect(host, username, password, headers):
            print 'Inside of ATD connect'
            credentials = '%s:%s' % (username, password)
            credentials_b64 = base64.b64encode(credentials)
            headers['VE-SDK-API'] = credentials_b64
            url = 'https://%s/php/session.php' % (host)
            print url
            try:
                print 'inside of try block'
                r = requests.get(url, headers=headers,
                                 verify=False, timeout=0.001)
                self.log('info', "testing connection to '{0}'.".format(url))
                print 'done with try block'
            except requests.ConnectionError:
                print 'inside of except 1 block'
                self.log(
                    'error', "Unable performing request at '{0}'.".format(url))
                print 'done with first except block'
                return
            except Exception as e:
                print 'inside of except 2 block'
                self.log(
                    'error', "Failed performing request at '{0}': {1}".format(url, e))
                print 'done with second except block'
                return
            self.log('info', "Done testing connection")
            print 'done with atd_connect and returning r'
            return r

        def atd_disconnect(host, session, userid, headers):
            logout_header = '%s:%s' % (session, userid)
            logout_header_base64 = base64.b64decode(logout_header)
            headers['VE-SDK-API'] = logout_header_base64
            url = 'https://%s/php/session.php' % (host)
            try:
                r = requests.delete(url, headers=headers, verify=False)

            except requests.ConnectionError:
                self.log(
                    'error', "Unable performing request at '{0}'.".format(url))
                return
            except Exception as e:
                self.log(
                    'error', "Failed performing request at '{0}': {1}".format(url, e))
            return r.json()

        print("Host: %s Username: %s Password: %s") % (
            host, username, password)
        print ("Starting Module")
        try:
            login = atd_connect(host, username, password, headers)
        except:
            return
        print login.status_code
        # session = login['results']['session']
        # userid = login['results']['userId']
        # logout = atd_disconnect(host, session, userid, headers)
        # if logout['results']['success']:
        #     print 'completed successfully'
