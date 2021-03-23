# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from __future__ import print_function

import collections
import os
import shutil

import llnl.util.filesystem as fs
import llnl.util.tty as tty
import spack.config
import spack.cmd.common.arguments
import spack.schema.env
import spack.environment as ev
import spack.schema.packages
import spack.util.spack_yaml as syaml
from spack.util.editor import editor
import spack.store
import spack.repo

description = "get and set configuration options"
section = "config"
level = "long"


def setup_parser(subparser):
    scopes = spack.config.scopes()
    scopes_metavar = spack.config.scopes_metavar

    # User can only choose one
    subparser.add_argument(
        '--scope', choices=scopes, metavar=scopes_metavar,
        help="configuration scope to read/modify")

    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='config_command')

    get_parser = sp.add_parser('get', help='print configuration values')
    get_parser.add_argument('section',
                            help="configuration section to print. "
                                 "options: %(choices)s",
                            nargs='?',
                            metavar='section',
                            choices=spack.config.section_schemas)

    blame_parser = sp.add_parser(
        'blame', help='print configuration annotated with source file:line')
    blame_parser.add_argument('section',
                              help="configuration section to print. "
                              "options: %(choices)s",
                              metavar='section',
                              choices=spack.config.section_schemas)

    edit_parser = sp.add_parser('edit', help='edit configuration file')
    edit_parser.add_argument('section',
                             help="configuration section to edit. "
                                  "options: %(choices)s",
                             metavar='section',
                             nargs='?',
                             choices=spack.config.section_schemas)
    edit_parser.add_argument(
        '--print-file', action='store_true',
        help="print the file name that would be edited")

    sp.add_parser('list', help='list configuration sections')

    add_parser = sp.add_parser('add', help='add configuration parameters')
    add_parser.add_argument(
        'path', nargs='?',
        help="colon-separated path to config that should be added,"
        " e.g. 'config:default:true'")
    add_parser.add_argument(
        '-f', '--file',
        help="file from which to set all config values"
    )

    prefer_upstream_parser = sp.add_parser(
        'prefer-upstream',
        help='set package preferences from upstream')

    prefer_upstream_parser.add_argument(
        '--local', action='store_true', default=False,
        help="Set packages preferences based on local installs, rather "
             "than upstream."
    )

    remove_parser = sp.add_parser('remove', aliases=['rm'],
                                  help='remove configuration parameters')
    remove_parser.add_argument(
        'path',
        help="colon-separated path to config that should be removed,"
        " e.g. 'config:default:true'")

    # Make the add parser available later
    setup_parser.add_parser = add_parser

    update = sp.add_parser(
        'update', help='update configuration files to the latest format'
    )
    spack.cmd.common.arguments.add_common_arguments(update, ['yes_to_all'])
    update.add_argument('section', help='section to update')

    revert = sp.add_parser(
        'revert',
        help='revert configuration files to their state before update'
    )
    spack.cmd.common.arguments.add_common_arguments(revert, ['yes_to_all'])
    revert.add_argument('section', help='section to update')


def _get_scope_and_section(args):
    """Extract config scope and section from arguments."""
    scope = args.scope
    section = getattr(args, 'section', None)
    path = getattr(args, 'path', None)

    # w/no args and an active environment, point to env manifest
    if not section:
        env = ev.get_env(args, 'config edit')
        if env:
            scope = env.env_file_config_scope_name()

    # set scope defaults
    elif not scope:
        scope = spack.config.default_modify_scope(section)

    # special handling for commands that take value instead of section
    if path:
        section = path[:path.find(':')] if ':' in path else path
        if not scope:
            scope = spack.config.default_modify_scope(section)

    return scope, section


def config_get(args):
    """Dump merged YAML configuration for a specific section.

    With no arguments and an active environment, print the contents of
    the environment's manifest file (spack.yaml).
    """
    scope, section = _get_scope_and_section(args)

    if scope and scope.startswith('env:'):
        config_file = spack.config.config.get_config_filename(scope, section)
        if os.path.exists(config_file):
            with open(config_file) as f:
                print(f.read())
        else:
            tty.die('environment has no %s file' % ev.manifest_name)

    elif section is not None:
        spack.config.config.print_section(section)

    else:
        tty.die('`spack config get` requires a section argument '
                'or an active environment.')


def config_blame(args):
    """Print out line-by-line blame of merged YAML."""
    spack.config.config.print_section(args.section, blame=True)


def config_edit(args):
    """Edit the configuration file for a specific scope and config section.

    With no arguments and an active environment, edit the spack.yaml for
    the active environment.
    """
    scope, section = _get_scope_and_section(args)
    if not scope and not section:
        tty.die('`spack config edit` requires a section argument '
                'or an active environment.')

    config_file = spack.config.config.get_config_filename(scope, section)
    if args.print_file:
        print(config_file)
    else:
        editor(config_file)


def config_list(args):
    """List the possible configuration sections.

    Used primarily for shell tab completion scripts.
    """
    print(' '.join(list(spack.config.section_schemas)))


def config_add(args):
    """Add the given configuration to the specified config scope

    This is a stateful operation that edits the config files."""
    if not (args.file or args.path):
        tty.error("No changes requested. Specify a file or value.")
        setup_parser.add_parser.print_help()
        exit(1)

    scope, section = _get_scope_and_section(args)

    if args.file:
        spack.config.add_from_file(args.file, scope=scope)

    if args.path:
        spack.config.add(args.path, scope=scope)


def config_remove(args):
    """Remove the given configuration from the specified config scope

    This is a stateful operation that edits the config files."""
    scope, _ = _get_scope_and_section(args)

    path, _, value = args.path.rpartition(':')
    existing = spack.config.get(path, scope=scope)

    if not isinstance(existing, (list, dict)):
        path, _, value = path.rpartition(':')
        existing = spack.config.get(path, scope=scope)

    value = syaml.load(value)

    if isinstance(existing, list):
        values = value if isinstance(value, list) else [value]
        for v in values:
            existing.remove(v)
    elif isinstance(existing, dict):
        existing.pop(value, None)
    else:
        # This should be impossible to reach
        raise spack.config.ConfigError('Config has nested non-dict values')

    spack.config.set(path, existing, scope)


def _can_update_config_file(scope_dir, cfg_file):
    dir_ok = fs.can_write_to_dir(scope_dir)
    cfg_ok = fs.can_access(cfg_file)
    return dir_ok and cfg_ok


def config_update(args):
    # Read the configuration files
    spack.config.config.get_config(args.section, scope=args.scope)
    updates = spack.config.config.format_updates[args.section]

    cannot_overwrite, skip_system_scope = [], False
    for scope in updates:
        cfg_file = spack.config.config.get_config_filename(
            scope.name, args.section
        )
        scope_dir = scope.path
        can_be_updated = _can_update_config_file(scope_dir, cfg_file)
        if not can_be_updated:
            if scope.name == 'system':
                skip_system_scope = True
                msg = ('Not enough permissions to write to "system" scope. '
                       'Skipping update at that location [cfg={0}]')
                tty.warn(msg.format(cfg_file))
                continue
            cannot_overwrite.append((scope, cfg_file))

    if cannot_overwrite:
        msg = 'Detected permission issues with the following scopes:\n\n'
        for scope, cfg_file in cannot_overwrite:
            msg += '\t[scope={0}, cfg={1}]\n'.format(scope.name, cfg_file)
        msg += ('\nEither ensure that you have sufficient permissions to '
                'modify these files or do not include these scopes in the '
                'update.')
        tty.die(msg)

    if skip_system_scope:
        updates = [x for x in updates if x.name != 'system']

    # Report if there are no updates to be done
    if not updates:
        msg = 'No updates needed for "{0}" section.'
        tty.msg(msg.format(args.section))
        return

    proceed = True
    if not args.yes_to_all:
        msg = ('The following configuration files are going to be updated to'
               ' the latest schema format:\n\n')
        for scope in updates:
            cfg_file = spack.config.config.get_config_filename(
                scope.name, args.section
            )
            msg += '\t[scope={0}, file={1}]\n'.format(scope.name, cfg_file)
        msg += ('\nIf the configuration files are updated, versions of Spack '
                'that are older than this version may not be able to read '
                'them. Spack stores backups of the updated files which can '
                'be retrieved with "spack config revert"')
        tty.msg(msg)
        proceed = tty.get_yes_or_no('Do you want to proceed?', default=False)

    if not proceed:
        tty.die('Operation aborted.')

    # Get a function to update the format
    update_fn = spack.config.ensure_latest_format_fn(args.section)
    for scope in updates:
        cfg_file = spack.config.config.get_config_filename(
            scope.name, args.section
        )
        with open(cfg_file) as f:
            data = syaml.load_config(f) or {}
            data = data.pop(args.section, {})
        update_fn(data)

        # Make a backup copy and rewrite the file
        bkp_file = cfg_file + '.bkp'
        shutil.copy(cfg_file, bkp_file)
        spack.config.config.update_config(
            args.section, data, scope=scope.name, force=True
        )
        msg = 'File "{0}" updated [backup={1}]'
        tty.msg(msg.format(cfg_file, bkp_file))


def _can_revert_update(scope_dir, cfg_file, bkp_file):
    dir_ok = fs.can_write_to_dir(scope_dir)
    cfg_ok = not os.path.exists(cfg_file) or fs.can_access(cfg_file)
    bkp_ok = fs.can_access(bkp_file)
    return dir_ok and cfg_ok and bkp_ok


def config_revert(args):
    scopes = [args.scope] if args.scope else [
        x.name for x in spack.config.config.file_scopes
    ]

    # Search for backup files in the configuration scopes
    Entry = collections.namedtuple('Entry', ['scope', 'cfg', 'bkp'])
    to_be_restored, cannot_overwrite = [], []
    for scope in scopes:
        cfg_file = spack.config.config.get_config_filename(scope, args.section)
        bkp_file = cfg_file + '.bkp'

        # If the backup files doesn't exist move to the next scope
        if not os.path.exists(bkp_file):
            continue

        # If it exists and we don't have write access in this scope
        # keep track of it and report a comprehensive error later
        entry = Entry(scope, cfg_file, bkp_file)
        scope_dir = os.path.dirname(bkp_file)
        can_be_reverted = _can_revert_update(scope_dir, cfg_file, bkp_file)
        if not can_be_reverted:
            cannot_overwrite.append(entry)
            continue

        to_be_restored.append(entry)

    # Report errors if we can't revert a configuration
    if cannot_overwrite:
        msg = 'Detected permission issues with the following scopes:\n\n'
        for e in cannot_overwrite:
            msg += '\t[scope={0.scope}, cfg={0.cfg}, bkp={0.bkp}]\n'.format(e)
        msg += ('\nEither ensure to have the right permissions before retrying'
                ' or be more specific on the scope to revert.')
        tty.die(msg)

    proceed = True
    if not args.yes_to_all:
        msg = ('The following scopes will be restored from the corresponding'
               ' backup files:\n')
        for entry in to_be_restored:
            msg += '\t[scope={0.scope}, bkp={0.bkp}]\n'.format(entry)
        msg += 'This operation cannot be undone.'
        tty.msg(msg)
        proceed = tty.get_yes_or_no('Do you want to proceed?', default=False)

    if not proceed:
        tty.die('Operation aborted.')

    for _, cfg_file, bkp_file in to_be_restored:
        shutil.copy(bkp_file, cfg_file)
        os.unlink(bkp_file)
        msg = 'File "{0}" reverted to old state'
        tty.msg(msg.format(cfg_file))


def config_prefer_upstream(args):
    """Generate a packages config based on the configuration of all upstream
    installs."""

    scope = args.scope
    if scope is None:
        scope = spack.config.default_modify_scope('packages')

    all_specs = set(spack.store.db.query(installed=True))
    local_specs = set(spack.store.db.query_local(installed=True))
    pref_specs = local_specs if args.local else all_specs - local_specs

    conflicting_variants = set()

    pkgs = {}
    for spec in pref_specs:
        # Collect all the upstream compilers and versions for this package.
        pkg = pkgs.get(spec.name, {
            'version': [],
            'compiler': [],
        })
        pkgs[spec.name] = pkg

        # We have no existing variant if this is our first added version.
        existing_variants = pkg.get('variants',
                                    None if not pkg['version'] else '')

        version = spec.version.string
        if version not in pkg['version']:
            pkg['version'].append(version)

        compiler = str(spec.compiler)
        if compiler not in pkg['compiler']:
            pkg['compiler'].append(compiler)

        # Get and list all the variants that differ from the default.
        variants = []
        for var_name, variant in spec.variants.items():
            if (var_name in ['patches']
                    or var_name not in spec.package.variants):
                continue

            if variant.value != spec.package.variants[var_name].default:
                variants.append(str(variant))
        variants.sort()
        variants = ' '.join(variants)

        if spec.name not in conflicting_variants:
            # Only specify the variants if there's a single variant
            # set across all versions/compilers.
            if existing_variants is not None and existing_variants != variants:
                conflicting_variants.add(spec.name)
                pkg.pop('variants', None)
            elif variants:
                pkg['variants'] = variants

    if conflicting_variants:
        tty.warn(
            "The following packages have multiple conflicting upstream "
            "specs. You may have to specify, by "
            "concretized hash, which spec you want when building "
            "packages that depend on them:\n - {0}"
            .format("\n - ".join(sorted(conflicting_variants))))

    # Simply write the config to the specified file.
    existing = spack.config.get('packages', scope=scope)
    new = spack.config.merge_yaml(existing, pkgs)
    spack.config.set('packages', new, scope)
    config_file = spack.config.config.get_config_filename(scope, section)

    tty.msg("Updated config at {0}".format(config_file))


def config(parser, args):
    action = {
        'get': config_get,
        'blame': config_blame,
        'edit': config_edit,
        'list': config_list,
        'add': config_add,
        'rm': config_remove,
        'remove': config_remove,
        'update': config_update,
        'revert': config_revert,
        'prefer-upstream': config_prefer_upstream,
    }
    action[args.config_command](args)
