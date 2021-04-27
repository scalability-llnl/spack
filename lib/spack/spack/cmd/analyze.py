# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

import llnl.util.tty as tty

import spack.analyzers
import spack.build_environment
import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.environment as ev
import spack.fetch_strategy
import spack.monitor
import spack.paths
import spack.report


description = "analyze installed packages"
section = "extensions"
level = "short"


def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='analyze_command')

    sp.add_parser('list-analyzers',
                  description="list available analyzers",
                  help="show list of analyzers that are available to run.")

    # This adds the monitor group to the subparser
    spack.monitor.get_monitor_group(subparser)

    # Run Parser
    run_parser = sp.add_parser('run', description="run an analyzer",
                               help="provide the name of the analyzer to run.")

    run_parser.add_argument(
        '--overwrite', action='store_true',
        help="re-analyze even if the output file already exists.")
    run_parser.add_argument(
        '-p', '--path', default=None,
        dest='path',
        help="write output to a different directory than ~/.spack/analyzers")
    run_parser.add_argument(
        '-a', '--analyzers', default=None,
        dest="analyzers", action="append",
        help="add an analyzer (defaults to all available)")
    arguments.add_common_arguments(run_parser, ['spec'])


def analyze_spec(spec, analyzers=None, outdir=None, monitor=None, overwrite=False):
    """
    Do an analysis for a spec, optionally adding monitoring.

    We also allow the user to specify a custom output directory.
    analyze_spec(spec, args.analyzers, args.outdir, monitor)

    Args:
        spec (Spec): spec object of installed package
        analyzers (list): list of analyzer (keys) to run
        monitor (monitor.SpackMonitorClient): a monitor client
        overwrite (bool): overwrite result if already exists
    """
    analyzers = analyzers or list(spack.analyzers.analyzer_types.keys())

    # Load the build environment from the spec install directory, and send
    # the spec to the monitor if it's not known
    if monitor:
        monitor.load_build_environment(spec)
        monitor.new_configuration([spec])

    for name in analyzers:

        # Instantiate the analyzer with the spec and outdir
        analyzer = spack.analyzers.get_analyzer(name)(spec, outdir)

        # Run the analyzer to get a json result - results are returned as
        # a dictionary with a key corresponding to the analyzer type, so
        # we can just update the data
        result = analyzer.run()

        # Send the result. We do them separately because:
        # 1. each analyzer might have differently organized output
        # 2. the size of a result can be large
        analyzer.save_result(result, overwrite)


def analyze(parser, args, **kwargs):

    # If the user wants to list analyzers, do so and exit
    if args.analyze_command == "list-analyzers":
        spack.analyzers.list_all()
        sys.exit(0)

    # handle active environment, if any
    env = ev.get_env(args, 'analyze')

    # Get an disambiguate spec (we should only have one)
    specs = spack.cmd.parse_specs(args.spec)
    if not specs:
        tty.die("You must provide one or more specs to analyze.")
    spec = spack.cmd.disambiguate_spec(specs[0], env)

    # The user wants to monitor builds using github.com/spack/spack-monitor
    # It is instantianted once here, and then available at spack.monitor.cli
    monitor = None
    if args.use_monitor:
        monitor = spack.monitor.get_client(
            host=args.monitor_host,
            prefix=args.monitor_prefix,
            disable_auth=args.monitor_disable_auth,
        )

    # Run the analysis
    analyze_spec(spec, args.analyzers, args.path, monitor, args.overwrite)
