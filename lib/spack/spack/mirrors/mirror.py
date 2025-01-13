# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import collections.abc
import operator
import os
import urllib.parse
from typing import Any, Dict, Optional, Tuple, Union

import llnl.util.tty as tty

import spack.config
import spack.util.path
import spack.util.spack_json as sjson
import spack.util.spack_yaml as syaml
import spack.util.url as url_util
from spack.error import MirrorError

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
                f'"{url}" is not a valid mirror URL. '
                f"Scheme must be one of {supported_url_schemes}."
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

    def ensure_mirror_usable(self, direction: str = "push"):
        access_pair = self._get_value("access_pair", direction)
        access_token_variable = self._get_value("access_token_variable", direction)

        errors = []

        # Verify that the credentials that are variables expand
        if access_pair and isinstance(access_pair, dict):
            if "id_variable" in access_pair and access_pair["id_variable"] not in os.environ:
                errors.append(f"id_variable {access_pair['id_variable']} not set in environment")
            if "secret_variable" in access_pair:
                if access_pair["secret_variable"] not in os.environ:
                    errors.append(
                        f"environment variable `{access_pair['secret_variable']}` "
                        "(secret_variable) not set"
                    )

        if access_token_variable:
            if access_token_variable not in os.environ:
                errors.append(
                    f"environment variable `{access_pair['access_token_variable']}` "
                    "(access_token_variable) not set"
                )

        if errors:
            msg = f"invalid {direction} configuration for mirror {self.name}: "
            msg += "\n    ".join(errors)
            raise MirrorError(msg)

    def _update_connection_dict(self, current_data: dict, new_data: dict, top_level: bool):
        # Only allow one to exist in the config
        if "access_token" in current_data and "access_token_variable" in new_data:
            current_data.pop("access_token")
        elif "access_token_variable" in current_data and "access_token" in new_data:
            current_data.pop("access_token_variable")

        # If updating to a new access_pair that is the deprecated list, warn
        warn_deprecated_access_pair = False
        if "access_pair" in new_data:
            warn_deprecated_access_pair = isinstance(new_data["access_pair"], list)
        # If the not updating the current access_pair, and it is the deprecated list, warn
        elif "access_pair" in current_data:
            warn_deprecated_access_pair = isinstance(current_data["access_pair"], list)

        if warn_deprecated_access_pair:
            tty.warn(
                f"in mirror {self.name}: support for plain text secrets in config files "
                "(access_pair: [id, secret]) is deprecated and will be removed in a future Spack "
                "version. Use environment variables instead (access_pair: "
                "{id: ..., secret_variable: ...})"
            )

        keys = [
            "url",
            "access_pair",
            "access_token",
            "access_token_variable",
            "profile",
            "endpoint_url",
        ]
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

    def get_credentials(self, direction: str) -> Dict[str, Any]:
        """Get the mirror credentials from the mirror config

        Args:
            direction: fetch or push mirror config

        Returns:
            Dictionary from credential type string to value

            Credential Type Map:
                access_token -> str
                access_pair  -> tuple(str,str)
                profile      -> str
        """
        creddict: Dict[str, Any] = {}
        access_token = self.get_access_token(direction)
        if access_token:
            creddict["access_token"] = access_token

        access_pair = self.get_access_pair(direction)
        if access_pair:
            creddict.update({"access_pair": access_pair})

        profile = self.get_profile(direction)
        if profile:
            creddict["profile"] = profile

        return creddict

    def get_access_token(self, direction: str) -> Optional[str]:
        tok = self._get_value("access_token_variable", direction)
        if tok:
            return os.environ.get(tok)
        else:
            return self._get_value("access_token", direction)
        return None

    def get_access_pair(self, direction: str) -> Optional[Tuple[str, str]]:
        pair = self._get_value("access_pair", direction)
        if isinstance(pair, (tuple, list)) and len(pair) == 2:
            return (pair[0], pair[1]) if all(pair) else None
        elif isinstance(pair, dict):
            id_ = os.environ.get(pair["id_variable"]) if "id_variable" in pair else pair["id"]
            secret = os.environ.get(pair["secret_variable"])
            return (id_, secret) if id_ and secret else None
        else:
            return None

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
