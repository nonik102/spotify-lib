import signal
from argparse import ArgumentParser, Namespace
from halo import Halo

from spotify_lib.definitions import PlayerResult, Provider, Dispatcher, Player

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

def run(args: Namespace):
    dispatcher = Dispatcher.from_namespace(args)
    provider = Provider.from_namespace(args)
    player = Player.from_namespace(args)

    result: PlayerResult | None = None
    while dispatcher.wait(result):
        to_play = provider.get_next()
        result = player.add(to_play)


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
            run(args)
        except Exception as e:
            spinner.stop()
            raise e
    except Exception as e:
        print(f"saw an error of type: {type(e)}")
        print("shutting down...")

