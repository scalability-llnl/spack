# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Classes and functions to manage package tags"""
import collections
import copy
from collections.abc import Mapping

import spack.error
import spack.repo
import spack.util.spack_json as sjson


def _get_installed_package_names():
    """Returns names of packages installed in the active environment."""
    import spack.environment

    specs = spack.environment.installed_specs()
    return [spec.name for spec in specs]


def packages_with_tags(tags, installed, skip_empty):
    """
    Returns a dict, indexed by tag, containing lists of names of packages
    containing the tag or, if no tags, for all available tags.

    Arguments:
        tags (list or None): list of tags of interest or None for all
        installed (bool): True if want names of packages that are installed;
            otherwise, False if want all packages with the tag
        skip_empty (bool): True if exclude tags with no associated packages;
            otherwise, False if want entries for all tags even when no such
            tagged packages
    """
    tag_pkgs = collections.defaultdict(lambda: list)
    spec_names = _get_installed_package_names() if installed else []
    keys = spack.repo.PATH.tag_index if tags is None else tags
    for tag in keys:
        packages = [
            name for name in spack.repo.PATH.tag_index[tag] if not installed or name in spec_names
        ]
        if packages or not skip_empty:
            tag_pkgs[tag] = packages
    return tag_pkgs


class TagIndex(Mapping):
    """Maps tags to list of packages."""

    def __init__(self, repository):
        self._tag_dict = collections.defaultdict(list)
        self.repository = repository

    @property
    def tags(self):
        return self._tag_dict

    def to_json(self, stream):
        sjson.dump({"tags": self._tag_dict}, stream)

    @staticmethod
    def from_json(stream, repository):
        d = sjson.load(stream)

        if not isinstance(d, dict):
            raise TagIndexError("TagIndex data was not a dict.")

        if "tags" not in d:
            raise TagIndexError("TagIndex data does not start with 'tags'")

        r = TagIndex(repository=repository)

        for tag, packages in d["tags"].items():
            r[tag].extend(packages)

        return r

    def __getitem__(self, item):
        return self._tag_dict[item]

    def __iter__(self):
        return iter(self._tag_dict)

    def __len__(self):
        return len(self._tag_dict)

    def copy(self):
        """Return a deep copy of this index."""
        clone = TagIndex(repository=self.repository)
        clone._tag_dict = copy.deepcopy(self._tag_dict)
        return clone

    def get_packages(self, tag):
        """Returns all packages associated with the tag."""
        return self.tags[tag] if tag in self.tags else []

    def merge(self, other):
        """Merge another tag index into this one.

        Args:
            other (TagIndex): tag index to be merged
        """
        other = other.copy()  # defensive copy.

        for tag in other.tags:
            if tag not in self.tags:
                self.tags[tag] = other.tags[tag]
                continue

            spkgs, opkgs = self.tags[tag], other.tags[tag]
            self.tags[tag] = sorted(list(set(spkgs + opkgs)))

    def update_package(self, pkg_name):
        """Updates a package in the tag index.

        Args:
            pkg_name (str): name of the package to be removed from the index
        """
        pkg_cls = self.repository.get_pkg_class(pkg_name)

        # Remove the package from the list of packages, if present
        for pkg_list in self._tag_dict.values():
            if pkg_name in pkg_list:
                pkg_list.remove(pkg_name)

        # Add it again under the appropriate tags
        for tag in getattr(pkg_cls, "tags", []):
            tag = tag.lower()
            self._tag_dict[tag].append(pkg_cls.name)


class TagIndexError(spack.error.SpackError):
    """Raised when there is a problem with a TagIndex."""
