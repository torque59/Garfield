#!/usr/bin/python
# NoSQL Exploitation FrameWork Copyright 2015 Francis Alexander
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Updated Architecture (Moving to PEP8 Standards)

import sys
import argparse
import settings


def main():

    parser = argparse.ArgumentParser(
        description='Garfield: An Offensive Framework for attacking DCMS V0.1', usage='%(prog)s [options]')

    if len(sys.argv) == 1:
        # parser.add_argument('-h','--help', help='Mandatory Options -t,-p ', required=False)
        parser.print_help()
        sys.exit(1)

	# Specify General Options

    general = parser.add_argument_group(title='Scan Options Target')
    general.add_argument('-ip', help='Target to Scan',
                         required=False, metavar='')
    # general.add_argument('-creds', help='Credentials Format "username:password"', required=False,metavar='')
    general.add_argument('-port', help='Specify Port',
                         required=False, type=int, metavar='')
    general.add_argument('-discover', help='Discover consul,etcd,Apache Zookeeper',
                         required=False,metavar='')
    general.add_argument('-attack', help='Checks for attacks possible on Consul,Zookeeper & Etcd',
                         required=False, metavar='')

    args = vars(parser.parse_args())

    settings.Settings(args)


if __name__ == "__main__":
    main()
