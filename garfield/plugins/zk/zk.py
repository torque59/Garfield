from garfield.lib.plugin import BasePlugin
from garfield.plugins.zk import fingerprinter, dumper, loader, remover


class Plugin(BasePlugin):
    def update_arg_parser(self, sub_parser):
        sub_parser.add_argument("--ip", dest="ip", type=str, default="localhost", help="Address of the target")
        sub_parser.add_argument("--port", dest="port", type=int, default=2181, help="Port of the target")

        sub_parser.add_argument(
                "--fingerprint", dest="fingerprint", action="store_true", default=False,
                help="Fingerprint given zookeeper version using an open port")
        sub_parser.add_argument(
                "--dump", dest="dump", const="/dev/null", nargs="?",
                help="Dump all zookeeper data to given file")
        sub_parser.add_argument(
                "--remove", dest="remove", action="store_true", default=False,
                help="Remove all nodes specified")
        sub_parser.add_argument(
                "--load", dest="load",
                help="Load all data from given file into zookeeper")
        sub_parser.add_argument(
                "--data-regex", dest="data_regex",
                help="Python regex to filter node with matching data")
        sub_parser.add_argument(
                "--node", dest="node", default="/",
                help="Zookeeper node to start traversing from")
        return(sub_parser)

    def run(self, args):
        if args.fingerprint is True:
            version = fingerprinter.run(args, self.helpers)
        if args.dump is not None:
            dumper.run(args, self.helpers)
        if args.load is not None:
            loader.run(args, self.helpers)
        if args.remove is not None:
            remover.run(args, self.helpers)
