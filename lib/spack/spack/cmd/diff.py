# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import spack.cmd

import spack.cmd.common.arguments as arguments
import spack.environment as ev
import spack.util.environment
import spack.diff

import llnl.util.tty as tty
import spack.util.spack_json as sjson
import sys

description = "compare two specs"
section = "basic"
level = "long"


def setup_parser(subparser):
    arguments.add_common_arguments(
        subparser, ['specs'])

    subparser.add_argument(
        '--json',
        action='store_true',
        default=False,
        dest='dump_json',
        help="Dump json output instead of pretty printing."
    )
    subparser.add_argument(
        '--first',
        action='store_true',
        default=False,
        dest='load_first',
        help="load the first match if multiple packages match the spec"
    )
    subparser.add_argument(
        '--oneline',
        action='store_true',
        default=False,
        dest='one_line',
        help="Show a one line diff, only comparing the top level attributes."
    )


def diff(parser, args):
    env = ev.get_env(args, 'diff')

    if len(args.specs) != 2:
        tty.die("You must provide two specs to diff.")

    specs = [spack.cmd.disambiguate_spec(spec, env, first=args.load_first)
             for spec in spack.cmd.parse_specs(args.specs)]

    # Create the Spec differ, compare old (0) against new (1)
    differ = spack.diff.SpecDiff(specs[0], specs[1])

    # Calculate the comparison to dump as json
    if args.dump_json:
        c = differ.to_json(to_str=True, colorful=False)
        print(sjson.dump(c))

    # or print a colored diff
    else:

        # Cut out early if the specs are the same
        if specs[0] == specs[1]:
            tty.info("No differences.")
            sys.exit(0)

        tty.info("Showing %s TO %s" % (differ.a_name, differ.b_name))

        # A single line diff shows only top level differences in the specs
        if args.one_line:
            print(differ.colored_diff())
        else:
            print(differ.tree())
