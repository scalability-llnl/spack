# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import os
import shutil
import sys
import textwrap
import logging
import logging.config

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
import spack.util.spack_yaml as syaml


description = "build and install packages"
section = "build"
level = "short"


def update_kwargs_from_args(args, kwargs):
    """Parse cli arguments and construct a dictionary
    that will be passed to Package.do_install API"""

    kwargs.update({
        'fail_fast': args.fail_fast,
        'keep_prefix': args.keep_prefix,
        'keep_stage': args.keep_stage,
        'restage': not args.dont_restage,
        'install_source': args.install_source,
        'verbose': args.verbose,
        'fake': args.fake,
        'dirty': args.dirty,
        'use_cache': args.use_cache,
        'install_global': args.install_global,
        'upstream': args.upstream,
        'cache_only': args.cache_only,
        'explicit': True,  # Always true for install command
        'stop_at': args.until,
        'unsigned': args.unsigned,
    })

    kwargs.update({
        'install_deps': ('dependencies' in args.things_to_install),
        'install_package': ('package' in args.things_to_install)
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
    subparser.add_argument(
        '-u', '--until', type=str, dest='until', default=None,
        help="phase to stop after when installing (default None)")
    arguments.add_common_arguments(subparser, ['jobs'])
    subparser.add_argument(
        '--overwrite', action='store_true',
        help="reinstall an existing spec, even if it has dependents")
    subparser.add_argument(
        '--fail-fast', action='store_true',
        help="stop all builds if any build fails (default is best effort)")
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
    cache_group.add_argument(
        '--cache-only', action='store_true', dest='cache_only', default=False,
        help="only install package from binary mirrors")

    subparser.add_argument(
        '--no-check-signature', action='store_true',
        dest='unsigned', default=False,
        help="do not check signatures of binary packages")
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
    subparser.add_argument(
        '--upstream', action='store', default=None,
        dest='upstream', metavar='UPSTREAM_NAME',
        help='specify which upstream spack to install too')
    subparser.add_argument(
        '-g', '--global', action='store_true', default=False,
        dest='install_global',
        help='install package to globally accesible location')

    cd_group = subparser.add_mutually_exclusive_group()
    arguments.add_common_arguments(cd_group, ['clean', 'dirty'])

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
        '--help-cdash',
        action='store_true',
        help="Show usage instructions for CDash reporting"
    )
    add_cdash_args(subparser, False)
    arguments.add_common_arguments(subparser, ['yes_to_all', 'spec'])


def add_cdash_args(subparser, add_help):
    cdash_help = {}
    if add_help:
        cdash_help['upload-url'] = "CDash URL where reports will be uploaded"
        cdash_help['build'] = """The name of the build that will be reported to CDash.
Defaults to spec of the package to install."""
        cdash_help['site'] = """The site name that will be reported to CDash.
Defaults to current system hostname."""
        cdash_help['track'] = """Results will be reported to this group on CDash.
Defaults to Experimental."""
        cdash_help['buildstamp'] = """Instead of letting the CDash reporter prepare the
buildstamp which, when combined with build name, site and project,
uniquely identifies the build, provide this argument to identify
the build yourself.  Format: %%Y%%m%%d-%%H%%M-[cdash-track]"""
    else:
        cdash_help['upload-url'] = argparse.SUPPRESS
        cdash_help['build'] = argparse.SUPPRESS
        cdash_help['site'] = argparse.SUPPRESS
        cdash_help['track'] = argparse.SUPPRESS
        cdash_help['buildstamp'] = argparse.SUPPRESS

    subparser.add_argument(
        '--cdash-upload-url',
        default=None,
        help=cdash_help['upload-url']
    )
    subparser.add_argument(
        '--cdash-build',
        default=None,
        help=cdash_help['build']
    )
    subparser.add_argument(
        '--cdash-site',
        default=None,
        help=cdash_help['site']
    )

    cdash_subgroup = subparser.add_mutually_exclusive_group()
    cdash_subgroup.add_argument(
        '--cdash-track',
        default='Experimental',
        help=cdash_help['track']
    )
    cdash_subgroup.add_argument(
        '--cdash-buildstamp',
        default=None,
        help=cdash_help['buildstamp']
    )


def default_log_file(spec):
    """Computes the default filename for the log file and creates
    the corresponding directory if not present
    """
    fmt = 'test-{x.name}-{x.version}-{hash}.xml'
    basename = fmt.format(x=spec, hash=spec.dag_hash())

    dirname = fs.os.path.join(spack.paths.user_config_path,
                              'var/spack',
                              'junit-report')
    fs.mkdirp(dirname)
    return fs.os.path.join(dirname, basename)


def install_spec(cli_args, kwargs, abstract_spec, spec):
    """Do the actual installation."""

    try:
        # Handle metrics logging if enabled
        if spack.config.get('config:metrics'):
            # Logs spec to install to syslog for metrics collection
            config_path = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(config_path, '../metrics_logger.yaml')
            with open(config_path, 'r') as f:
                yaml_dict = syaml.load(f)
            logging.config.dictConfig(yaml_dict)
            if sys.platform == 'darwin':
                if spack.config.get('config:metrics_address'):
                    addr = spack.config.get('config:metrics_address')
                    yaml_dict['handlers']['handler_darwin']['address'] = addr
                logger = logging.getLogger('metrics_darwin')
            else:
                if spack.config.get('config:metrics_address'):
                    addr = spack.config.get('config:metrics_address')
                    yaml_dict['handlers']['handler_linux']['address'] = addr
                logger = logging.getLogger('metrics_linux')
            logger.info("SPACK_INSTALL: " + str(spec))

        # handle active environment, if any
        env = ev.get_env(cli_args, 'install')

        if env:
            with env.write_transaction():
                concrete = env.concretize_and_add(
                    abstract_spec, spec)
                env.write(regenerate_views=False)
            env._install(concrete, **kwargs)
            with env.write_transaction():
                env.regenerate_views()
        else:
            spec.package.do_install(**kwargs)
        spack.config.set('config:active_tree', '~/.spack/opt/spack',
                         scope='user')
        spack.config.set('config:active_upstream', None,
                         scope='user')

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
    # Install Package to Global Upstream for multi-user use
    if args.install_global:
        spack.config.set('config:active_upstream', 'global',
                         scope='user')
        global_root = spack.config.get('upstreams')
        global_root = global_root['global']['install_tree']
        global_root = spack.util.path.canonicalize_path(global_root)
        spack.config.set('config:active_tree', global_root,
                         scope='user')
    elif args.upstream:
        if args.upstream not in spack.config.get('upstreams'):
            tty.die("specified upstream does not exist")
        spack.config.set('config:active_upstream', args.upstream,
                         scope='user')
        root = spack.config.get('upstreams')
        root = root[args.upstream]['install_tree']
        root = spack.util.path.canonicalize_path(root)
        spack.config.set('config:active_tree', root, scope='user')
    else:
        spack.config.set('config:active_upstream', None,
                         scope='user')
        spack.config.set('config:active_tree',
                         spack.config.get('config:install_tree'),
                         scope='user')
    if args.help_cdash:
        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=textwrap.dedent('''\
environment variables:
  SPACK_CDASH_AUTH_TOKEN
                        authentication token to present to CDash
                        '''))
        add_cdash_args(parser, True)
        parser.print_help()
        return

    if not args.spec and not args.specfiles:
        # if there are no args but an active environment or spack.yaml file
        # then install the packages from it.
        env = ev.get_env(args, 'install')
        if env:
            if not args.only_concrete:
                with env.write_transaction():
                    concretized_specs = env.concretize()
                    ev.display_specs(concretized_specs)

                    # save view regeneration for later, so that we only do it
                    # once, as it can be slow.
                    env.write(regenerate_views=False)

            tty.msg("Installing environment %s" % env.name)
            env.install_all(args)
            with env.write_transaction():
                # It is not strictly required to synchronize view regeneration
                # but doing so can prevent redundant work in the filesystem.
                env.regenerate_views()
            return
        else:
            tty.die("install requires a package argument or a spack.yaml file")

    if args.no_checksum:
        spack.config.set('config:checksum', False, scope='command_line')

    # Parse cli arguments and construct a dictionary
    # that will be passed to Package.do_install API
    update_kwargs_from_args(args, kwargs)

    if args.run_tests:
        tty.warn("Deprecated option: --run-tests: use --test=all instead")

    # 1. Abstract specs from cli
    reporter = spack.report.collect_info(args.log_format, args)
    if args.log_file:
        reporter.filename = args.log_file

    abstract_specs = spack.cmd.parse_specs(args.spec)
    tests = False
    if args.test == 'all' or args.run_tests:
        tests = True
    elif args.test == 'root':
        tests = [spec.name for spec in abstract_specs]
    kwargs['tests'] = tests

    try:
        specs = spack.cmd.parse_specs(
            args.spec, concretize=True, tests=tests)
    except SpackError as e:
        tty.debug(e)
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
