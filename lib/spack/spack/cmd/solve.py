# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re
import sys

import llnl.util.tty as tty
import llnl.util.tty.color as color

import spack
import spack.cmd
import spack.cmd.spec
import spack.config
import spack.environment
import spack.hash_types as ht
import spack.solver.asp as asp
import spack.spec

description = "concretize a specs using an ASP solver"
section = "developer"
level = "long"

#: output options
show_options = ("asp", "opt", "output", "solutions")


def setup_parser(subparser):
    # Solver arguments
    subparser.add_argument(
        "--show",
        action="store",
        default="opt,solutions",
        help="select outputs\n\ncomma-separated list of:\n"
        "  asp          asp program text\n"
        "  opt          optimization criteria for best model\n"
        "  output       raw clingo output\n"
        "  solutions    models found by asp program\n"
        "  all          all of the above",
    )
    subparser.add_argument(
        "--timers",
        action="store_true",
        default=False,
        help="print out timers for different solve phases",
    )
    subparser.add_argument(
        "--stats", action="store_true", default=False, help="print out statistics from clingo"
    )

    spack.cmd.spec.setup_parser(subparser)


def _process_result(result, show, required_format, kwargs):
    opt, _, _ = min(result.answers)
    if ("opt" in show) and (not required_format):
        tty.msg("Best of %d considered solutions." % result.nmodels)
        tty.msg("Optimization Criteria:")

        maxlen = max(len(s[2]) for s in result.criteria)
        color.cprint("@*{  Priority  Criterion %sInstalled  ToBuild}" % ((maxlen - 10) * " "))

        fmt = "  @K{%%-8d}  %%-%ds%%9s  %%7s" % maxlen
        for i, (installed_cost, build_cost, name) in enumerate(result.criteria, 1):
            color.cprint(
                fmt
                % (
                    i,
                    name,
                    "-" if build_cost is None else installed_cost,
                    installed_cost if build_cost is None else build_cost,
                )
            )
        print()

    # dump the solutions as concretized specs
    if "solutions" in show:
        if required_format:
            for spec in result.specs:
                # With -y, just print YAML to output.
                if required_format == "yaml":
                    # use write because to_yaml already has a newline.
                    sys.stdout.write(spec.to_yaml(hash=ht.dag_hash))
                elif required_format == "json":
                    sys.stdout.write(spec.to_json(hash=ht.dag_hash))
        else:
            sys.stdout.write(spack.spec.tree(result.specs, color=sys.stdout.isatty(), **kwargs))
        print()

    if result.unsolved_specs and "solutions" in show:
        tty.msg(asp.Result.format_unsolved(result.unsolved_specs))


def solve(parser, args):
    # these are the same options as `spack spec`
    install_status_fn = spack.spec.Spec.install_status

    fmt = spack.spec.DISPLAY_FORMAT
    if args.namespaces:
        fmt = "{namespace}." + fmt

    kwargs = {
        "cover": args.cover,
        "format": fmt,
        "hashlen": None if args.very_long else 7,
        "show_types": args.types,
        "status_fn": install_status_fn if args.install_status else None,
        "hashes": args.long or args.very_long,
    }

    # process output options
    show = re.split(r"\s*,\s*", args.show)
    if "all" in show:
        show = show_options
    for d in show:
        if d not in show_options:
            raise ValueError(
                "Invalid option for '--show': '%s'\nchoose from: (%s)"
                % (d, ", ".join(show_options + ("all",)))
            )

    # Format required for the output (JSON, YAML or None)
    required_format = args.format

    # If we have an active environment, pick the specs from there
    env = spack.environment.active_environment()
    if args.specs:
        specs = spack.cmd.parse_specs(args.specs)
    elif env:
        specs = list(env.user_specs)
    else:
        tty.die("spack solve requires at least one spec or an active environment")

    solver = asp.Solver()
    output = sys.stdout if "asp" in show else None
    setup_only = set(show) == {"asp"}
    unify = spack.config.get("concretizer:unify")
    allow_deprecated = spack.config.get("config:deprecated", False)
    if unify != "when_possible":
        # set up solver parameters
        # Note: reuse and other concretizer prefs are passed as configuration
        result = solver.solve(
            specs,
            out=output,
            timers=args.timers,
            stats=args.stats,
            setup_only=setup_only,
            allow_deprecated=allow_deprecated,
        )
        if not setup_only:
            _process_result(result, show, required_format, kwargs)
    else:
        for idx, result in enumerate(
            solver.solve_in_rounds(
                specs,
                out=output,
                timers=args.timers,
                stats=args.stats,
                allow_deprecated=allow_deprecated,
            )
        ):
            if "solutions" in show:
                tty.msg("ROUND {0}".format(idx))
                tty.msg("")
            else:
                print("% END ROUND {0}\n".format(idx))
            if not setup_only:
                _process_result(result, show, required_format, kwargs)
