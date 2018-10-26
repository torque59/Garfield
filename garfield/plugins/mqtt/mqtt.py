from garfield.lib.plugin import BasePlugin
from garfield.plugins.mqtt import consumer


class Plugin(BasePlugin):
    def update_arg_parser(self, sub_parser):
        sub_parser.add_argument("--ip", dest="ip", type=str, default="localhost", help="Address of the target")
        sub_parser.add_argument("--port", dest="port", type=int, default=1883, help="Port of the target")
        sub_parser.add_argument("--topic", dest="topic", type=str, default="$SYS/#", help="Topic name to consume")

        sub_parser.add_argument(
                "--consumer", dest="consumer", action="store_true", default=False,
                help="Consumer to consume from topic")

        return(sub_parser)

    def run(self, args):
        if args.consumer is True:
            consumer.run(args, self.helpers)
