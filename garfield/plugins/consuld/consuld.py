from garfield.lib.plugin import BasePlugin
from garfield.plugins.consuld import fingerprinter,attacks


class Plugin(BasePlugin):
    def update_arg_parser(self, sub_parser):
        sub_parser.add_argument("--ip", dest="ip", help="Address of the target")
        sub_parser.add_argument("--port", dest="port", type=int, default=8500, help="Port of the target")

        sub_parser.add_argument(
                "--fingerprint", dest="fingerprint", action="store_true", default=False,
                help="Fingerprint given consul version using an open port")
        sub_parser.add_argument(
                "--dump", dest="dump", const="/dev/null", nargs="?",
                help="Dump all Consul data to given file")
        sub_parser.add_argument(
                "--attack", dest="attack", action="store_true", default=False,
                help="Attacks consul version using an open port")

    def run(self, args):
        if args.fingerprint is True:
            fingerprinter.run(args, self.helpers)
        if args.dump is not None:
            dumper.run(args, self.helpers)
        if args.attack is not None:
            attacks.run(args, self.helpers)
