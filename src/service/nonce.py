from bs4 import BeautifulSoup
from exploits.exploit import AbstractExploit


class Nonce(object):
    def __init__(self, connection, hostname):
        self.connection = connection
        self.hostname = hostname

    def get_nonce(self, exploit: AbstractExploit, headers):
        nonce = None
        if exploit.get_nonce_url():
            response = self.connection.request(
                hostname=self.hostname + exploit.get_nonce_url(),
                data='',
                headers=headers
            )

            if response is not None:
                soup = BeautifulSoup(response)
                try:
                    nonce = soup.find('input', {'id': '_wpnonce'}).get('value')
                except:
                    pass

        return nonce
