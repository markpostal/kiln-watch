import getopt
import sys
import logging
from .Observations import Observations
from .Service import app

"""
This program will monitor the network for kiln-watch broadcasts and present
the data to a user in a web based interface.
"""


def usage() -> None:
    """
        Print the usage statement
    """
    print('''

python3 %s <arguments>


Arguments:

    -h, --help           # Display usage info
    -d, --debug          # Validate the model(s) only.
    -p, --http_port      # The port on which the service listens for HTTP requests
    -b, --broadcast_port # The port on which the service listens for UDP broadcasts
    
''' % sys.argv[0])


def command_line_interface(argv=sys.argv):
    """
        command line interface supports unit tests
        argv - sys.argv, or something similar for testing
    """
    logging_mode = logging.WARNING

    try:
        opts, args = getopt.getopt(argv[1:], "hdsp:b:", ['help', 'debug', 'simulate', 'http_port=', 'broadcast_port='])
    except getopt.GetoptError as err:
        print(err)
        usage()
        return 2

    broadcast_port = 23464
    http_port = 4000
    simulate = False

    for o, a in opts:
        if o in ("-d", "--debug"):
            logging_mode = logging.DEBUG
        elif o in ("-h", "--help"):
            usage()
            return 1
        elif o in ("-s", "--simulate"):
            simulate = True
        elif o in ("-p", "--http_port"):
            http_port = int(a)
        elif o in ("-b", "--broadcast_port"):
            broadast_port = int(a)
        else:
            assert False, "Unhandled option: %s" % o

    logging.basicConfig(encoding='utf-8', level=logging_mode, format="%(levelname)s:%(message)s")
    logging.debug("Debug logging enabled")

    # Start collecting data
    observations = Observations()
    if simulate:
        handle = observations.simulate(3)
    else:
        handle = observations.collect()
    observations.organize()

    # Run the web app
    app.run(debug=False, host='0.0.0.0', port=http_port)

    # Shutdown the collection thread
    observations.stop()
    handle.join()


if __name__ == '__main__':
    ''' Main loop '''
    command_line_interface(sys.argv)
