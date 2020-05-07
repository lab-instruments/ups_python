import socket as s
import pickle as p
import netifaces as n


class DiscClient:

    def __init__(self):

        # Create UDP Socket Object
        self.sock = s.socket(s.AF_INET, s.SOCK_DGRAM)
        self.sock.setsockopt(s.SOL_SOCKET, s.SO_BROADCAST, 1)
        self.sock.settimeout(5)

        # Get Broadcast IP Address
        for iface in n.interfaces():
            if iface != 'lo':
                # print(n.ifaddresses(iface)[2][0])
                self.bcast_addr = n.ifaddresses(iface)[2][0]['broadcast']
                self.ip_addr = n.ifaddresses(iface)[2][0]['addr']
        self.port = 9989

    def run(self):

        # Report Client Start
        print('Start Client Socket...')

        # Generate Response Dictionary and Pickle
        req = {
            'TYPE': 'DEVICE_SEARCH_REQ',
            'DEVICE_TYPE': 'UPS'
        }
        req_p = p.dumps(req)

        # Try to Send Discovery
        try:

            # Send Data
            print('Send to {0}:{1}'.format(self.bcast_addr, self.port))
            self.sock.sendto(req_p, (self.bcast_addr, self.port))

            # Receive Data
            while True:
                d, a = self.sock.recvfrom(4096)

                # Report
                d_unpckl = p.loads(d)
                print('Got return from {0}'.format(a))
                print(d_unpckl)

        except Exception as e:
            print(e)
            print('Close Client Socket ...')
            self.sock.close()


if __name__ == "__main__":
    client = DiscClient()
    client.run()
