# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os.path
import shutil
import sys
import tempfile

import llnl.util.filesystem
import llnl.util.tty
import llnl.util.tty.color

import spack
import spack.bootstrap
import spack.bootstrap.config
import spack.bootstrap.core
import spack.config
import spack.mirror
import spack.spec
import spack.stage
import spack.util.path
import spack.util.spack_yaml
from spack.cmd.common import arguments

description = "manage bootstrap configuration"
section = "system"
level = "long"


# Tarball to be downloaded if binary packages are requested in a local mirror
BINARY_TARBALL = "https://github.com/spack/spack-bootstrap-mirrors/releases/download/v0.4/bootstrap-buildcache.tar.gz"

#: Subdirectory where to create the mirror
LOCAL_MIRROR_DIR = "bootstrap_cache"

# Metadata for a generated binary mirror
BINARY_METADATA = {
    "type": "buildcache",
    "description": (
        "Buildcache copied from a public tarball available on Github."
        "The sha256 checksum of binaries is checked before installation."
    ),
    "info": {
        # This is a mis-nomer since it's not a URL; but file urls cannot
        # represent relative paths, so we have to live with it for now.
        "url": os.path.join("..", "..", LOCAL_MIRROR_DIR),
        "homepage": "https://github.com/spack/spack-bootstrap-mirrors",
        "releases": "https://github.com/spack/spack-bootstrap-mirrors/releases",
        "tarball": BINARY_TARBALL,
    },
}

CLINGO_JSON = "$spack/share/spack/bootstrap/github-actions-v0.4/clingo.json"
GNUPG_JSON = "$spack/share/spack/bootstrap/github-actions-v0.4/gnupg.json"
PATCHELF_JSON = "$spack/share/spack/bootstrap/github-actions-v0.4/patchelf.json"

# Metadata for a generated source mirror
SOURCE_METADATA = {
    "type": "install",
    "description": "Mirror with software needed to bootstrap Spack",
    "info": {
        # This is a mis-nomer since it's not a URL; but file urls cannot
        # represent relative paths, so we have to live with it for now.
        "url": os.path.join("..", "..", LOCAL_MIRROR_DIR)
    },
}


def _add_scope_option(parser):
    parser.add_argument(
        "--scope", action=arguments.ConfigScope, help="configuration scope to read/modify"
    )


def setup_parser(subparser):
    sp = subparser.add_subparsers(dest="subcommand")

    now = sp.add_parser("now", help="Spack ready, right now!")
    now.add_argument("--dev", action="store_true", help="bootstrap dev dependencies too")

    status = sp.add_parser("status", help="get the status of Spack")
    status.add_argument(
        "--optional",
        action="store_true",
        default=False,
        help="show the status of rarely used optional dependencies",
    )
    status.add_argument(
        "--dev",
        action="store_true",
        default=False,
        help="show the status of dependencies needed to develop Spack",
    )

    enable = sp.add_parser("enable", help="enable bootstrapping")
    _add_scope_option(enable)
    enable.add_argument("name", help="name of the source to be enabled", nargs="?", default=None)

    disable = sp.add_parser("disable", help="disable bootstrapping")
    _add_scope_option(disable)
    disable.add_argument("name", help="name of the source to be disabled", nargs="?", default=None)

    reset = sp.add_parser("reset", help="reset bootstrapping configuration to Spack defaults")
    arguments.add_common_arguments(reset, ["yes_to_all"])

    root = sp.add_parser("root", help="get/set the root bootstrap directory")
    _add_scope_option(root)
    root.add_argument(
        "path", nargs="?", default=None, help="set the bootstrap directory to this value"
    )

    list = sp.add_parser("list", help="list all the sources of software to bootstrap Spack")
    _add_scope_option(list)

    add = sp.add_parser("add", help="add a new source for bootstrapping")
    _add_scope_option(add)
    add.add_argument(
        "--trust", action="store_true", help="enable the source immediately upon addition"
    )
    add.add_argument("name", help="name of the new source of software")
    add.add_argument("metadata_dir", help="directory where to find metadata files")

    remove = sp.add_parser("remove", help="remove a bootstrapping source")
    remove.add_argument("name", help="name of the source to be removed")

    mirror = sp.add_parser("mirror", help="create a local mirror to bootstrap Spack")
    mirror.add_argument(
        "--binary-packages", action="store_true", help="download public binaries in the mirror"
    )
    mirror.add_argument("--dev", action="store_true", help="download dev dependencies too")
    mirror.add_argument(
        metavar="DIRECTORY",
        dest="root_dir",
        help="root directory in which to create the mirror and metadata",
    )


def _enable_or_disable(args):
    value = args.subcommand == "enable"
    if args.name is None:
        # Set to True if we called "enable", otherwise set to false
        old_value = spack.config.get("bootstrap:enable", scope=args.scope)
        if old_value == value:
            llnl.util.tty.msg("Bootstrapping is already {}d".format(args.subcommand))
        else:
            spack.config.set("bootstrap:enable", value, scope=args.scope)
            llnl.util.tty.msg("Bootstrapping has been {}d".format(args.subcommand))
        return

    if value is True:
        _enable_source(args)
    else:
        _disable_source(args)


def _reset(args):
    if not args.yes_to_all:
        msg = [
            "Bootstrapping configuration is being reset to Spack's defaults. "
            "Current configuration will be lost.\n",
            "Do you want to continue?",
        ]
        ok_to_continue = llnl.util.tty.get_yes_or_no("".join(msg), default=True)
        if not ok_to_continue:
            raise RuntimeError("Aborting")

    for scope in spack.config.CONFIG.writable_scopes:
        # The default scope should stay untouched
        if scope.name == "defaults":
            continue

        # If we are in an env scope we can't delete a file, but the best we
        # can do is nullify the corresponding configuration
        if scope.name.startswith("env") and spack.config.get("bootstrap", scope=scope.name):
            spack.config.set("bootstrap", {}, scope=scope.name)
            continue

        # If we are outside of an env scope delete the bootstrap.yaml file
        bootstrap_yaml = os.path.join(scope.path, "bootstrap.yaml")
        backup_file = bootstrap_yaml + ".bkp"
        if os.path.exists(bootstrap_yaml):
            shutil.move(bootstrap_yaml, backup_file)

        spack.config.CONFIG.clear_caches()


def _root(args):
    if args.path:
        spack.config.set("bootstrap:root", args.path, scope=args.scope)

    root = spack.config.get("bootstrap:root", default=None, scope=args.scope)
    if root:
        root = spack.util.path.canonicalize_path(root)
    print(root)


def _list(args):
    sources = spack.bootstrap.core.bootstrapping_sources(scope=args.scope)
    if not sources:
        llnl.util.tty.msg("No method available for bootstrapping Spack's dependencies")
        return

    def _print_method(source, trusted):
        color = llnl.util.tty.color

        def fmt(header, content):
            header_fmt = "@*b{{{0}:}} {1}"
            color.cprint(header_fmt.format(header, content))

        trust_str = "@*y{DISABLED}"
        if trusted is True:
            trust_str = "@*g{ENABLED}"
        elif trusted is False:
            trust_str = "@*r{DISABLED}"

        fmt("Name", source["name"] + " " + trust_str)
        print()
        if trusted is True or args.verbose:
            fmt("  Type", source["type"])
            print()

            info_lines = ["\n"]
            for key, value in source.get("info", {}).items():
                info_lines.append(" " * 4 + "@*{{{0}}}: {1}\n".format(key, value))
            if len(info_lines) > 1:
                fmt("  Info", "".join(info_lines))

            description_lines = ["\n"]
            for line in source["description"].split("\n"):
                description_lines.append(" " * 4 + line + "\n")

            fmt("  Description", "".join(description_lines))

    trusted = spack.config.get("bootstrap:trusted", {})

    def sort_fn(x):
        x_trust = trusted.get(x["name"], None)
        if x_trust is True:
            return 0
        elif x_trust is None:
            return 1
        return 2

    sources = sorted(sources, key=sort_fn)
    for s in sources:
        _print_method(s, trusted.get(s["name"], None))


def _write_bootstrapping_source_status(name, enabled, scope=None):
    """Write if a bootstrapping source is enable or disabled to config file.

    Args:
        name (str): name of the bootstrapping source.
        enabled (bool): True if the source is enabled, False if it is disabled.
        scope (None or str): configuration scope to modify. If none use the default scope.
    """
    sources = spack.config.get("bootstrap:sources")

    matches = [s for s in sources if s["name"] == name]
    if not matches:
        names = [s["name"] for s in sources]
        msg = (
            'there is no bootstrapping method named "{0}". Valid '
            "method names are: {1}".format(name, ", ".join(names))
        )
        raise RuntimeError(msg)

    if len(matches) > 1:
        msg = (
            'there is more than one bootstrapping method named "{0}". '
            "Please delete all methods but one from bootstrap.yaml "
            "before proceeding"
        ).format(name)
        raise RuntimeError(msg)

    # Setting the scope explicitly is needed to not copy over to a new scope
    # the entire default configuration for bootstrap.yaml
    scope = scope or spack.config.default_modify_scope("bootstrap")
    spack.config.add("bootstrap:trusted:{0}:{1}".format(name, str(enabled)), scope=scope)


def _enable_source(args):
    _write_bootstrapping_source_status(args.name, enabled=True, scope=args.scope)
    msg = '"{0}" is now enabled for bootstrapping'
    llnl.util.tty.msg(msg.format(args.name))


def _disable_source(args):
    _write_bootstrapping_source_status(args.name, enabled=False, scope=args.scope)
    msg = '"{0}" is now disabled and will not be used for bootstrapping'
    llnl.util.tty.msg(msg.format(args.name))


def _status(args):
    sections = ["core", "buildcache"]
    if args.optional:
        sections.append("optional")
    if args.dev:
        sections.append("develop")

    header = "@*b{{Spack v{0} - {1}}}".format(
        spack.spack_version, spack.bootstrap.config.spec_for_current_python()
    )
    print(llnl.util.tty.color.colorize(header))
    print()
    # Use the context manager here to avoid swapping between user and
    # bootstrap config many times
    missing = False
    with spack.bootstrap.ensure_bootstrap_configuration():
        for current_section in sections:
            status_msg, fail = spack.bootstrap.status_message(section=current_section)
            missing = missing or fail
            if status_msg:
                print(llnl.util.tty.color.colorize(status_msg))
        print()
    legend = (
        "Spack will take care of bootstrapping any missing dependency marked"
        " as [@*y{B}]. Dependencies marked as [@*y{-}] are instead required"
        " to be found on the system."
    )
    if missing:
        print(llnl.util.tty.color.colorize(legend))
        print()
        sys.exit(1)


def _add(args):
    initial_sources = spack.bootstrap.core.bootstrapping_sources()
    names = [s["name"] for s in initial_sources]

    # If the name is already used error out
    if args.name in names:
        msg = 'a source named "{0}" already exist. Please choose a different name'
        raise RuntimeError(msg.format(args.name))

    # Check that the metadata file exists
    metadata_dir = spack.util.path.canonicalize_path(args.metadata_dir)
    if not os.path.exists(metadata_dir) or not os.path.isdir(metadata_dir):
        raise RuntimeError('the directory "{0}" does not exist'.format(args.metadata_dir))

    file = os.path.join(metadata_dir, "metadata.yaml")
    if not os.path.exists(file):
        raise RuntimeError('the file "{0}" does not exist'.format(file))

    # Insert the new source as the highest priority one
    write_scope = args.scope or spack.config.default_modify_scope(section="bootstrap")
    sources = spack.config.get("bootstrap:sources", scope=write_scope) or []
    sources = [{"name": args.name, "metadata": args.metadata_dir}] + sources
    spack.config.set("bootstrap:sources", sources, scope=write_scope)

    msg = 'New bootstrapping source "{0}" added in the "{1}" configuration scope'
    llnl.util.tty.msg(msg.format(args.name, write_scope))
    if args.trust:
        _enable_source(args)


def _remove(args):
    initial_sources = spack.bootstrap.core.bootstrapping_sources()
    names = [s["name"] for s in initial_sources]
    if args.name not in names:
        msg = (
            'cannot find any bootstrapping source named "{0}". '
            "Run `spack bootstrap list` to see available sources."
        )
        raise RuntimeError(msg.format(args.name))

    for current_scope in spack.config.scopes():
        sources = spack.config.get("bootstrap:sources", scope=current_scope) or []
        if args.name in [s["name"] for s in sources]:
            sources = [s for s in sources if s["name"] != args.name]
            spack.config.set("bootstrap:sources", sources, scope=current_scope)
            msg = (
                'Removed the bootstrapping source named "{0}" from the '
                '"{1}" configuration scope.'
            )
            llnl.util.tty.msg(msg.format(args.name, current_scope))
        trusted = spack.config.get("bootstrap:trusted", scope=current_scope) or []
        if args.name in trusted:
            trusted.pop(args.name)
            spack.config.set("bootstrap:trusted", trusted, scope=current_scope)
            msg = 'Deleting information on "{0}" from list of trusted sources'
            llnl.util.tty.msg(msg.format(args.name))


def _mirror(args):
    mirror_dir = spack.util.path.canonicalize_path(os.path.join(args.root_dir, LOCAL_MIRROR_DIR))

    # TODO: Here we are adding gnuconfig manually, but this can be fixed
    # TODO: as soon as we have an option to add to a mirror all the possible
    # TODO: dependencies of a spec
    root_specs = spack.bootstrap.all_core_root_specs() + ["gnuconfig"]
    if args.dev:
        root_specs += spack.bootstrap.BootstrapEnvironment.spack_dev_requirements()

    for spec_str in root_specs:
        msg = 'Adding "{0}" and dependencies to the mirror at {1}'
        llnl.util.tty.msg(msg.format(spec_str, mirror_dir))
        # Suppress tty from the call below for terser messages
        llnl.util.tty.set_msg_enabled(False)
        spec = spack.spec.Spec(spec_str).concretized()
        for node in spec.traverse():
            spack.mirror.create(mirror_dir, [node])
        llnl.util.tty.set_msg_enabled(True)

    if args.binary_packages:
        msg = 'Adding binary packages from "{0}" to the mirror at {1}'
        llnl.util.tty.msg(msg.format(BINARY_TARBALL, mirror_dir))
        llnl.util.tty.set_msg_enabled(False)
        stage = spack.stage.Stage(BINARY_TARBALL, path=tempfile.mkdtemp())
        stage.create()
        stage.fetch()
        stage.expand_archive()
        build_cache_dir = os.path.join(stage.source_path, "build_cache")
        shutil.move(build_cache_dir, mirror_dir)
        llnl.util.tty.set_msg_enabled(True)

    def write_metadata(subdir, metadata):
        metadata_rel_dir = os.path.join("metadata", subdir)
        metadata_yaml = os.path.join(args.root_dir, metadata_rel_dir, "metadata.yaml")
        llnl.util.filesystem.mkdirp(os.path.dirname(metadata_yaml))
        with open(metadata_yaml, mode="w") as f:
            spack.util.spack_yaml.dump(metadata, stream=f)
        return os.path.dirname(metadata_yaml), metadata_rel_dir

    instructions = (
        "\nTo register the mirror on the platform where it's supposed "
        'to be used, move "{0}" to its final location and run the '
        "following command(s):\n\n"
    ).format(args.root_dir)
    cmd = "  % spack bootstrap add --trust {0} <final-path>/{1}\n"
    _, rel_directory = write_metadata(subdir="sources", metadata=SOURCE_METADATA)
    instructions += cmd.format("local-sources", rel_directory)
    if args.binary_packages:
        abs_directory, rel_directory = write_metadata(subdir="binaries", metadata=BINARY_METADATA)
        shutil.copy(spack.util.path.canonicalize_path(CLINGO_JSON), abs_directory)
        shutil.copy(spack.util.path.canonicalize_path(GNUPG_JSON), abs_directory)
        shutil.copy(spack.util.path.canonicalize_path(PATCHELF_JSON), abs_directory)
        instructions += cmd.format("local-binaries", rel_directory)
    print(instructions)


def _now(args):
    with spack.bootstrap.ensure_bootstrap_configuration():
        spack.bootstrap.ensure_core_dependencies()
        if args.dev:
            spack.bootstrap.ensure_environment_dependencies()


def bootstrap(parser, args):
    callbacks = {
        "status": _status,
        "enable": _enable_or_disable,
        "disable": _enable_or_disable,
        "reset": _reset,
        "root": _root,
        "list": _list,
        "add": _add,
        "remove": _remove,
        "mirror": _mirror,
        "now": _now,
    }
    callbacks[args.subcommand](args)
