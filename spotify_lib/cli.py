import signal
from argparse import ArgumentParser
from time import sleep
from halo import Halo


def add_arguments(parser: ArgumentParser) -> None:
    music_sources = parser.add_argument_group("Music Sources", "Where to draw music from")
    music_sources.add_argument(
        "--artist",
        action="append",
        type=str,
        help="list of artists to play music from"
    )
    music_sources.add_argument(
        "--track",
        action="append",
        type=str,
        help="list of tracks to play"
    )
    music_sources.add_argument(
        "--album",
        action="append",
        type=str,
        help="list of albums to play music from"
    )

spinner = Halo(text="playing...", spinner="bouncingBall")

def signal_handler(sig, frame):
    raise Exception()

def run():
    sleep(10)

def main() -> None:
    parser = ArgumentParser()
    add_arguments(parser)
    args = parser.parse_args()
    for name, val in vars(args).items():
        print(f"[{name}] {val}")

    # register signal handlers
    signal.signal(signal.SIGINT, signal_handler)

    try:
        # wrap for spinner handling
        spinner.start()
        try:
            run()
        except Exception as e:
            spinner.stop()
            raise e
    except Exception as e:
        print(f"saw an error of type: {type(e)}")
        print("shutting down...")

