# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import os
import shutil
import sys
from typing import List

import llnl.util.filesystem as fs
from llnl.string import plural
from llnl.util import lang, tty

import spack.cmd
import spack.config
import spack.environment as ev
import spack.paths
import spack.report
import spack.spec
import spack.store
from spack.cmd.common import arguments
from spack.error import InstallError, SpackError
from spack.installer import PackageInstaller

description = "build and install packages"
section = "build"
level = "short"


# Determine value of cache flag
def cache_opt(default_opt, use_buildcache):
    if use_buildcache == "auto":
        return default_opt
    elif use_buildcache == "only":
        return True
    elif use_buildcache == "never":
        return False


def install_kwargs_from_args(args):
    """Translate command line arguments into a dictionary that will be passed
    to the package installer.
    """
    pkg_use_bc, dep_use_bc = args.use_buildcache

    return {
        "fail_fast": args.fail_fast,
        "keep_prefix": args.keep_prefix,
        "keep_stage": args.keep_stage,
        "restage": not args.dont_restage,
        "install_source": args.install_source,
        "verbose": args.verbose or args.install_verbose,
        "fake": args.fake,
        "dirty": args.dirty,
        "package_use_cache": cache_opt(args.use_cache, pkg_use_bc),
        "package_cache_only": cache_opt(args.cache_only, pkg_use_bc),
        "dependencies_use_cache": cache_opt(args.use_cache, dep_use_bc),
        "dependencies_cache_only": cache_opt(args.cache_only, dep_use_bc),
        "include_build_deps": args.include_build_deps,
        "stop_at": args.until,
        "unsigned": args.unsigned,
        "install_deps": ("dependencies" in args.things_to_install),
        "install_package": ("package" in args.things_to_install),
    }


def setup_parser(subparser):
    subparser.add_argument(
        "--only",
        default="package,dependencies",
        dest="things_to_install",
        choices=["package", "dependencies"],
        help="select the mode of installation\n\n"
        "default is to install the package along with all its dependencies. "
        "alternatively, one can decide to install only the package or only the dependencies",
    )
    subparser.add_argument(
        "-u",
        "--until",
        type=str,
        dest="until",
        default=None,
        help="phase to stop after when installing (default None)",
    )
    arguments.add_common_arguments(subparser, ["jobs"])
    subparser.add_argument(
        "--overwrite",
        action="store_true",
        help="reinstall an existing spec, even if it has dependents",
    )
    subparser.add_argument(
        "--fail-fast",
        action="store_true",
        help="stop all builds if any build fails (default is best effort)",
    )
    subparser.add_argument(
        "--keep-prefix",
        action="store_true",
        help="don't remove the install prefix if installation fails",
    )
    subparser.add_argument(
        "--keep-stage",
        action="store_true",
        help="don't remove the build stage if installation succeeds",
    )
    subparser.add_argument(
        "--dont-restage",
        action="store_true",
        help="if a partial install is detected, don't delete prior state",
    )

    cache_group = subparser.add_mutually_exclusive_group()
    cache_group.add_argument(
        "--use-cache",
        action="store_true",
        dest="use_cache",
        default=True,
        help="check for pre-built Spack packages in mirrors (default)",
    )
    cache_group.add_argument(
        "--no-cache",
        action="store_false",
        dest="use_cache",
        default=True,
        help="do not check for pre-built Spack packages in mirrors",
    )
    cache_group.add_argument(
        "--cache-only",
        action="store_true",
        dest="cache_only",
        default=False,
        help="only install package from binary mirrors",
    )
    cache_group.add_argument(
        "--use-buildcache",
        dest="use_buildcache",
        type=arguments.use_buildcache,
        default="package:auto,dependencies:auto",
        metavar="[{auto,only,never},][package:{auto,only,never},][dependencies:{auto,only,never}]",
        help="select the mode of buildcache for the 'package' and 'dependencies'\n\n"
        "default: package:auto,dependencies:auto\n\n"
        "- `auto` behaves like --use-cache\n"
        "- `only` behaves like --cache-only\n"
        "- `never` behaves like --no-cache",
    )

    subparser.add_argument(
        "--include-build-deps",
        action="store_true",
        dest="include_build_deps",
        default=False,
        help="include build deps when installing from cache, "
        "useful for CI pipeline troubleshooting",
    )

    subparser.add_argument(
        "--no-check-signature",
        action="store_true",
        dest="unsigned",
        default=None,
        help="do not check signatures of binary packages (override mirror config)",
    )
    subparser.add_argument(
        "--show-log-on-error",
        action="store_true",
        help="print full build log to stderr if build fails",
    )
    subparser.add_argument(
        "--source",
        action="store_true",
        dest="install_source",
        help="install source files in prefix",
    )
    arguments.add_common_arguments(subparser, ["no_checksum"])
    subparser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        dest="install_verbose",
        help="display verbose build output while installing",
    )
    subparser.add_argument("--fake", action="store_true", help="fake install for debug purposes")
    subparser.add_argument(
        "--only-concrete",
        action="store_true",
        default=False,
        help="(with environment) only install already concretized specs",
    )

    updateenv_group = subparser.add_mutually_exclusive_group()
    updateenv_group.add_argument(
        "--add",
        action="store_true",
        default=False,
        help="(with environment) add spec to the environment as a root",
    )
    updateenv_group.add_argument(
        "--no-add",
        action="store_false",
        dest="add",
        help="(with environment) do not add spec to the environment as a root",
    )

    subparser.add_argument(
        "-f",
        "--file",
        action="append",
        default=[],
        dest="specfiles",
        metavar="SPEC_YAML_FILE",
        help="read specs to install from .yaml files",
    )

    cd_group = subparser.add_mutually_exclusive_group()
    arguments.add_common_arguments(cd_group, ["clean", "dirty"])

    testing = subparser.add_mutually_exclusive_group()
    testing.add_argument(
        "--test",
        default=None,
        choices=["root", "all"],
        help="run tests on only root packages or all packages",
    )
    arguments.add_common_arguments(subparser, ["log_format"])
    subparser.add_argument("--log-file", default=None, help="filename for the log file")
    subparser.add_argument(
        "--help-cdash", action="store_true", help="show usage instructions for CDash reporting"
    )
    arguments.add_cdash_args(subparser, False)
    arguments.add_common_arguments(subparser, ["yes_to_all", "spec"])
    arguments.add_concretizer_args(subparser)


def default_log_file(spec):
    """Computes the default filename for the log file and creates
    the corresponding directory if not present
    """
    basename = spec.format_path("test-{name}-{version}-{hash}.xml")
    dirname = fs.os.path.join(spack.paths.reports_path, "junit")
    fs.mkdirp(dirname)
    return fs.os.path.join(dirname, basename)


def report_filename(args: argparse.Namespace, specs: List[spack.spec.Spec]) -> str:
    """Return the filename to be used for reporting to JUnit or CDash format."""
    result = args.log_file or default_log_file(specs[0])
    return result


def compute_tests_install_kwargs(specs, cli_test_arg):
    """Translate the test cli argument into the proper install argument"""
    if cli_test_arg == "all":
        return True
    elif cli_test_arg == "root":
        return [spec.name for spec in specs]
    return False


def require_user_confirmation_for_overwrite(concrete_specs, args):
    if args.yes_to_all:
        return

    installed = list(filter(lambda x: x, map(spack.store.STORE.db.query_one, concrete_specs)))
    display_args = {"long": True, "show_flags": True, "variants": True}

    if installed:
        tty.msg("The following package specs will be reinstalled:\n")
        spack.cmd.display_specs(installed, **display_args)

    not_installed = list(filter(lambda x: x not in installed, concrete_specs))
    if not_installed:
        tty.msg(
            "The following package specs are not installed and"
            " the --overwrite flag was given. The package spec"
            " will be newly installed:\n"
        )
        spack.cmd.display_specs(not_installed, **display_args)

    # We have some specs, so one of the above must have been true
    answer = tty.get_yes_or_no("Do you want to proceed?", default=False)
    if not answer:
        tty.die("Reinstallation aborted.")


def _dump_log_on_error(e: InstallError):
    e.print_context()
    assert e.pkg, "Expected InstallError to include the associated package"
    if not os.path.exists(e.pkg.log_path):
        tty.error("'spack install' created no log.")
    else:
        sys.stderr.write("Full build log:\n")
        with open(e.pkg.log_path, errors="replace") as log:
            shutil.copyfileobj(log, sys.stderr)


def _die_require_env():
    msg = "install requires a package argument or active environment"
    if "spack.yaml" in os.listdir(os.getcwd()):
        # There's a spack.yaml file in the working dir, the user may
        # have intended to use that
        msg += (
            "\n\n"
            "Did you mean to install using the `spack.yaml`"
            " in this directory? Try: \n"
            "    spack env activate .\n"
            "    spack install\n"
            "  OR\n"
            "    spack --env . install"
        )
    tty.die(msg)


def install(parser, args):
    # TODO: unify args.verbose?
    tty.set_verbose(args.verbose or args.install_verbose)

    if args.help_cdash:
        arguments.print_cdash_help()
        return

    if args.no_checksum:
        spack.config.set("config:checksum", False, scope="command_line")

    if args.log_file and not args.log_format:
        msg = "the '--log-format' must be specified when using '--log-file'"
        tty.die(msg)

    arguments.sanitize_reporter_options(args)

    def reporter_factory(specs):
        if args.log_format is None:
            return lang.nullcontext()

        return spack.report.build_context_manager(
            reporter=args.reporter(), filename=report_filename(args, specs=specs), specs=specs
        )

    install_kwargs = install_kwargs_from_args(args)

    env = ev.active_environment()

    if not env and not args.spec and not args.specfiles:
        _die_require_env()

    try:
        if env:
            install_with_active_env(env, args, install_kwargs, reporter_factory)
        else:
            install_without_active_env(args, install_kwargs, reporter_factory)
    except InstallError as e:
        if args.show_log_on_error:
            _dump_log_on_error(e)
        raise


def _maybe_add_and_concretize(args, env, specs):
    """Handle the overloaded spack install behavior of adding
    and automatically concretizing specs"""

    # Users can opt out of accidental concretizations with --only-concrete
    if args.only_concrete:
        return

    # Otherwise, we will modify the environment.
    with env.write_transaction():
        # `spack add` adds these specs.
        if args.add:
            for spec in specs:
                env.add(spec)

        # `spack concretize`
        tests = compute_tests_install_kwargs(env.user_specs, args.test)
        concretized_specs = env.concretize(tests=tests)
        if concretized_specs:
            tty.msg(f"Concretized {plural(len(concretized_specs), 'spec')}")
            ev.display_specs([concrete for _, concrete in concretized_specs])

        # save view regeneration for later, so that we only do it
        # once, as it can be slow.
        env.write(regenerate=False)


def install_with_active_env(env: ev.Environment, args, install_kwargs, reporter_factory):
    specs = spack.cmd.parse_specs(args.spec)

    # The following two commands are equivalent:
    # 1. `spack install --add x y z`
    # 2. `spack add x y z && spack concretize && spack install --only-concrete`
    # here we do the `add` and `concretize` part.
    _maybe_add_and_concretize(args, env, specs)

    # Now we're doing `spack install --only-concrete`.
    if args.add or not specs:
        specs_to_install = env.concrete_roots()
        if not specs_to_install:
            tty.msg(f"{env.name} environment has no specs to install")
            return

    # `spack install x y z` without --add is installing matching specs in the env.
    else:
        specs_to_install = env.all_matching_specs(*specs)
        if not specs_to_install:
            msg = (
                "Cannot install '{0}' because no matching specs are in the current environment."
                " You can add specs to the environment with 'spack add {0}', or as part"
                " of the install command with 'spack install --add {0}'"
            ).format(" ".join(args.spec))
            tty.die(msg)

    install_kwargs["tests"] = compute_tests_install_kwargs(specs_to_install, args.test)

    if args.overwrite:
        require_user_confirmation_for_overwrite(specs_to_install, args)
        install_kwargs["overwrite"] = [spec.dag_hash() for spec in specs_to_install]

    try:
        with reporter_factory(specs_to_install):
            env.install_specs(specs_to_install, **install_kwargs)
    finally:
        if env.views:
            with env.write_transaction():
                env.write(regenerate=True)


def concrete_specs_from_cli(args, install_kwargs):
    """Return abstract and concrete spec parsed from the command line."""
    abstract_specs = spack.cmd.parse_specs(args.spec)
    install_kwargs["tests"] = compute_tests_install_kwargs(abstract_specs, args.test)
    try:
        concrete_specs = spack.cmd.parse_specs(
            args.spec, concretize=True, tests=install_kwargs["tests"]
        )
    except SpackError as e:
        tty.debug(e)
        if args.log_format is not None:
            reporter = args.reporter()
            reporter.concretization_report(report_filename(args, abstract_specs), e.message)
        raise
    return concrete_specs


def concrete_specs_from_file(args):
    """Return the list of concrete specs read from files."""
    result = []
    for file in args.specfiles:
        with open(file, "r") as f:
            if file.endswith("yaml") or file.endswith("yml"):
                s = spack.spec.Spec.from_yaml(f)
            else:
                s = spack.spec.Spec.from_json(f)

        concretized = s.concretized()
        if concretized.dag_hash() != s.dag_hash():
            msg = 'skipped invalid file "{0}". '
            msg += "The file does not contain a concrete spec."
            tty.warn(msg.format(file))
            continue
        result.append(concretized)
    return result


def install_without_active_env(args, install_kwargs, reporter_factory):
    concrete_specs = concrete_specs_from_cli(args, install_kwargs) + concrete_specs_from_file(args)

    if len(concrete_specs) == 0:
        tty.die("The `spack install` command requires a spec to install.")

    with reporter_factory(concrete_specs):
        if args.overwrite:
            require_user_confirmation_for_overwrite(concrete_specs, args)
            install_kwargs["overwrite"] = [spec.dag_hash() for spec in concrete_specs]

        installs = [s.package for s in concrete_specs]
        install_kwargs["explicit"] = [s.dag_hash() for s in concrete_specs]
        builder = PackageInstaller(installs, **install_kwargs)
        builder.install()
