# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
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
import collections
import collections.abc
import operator
import os
import os.path
import sys
import traceback
import urllib.parse
from typing import List, Optional, Union

import llnl.url
import llnl.util.symlink
import llnl.util.tty as tty
from llnl.util.filesystem import mkdirp

import spack.caches
import spack.config
import spack.error
import spack.fetch_strategy
import spack.mirror
import spack.oci.image
import spack.repo
import spack.spec
import spack.util.path
import spack.util.spack_json as sjson
import spack.util.spack_yaml as syaml
import spack.util.url as url_util
import spack.version

#: What schemes do we support
supported_url_schemes = ("file", "http", "https", "sftp", "ftp", "s3", "gs", "oci")


def _url_or_path_to_url(url_or_path: str) -> str:
    """For simplicity we allow mirror URLs in config files to be local, relative paths.
    This helper function takes care of distinguishing between URLs and paths, and
    canonicalizes paths before transforming them into file:// URLs."""
    # Is it a supported URL already? Then don't do path-related canonicalization.
    parsed = urllib.parse.urlparse(url_or_path)
    if parsed.scheme in supported_url_schemes:
        return url_or_path

    # Otherwise we interpret it as path, and we should promote it to file:// URL.
    return url_util.path_to_file_url(spack.util.path.canonicalize_path(url_or_path))


class Mirror:
    """Represents a named location for storing source tarballs and binary
    packages.

    Mirrors have a fetch_url that indicate where and how artifacts are fetched
    from them, and a push_url that indicate where and how artifacts are pushed
    to them. These two URLs are usually the same.
    """

    def __init__(self, data: Union[str, dict], name: Optional[str] = None):
        self._data = data
        self._name = name

    @staticmethod
    def from_yaml(stream, name=None):
        return Mirror(syaml.load(stream), name)

    @staticmethod
    def from_json(stream, name=None):
        try:
            return Mirror(sjson.load(stream), name)
        except Exception as e:
            raise sjson.SpackJSONError("error parsing JSON mirror:", str(e)) from e

    @staticmethod
    def from_local_path(path: str):
        return Mirror(url_util.path_to_file_url(path))

    @staticmethod
    def from_url(url: str):
        """Create an anonymous mirror by URL. This method validates the URL."""
        if not urllib.parse.urlparse(url).scheme in supported_url_schemes:
            raise ValueError(
                '"{}" is not a valid mirror URL. Scheme must be once of {}.'.format(
                    url, ", ".join(supported_url_schemes)
                )
            )
        return Mirror(url)

    def __eq__(self, other):
        if not isinstance(other, Mirror):
            return NotImplemented
        return self._data == other._data and self._name == other._name

    def __str__(self):
        return f"{self._name}: {self.push_url} {self.fetch_url}"

    def __repr__(self):
        return f"Mirror(name={self._name!r}, data={self._data!r})"

    def to_json(self, stream=None):
        return sjson.dump(self.to_dict(), stream)

    def to_yaml(self, stream=None):
        return syaml.dump(self.to_dict(), stream)

    def to_dict(self):
        return self._data

    def display(self, max_len=0):
        fetch, push = self.fetch_url, self.push_url
        # don't print the same URL twice
        url = fetch if fetch == push else f"fetch: {fetch} push: {push}"
        source = "s" if self.source else " "
        binary = "b" if self.binary else " "
        print(f"{self.name: <{max_len}} [{source}{binary}] {url}")

    @property
    def name(self):
        return self._name or "<unnamed>"

    @property
    def binary(self):
        return isinstance(self._data, str) or self._data.get("binary", True)

    @property
    def source(self):
        return isinstance(self._data, str) or self._data.get("source", True)

    @property
    def signed(self) -> bool:
        return isinstance(self._data, str) or self._data.get("signed", True)

    @property
    def autopush(self) -> bool:
        if isinstance(self._data, str):
            return False
        return self._data.get("autopush", False)

    @property
    def fetch_url(self):
        """Get the valid, canonicalized fetch URL"""
        return self.get_url("fetch")

    @property
    def push_url(self):
        """Get the valid, canonicalized fetch URL"""
        return self.get_url("push")

    def _update_connection_dict(self, current_data: dict, new_data: dict, top_level: bool):
        keys = ["url", "access_pair", "access_token", "profile", "endpoint_url"]
        if top_level:
            keys += ["binary", "source", "signed", "autopush"]
        changed = False
        for key in keys:
            if key in new_data and current_data.get(key) != new_data[key]:
                current_data[key] = new_data[key]
                changed = True
        return changed

    def update(self, data: dict, direction: Optional[str] = None) -> bool:
        """Modify the mirror with the given data. This takes care
        of expanding trivial mirror definitions by URL to something more
        rich with a dict if necessary

        Args:
            data (dict): The data to update the mirror with.
            direction (str): The direction to update the mirror in (fetch
                or push or None for top-level update)

        Returns:
            bool: True if the mirror was updated, False otherwise."""

        # Modify the top-level entry when no direction is given.
        if not data:
            return False

        # If we only update a URL, there's typically no need to expand things to a dict.
        set_url = data["url"] if len(data) == 1 and "url" in data else None

        if direction is None:
            # First deal with the case where the current top-level entry is just a string.
            if isinstance(self._data, str):
                # Can we replace that string with something new?
                if set_url:
                    if self._data == set_url:
                        return False
                    self._data = set_url
                    return True

                # Otherwise promote to a dict
                self._data = {"url": self._data}

            # And update the dictionary accordingly.
            return self._update_connection_dict(self._data, data, top_level=True)

        # Otherwise, update the fetch / push entry; turn top-level
        # url string into a dict if necessary.
        if isinstance(self._data, str):
            self._data = {"url": self._data}

        # Create a new fetch / push entry if necessary
        if direction not in self._data:
            # Keep config minimal if we're just setting the URL.
            if set_url:
                self._data[direction] = set_url
                return True
            self._data[direction] = {}

        entry = self._data[direction]

        # Keep the entry simple if we're just swapping out the URL.
        if isinstance(entry, str):
            if set_url:
                if entry == set_url:
                    return False
                self._data[direction] = set_url
                return True

            # Otherwise promote to a dict
            self._data[direction] = {"url": entry}

        return self._update_connection_dict(self._data[direction], data, top_level=False)

    def _get_value(self, attribute: str, direction: str):
        """Returns the most specific value for a given attribute (either push/fetch or global)"""
        if direction not in ("fetch", "push"):
            raise ValueError(f"direction must be either 'fetch' or 'push', not {direction}")

        if isinstance(self._data, str):
            return None

        # Either a string (url) or a dictionary, we care about the dict here.
        value = self._data.get(direction, {})

        # Return top-level entry if only a URL was set.
        if isinstance(value, str) or attribute not in value:
            return self._data.get(attribute)

        return value[attribute]

    def get_url(self, direction: str) -> str:
        if direction not in ("fetch", "push"):
            raise ValueError(f"direction must be either 'fetch' or 'push', not {direction}")

        # Whole mirror config is just a url.
        if isinstance(self._data, str):
            return _url_or_path_to_url(self._data)

        # Default value
        url = self._data.get("url")

        # Override it with a direction-specific value
        if direction in self._data:
            # Either a url as string or a dict with url key
            info = self._data[direction]
            if isinstance(info, str):
                url = info
            elif "url" in info:
                url = info["url"]

        if not url:
            raise ValueError(f"Mirror {self.name} has no URL configured")

        return _url_or_path_to_url(url)

    def get_access_token(self, direction: str) -> Optional[str]:
        return self._get_value("access_token", direction)

    def get_access_pair(self, direction: str) -> Optional[List]:
        return self._get_value("access_pair", direction)

    def get_profile(self, direction: str) -> Optional[str]:
        return self._get_value("profile", direction)

    def get_endpoint_url(self, direction: str) -> Optional[str]:
        return self._get_value("endpoint_url", direction)


class MirrorCollection(collections.abc.Mapping):
    """A mapping of mirror names to mirrors."""

    def __init__(
        self,
        mirrors=None,
        scope=None,
        binary: Optional[bool] = None,
        source: Optional[bool] = None,
        autopush: Optional[bool] = None,
    ):
        """Initialize a mirror collection.

        Args:
            mirrors: A name-to-mirror mapping to initialize the collection with.
            scope: The scope to use when looking up mirrors from the config.
            binary: If True, only include binary mirrors.
                    If False, omit binary mirrors.
                    If None, do not filter on binary mirrors.
            source: If True, only include source mirrors.
                    If False, omit source mirrors.
                    If None, do not filter on source mirrors.
            autopush: If True, only include mirrors that have autopush enabled.
                      If False, omit mirrors that have autopush enabled.
                      If None, do not filter on autopush."""
        mirrors_data = (
            mirrors.items()
            if mirrors is not None
            else spack.config.get("mirrors", scope=scope).items()
        )
        mirrors = (Mirror(data=mirror, name=name) for name, mirror in mirrors_data)

        def _filter(m: Mirror):
            if source is not None and m.source != source:
                return False
            if binary is not None and m.binary != binary:
                return False
            if autopush is not None and m.autopush != autopush:
                return False
            return True

        self._mirrors = {m.name: m for m in mirrors if _filter(m)}

    def __eq__(self, other):
        return self._mirrors == other._mirrors

    def to_json(self, stream=None):
        return sjson.dump(self.to_dict(True), stream)

    def to_yaml(self, stream=None):
        return syaml.dump(self.to_dict(True), stream)

    # TODO: this isn't called anywhere
    @staticmethod
    def from_yaml(stream, name=None):
        data = syaml.load(stream)
        return MirrorCollection(data)

    @staticmethod
    def from_json(stream, name=None):
        try:
            d = sjson.load(stream)
            return MirrorCollection(d)
        except Exception as e:
            raise sjson.SpackJSONError("error parsing JSON mirror collection:", str(e)) from e

    def to_dict(self, recursive=False):
        return syaml.syaml_dict(
            sorted(
                ((k, (v.to_dict() if recursive else v)) for (k, v) in self._mirrors.items()),
                key=operator.itemgetter(0),
            )
        )

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
            result = Mirror(fetch=name_or_url)

        return result

    def __iter__(self):
        return iter(self._mirrors)

    def __len__(self):
        return len(self._mirrors)


def _determine_extension(fetcher):
    if isinstance(fetcher, spack.fetch_strategy.URLFetchStrategy):
        if fetcher.expand_archive:
            # If we fetch with a URLFetchStrategy, use URL's archive type
            ext = llnl.url.determine_url_file_extension(fetcher.url)

            if ext:
                # Remove any leading dots
                ext = ext.lstrip(".")
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
        ext = "tar.gz"

    return ext


class MirrorLayout:
    """A ``MirrorLayout`` object describes the relative path of a mirror entry."""

    def __init__(self, path: str) -> None:
        self.path = path

    def __iter__(self):
        """Yield all paths including aliases where the resource can be found."""
        yield self.path

    def make_alias(self, root: str) -> None:
        """Make the entry ``root / self.path`` available under a human readable alias"""
        pass


class DefaultLayout(MirrorLayout):
    def __init__(self, alias_path: str, digest_path: Optional[str] = None) -> None:
        # When we have a digest, it is used as the primary storage location. If not, then we use
        # the human-readable alias. In case of mirrors of a VCS checkout, we currently do not have
        # a digest, that's why an alias is required and a digest optional.
        super().__init__(path=digest_path or alias_path)
        self.alias = alias_path
        self.digest_path = digest_path

    def make_alias(self, root: str) -> None:
        """Symlink a human readible path in our mirror to the actual storage location."""
        # We already use the human-readable path as the main storage location.
        if not self.digest_path:
            return

        alias, digest = os.path.join(root, self.alias), os.path.join(root, self.digest_path)

        alias_dir = os.path.dirname(alias)
        relative_dst = os.path.relpath(digest, start=alias_dir)

        mkdirp(alias_dir)
        tmp = f"{alias}.tmp"
        llnl.util.symlink.symlink(relative_dst, tmp)

        try:
            os.rename(tmp, alias)
        except OSError:
            # Clean up the temporary if possible
            try:
                os.unlink(tmp)
            except OSError:
                pass
            raise

    def __iter__(self):
        if self.digest_path:
            yield self.digest_path
        yield self.alias


class OCILayout(MirrorLayout):
    """Follow the OCI Image Layout Specification to archive blobs where paths are of the form
    ``blobs/<algorithm>/<digest>``"""

    def __init__(self, digest: spack.oci.image.Digest) -> None:
        super().__init__(os.path.join("blobs", digest.algorithm, digest.digest))


def default_mirror_layout(
    fetcher: "spack.fetch_strategy.FetchStrategy",
    per_package_ref: str,
    spec: Optional["spack.spec.Spec"] = None,
) -> MirrorLayout:
    """Returns a ``MirrorReference`` object which keeps track of the relative
    storage path of the resource associated with the specified ``fetcher``."""
    ext = None
    if spec:
        pkg_cls = spack.repo.PATH.get_pkg_class(spec.name)
        versions = pkg_cls.versions.get(spec.version, {})
        ext = versions.get("extension", None)
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
        global_ref = os.path.join("_source-cache", global_ref)
    if global_ref and ext:
        global_ref += ".%s" % ext

    return DefaultLayout(per_package_ref, global_ref)


def get_all_versions(specs):
    """Given a set of initial specs, return a new set of specs that includes
    each version of each package in the original set.

    Note that if any spec in the original set specifies properties other than
    version, this information will be omitted in the new set; for example; the
    new set of specs will not include variant settings.
    """
    version_specs = []
    for spec in specs:
        pkg_cls = spack.repo.PATH.get_pkg_class(spec.name)
        # Skip any package that has no known versions.
        if not pkg_cls.versions:
            tty.msg("No safe (checksummed) versions for package %s" % pkg_cls.name)
            continue

        for version in pkg_cls.versions:
            version_spec = spack.spec.Spec(pkg_cls.name)
            version_spec.versions = spack.version.VersionList([version])
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
            if spec.concrete or v.intersects(spec.versions):
                s = spack.spec.Spec(pkg.name)
                s.versions = spack.version.VersionList([v])
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


def create(path, specs, skip_unstable_versions=False):
    """Create a directory to be used as a spack mirror, and fill it with
    package archives.

    Arguments:
        path: Path to create a mirror directory hierarchy in.
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
    """
    # automatically spec-ify anything in the specs array.
    specs = [s if isinstance(s, spack.spec.Spec) else spack.spec.Spec(s) for s in specs]

    mirror_cache, mirror_stats = mirror_cache_and_stats(path, skip_unstable_versions)
    for spec in specs:
        mirror_stats.next_spec(spec)
        create_mirror_from_package_object(spec.package, mirror_cache, mirror_stats)

    return mirror_stats.stats()


def mirror_cache_and_stats(path, skip_unstable_versions=False):
    """Return both a mirror cache and a mirror stats, starting from the path
    where a mirror ought to be created.

    Args:
        path (str): path to create a mirror directory hierarchy in.
        skip_unstable_versions: if true, this skips adding resources when
            they do not have a stable archive checksum (as determined by
            ``fetch_strategy.stable_target``)
    """
    # Get the absolute path of the root before we start jumping around.
    if not os.path.isdir(path):
        try:
            mkdirp(path)
        except OSError as e:
            raise MirrorError("Cannot create directory '%s':" % path, str(e))
    mirror_cache = spack.caches.MirrorCache(path, skip_unstable_versions=skip_unstable_versions)
    mirror_stats = MirrorStats()
    return mirror_cache, mirror_stats


def add(mirror: Mirror, scope=None):
    """Add a named mirror in the given scope"""
    mirrors = spack.config.get("mirrors", scope=scope)
    if not mirrors:
        mirrors = syaml.syaml_dict()

    if mirror.name in mirrors:
        tty.die("Mirror with name {} already exists.".format(mirror.name))

    items = [(n, u) for n, u in mirrors.items()]
    items.insert(0, (mirror.name, mirror.to_dict()))
    mirrors = syaml.syaml_dict(items)
    spack.config.set("mirrors", mirrors, scope=scope)


def remove(name, scope):
    """Remove the named mirror in the given scope"""
    mirrors = spack.config.get("mirrors", scope=scope)
    if not mirrors:
        mirrors = syaml.syaml_dict()

    if name not in mirrors:
        tty.die("No mirror with name %s" % name)

    mirrors.pop(name)
    spack.config.set("mirrors", mirrors, scope=scope)
    tty.msg("Removed mirror %s." % name)


class MirrorStats:
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


def create_mirror_from_package_object(pkg_obj, mirror_cache, mirror_stats):
    """Add a single package object to a mirror.

    The package object is only required to have an associated spec
    with a concrete version.

    Args:
        pkg_obj (spack.package_base.PackageBase): package object with to be added.
        mirror_cache (spack.caches.MirrorCache): mirror where to add the spec.
        mirror_stats (spack.mirror.MirrorStats): statistics on the current mirror

    Return:
        True if the spec was added successfully, False otherwise
    """
    tty.msg("Adding package {} to mirror".format(pkg_obj.spec.format("{name}{@version}")))
    num_retries = 3
    while num_retries > 0:
        try:
            # Includes patches and resources
            with pkg_obj.stage as pkg_stage:
                pkg_stage.cache_mirror(mirror_cache, mirror_stats)
            exception = None
            break
        except Exception as e:
            exc_tuple = sys.exc_info()
            exception = e
        num_retries -= 1
    if exception:
        if spack.config.get("config:debug"):
            traceback.print_exception(file=sys.stderr, *exc_tuple)
        else:
            tty.warn(
                "Error while fetching %s" % pkg_obj.spec.cformat("{name}{@version}"),
                getattr(exception, "message", exception),
            )
        mirror_stats.error()
        return False
    return True


def require_mirror_name(mirror_name):
    """Find a mirror by name and raise if it does not exist"""
    mirror = spack.mirror.MirrorCollection().get(mirror_name)
    if not mirror:
        raise ValueError('no mirror named "{0}"'.format(mirror_name))
    return mirror


class MirrorError(spack.error.SpackError):
    """Superclass of all mirror-creation related errors."""

    def __init__(self, msg, long_msg=None):
        super().__init__(msg, long_msg)
