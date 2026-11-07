#!/usr/bin/env python3
import socket, sys, argparse
# the following depends on the shared folder and needs to be
# coppied into manager and commandline. 
from socket_communication import SOCKET_PATH, write_message, read_message

RED, GREEN, YELLOW, RESET = "\033[31m", "\033[32m", "\033[33m", "\033[0m"

def positive_int(s: str) -> int:
    v = int(s)
    if v<=0:
        raise argparse.ArgumentTypeError("timer must be positive number of seconds")
    return v

def command_parse():
    parser = argparse.ArgumentParser(prog="pi-manager"
        ,description="CLI to interact with custom deployment and management Tool of Dockers"
    )
    paths = parser.add_subparsers(dest="path")
    service = paths.add_parser("service"
        ,aliases=["s"]
        ,help="Controls the projects and dockers running on the PI"
    )
    health = paths.add_parser("health"
        ,aliases=["h"]
        ,help="Controls the Hardware side like stats, backups and notifcation"
    )

    # service path
    service_actions = service.add_subparsers(dest="action")
    # list
    list_cmd = service_actions.add_parser("list", help="list all builds")
    list_cmd.add_argument("-f","--filter", choices=["awake","sleep","down"], help="filter the list, depending on given option")
    # status
    service_status = service_actions.add_parser("status", help="show status of project")
    service_status.add_argument("target", help="project name")
    # build
    build = service_actions.add_parser("build", help="enqueue build + start project")
    build.add_argument("target", help="project name")
    # start
    start = service_actions.add_parser("start", help="start up project")
    start.add_argument("target", help="project name")
    # stop
    stop = service_actions.add_parser("stop", help="stop running project")
    stop.add_argument("target", help="project name")
    # sleep
    sleep = service_actions.add_parser("sleep", help="let project sleep (i.e. still in memory)")
    sleep.add_argument("target", help="project name")
    sleep.add_argument("-t","--timer", type=positive_int, help="sets the timer to x seconds till sleep")
    # wake
    wake = service_actions.add_parser("wake", help="let project wake (only if put to sleep)")
    wake.add_argument("target", help="project name")

    # health path
    health_action= health.add_subparsers(dest="action")
    # status
    health_status = health_action.add_parser("status", help="gives the status of the PI-Manager")

    return parser

def build_payload(args) -> dict:
    PATH_ALIASES = {"s": "service", "serv": "service", "h": "health"}

    path = PATH_ALIASES.get(args.path, args.path)
    cargo = {"selector": path, "action": args.action}

    ROUTING_KEYS = ["path","action"] # sort out the routing/selecting Part of the command.
    cargo["payload"] = {
        k: v for k, v in vars(args).items() 
        if k not in ROUTING_KEYS and v
    }

    return cargo

def socket_transaction(payload):
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
        client.connect(SOCKET_PATH)
        # Send
        write_message(client,payload)
        # Recive
        return read_message(client)
            
def message_renderer(response_dict):
    print(f"Recieved: {response_dict}")

def main(argv=None) -> int:
    parser = command_parse()
    args = parser.parse_args(argv)

    if args.path is None:
        args.path, args.action = "health", "status"
    elif args.action is None:
        args.action = "status"

    payload = build_payload(args)

    try:
        response = socket_transaction(payload)
    except (ConnectionRefusedError, FileNotFoundError):
        print(f"{RED}ERROR: daemon not reachable{RESET}", file=sys.stderr)
        return 3
    except socket.timeout:
        print(f"{RED}ERROR: daemon did not respond{RESET}", file=sys.stderr)
        return 4
    except (OSError, ValueError) as e:
        print(f"{RED}ERROR: protocol failure: {e}{RESET}", file=sys.stderr)
        return 5

    message_renderer(response)
    return 0 if response.get("ok") else 1

if __name__ == "__main__":
    sys.exit(main())