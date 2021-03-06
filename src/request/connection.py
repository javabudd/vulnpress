import urllib.request
import urllib.error
import urllib.parse
import http.client
import socket
import http.cookiejar

from bs4 import BeautifulSoup


class Connection:
    def __init__(self):
        self.cookieJar = http.cookiejar.CookieJar()

    def request(
        self,
        hostname,
        data,
        headers,
        nonce=None,
        urlencode=False,
        method='GET',
        encode='utf-8',
        decode='iso-8859-1'
    ):
        try:
            if urlencode:
                data = urllib.parse.urlencode(eval(data))
            if nonce is not None:
                data += '&_wpnonce=' + nonce

            request = urllib.request.Request(
                hostname,
                data=data.encode(encode, 'ignore'),
                headers=headers,
                method=method
            )

            self.cookieJar.add_cookie_header(request)
            response = urllib.request.urlopen(request, timeout=10)
            response_decoded = response.read().decode(decode, 'ignore')
            response.close()

            return response_decoded

        except urllib.request.HTTPError:
            return None

    def login(self, hostname, username, password):
        # Attempt login
        is_logged_in = False
        opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cookieJar)
        )
        url = hostname + '/wp-login.php'
        data = {'log': username, 'pwd': password, 'submit': 'Log In'}
        data = urllib.parse.urlencode(data)
        opener.open(url, data.encode('utf-8'))

        # Verify successful login
        response = opener.open(hostname)
        soup = BeautifulSoup(response)
        atags = soup.find_all('a')
        if atags:
            for atag in atags:
                hrefs = atag.get('href')
                if hostname + '/wp-login.php?action=logout' in hrefs:
                    is_logged_in = True

        return is_logged_in

    @staticmethod
    def verify_socket(hostname):
        verified = True
        try:
            port = 80
            if hostname[:7] == "http://":
                hostname = hostname[7:]
            elif hostname[:8] == "https://":
                hostname = hostname[8:]
                port = 443

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            s.connect((hostname, port))
        except socket.error:
            verified = False

        return verified

    @staticmethod
    def reset_session():
        cj = http.cookiejar.CookieJar()
        # Clear previous cookies
        cj.clear()
        # Clean the temp folder
        urllib.request.urlcleanup()

    @staticmethod
    def verify_url(hostname):
        try:
            return urllib.request.urlopen(hostname, timeout=10)
        except urllib.request.URLError:
            return False
