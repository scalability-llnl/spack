# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

import llnl.util.tty as tty

from spack.util.log_parse import make_log_context, parse_log_events

description = "filter errors and warnings from build logs"
section = "build"
level = "long"

event_types = ("errors", "warnings")


def setup_parser(subparser):
    subparser.add_argument(
        "--show",
        action="store",
        default="errors",
        help="comma-separated list of what to show; options: errors, warnings",
    )
    subparser.add_argument(
        "-c",
        "--context",
        action="store",
        type=int,
        default=3,
        help="lines of context to show around lines of interest",
    )
    subparser.add_argument(
        "-p",
        "--profile",
        action="store_true",
        help="print out a profile of time spent in regexes during parse",
    )
    subparser.add_argument(
        "-w",
        "--width",
        action="store",
        type=int,
        default=None,
        help="wrap width: auto-size to terminal by default; 0 for no wrap",
    )
    subparser.add_argument(
        "-j",
        "--jobs",
        action="store",
        type=int,
        default=None,
        help="number of jobs to parse log file (default: 1 for short logs, "
        "ncpus for long logs)",
    )

    subparser.add_argument("file", help="a log file containing build output, or - for stdin")


def log_parse(parser, args):
    input = args.file
    if args.file == "-":
        input = sys.stdin

    errors, warnings = parse_log_events(input, args.context, args.jobs, args.profile)
    if args.profile:
        return

    types = [s.strip() for s in args.show.split(",")]
    for e in types:
        if e not in event_types:
            tty.die("Invalid event type: %s" % e)

    events = []
    if "errors" in types:
        events.extend(errors)
        print("%d errors" % len(errors))
    if "warnings" in types:
        events.extend(warnings)
        print("%d warnings" % len(warnings))

    print(make_log_context(events, args.width))
