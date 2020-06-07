import argparse
from proxy import Proxy


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=' Enter your port to use '
                                                 'this')
    parser.add_argument('-p', '--port', help='your port')
    port = parser.parse_args().port
    prog = Proxy(port)
    prog.process()
