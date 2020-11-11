import socket as s
import pickle as p
import netifaces as n
import logging

# Setup Log Handler
log = logging.getLogger(__name__)

# ------------------------------------------------------------------------------
#  UPS Discovery Client Class
# ------------------------------------------------------------------------------
class DiscoveryClient:

    # --------------------------------------------------------------------------
    #  Init Method
    # --------------------------------------------------------------------------
    def __init__(self, to=5):

        # Log Start
        log.info('Start Discovery Server')

        # ----------------------------------------------------------------------
        #  Create UDP Socket Object, Enable Broadcast and Set Timeout to 5
        # ----------------------------------------------------------------------
        self.sock = s.socket(s.AF_INET, s.SOCK_DGRAM)
        self.sock.setsockopt(s.SOL_SOCKET, s.SO_BROADCAST, 1)
        self.sock.settimeout(to)

        # ----------------------------------------------------------------------
        #  Get Broadcast IP Address
        #    Get list of interfaces, filter out lo and get the broadcast and
        #    local address.
        # ----------------------------------------------------------------------
        self.bcast_addr = []
        self.ip_addr = []
        for iface in n.interfaces():

            if iface != 'lo':
                # Parse Broadcast and Local Address
                try:
                    self.bcast_addr.append(n.ifaddresses(iface)[2][0]['broadcast'])
                    self.ip_addr.append(n.ifaddresses(iface)[2][0]['addr'])

                except:
                    log.info('Interface {0} does not have IP/BCAST address')

        # Report Address
        log.info('Register broadcast address :  {0}'.format(self.bcast_addr))
        log.info('Register IP address :  {0}'.format(self.ip_addr))

        # Set Port to 9989
        self.port = 9989

    # --------------------------------------------------------------------------
    #  Run Method
    #    Primary method to discover UPS devices on the local network.
    # --------------------------------------------------------------------------
    def run(self):

        # Report Client Start
        log.info('Send discovery packet')

        # Generate Response Dictionary and Pickle
        req = {
            'TYPE': 'DEVICE_SEARCH_REQ',
            'DEVICE_TYPE': 'UPS'
        }
        req_p = p.dumps(req)

        # Return Variable
        ret = []

        # ----------------------------------------------------------------------
        #  Primary Discovery Loop
        #    1. Send discovery packet to broadcast address.
        #    2. Listen in a loop and parse responses until timeout exception:
        #      a. Listen for response.
        #      b. On response, attempt to unpickle binary data.  Build list on
        #         successful unpickle.
        #      c. Return list after socket timeout exception.
        # ----------------------------------------------------------------------
        try:

            # Send Data
            log.info('Send to discovery packet to {0}:{1}'.format(self.bcast_addr, self.port))

            # Send to All Addresses
            for addr in self.bcast_addr:
                self.sock.sendto(req_p, (addr, self.port))
            # self.sock.sendto(req_p, (self.bcast_addr[1], self.port))

            # Receive Data
            while True:

                # Receive Data
                d, a = self.sock.recvfrom(4096)

                # Unpickle payload
                d_unpckl = p.loads(d)
                log.info('Got return from {0}; Data {1}'.format(a, d_unpckl))
                ret.append(a[0])

        except Exception as e:
            log.info(e)
            pass

        # Done .. Return
        return ret


if __name__ == "__main__":

    # Setup Logging
    logging.basicConfig(
                        format='%(module)s.%(funcName)s: %(message)s',
                        level=logging.DEBUG
                       )

    # Setup Discovery Client Object with Timeout 1
    client = DiscoveryClient(1)

    # Run Discovery Client
    addr = client.run()

    if addr:
        print(addr[0])
    else:
        print('')
