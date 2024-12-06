# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import collections
import os
import shutil
import sys
from typing import List

import llnl.util.filesystem as fs
import llnl.util.tty as tty

import spack.config
import spack.environment as ev
import spack.error
import spack.schema.env
import spack.spec
import spack.store
import spack.util.spack_yaml as syaml
from spack.cmd.common import arguments
from spack.util.editor import editor

description = "get and set configuration options"
section = "config"
level = "long"


def setup_parser(subparser):
    # User can only choose one
    subparser.add_argument(
        "--scope", action=arguments.ConfigScope, help="configuration scope to read/modify"
    )

    sp = subparser.add_subparsers(metavar="SUBCOMMAND", dest="config_command")

    get_parser = sp.add_parser("get", help="print configuration values")
    get_parser.add_argument(
        "section",
        help="configuration section to print\n\noptions: %(choices)s",
        nargs="?",
        metavar="section",
        choices=spack.config.SECTION_SCHEMAS,
    )

    blame_parser = sp.add_parser(
        "blame", help="print configuration annotated with source file:line"
    )
    blame_parser.add_argument(
        "section",
        help="configuration section to print\n\noptions: %(choices)s",
        nargs="?",
        metavar="section",
        choices=spack.config.SECTION_SCHEMAS,
    )

    edit_parser = sp.add_parser("edit", help="edit configuration file")
    edit_parser.add_argument(
        "section",
        help="configuration section to edit\n\noptions: %(choices)s",
        metavar="section",
        nargs="?",
        choices=spack.config.SECTION_SCHEMAS,
    )
    edit_parser.add_argument(
        "--print-file", action="store_true", help="print the file name that would be edited"
    )

    sp.add_parser("list", help="list configuration sections")

    add_parser = sp.add_parser("add", help="add configuration parameters")
    add_parser.add_argument(
        "path",
        nargs="?",
        help="colon-separated path to config that should be added, e.g. 'config:default:true'",
    )
    add_parser.add_argument("-f", "--file", help="file from which to set all config values")

    change_parser = sp.add_parser("change", help="swap variants etc. on specs in config")
    change_parser.add_argument("path", help="colon-separated path to config section with specs")
    change_parser.add_argument("--match-spec", help="only change constraints that match this")

    prefer_upstream_parser = sp.add_parser(
        "prefer-upstream", help="set package preferences from upstream"
    )

    prefer_upstream_parser.add_argument(
        "--local",
        action="store_true",
        default=False,
        help="set packages preferences based on local installs, rather than upstream",
    )

    remove_parser = sp.add_parser("remove", aliases=["rm"], help="remove configuration parameters")
    remove_parser.add_argument(
        "path",
        help="colon-separated path to config that should be removed,"
        " e.g. 'config:default:true'",
    )

    # Make the add parser available later
    setup_parser.add_parser = add_parser

    update = sp.add_parser("update", help="update configuration files to the latest format")
    arguments.add_common_arguments(update, ["yes_to_all"])
    update.add_argument("section", help="section to update")

    revert = sp.add_parser(
        "revert", help="revert configuration files to their state before update"
    )
    arguments.add_common_arguments(revert, ["yes_to_all"])
    revert.add_argument("section", help="section to update")


def _get_scope_and_section(args):
    """Extract config scope and section from arguments."""
    scope = args.scope
    section = getattr(args, "section", None)
    path = getattr(args, "path", None)

    # w/no args and an active environment, point to env manifest
    if not section and not scope:
        env = ev.active_environment()
        if env:
            scope = env.scope_name

    # set scope defaults
    elif not scope:
        scope = spack.config.default_modify_scope(section)

    # special handling for commands that take value instead of section
    if path:
        section = path[: path.find(":")] if ":" in path else path
        if not scope:
            scope = spack.config.default_modify_scope(section)

    return scope, section


def print_configuration(args, *, blame: bool) -> None:
    if args.scope and args.section is None:
        tty.die(f"the argument --scope={args.scope} requires specifying a section.")

    if args.section is not None:
        spack.config.CONFIG.print_section(args.section, blame=blame, scope=args.scope)
        return

    print_flattened_configuration(blame=blame)


def print_flattened_configuration(*, blame: bool) -> None:
    """Prints to stdout a flattened version of the configuration.

    Args:
        blame: if True, shows file provenance for each entry in the configuration.
    """
    env = ev.active_environment()
    if env is not None:
        pristine = env.manifest.yaml_content
        flattened = pristine.copy()
        flattened[spack.schema.env.TOP_LEVEL_KEY] = pristine[spack.schema.env.TOP_LEVEL_KEY].copy()
    else:
        flattened = syaml.syaml_dict()
        flattened[spack.schema.env.TOP_LEVEL_KEY] = syaml.syaml_dict()

    for config_section in spack.config.SECTION_SCHEMAS:
        current = spack.config.get(config_section)
        flattened[spack.schema.env.TOP_LEVEL_KEY][config_section] = current
    syaml.dump_config(flattened, stream=sys.stdout, default_flow_style=False, blame=blame)


def config_get(args):
    """Dump merged YAML configuration for a specific section.

    With no arguments and an active environment, print the contents of
    the environment's manifest file (spack.yaml).
    """
    print_configuration(args, blame=False)


def config_blame(args):
    """Print out line-by-line blame of merged YAML."""
    print_configuration(args, blame=True)


def config_edit(args):
    """Edit the configuration file for a specific scope and config section.

    With no arguments and an active environment, edit the spack.yaml for
    the active environment.
    """
    spack_env = os.environ.get(ev.spack_env_var)
    if spack_env and not args.scope:
        # Don't use the scope object for envs, as `config edit` can be called
        # for a malformed environment. Use SPACK_ENV to find spack.yaml.
        config_file = ev.manifest_file(spack_env)
    else:
        # If we aren't editing a spack.yaml file, get config path from scope.
        scope, section = _get_scope_and_section(args)
        if not scope and not section:
            tty.die("`spack config edit` requires a section argument or an active environment.")
        config_file = spack.config.CONFIG.get_config_filename(scope, section)

    if args.print_file:
        print(config_file)
    else:
        editor(config_file)


def config_list(args):
    """List the possible configuration sections.

    Used primarily for shell tab completion scripts.
    """
    print(" ".join(list(spack.config.SECTION_SCHEMAS)))


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

    path, _, value = args.path.rpartition(":")
    existing = spack.config.get(path, scope=scope)

    if not isinstance(existing, (list, dict)):
        path, _, value = path.rpartition(":")
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
        raise spack.error.ConfigError("Config has nested non-dict values")

    spack.config.set(path, existing, scope)


def _can_update_config_file(scope: spack.config.ConfigScope, cfg_file):
    if isinstance(scope, spack.config.SingleFileScope):
        return fs.can_access(cfg_file)
    elif isinstance(scope, spack.config.DirectoryConfigScope):
        return fs.can_write_to_dir(scope.path) and fs.can_access(cfg_file)
    return False


def _config_change_requires_scope(path, spec, scope, match_spec=None):
    """Return whether or not anything changed."""
    require = spack.config.get(path, scope=scope)
    if not require:
        return False

    changed = False

    def override_cfg_spec(spec_str):
        nonlocal changed

        init_spec = spack.spec.Spec(spec_str)
        # Overridden spec cannot be anonymous
        init_spec.name = spec.name
        if match_spec and not init_spec.satisfies(match_spec):
            # If there is a match_spec, don't change constraints that
            # don't match it
            return spec_str
        elif not init_spec.intersects(spec):
            changed = True
            return str(spack.spec.Spec.override(init_spec, spec))
        else:
            # Don't override things if they intersect, otherwise we'd
            # be e.g. attaching +debug to every single version spec
            return spec_str

    if isinstance(require, str):
        new_require = override_cfg_spec(require)
    else:
        new_require = []
        for item in require:
            if "one_of" in item:
                item["one_of"] = [override_cfg_spec(x) for x in item["one_of"]]
            elif "any_of" in item:
                item["any_of"] = [override_cfg_spec(x) for x in item["any_of"]]
            elif "spec" in item:
                item["spec"] = override_cfg_spec(item["spec"])
            elif isinstance(item, str):
                item = override_cfg_spec(item)
            else:
                raise ValueError(f"Unexpected requirement: ({type(item)}) {str(item)}")
            new_require.append(item)

    spack.config.set(path, new_require, scope=scope)
    return changed


def _config_change(config_path, match_spec_str=None):
    all_components = spack.config.process_config_path(config_path)
    key_components = all_components[:-1]
    key_path = ":".join(key_components)

    spec = spack.spec.Spec(syaml.syaml_str(all_components[-1]))

    match_spec = None
    if match_spec_str:
        match_spec = spack.spec.Spec(match_spec_str)

    if key_components[-1] == "require":
        # Extract the package name from the config path, which allows
        # args.spec to be anonymous if desired
        pkg_name = key_components[1]
        spec.name = pkg_name

        changed = False
        for scope in spack.config.writable_scope_names():
            changed |= _config_change_requires_scope(key_path, spec, scope, match_spec=match_spec)

        if not changed:
            existing_requirements = spack.config.get(key_path)
            if isinstance(existing_requirements, str):
                raise spack.error.ConfigError(
                    "'config change' needs to append a requirement,"
                    " but existing require: config is not a list"
                )

            ideal_scope_to_modify = None
            for scope in spack.config.writable_scope_names():
                if spack.config.get(key_path, scope=scope):
                    ideal_scope_to_modify = scope
                    break

            update_path = f"{key_path}:[{str(spec)}]"
            spack.config.add(update_path, scope=ideal_scope_to_modify)
    else:
        raise ValueError("'config change' can currently only change 'require' sections")


def config_change(args):
    _config_change(args.path, args.match_spec)


def config_update(args):
    # Read the configuration files
    spack.config.CONFIG.get_config(args.section, scope=args.scope)
    updates: List[spack.config.ConfigScope] = [
        x
        for x in spack.config.CONFIG.format_updates[args.section]
        if not isinstance(x, spack.config.InternalConfigScope) and x.writable
    ]

    cannot_overwrite, skip_system_scope = [], False
    for scope in updates:
        cfg_file = spack.config.CONFIG.get_config_filename(scope.name, args.section)
        can_be_updated = _can_update_config_file(scope, cfg_file)
        if not can_be_updated:
            if scope.name == "system":
                skip_system_scope = True
                tty.warn(
                    'Not enough permissions to write to "system" scope. '
                    f"Skipping update at that location [cfg={cfg_file}]"
                )
                continue
            cannot_overwrite.append((scope, cfg_file))

    if cannot_overwrite:
        msg = "Detected permission issues with the following scopes:\n\n"
        for scope, cfg_file in cannot_overwrite:
            msg += "\t[scope={0}, cfg={1}]\n".format(scope.name, cfg_file)
        msg += (
            "\nEither ensure that you have sufficient permissions to "
            "modify these files or do not include these scopes in the "
            "update."
        )
        tty.die(msg)

    if skip_system_scope:
        updates = [x for x in updates if x.name != "system"]

    # Report if there are no updates to be done
    if not updates:
        msg = 'No updates needed for "{0}" section.'
        tty.msg(msg.format(args.section))
        return

    proceed = True
    if not args.yes_to_all:
        msg = (
            "The following configuration files are going to be updated to"
            " the latest schema format:\n\n"
        )
        for scope in updates:
            cfg_file = spack.config.CONFIG.get_config_filename(scope.name, args.section)
            msg += "\t[scope={0}, file={1}]\n".format(scope.name, cfg_file)
        msg += (
            "\nIf the configuration files are updated, versions of Spack "
            "that are older than this version may not be able to read "
            "them. Spack stores backups of the updated files which can "
            'be retrieved with "spack config revert"'
        )
        tty.msg(msg)
        proceed = tty.get_yes_or_no("Do you want to proceed?", default=False)

    if not proceed:
        tty.die("Operation aborted.")

    # Get a function to update the format
    update_fn = spack.config.ensure_latest_format_fn(args.section)
    for scope in updates:
        data = scope.get_section(args.section).pop(args.section)
        update_fn(data)

        # Make a backup copy and rewrite the file
        bkp_file = cfg_file + ".bkp"
        shutil.copy(cfg_file, bkp_file)
        spack.config.CONFIG.update_config(args.section, data, scope=scope.name, force=True)
        tty.msg(f'File "{cfg_file}" update [backup={bkp_file}]')


def _can_revert_update(scope_dir, cfg_file, bkp_file):
    dir_ok = fs.can_write_to_dir(scope_dir)
    cfg_ok = not os.path.exists(cfg_file) or fs.can_access(cfg_file)
    bkp_ok = fs.can_access(bkp_file)
    return dir_ok and cfg_ok and bkp_ok


def config_revert(args):
    scopes = [args.scope] if args.scope else [x.name for x in spack.config.CONFIG.writable_scopes]

    # Search for backup files in the configuration scopes
    Entry = collections.namedtuple("Entry", ["scope", "cfg", "bkp"])
    to_be_restored, cannot_overwrite = [], []
    for scope in scopes:
        cfg_file = spack.config.CONFIG.get_config_filename(scope, args.section)
        bkp_file = cfg_file + ".bkp"

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
        msg = "Detected permission issues with the following scopes:\n\n"
        for e in cannot_overwrite:
            msg += "\t[scope={0.scope}, cfg={0.cfg}, bkp={0.bkp}]\n".format(e)
        msg += (
            "\nEither ensure to have the right permissions before retrying"
            " or be more specific on the scope to revert."
        )
        tty.die(msg)

    proceed = True
    if not args.yes_to_all:
        msg = "The following scopes will be restored from the corresponding backup files:\n"
        for entry in to_be_restored:
            msg += "\t[scope={0.scope}, bkp={0.bkp}]\n".format(entry)
        msg += "This operation cannot be undone."
        tty.msg(msg)
        proceed = tty.get_yes_or_no("Do you want to proceed?", default=False)

    if not proceed:
        tty.die("Operation aborted.")

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
        scope = spack.config.default_modify_scope("packages")

    all_specs = set(spack.store.STORE.db.query(installed=True))
    local_specs = set(spack.store.STORE.db.query_local(installed=True))
    pref_specs = local_specs if args.local else all_specs - local_specs

    conflicting_variants = set()

    pkgs = {}
    for spec in pref_specs:
        # Collect all the upstream compilers and versions for this package.
        pkg = pkgs.get(spec.name, {"version": []})
        all = pkgs.get("all", {"compiler": []})
        pkgs["all"] = all
        pkgs[spec.name] = pkg

        # We have no existing variant if this is our first added version.
        existing_variants = pkg.get("variants", None if not pkg["version"] else "")

        version = spec.version.string
        if version not in pkg["version"]:
            pkg["version"].append(version)

        compiler = str(spec.compiler)
        if compiler not in all["compiler"]:
            all["compiler"].append(compiler)

        # Get and list all the variants that differ from the default.
        variants = []
        for var_name, variant in spec.variants.items():
            if var_name in ["patches"] or not spec.package.has_variant(var_name):
                continue

            vdef = spec.package.get_variant(var_name)
            if variant.value != vdef.default:
                variants.append(str(variant))
        variants.sort()
        variants = " ".join(variants)

        if spec.name not in conflicting_variants:
            # Only specify the variants if there's a single variant
            # set across all versions/compilers.
            if existing_variants is not None and existing_variants != variants:
                conflicting_variants.add(spec.name)
                pkg.pop("variants", None)
            elif variants:
                pkg["variants"] = variants

    if conflicting_variants:
        tty.warn(
            "The following packages have multiple conflicting upstream "
            "specs. You may have to specify, by "
            "concretized hash, which spec you want when building "
            "packages that depend on them:\n - {0}".format(
                "\n - ".join(sorted(conflicting_variants))
            )
        )

    # Simply write the config to the specified file.
    existing = spack.config.get("packages", scope=scope)
    new = spack.config.merge_yaml(existing, pkgs)
    spack.config.set("packages", new, scope)
    config_file = spack.config.CONFIG.get_config_filename(scope, section)

    tty.msg("Updated config at {0}".format(config_file))


def config(parser, args):
    action = {
        "get": config_get,
        "blame": config_blame,
        "edit": config_edit,
        "list": config_list,
        "add": config_add,
        "rm": config_remove,
        "remove": config_remove,
        "update": config_update,
        "revert": config_revert,
        "prefer-upstream": config_prefer_upstream,
        "change": config_change,
    }
    action[args.config_command](args)
