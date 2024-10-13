# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import argparse
import os.path
import textwrap

from llnl.util.lang import stable_partition

import spack.cmd
import spack.config
import spack.deptypes as dt
import spack.environment as ev
import spack.mirror
import spack.reporters
import spack.spec
import spack.store
from spack.util.pattern import Args

__all__ = ["add_common_arguments"]

#: dictionary of argument-generating functions, keyed by name
_arguments = {}


def arg(fn):
    """Decorator for a function that generates a common argument.

    This ensures that argument bunches are created lazily. Decorate
    argument-generating functions below with @arg so that
    ``add_common_arguments()`` can find them.

    """
    _arguments[fn.__name__] = fn
    return fn


def add_common_arguments(parser, list_of_arguments):
    """Extend a parser with extra arguments

    Args:
        parser: parser to be extended
        list_of_arguments: arguments to be added to the parser
    """
    for argument in list_of_arguments:
        if argument not in _arguments:
            message = 'Trying to add non existing argument "{0}" to a command'
            raise KeyError(message.format(argument))

        x = _arguments[argument]()
        parser.add_argument(*x.flags, **x.kwargs)


class ConstraintAction(argparse.Action):
    """Constructs a list of specs based on constraints from the command line

    An instance of this class is supposed to be used as an argument action
    in a parser. It will read a constraint and will attach a function to the
    arguments that accepts optional keyword arguments.

    To obtain the specs from a command the function must be called.
    """

    def __call__(self, parser, namespace, values, option_string=None):
        # Query specs from command line
        self.constraint = namespace.constraint = values
        self.constraint_specs = namespace.constraint_specs = []
        namespace.specs = self._specs

    def _specs(self, **kwargs):
        # store parsed specs in spec.constraint after a call to specs()
        self.constraint_specs[:] = spack.cmd.parse_specs(self.constraint)

        # If an environment is provided, we'll restrict the search to
        # only its installed packages.
        env = ev.active_environment()
        if env:
            kwargs["hashes"] = set(env.all_hashes())

        # return everything for an empty query.
        if not self.constraint_specs:
            return spack.store.STORE.db.query(**kwargs)

        # Return only matching stuff otherwise.
        specs = {}
        for spec in self.constraint_specs:
            for s in spack.store.STORE.db.query(spec, **kwargs):
                # This is fast for already-concrete specs
                specs[s.dag_hash()] = s

        return sorted(specs.values())


class SetParallelJobs(argparse.Action):
    """Sets the correct value for parallel build jobs.

    The value is is set in the command line configuration scope so that
    it can be retrieved using the spack.config API.
    """

    def __call__(self, parser, namespace, jobs, option_string):
        # Jobs is a single integer, type conversion is already applied
        # see https://docs.python.org/3/library/argparse.html#action-classes
        if jobs < 1:
            msg = 'invalid value for argument "{0}" ' '[expected a positive integer, got "{1}"]'
            raise ValueError(msg.format(option_string, jobs))

        spack.config.set("config:build_jobs", jobs, scope="command_line")

        setattr(namespace, "jobs", jobs)


class DeptypeAction(argparse.Action):
    """Creates a flag of valid dependency types from a deptype argument."""

    def __call__(self, parser, namespace, values, option_string=None):
        if not values or values == "all":
            deptype = dt.ALL
        else:
            deptype = dt.canonicalize(values.split(","))
        setattr(namespace, self.dest, deptype)


class ConfigScope(argparse.Action):
    """Pick the currently configured config scopes."""

    def __init__(self, *args, **kwargs) -> None:
        kwargs.setdefault("metavar", spack.config.SCOPES_METAVAR)
        super().__init__(*args, **kwargs)

    @property
    def default(self):
        return self._default() if callable(self._default) else self._default

    @default.setter
    def default(self, value):
        self._default = value

    @property
    def choices(self):
        return spack.config.scopes().keys()

    @choices.setter
    def choices(self, value):
        pass

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)


def _cdash_reporter(namespace):
    """Helper function to create a CDash reporter. This function gets an early reference to the
    argparse namespace under construction, so it can later use it to create the object.
    """

    def _factory():
        def installed_specs(args):
            if getattr(args, "spec", ""):
                packages = args.spec
            elif getattr(args, "specs", ""):
                packages = args.specs
            elif getattr(args, "package", ""):
                # Ensure CI 'spack test run' can output CDash results
                packages = args.package
            else:
                packages = []
                for file in args.specfiles:
                    with open(file, "r") as f:
                        s = spack.spec.Spec.from_yaml(f)
                        packages.append(s.format())
            return packages

        configuration = spack.reporters.CDashConfiguration(
            upload_url=namespace.cdash_upload_url,
            packages=installed_specs(namespace),
            build=namespace.cdash_build,
            site=namespace.cdash_site,
            buildstamp=namespace.cdash_buildstamp,
            track=namespace.cdash_track,
        )
        return spack.reporters.CDash(configuration=configuration)

    return _factory


class CreateReporter(argparse.Action):
    """Create the correct object to generate reports for installation and testing."""

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)
        if values == "junit":
            setattr(namespace, "reporter", spack.reporters.JUnit)
        elif values == "cdash":
            setattr(namespace, "reporter", _cdash_reporter(namespace))


@arg
def log_format():
    return Args(
        "--log-format",
        default=None,
        action=CreateReporter,
        choices=("junit", "cdash"),
        help="format to be used for log files",
    )


# TODO: merge constraint and installed_specs
@arg
def constraint():
    return Args(
        "constraint",
        nargs=argparse.REMAINDER,
        action=ConstraintAction,
        help="constraint to select a subset of installed packages",
        metavar="installed_specs",
    )


@arg
def package():
    return Args("package", help="package name")


@arg
def packages():
    return Args("packages", nargs="+", help="one or more package names", metavar="package")


# Specs must use `nargs=argparse.REMAINDER` because a single spec can
# contain spaces, and contain variants like '-mpi' that argparse thinks
# are a collection of optional flags.
@arg
def spec():
    return Args("spec", nargs=argparse.REMAINDER, help="package spec")


@arg
def specs():
    return Args("specs", nargs=argparse.REMAINDER, help="one or more package specs")


@arg
def installed_spec():
    return Args(
        "spec", nargs=argparse.REMAINDER, help="installed package spec", metavar="installed_spec"
    )


@arg
def installed_specs():
    return Args(
        "specs",
        nargs=argparse.REMAINDER,
        help="one or more installed package specs",
        metavar="installed_specs",
    )


@arg
def yes_to_all():
    return Args(
        "-y",
        "--yes-to-all",
        action="store_true",
        dest="yes_to_all",
        help='assume "yes" is the answer to every confirmation request',
    )


@arg
def recurse_dependencies():
    return Args(
        "-r",
        "--dependencies",
        action="store_true",
        dest="recurse_dependencies",
        help="recursively traverse spec dependencies",
    )


@arg
def recurse_dependents():
    return Args(
        "-R",
        "--dependents",
        action="store_true",
        dest="dependents",
        help="also uninstall any packages that depend on the ones given via command line",
    )


@arg
def clean():
    return Args(
        "--clean",
        action="store_false",
        default=spack.config.get("config:dirty"),
        dest="dirty",
        help="unset harmful variables in the build environment (default)",
    )


@arg
def deptype():
    return Args(
        "--deptype",
        action=DeptypeAction,
        default=dt.ALL,
        help="comma-separated list of deptypes to traverse (default=%s)" % ",".join(dt.ALL_TYPES),
    )


@arg
def dirty():
    return Args(
        "--dirty",
        action="store_true",
        default=spack.config.get("config:dirty"),
        dest="dirty",
        help="preserve user environment in spack's build environment (danger!)",
    )


@arg
def long():
    return Args(
        "-l", "--long", action="store_true", help="show dependency hashes as well as versions"
    )


@arg
def very_long():
    return Args(
        "-L",
        "--very-long",
        action="store_true",
        help="show full dependency hashes as well as versions",
    )


@arg
def tags():
    return Args(
        "-t",
        "--tag",
        action="append",
        dest="tags",
        metavar="TAG",
        help="filter a package query by tag (multiple use allowed)",
    )


@arg
def namespaces():
    return Args(
        "-N",
        "--namespaces",
        action="store_true",
        default=False,
        help="show fully qualified package names",
    )


@arg
def jobs():
    return Args(
        "-j",
        "--jobs",
        action=SetParallelJobs,
        type=int,
        dest="jobs",
        help="explicitly set number of parallel jobs",
    )


@arg
def install_status():
    return Args(
        "-I",
        "--install-status",
        action="store_true",
        default=True,
        help=(
            "show install status of packages\n"
            "[+] installed       [^] installed in an upstream\n"
            " -  not installed   [-] missing dep of installed package\n"
        ),
    )


@arg
def no_install_status():
    return Args(
        "--no-install-status",
        dest="install_status",
        action="store_false",
        default=True,
        help="do not show install status annotations",
    )


@arg
def no_checksum():
    return Args(
        "-n",
        "--no-checksum",
        action="store_true",
        default=False,
        help="do not use checksums to verify downloaded files (unsafe)",
    )


@arg
def deprecated():
    return Args(
        "--deprecated",
        action="store_true",
        default=False,
        help="fetch deprecated versions without warning",
    )


def add_cdash_args(subparser, add_help):
    cdash_help = {}
    if add_help:
        cdash_help["upload-url"] = "CDash URL where reports will be uploaded"
        cdash_help["build"] = (
            "name of the build that will be reported to CDash\n\n"
            "defaults to spec of the package to operate on"
        )
        cdash_help["site"] = (
            "site name that will be reported to CDash\n\n" "defaults to current system hostname"
        )
        cdash_help["track"] = (
            "results will be reported to this group on CDash\n\n" "defaults to Experimental"
        )
        cdash_help["buildstamp"] = (
            "use custom buildstamp\n\n"
            "instead of letting the CDash reporter prepare the "
            "buildstamp which, when combined with build name, site and project, "
            "uniquely identifies the build, provide this argument to identify "
            "the build yourself. format: %%Y%%m%%d-%%H%%M-[cdash-track]"
        )
    else:
        cdash_help["upload-url"] = argparse.SUPPRESS
        cdash_help["build"] = argparse.SUPPRESS
        cdash_help["site"] = argparse.SUPPRESS
        cdash_help["track"] = argparse.SUPPRESS
        cdash_help["buildstamp"] = argparse.SUPPRESS

    subparser.add_argument("--cdash-upload-url", default=None, help=cdash_help["upload-url"])
    subparser.add_argument("--cdash-build", default=None, help=cdash_help["build"])
    subparser.add_argument("--cdash-site", default=None, help=cdash_help["site"])

    cdash_subgroup = subparser.add_mutually_exclusive_group()
    cdash_subgroup.add_argument("--cdash-track", default="Experimental", help=cdash_help["track"])
    cdash_subgroup.add_argument("--cdash-buildstamp", default=None, help=cdash_help["buildstamp"])


def print_cdash_help():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """\
environment variables:
SPACK_CDASH_AUTH_TOKEN
                    authentication token to present to CDash
                    """
        ),
    )
    add_cdash_args(parser, True)
    parser.print_help()


def sanitize_reporter_options(namespace: argparse.Namespace):
    """Sanitize options that affect generation and configuration of reports, like
    CDash or JUnit.

    Args:
        namespace: options parsed from cli
    """
    has_any_cdash_option = (
        namespace.cdash_upload_url or namespace.cdash_build or namespace.cdash_site
    )
    if namespace.log_format == "junit" and has_any_cdash_option:
        raise argparse.ArgumentTypeError("cannot pass any cdash option when --log-format=junit")

    # If any CDash option is passed, assume --log-format=cdash is implied
    if namespace.log_format is None and has_any_cdash_option:
        namespace.log_format = "cdash"
        namespace.reporter = _cdash_reporter(namespace)


class ConfigSetAction(argparse.Action):
    """Generic action for setting spack config options from CLI.

    This works like a ``store_const`` action but you can set the
    ``dest`` to some Spack configuration path (like ``concretizer:reuse``)
    and the ``const`` will be stored there using ``spack.config.set()``
    """

    def __init__(
        self, option_strings, dest, const, default=None, required=False, help=None, metavar=None
    ):
        # save the config option we're supposed to set
        self.config_path = dest

        # destination is translated to a legal python identifier by
        # substituting '_' for ':'.
        dest = dest.replace(":", "_")

        super().__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=0,
            const=const,
            default=default,
            required=required,
            help=help,
        )

    def __call__(self, parser, namespace, values, option_string):
        # Retrieve the name of the config option and set it to
        # the const from the constructor or a value from the CLI.
        # Note that this is only called if the argument is actually
        # specified on the command line.
        spack.config.set(self.config_path, self.const, scope="command_line")


def add_concretizer_args(subparser):
    """Add a subgroup of arguments for controlling concretization.

    These will appear in a separate group called 'concretizer arguments'.
    There's no need to handle them in your command logic -- they all use
    ``ConfigSetAction``, which automatically handles setting configuration
    options.

    If you *do* need to access a value passed on the command line, you can
    get at, e.g., the ``concretizer:reuse`` via ``args.concretizer_reuse``.
    Just substitute ``_`` for ``:``.
    """
    subgroup = subparser.add_argument_group("concretizer arguments")
    subgroup.add_argument(
        "-U",
        "--fresh",
        action=ConfigSetAction,
        dest="concretizer:reuse",
        const=False,
        default=None,
        help="do not reuse installed deps; build newest configuration",
    )
    subgroup.add_argument(
        "--reuse",
        action=ConfigSetAction,
        dest="concretizer:reuse",
        const=True,
        default=None,
        help="reuse installed packages/buildcaches when possible",
    )
    subgroup.add_argument(
        "--fresh-roots",
        "--reuse-deps",
        action=ConfigSetAction,
        dest="concretizer:reuse",
        const="dependencies",
        default=None,
        help="concretize with fresh roots and reused dependencies",
    )
    subgroup.add_argument(
        "--deprecated",
        action=ConfigSetAction,
        dest="config:deprecated",
        const=True,
        default=None,
        help="allow concretizer to select deprecated versions",
    )


def add_connection_args(subparser, add_help):
    subparser.add_argument(
        "--s3-access-key-id", help="ID string to use to connect to this S3 mirror"
    )
    subparser.add_argument(
        "--s3-access-key-secret", help="secret string to use to connect to this S3 mirror"
    )
    subparser.add_argument(
        "--s3-access-token", help="access token to use to connect to this S3 mirror"
    )
    subparser.add_argument(
        "--s3-profile", help="S3 profile name to use to connect to this S3 mirror", default=None
    )
    subparser.add_argument(
        "--s3-endpoint-url", help="endpoint URL to use to connect to this S3 mirror"
    )
    subparser.add_argument("--oci-username", help="username to use to connect to this OCI mirror")
    subparser.add_argument("--oci-password", help="password to use to connect to this OCI mirror")


def use_buildcache(cli_arg_value):
    """Translate buildcache related command line arguments into a pair of strings,
    representing whether the root or its dependencies can use buildcaches.

    Argument type that accepts comma-separated subargs:

        1. auto|only|never
        2. package:auto|only|never
        3. dependencies:auto|only|never

    Args:
        cli_arg_value (str): command line argument value to be translated

    Return:
        Tuple of two strings
    """
    valid_keys = frozenset(["package", "dependencies"])
    valid_values = frozenset(["only", "never", "auto"])

    # Split in args, split in key/value, and trim whitespace
    args = [tuple(map(lambda x: x.strip(), part.split(":"))) for part in cli_arg_value.split(",")]

    # Verify keys and values
    def is_valid(arg):
        if len(arg) == 1:
            return arg[0] in valid_values
        if len(arg) == 2:
            return arg[0] in valid_keys and arg[1] in valid_values
        return False

    valid, invalid = stable_partition(args, is_valid)

    # print first error
    if invalid:
        raise argparse.ArgumentTypeError("invalid argument `{}`".format(":".join(invalid[0])))

    # Default values
    package = "auto"
    dependencies = "auto"

    # Override in order.
    for arg in valid:
        if len(arg) == 1:
            package = dependencies = arg[0]
            continue
        key, val = arg
        if key == "package":
            package = val
        else:
            dependencies = val

    return package, dependencies


def mirror_name_or_url(m):
    # Look up mirror by name or use anonymous mirror with path/url.
    # We want to guard against typos in mirror names, to avoid pushing
    # accidentally to a dir in the current working directory.

    # If there's a \ or / in the name, it's interpreted as a path or url.
    if "/" in m or "\\" in m:
        return spack.mirror.Mirror(m)

    # Otherwise, the named mirror is required to exist.
    try:
        return spack.mirror.require_mirror_name(m)
    except ValueError as e:
        raise argparse.ArgumentTypeError(
            str(e) + ". Did you mean {}?".format(os.path.join(".", m))
        )


def mirror_url(url):
    try:
        return spack.mirror.Mirror.from_url(url)
    except ValueError as e:
        raise argparse.ArgumentTypeError(str(e))


def mirror_directory(path):
    try:
        return spack.mirror.Mirror.from_local_path(path)
    except ValueError as e:
        raise argparse.ArgumentTypeError(str(e))


def mirror_name(name):
    try:
        return spack.mirror.require_mirror_name(name)
    except ValueError as e:
        raise argparse.ArgumentTypeError(str(e))
