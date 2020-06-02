import requests
import enum
import json as j


# ------------------------------------------------------------------------------
#  Enumeration for Modes
# ------------------------------------------------------------------------------
class Modes(enum.Enum):
    IDLE = 0
    LOOP_BACK = 1
    DAC_TEST = 2
    RUN = 3

# ------------------------------------------------------------------------------
#  UPS REST API Interface Class
# ------------------------------------------------------------------------------
class UpsApi:

    def __init__(self):

        # Class Enabled Flag
        self.en = 0

        # Routes
        self.routes_led = ''
        self.routes_check = ''

        # UPS Server Location
        self.ups_server_ip = ''
        self.ups_server_port = 0

    # --------------------------------------------------------------------------
    #  Set Path Method
    #    This method sets the host and port for the UPS device.
    # --------------------------------------------------------------------------
    def connect(self, host, port=8088):

        # Enable Class
        self.en = 1

        # Save UPS IP/Port
        self.ups_server_ip = host
        self.ups_server_port = port

        # Generate Routers
        self._generate_routes()

    # --------------------------------------------------------------------------
    #  Generate Routes Internal Method
    #    This method generates the route paths.
    # --------------------------------------------------------------------------
    def _generate_routes(self):

        # LED Route
        self.routes_led = 'http://{0}:{1}/led'.format(
                                                      self.ups_server_ip,
                                                      self.ups_server_port
                                                     )

        # Check Route
        self.routes_check = 'http://{0}:{1}/check'.format(
                                                          self.ups_server_ip,
                                                          self.ups_server_port
                                                         )

        # DAC0 Route
        self.routes_dac0 = 'http://{0}:{1}/dac0'.format(
                                                        self.ups_server_ip,
                                                        self.ups_server_port
                                                       )

        # DAC1 Route
        self.routes_dac1 = 'http://{0}:{1}/dac1'.format(
                                                        self.ups_server_ip,
                                                        self.ups_server_port
                                                       )

        # Mode Route
        self.routes_mode = 'http://{0}:{1}/mode'.format(
                                                        self.ups_server_ip,
                                                        self.ups_server_port
                                                       )

        # Run Start Route
        self.routes_run = 'http://{0}:{1}/run'.format(
                                                      self.ups_server_ip,
                                                      self.ups_server_port
                                                     )

        # Run Stop Route
        self.routes_stop = 'http://{0}:{1}/stop'.format(
                                                        self.ups_server_ip,
                                                        self.ups_server_port
                                                       )

        # Pinch Valve Route
        self.routes_valve = 'http://{0}:{1}/valve'.format(
                                                          self.ups_server_ip,
                                                          self.ups_server_port
                                                         )

        # Status Route
        self.routes_status = 'http://{0}:{1}/status'.format(
                                                            self.ups_server_ip,
                                                            self.ups_server_port
                                                           )

    # --------------------------------------------------------------------------
    #  Status Method
    # --------------------------------------------------------------------------
    # Get Status
    def get_status(self):

        # Check the Enable Bit
        if not self.en:
            raise Exception('Class routes not initialized')

        # Issue Request
        status_get = requests.get(self.routes_status)

        # Check Response Code
        if status_get.status_code != 200:
            exc = 'HTTP request error :: {0}'.format(status_get.status_code)
            raise Exception(exc)

        return j.loads(status_get.text)

    # --------------------------------------------------------------------------
    #  Stop Method
    # --------------------------------------------------------------------------
    # Set RUN
    def set_stop(self):

        # Issue Request
        stop_put = requests.put(self.routes_stop)

        # Check Response Code
        if stop_put.status_code != 200:
            exc = 'HTTP request error :: {0}'.format(stop_put.status_code)
            raise Exception(exc)

    # --------------------------------------------------------------------------
    #  Run Methods
    # --------------------------------------------------------------------------
    # Set RUN
    def set_run(self, run_loops, run_pre_cnt, run_post_cnt, run_cnt):

        # Setup Run Message
        msg = {}
        msg['RUN_LOOPS'] = run_loops
        msg['RUN_PRE_CNT'] = run_pre_cnt
        msg['RUN_POST_CNT'] = run_post_cnt
        msg['RUN_CNT'] = run_cnt

        # Check the Enable Bit
        if not self.en:
            raise Exception('Class routes not initialized')

        # Check the Run Loops Range
        if run_loops < 0 or run_loops > 100:
            raise Exception('RUN_LOOPS request out of range')

        if run_pre_cnt < 0 or run_pre_cnt > 100:
            raise Exception('RUN_PRE_CNT request out of range')

        if run_post_cnt < 0 or run_post_cnt > 100:
            raise Exception('RUN_POST_CNT request out of range')

        if run_cnt < 0 or run_cnt > 100:
            raise Exception('RUN_CNT request out of range')

        # Issue Request
        run_put = requests.put(self.routes_run, json=msg)

        # Check Response Code
        if run_put.status_code != 200:
            exc = 'HTTP request error :: {0}'.format(run_put.status_code)
            raise Exception(exc)

    # Get RUN
    def get_run(self):

        # Setup Run Message
        msg = {}
        msg['RUN_LOOPS'] = run_loops
        msg['RUN_PRE_CNT'] = run_pre_cnt
        msg['RUN_POST_CNT'] = run_post_cnt
        msg['RUN_CNT'] = run_cnt

        # Check the Enable Bit
        if not self.en:
            raise Exception('Class routes not initialized')

        # Issue Request
        run_get = requests.get(self.routes_run)

        # Check Response Code
        if run_get.status_code != 200:
            exc = 'HTTP request error :: {0}'.format(run_get.status_code)
            raise Exception(exc)

        return j.loads(run_get.text)

    # --------------------------------------------------------------------------
    #  LED Methods
    # --------------------------------------------------------------------------
    # Set LED
    def set_led(self, led):

        # Check the Enable Bit
        if not self.en:
            raise Exception('Class routes not initialized')

        # Check the LED Input Range
        if led < 0 or led > 15:
            raise Exception('LED request out of range')

        # Issue Request
        led_put = requests.put(self.routes_led, json={'LED': led})

        # Check Response Code
        if led_put.status_code != 200:
            exc = 'HTTP request error :: {0}'.format(led_put.status_code)
            raise Exception(exc)

    # Get LED
    def get_led(self):

        # Check the Enable Bit
        if not self.en:
            raise Exception('Class routes not initialized')

        # Issue Request
        led_get = requests.get(self.routes_led)

        # Check Response Code
        if led_get.status_code != 200:
            exc = 'HTTP request error :: {0}'.format(led_get.status_code)
            raise Exception(exc)

        # Parse Return
        ret = j.loads(led_get.text)
        val = int(ret['LED'])

        # Done ... Return
        return val

    # --------------------------------------------------------------------------
    #  DAC0 Methods
    # --------------------------------------------------------------------------
    # Set DAC0
    def set_dac0(self, dac0):

        # Check the Enable Bit
        if not self.en:
            raise Exception('Class routes not initialized')

        # Check the LED Input Range
        if dac0 < 0 or dac0 > 4095:
            raise Exception('DAC0 request out of range')

        # Issue Request
        dac0_put = requests.put(self.routes_dac0, json={'DAC0': dac0})

        # Check Response Code
        if dac0_put.status_code != 200:
            exc = 'HTTP request error :: {0}'.format(dac0_put.status_code)
            raise Exception(exc)

    # Get DAC0
    def get_dac0(self):

        # Check the Enable Bit
        if not self.en:
            raise Exception('Class routes not initialized')

        # Issue Request
        dac0_get = requests.get(self.routes_dac0)

        # Check Response Code
        if dac0_get.status_code != 200:
            exc = 'HTTP request error :: {0}'.format(dac0_get.status_code)
            raise Exception(exc)

        # Parse Return
        ret = j.loads(dac0_get.text)
        val = int(ret['DAC0'])

        # Done ... Return
        return val

    # --------------------------------------------------------------------------
    #  DAC1 Methods
    # --------------------------------------------------------------------------
    # Set DAC1
    def set_dac1(self, dac1):

        # Check the Enable Bit
        if not self.en:
            raise Exception('Class routes not initialized')

        # Check the LED Input Range
        if dac1 < 0 or dac1 > 4095:
            raise Exception('DAC1 request out of range')

        # Issue Request
        dac1_put = requests.put(self.routes_dac1, json={'DAC1': dac1})

        # Check Response Code
        if dac1_put.status_code != 200:
            exc = 'HTTP request error :: {0}'.format(dac1_put.status_code)
            raise Exception(exc)

    # Get LED
    def get_dac1(self):

        # Check the Enable Bit
        if not self.en:
            raise Exception('Class routes not initialized')

        # Issue Request
        dac1_get = requests.get(self.routes_dac1)

        # Check Response Code
        if dac1_get.status_code != 200:
            exc = 'HTTP request error :: {0}'.format(dac1_get.status_code)
            raise Exception(exc)

        # Parse Return
        ret = j.loads(dac1_get.text)
        val = int(ret['DAC1'])

        # Done ... Return
        return val

    # --------------------------------------------------------------------------
    #  Mode Methods
    # --------------------------------------------------------------------------
    # Set Mode
    def set_mode(self, mode):

        # Check the Enable Bit
        if not self.en:
            raise Exception('Class routes not initialized')

        # Check the LED Input Range
        if mode < 0 or mode > 3:
            raise Exception('MODE request out of range')

        # Issue Request
        mode_put = requests.put(self.routes_mode, json={'MODE': mode})

        # Check Response Code
        if mode_put.status_code != 200:
            exc = 'HTTP request error :: {0}'.format(mode_put.status_code)
            raise Exception(exc)

    # Get Mode
    def get_mode(self):

        # Check the Enable Bit
        if not self.en:
            raise Exception('Class routes not initialized')

        # Issue Request
        mode_get = requests.get(self.routes_mode)

        # Check Response Code
        if mode_get.status_code != 200:
            exc = 'HTTP request error :: {0}'.format(mode_get.status_code)
            raise Exception(exc)

        # Parse Return
        ret = j.loads(mode_get.text)
        val = int(ret['MODE'])

        # Done ... Return
        return val

    # --------------------------------------------------------------------------
    #  Valve Methods
    # --------------------------------------------------------------------------
    # Set Valve State
    def set_valve(self, pv):

        # Check the Enable Bit
        if not self.en:
            raise Exception('Class routes not initialized')

        # Check the LED Input Range
        if pv < 0 or pv > 1:
            raise Exception('VALVE request out of range')

        # Issue Request
        pv_put = requests.put(self.routes_valve, json={'VALVE': pv})

        # Check Response Code
        if pv_put.status_code != 200:
            exc = 'HTTP request error :: {0}'.format(pv_put.status_code)
            raise Exception(exc)

    # Get Mode
    def get_valve(self):

        # Check the Enable Bit
        if not self.en:
            raise Exception('Class routes not initialized')

        # Issue Request
        pv_get = requests.get(self.routes_valve)

        # Check Response Code
        if pv_get.status_code != 200:
            exc = 'HTTP request error :: {0}'.format(pv_get.status_code)
            raise Exception(exc)

        # Parse Return
        ret = j.loads(pv_get.text)
        pv = int(ret['VALVE'])

        # Done ... Return
        return pv

    # --------------------------------------------------------------------------
    #  Get Check Code
    #    This method retreives the check code from the server.
    # --------------------------------------------------------------------------
    def check(self):

        # Check the Enable Bit
        if not self.en:
            raise Exception('Class routes not initialized')

        # Issue Request
        check_get = requests.get(self.routes_check)

        # Check Response Code
        if check_get.status_code != 200:
            exc = 'HTTP request error :: {0}'.format(check_get.status_code)
            raise Exception(exc)

        # Parse Return
        ret = j.loads(check_get.text)
        check_val = int(ret['CHECK_CODE'])

        # Compare Return to Expected Value
        if check_val == 123456789:
            return 0
        else:
            return 1


if __name__ == "__main__":
    ups_api = UpsApi()
    ups_api.connect('10.1.1.151')

    print(ups_api.check())

    ups_api.set_led(0xF)
    print(ups_api.get_led())
    ups_api.set_led(0x1)
    print(ups_api.get_led())
