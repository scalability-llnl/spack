# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import os
import shutil
import sys

import llnl.util.filesystem as fs
import llnl.util.tty as tty

import spack.build_environment
import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.environment as ev
import spack.fetch_strategy
import spack.paths
import spack.report
from spack.error import SpackError


description = "build and install packages"
section = "build"
level = "short"


def update_kwargs_from_args(args, kwargs):
    """Parse cli arguments and construct a dictionary
    that will be passed to Package.do_install API"""

    kwargs.update({
        'keep_prefix': args.keep_prefix,
        'keep_stage': args.keep_stage,
        'restage': not args.dont_restage,
        'install_source': args.install_source,
        'make_jobs': args.jobs,
        'verbose': args.verbose,
        'fake': args.fake,
        'dirty': args.dirty,
        'use_cache': args.use_cache
    })
    if hasattr(args, 'setup'):
        setups = set()
        for arglist_s in args.setup:
            for arg in [x.strip() for x in arglist_s.split(',')]:
                setups.add(arg)
        kwargs['setup'] = setups
        tty.msg('Setup={0}'.format(kwargs['setup']))


def setup_parser(subparser):
    subparser.add_argument(
        '--only',
        default='package,dependencies',
        dest='things_to_install',
        choices=['package', 'dependencies'],
        help="""select the mode of installation.
the default is to install the package along with all its dependencies.
alternatively one can decide to install only the package or only
the dependencies"""
    )
    arguments.add_common_arguments(subparser, ['jobs', 'install_status'])
    subparser.add_argument(
        '--overwrite', action='store_true',
        help="reinstall an existing spec, even if it has dependents")
    subparser.add_argument(
        '--keep-prefix', action='store_true',
        help="don't remove the install prefix if installation fails")
    subparser.add_argument(
        '--keep-stage', action='store_true',
        help="don't remove the build stage if installation succeeds")
    subparser.add_argument(
        '--dont-restage', action='store_true',
        help="if a partial install is detected, don't delete prior state")

    cache_group = subparser.add_mutually_exclusive_group()
    cache_group.add_argument(
        '--use-cache', action='store_true', dest='use_cache', default=True,
        help="check for pre-built Spack packages in mirrors (default)")
    cache_group.add_argument(
        '--no-cache', action='store_false', dest='use_cache', default=True,
        help="do not check for pre-built Spack packages in mirrors")

    subparser.add_argument(
        '--show-log-on-error', action='store_true',
        help="print full build log to stderr if build fails")
    subparser.add_argument(
        '--source', action='store_true', dest='install_source',
        help="install source files in prefix")
    arguments.add_common_arguments(subparser, ['no_checksum'])
    subparser.add_argument(
        '-v', '--verbose', action='store_true',
        help="display verbose build output while installing")
    subparser.add_argument(
        '--fake', action='store_true',
        help="fake install for debug purposes.")
    subparser.add_argument(
        '--only-concrete', action='store_true', default=False,
        help='(with environment) only install already concretized specs')
    subparser.add_argument(
        '-f', '--file', action='append', default=[],
        dest='specfiles', metavar='SPEC_YAML_FILE',
        help="install from file. Read specs to install from .yaml files")

    cd_group = subparser.add_mutually_exclusive_group()
    arguments.add_common_arguments(cd_group, ['clean', 'dirty'])

    subparser.add_argument(
        'package',
        nargs=argparse.REMAINDER,
        help="spec of the package to install"
    )
    testing = subparser.add_mutually_exclusive_group()
    testing.add_argument(
        '--test', default=None,
        choices=['root', 'all'],
        help="""If 'root' is chosen, run package tests during
installation for top-level packages (but skip tests for dependencies).
if 'all' is chosen, run package tests during installation for all
packages. If neither are chosen, don't run tests for any packages."""
    )
    testing.add_argument(
        '--run-tests', action='store_true',
        help='run package tests during installation (same as --test=all)'
    )
    subparser.add_argument(
        '--log-format',
        default=None,
        choices=spack.report.valid_formats,
        help="format to be used for log files"
    )
    subparser.add_argument(
        '--log-file',
        default=None,
        help="filename for the log file. if not passed a default will be used"
    )
    subparser.add_argument(
        '--cdash-upload-url',
        default=None,
        help="CDash URL where reports will be uploaded"
    )
    subparser.add_argument(
        '--cdash-build',
        default=None,
        help="""The name of the build that will be reported to CDash.
Defaults to spec of the package to install."""
    )
    subparser.add_argument(
        '--cdash-site',
        default=None,
        help="""The site name that will be reported to CDash.
Defaults to current system hostname."""
    )
    subparser.add_argument(
        '--cdash-track',
        default='Experimental',
        help="""Results will be reported to this group on CDash.
Defaults to Experimental."""
    )
    arguments.add_common_arguments(subparser, ['yes_to_all'])


def default_log_file(spec):
    """Computes the default filename for the log file and creates
    the corresponding directory if not present
    """
    fmt = 'test-{x.name}-{x.version}-{hash}.xml'
    basename = fmt.format(x=spec, hash=spec.dag_hash())
    dirname = fs.os.path.join(spack.paths.var_path, 'junit-report')
    fs.mkdirp(dirname)
    return fs.os.path.join(dirname, basename)


def install_spec(cli_args, kwargs, abstract_spec, spec):
    """Do the actual installation."""
    # handle active environment, if any
    def install(spec, kwargs):
        env = ev.get_env(cli_args, 'install')
        if env:
            env.install(abstract_spec, spec, **kwargs)
            env.write()
        else:
            spec.package.do_install(**kwargs)

    try:
        if cli_args.things_to_install == 'dependencies':
            # Install dependencies as-if they were installed
            # for root (explicit=False in the DB)
            kwargs['explicit'] = False
            for s in spec.dependencies():
                install(s, kwargs)
        else:
            kwargs['explicit'] = True
            install(spec, kwargs)

    except spack.build_environment.InstallError as e:
        if cli_args.show_log_on_error:
            e.print_context()
            if not os.path.exists(e.pkg.build_log_path):
                tty.error("'spack install' created no log.")
            else:
                sys.stderr.write('Full build log:\n')
                with open(e.pkg.build_log_path) as log:
                    shutil.copyfileobj(log, sys.stderr)
        raise


def install(parser, args, **kwargs):
    if not args.package and not args.specfiles:
        # if there are no args but an active environment or spack.yaml file
        # then install the packages from it.
        env = ev.get_env(args, 'install')
        if env:
            if not args.only_concrete:
                env.concretize()
                env.write()
            tty.msg("Installing environment %s" % env.name)
            env.install_all(args)
            return
        else:
            tty.die("install requires a package argument or a spack.yaml file")

    if args.jobs is not None:
        if args.jobs <= 0:
            tty.die("The -j option must be a positive integer!")

    if args.no_checksum:
        spack.config.set('config:checksum', False, scope='command_line')

    # Parse cli arguments and construct a dictionary
    # that will be passed to Package.do_install API
    update_kwargs_from_args(args, kwargs)
    kwargs.update({
        'install_deps': ('dependencies' in args.things_to_install),
        'install_package': ('package' in args.things_to_install)
    })

    if args.run_tests:
        tty.warn("Deprecated option: --run-tests: use --test=all instead")

    # 1. Abstract specs from cli
    reporter = spack.report.collect_info(args.log_format, args)
    if args.log_file:
        reporter.filename = args.log_file

    abstract_specs = spack.cmd.parse_specs(args.package)
    tests = False
    if args.test == 'all' or args.run_tests:
        tests = True
    elif args.test == 'root':
        tests = [spec.name for spec in abstract_specs]
    kwargs['tests'] = tests

    try:
        specs = spack.cmd.parse_specs(
            args.package, concretize=True, tests=tests)
    except SpackError as e:
        reporter.concretization_report(e.message)
        raise

    # 2. Concrete specs from yaml files
    for file in args.specfiles:
        with open(file, 'r') as f:
            s = spack.spec.Spec.from_yaml(f)

        if s.concretized().dag_hash() != s.dag_hash():
            msg = 'skipped invalid file "{0}". '
            msg += 'The file does not contain a concrete spec.'
            tty.warn(msg.format(file))
            continue

        abstract_specs.append(s)
        specs.append(s.concretized())

    if len(specs) == 0:
        tty.die('The `spack install` command requires a spec to install.')

    if not args.log_file and not reporter.filename:
        reporter.filename = default_log_file(specs[0])
    reporter.specs = specs
    with reporter:
        if args.overwrite:

            installed = list(filter(lambda x: x,
                                    map(spack.store.db.query_one, specs)))
            if not args.yes_to_all:
                display_args = {
                    'long': True,
                    'show_flags': True,
                    'variants': True
                }

                if installed:
                    tty.msg('The following package specs will be '
                            'reinstalled:\n')
                    spack.cmd.display_specs(installed, **display_args)

                not_installed = list(filter(lambda x: x not in installed,
                                            specs))
                if not_installed:
                    tty.msg('The following package specs are not installed and'
                            ' the --overwrite flag was given. The package spec'
                            ' will be newly installed:\n')
                    spack.cmd.display_specs(not_installed, **display_args)

                # We have some specs, so one of the above must have been true
                answer = tty.get_yes_or_no(
                    'Do you want to proceed?', default=False
                )
                if not answer:
                    tty.die('Reinstallation aborted.')

            for abstract, concrete in zip(abstract_specs, specs):
                if concrete in installed:
                    with fs.replace_directory_transaction(concrete.prefix):
                        install_spec(args, kwargs, abstract, concrete)
                else:
                    install_spec(args, kwargs, abstract, concrete)

        else:
            for abstract, concrete in zip(abstract_specs, specs):
                install_spec(args, kwargs, abstract, concrete)
