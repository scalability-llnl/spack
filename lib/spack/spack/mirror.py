# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
This file contains code for creating spack mirror directories.  A
mirror is an organized hierarchy containing specially named archive
files.  This enabled spack to know where to find files in a mirror if
the main server for a particular package is down.  Or, if the computer
where spack is run is not connected to the internet, it allows spack
to download packages directly from a mirror (e.g., on an intranet).
"""
import sys
import os
import traceback
import os.path
import operator

import six

import ruamel.yaml.error as yaml_error

from ordereddict_backport import OrderedDict

try:
    from collections.abc import Mapping  # novm
except ImportError:
    from collections import Mapping

import llnl.util.tty as tty
from llnl.util.filesystem import mkdirp

import spack.config
import spack.error
import spack.url as url
import spack.fetch_strategy as fs
import spack.util.spack_json as sjson
import spack.util.spack_yaml as syaml
import spack.util.url as url_util
import spack.spec
from spack.version import VersionList
from spack.util.spack_yaml import syaml_dict


def _display_mirror_entry(size, name, url, type_=None):
    if type_:
        type_ = "".join((" (", type_, ")"))
    else:
        type_ = ""

    print("%-*s%s%s" % (size + 4, name, url, type_))


class Mirror(object):
    """Represents a named location for storing source tarballs and binary
    packages.

    Mirrors have a fetch_url that indicate where and how artifacts are fetched
    from them, and a push_url that indicate where and how artifacts are pushed
    to them.  These two URLs are usually the same.
    """

    def __init__(self, fetch_url, push_url=None, name=None):
        self._fetch_url = fetch_url
        self._push_url = push_url
        self._name = name

    def to_json(self, stream=None):
        return sjson.dump(self.to_dict(), stream)

    def to_yaml(self, stream=None):
        return syaml.dump(self.to_dict(), stream)

    @staticmethod
    def from_yaml(stream, name=None):
        try:
            data = syaml.load(stream)
            return Mirror.from_dict(data, name)
        except yaml_error.MarkedYAMLError as e:
            raise syaml.SpackYAMLError("error parsing YAML spec:", str(e))

    @staticmethod
    def from_json(stream, name=None):
        d = sjson.load(stream)
        return Mirror.from_dict(d, name)

    def to_dict(self):
        if self._push_url is None:
            return self._fetch_url
        else:
            return syaml_dict([
                ('fetch', self._fetch_url),
                ('push', self._push_url)])

    @staticmethod
    def from_dict(d, name=None):
        if isinstance(d, six.string_types):
            return Mirror(d, name=name)
        else:
            return Mirror(d['fetch'], d['push'], name)

    @staticmethod
    def from_args(args):
        result = None

        if ((args.directory and args.mirror_name) or
                (args.mirror_name and args.mirror_url) or
                (args.mirror_url and args.directory)):
            raise ValueError('no more than one of "directory",'
                             ' "mirror_url", and "mirror_name" allowed')

        if args.directory:
            location = args.directory

            # User meant to provide a path to a local directory.
            # Ensure that they did not accidentally pass a URL.
            scheme = url_util.parse(location, scheme='<missing>').scheme
            if scheme != '<missing>':
                raise ValueError(
                    '"directory" must be a local path (got a URL)')

            # User meant to provide a path to a local directory.
            # Ensure that the mirror lookup does not mistake it for a named
            # mirror.
            location = 'file://' + location
            result = spack.mirror.MirrorCollection().lookup(location)

        elif args.mirror_name:
            location = args.mirror_name

            # User meant to provide the name of a preconfigured mirror.
            # Ensure that the mirror lookup actually returns a named mirror.
            result = spack.mirror.MirrorCollection().lookup(location)
            if result.name == "<unnamed>":
                raise ValueError(
                    'no configured mirror named "{name}"'.format(
                        name=location))

        elif args.mirror_url:
            location = args.mirror_url

            # User meant to provide a URL for an anonymous mirror.
            # Ensure that they actually provided a URL.
            scheme = url_util.parse(location, scheme='<missing>').scheme
            if scheme == '<missing>':
                raise ValueError(
                    '"{url}" is not a valid URL'.format(url=location))

            result = spack.mirror.MirrorCollection().lookup(location)

        else:
            # User did not provide any mirror specifications.
            # Use source_cache as the default mirror.
            result = spack.mirror.Mirror(
                spack.config.get('config:source_cache'))

        return result

    def display(self, max_len=0):
        if self._push_url is None:
            _display_mirror_entry(max_len, self._name, self._fetch_url)
        else:
            _display_mirror_entry(
                max_len, self._name, self._fetch_url, "fetch")
            _display_mirror_entry(
                max_len, self._name, self._push_url, "push")

    def __str__(self):
        name = self._name
        if name is None:
            name = ''
        else:
            name = ' "%s"' % name

        if self._push_url is None:
            return "[Mirror%s (%s)]" % (name, self._fetch_url)

        return "[Mirror%s (fetch: %s, push: %s)]" % (
            name, self._fetch_url, self._push_url)

    def __repr__(self):
        return ''.join((
            'Mirror(',
            ', '.join(
                '%s=%s' % (k, repr(v))
                for k, v in (
                    ('fetch_url', self._fetch_url),
                    ('push_url', self._push_url),
                    ('name', self._name))
                if k == 'fetch_url' or v),
            ')'
        ))

    @property
    def name(self):
        return self._name or "<unnamed>"

    @property
    def fetch_url(self):
        return self._fetch_url

    @fetch_url.setter
    def fetch_url(self, url):
        self._fetch_url = url
        self._normalize()

    @property
    def push_url(self):
        if self._push_url is None:
            return self._fetch_url
        return self._push_url

    @push_url.setter
    def push_url(self, url):
        self._push_url = url
        self._normalize()

    def _normalize(self):
        if self._push_url is not None and self._push_url == self._fetch_url:
            self._push_url = None


class MirrorCollection(Mapping):
    """A mapping of mirror names to mirrors."""

    def __init__(self, mirrors=None, scope=None):
        self._mirrors = OrderedDict(
            (name, Mirror.from_dict(mirror, name))
            for name, mirror in (
                mirrors.items() if mirrors is not None else
                spack.config.get('mirrors', scope=scope).items()))

    def to_json(self, stream=None):
        return sjson.dump(self.to_dict(True), stream)

    def to_yaml(self, stream=None):
        return syaml.dump(self.to_dict(True), stream)

    # TODO: this isn't called anywhere
    @staticmethod
    def from_yaml(stream, name=None):
        try:
            data = syaml.load(stream)
            return MirrorCollection(data)
        except yaml_error.MarkedYAMLError as e:
            raise syaml.SpackYAMLError("error parsing YAML spec:", str(e))

    @staticmethod
    def from_json(stream, name=None):
        d = sjson.load(stream)
        return MirrorCollection(d)

    def to_dict(self, recursive=False):
        return syaml_dict(sorted(
            (
                (k, (v.to_dict() if recursive else v))
                for (k, v) in self._mirrors.items()
            ), key=operator.itemgetter(0)
        ))

    @staticmethod
    def from_dict(d):
        return MirrorCollection(d)

    def __getitem__(self, item):
        return self._mirrors[item]

    def display(self):
        max_len = max(len(mirror.name) for mirror in self._mirrors.values())
        for mirror in self._mirrors.values():
            mirror.display(max_len)

    def lookup(self, name_or_url):
        """Looks up and returns a Mirror.

        If this MirrorCollection contains a named Mirror under the name
        [name_or_url], then that mirror is returned.  Otherwise, [name_or_url]
        is assumed to be a mirror URL, and an anonymous mirror with the given
        URL is returned.
        """
        result = self.get(name_or_url)

        if result is None:
            result = Mirror(fetch_url=name_or_url)

        return result

    def __iter__(self):
        return iter(self._mirrors)

    def __len__(self):
        return len(self._mirrors)


def _determine_extension(fetcher):
    if isinstance(fetcher, fs.URLFetchStrategy):
        if fetcher.expand_archive:
            # If we fetch with a URLFetchStrategy, use URL's archive type
            ext = url.determine_url_file_extension(fetcher.url)

            if ext:
                # Remove any leading dots
                ext = ext.lstrip('.')
            else:
                msg = """\
Unable to parse extension from {0}.

If this URL is for a tarball but does not include the file extension
in the name, you can explicitly declare it with the following syntax:

    version('1.2.3', 'hash', extension='tar.gz')

If this URL is for a download like a .jar or .whl that does not need
to be expanded, or an uncompressed installation script, you can tell
Spack not to expand it with the following syntax:

    version('1.2.3', 'hash', expand=False)
"""
                raise MirrorError(msg.format(fetcher.url))
        else:
            # If the archive shouldn't be expanded, don't check extension.
            ext = None
    else:
        # Otherwise we'll make a .tar.gz ourselves
        ext = 'tar.gz'

    return ext


class MirrorReference(object):
    """A ``MirrorReference`` stores the relative paths where you can store a
    package/resource in a mirror directory.

    The appropriate storage location is given by ``storage_path``. The
    ``cosmetic_path`` property provides a reference that a human could generate
    themselves based on reading the details of the package.

    A user can iterate over a ``MirrorReference`` object to get all the
    possible names that might be used to refer to the resource in a mirror;
    this includes names generated by previous naming schemes that are no-longer
    reported by ``storage_path`` or ``cosmetic_path``.
    """
    def __init__(self, cosmetic_path, global_path=None):
        self.global_path = global_path
        self.cosmetic_path = cosmetic_path

    @property
    def storage_path(self):
        if self.global_path:
            return self.global_path
        else:
            return self.cosmetic_path

    def __iter__(self):
        if self.global_path:
            yield self.global_path
        yield self.cosmetic_path


def mirror_archive_paths(fetcher, per_package_ref, spec=None):
    """Returns a ``MirrorReference`` object which keeps track of the relative
    storage path of the resource associated with the specified ``fetcher``."""
    ext = None
    if spec:
        versions = spec.package.versions.get(spec.package.version, {})
        ext = versions.get('extension', None)
    # If the spec does not explicitly specify an extension (the default case),
    # then try to determine it automatically. An extension can only be
    # specified for the primary source of the package (e.g. the source code
    # identified in the 'version' declaration). Resources/patches don't have
    # an option to specify an extension, so it must be inferred for those.
    ext = ext or _determine_extension(fetcher)

    if ext:
        per_package_ref += ".%s" % ext

    global_ref = fetcher.mirror_id()
    if global_ref:
        global_ref = os.path.join('_source-cache', global_ref)
    if global_ref and ext:
        global_ref += ".%s" % ext

    return MirrorReference(per_package_ref, global_ref)


def get_all_versions(specs):
    """Given a set of initial specs, return a new set of specs that includes
    each version of each package in the original set.

    Note that if any spec in the original set specifies properties other than
    version, this information will be omitted in the new set; for example; the
    new set of specs will not include variant settings.
    """

    version_specs = []
    for spec in specs:
        pkg = spec.package

        # Skip any package that has no known versions.
        if not pkg.versions:
            tty.msg("No safe (checksummed) versions for package %s" % pkg.name)
            continue

        for version in pkg.versions:
            version_spec = spack.spec.Spec(pkg.name)
            version_spec.versions = VersionList([version])
            version_specs.append(version_spec)

    return version_specs


def get_matching_versions(specs, num_versions=1):
    """Get a spec for EACH known version matching any spec in the list.
    For concrete specs, this retrieves the concrete version and, if more
    than one version per spec is requested, retrieves the latest versions
    of the package.
    """
    matching = []
    for spec in specs:
        pkg = spec.package

        # Skip any package that has no known versions.
        if not pkg.versions:
            tty.msg("No safe (checksummed) versions for package %s" % pkg.name)
            continue

        pkg_versions = num_versions

        version_order = list(reversed(sorted(pkg.versions)))
        matching_spec = []
        if spec.concrete:
            matching_spec.append(spec)
            pkg_versions -= 1
            if spec.version in version_order:
                version_order.remove(spec.version)

        for v in version_order:
            # Generate no more than num_versions versions for each spec.
            if pkg_versions < 1:
                break

            # Generate only versions that satisfy the spec.
            if spec.concrete or v.satisfies(spec.versions):
                s = spack.spec.Spec(pkg.name)
                s.versions = VersionList([v])
                s.variants = spec.variants.copy()
                # This is needed to avoid hanging references during the
                # concretization phase
                s.variants.spec = s
                matching_spec.append(s)
                pkg_versions -= 1

        if not matching_spec:
            tty.warn("No known version matches spec: %s" % spec)
        matching.extend(matching_spec)

    return matching


def create(url, specs, skip_unstable_versions=False):
    """Create a directory or remote location to be used as a spack mirror, and
    fill it with package archives.

    Arguments:
        url: Path to create a mirror hierarchy in.
        specs: Any package versions matching these specs will be added \
            to the mirror.
        skip_unstable_versions: if true, this skips adding resources when
            they do not have a stable archive checksum (as determined by
            ``fetch_strategy.stable_target``)

    Return Value:
        Returns a tuple of lists: (present, mirrored, error)

        * present:  Package specs that were already present.
        * mirrored: Package specs that were successfully mirrored.
        * error:    Package specs that failed to mirror due to some error.

    This routine iterates through all known package versions, and
    it creates specs for those versions.  If the version satisfies any spec
    in the specs list, it is downloaded and added to the mirror.
    """
    parsed = url_util.parse(url)
    mirror_root = url_util.local_file_path(parsed)

    # automatically spec-ify anything in the specs array.
    specs = [
        s if isinstance(s, spack.spec.Spec) else spack.spec.Spec(s)
        for s in specs]

    if mirror_root:
        # Get the absolute path of the root before we start jumping around.
        if not os.path.isdir(mirror_root):
            try:
                mkdirp(mirror_root)
            except OSError as e:
                raise MirrorError(
                    "Cannot create directory '%s':" % mirror_root, str(e))

    mirror_cache = spack.caches.MirrorCache(
        parsed, skip_unstable_versions=skip_unstable_versions)
    mirror_stats = MirrorStats()

    # Iterate through packages and download all safe tarballs for each
    for spec in specs:
        mirror_stats.next_spec(spec)
        _add_single_spec(spec, mirror_cache, mirror_stats)

    return mirror_stats.stats()


class MirrorStats(object):
    def __init__(self):
        self.present = {}
        self.new = {}
        self.errors = set()

        self.current_spec = None
        self.added_resources = set()
        self.existing_resources = set()

    def next_spec(self, spec):
        self._tally_current_spec()
        self.current_spec = spec

    def _tally_current_spec(self):
        if self.current_spec:
            if self.added_resources:
                self.new[self.current_spec] = len(self.added_resources)
            if self.existing_resources:
                self.present[self.current_spec] = len(self.existing_resources)
            self.added_resources = set()
            self.existing_resources = set()
        self.current_spec = None

    def stats(self):
        self._tally_current_spec()
        return list(self.present), list(self.new), list(self.errors)

    def already_existed(self, resource):
        # If an error occurred after caching a subset of a spec's
        # resources, a secondary attempt may consider them already added
        if resource not in self.added_resources:
            self.existing_resources.add(resource)

    def added(self, resource):
        self.added_resources.add(resource)

    def error(self):
        self.errors.add(self.current_spec)


def _add_single_spec(spec, mirror, mirror_stats):
    tty.msg("Adding package {pkg} to mirror".format(
        pkg=spec.format("{name}{@version}")
    ))
    num_retries = 3
    while num_retries > 0:
        try:
            with spec.package.stage as pkg_stage:
                pkg_stage.cache_mirror(mirror, mirror_stats)
                for patch in spec.package.all_patches():
                    if patch.stage:
                        patch.stage.cache_mirror(mirror, mirror_stats)
                    patch.clean()
            exception = None
            break
        except Exception as e:
            exc_tuple = sys.exc_info()
            exception = e
        num_retries -= 1

    if exception:
        if spack.config.get('config:debug'):
            traceback.print_exception(file=sys.stderr, *exc_tuple)
        else:
            tty.warn(
                "Error while fetching %s" % spec.cformat('{name}{@version}'),
                getattr(exception, 'message', exception))
        mirror_stats.error()


class MirrorError(spack.error.SpackError):
    """Superclass of all mirror-creation related errors."""

    def __init__(self, msg, long_msg=None):
        super(MirrorError, self).__init__(msg, long_msg)
