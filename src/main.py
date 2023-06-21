import argparse
import asyncio
import functools
import logging
from getpass import getpass
import signal

from src.ImageBuilder import ImageBuilder
from src.TwitterHandler import TwitterHandler
    
class main:
    def __init__(self, pwd: str, key: str = "TWITTER") -> None:
        self.image_builder = ImageBuilder()
        self.tweeterHandler = TwitterHandler(pwd ,key)

    def run(self) -> None:
        self.image_builder.generate_clipping_data()
        self.image_builder.clipping.image.show()
        self.tweeterHandler.tweet_image(self.image_builder.clipping)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
    description="Tweet Clippings",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--seconds', dest="seconds", type=int, nargs='?', default=86400)
    parser.add_argument('--key', dest="key", type=str, nargs='?', help="Name of key for Twitter API in encrypted dictionnary", default= "TWITTER")
    parser.add_argument("-q","--quiet",action="count",default=0,
                    help="Be more quiet.")
    parser.add_argument("-v", "--verbose",action="count",default=0,
                    help="Be more verbose. Both -v and -q may be used multiple times.")
    parser.add_argument('--log-file', dest="log_file", type=str, nargs='?')
    
    args = parser.parse_args()
    
    # Setup logging
    args.verbosity = args.verbose - args.quiet
    if args.verbosity == 0:
        logging.root.setLevel(logging.INFO)
    elif args.verbosity >= 1:
        logging.root.setLevel(logging.DEBUG)
    elif args.verbosity == -1:
        logging.root.setLevel(logging.WARNING)
    elif args.verbosity <= -2:
        logging.root.setLevel(logging.ERROR)
    
    logging.basicConfig(format='%(levelname)s - %(asctime)s - %(name)s - %(message)s', filename=args.log_file)
    
    logger: logging.Logger = logging.getLogger()

    pwd = getpass("provide password for pk:")
    
    executor = main(pwd)

    def ask_exit(signame, loop, logger):
        logger.info("got signal %s: exit" % signame)
        loop.stop()

    loop = asyncio.get_event_loop()

    for signame in {'SIGINT', 'SIGTERM'}:
        loop.add_signal_handler(
            getattr(signal, signame),
            functools.partial(ask_exit, signame, loop, logger))

    async def periodic(seconds):
        while True:
            executor.run()
            await asyncio.sleep(seconds)

    def stop():
        task.cancel()

    task = loop.create_task(periodic(args.seconds))

    try:
        loop.run_until_complete(task)
    except asyncio.CancelledError:
        pass
