# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""
This module contains the traversal logic and models that can be used to generate
depfiles from an environment.
"""

import os
import re
import shlex
from enum import Enum
from typing import List, Optional

import spack.deptypes as dt
import spack.environment.environment as ev
import spack.paths
import spack.spec
import spack.traverse as traverse


class UseBuildCache(Enum):
    ONLY = 1
    NEVER = 2
    AUTO = 3

    @staticmethod
    def from_string(s: str) -> "UseBuildCache":
        if s == "only":
            return UseBuildCache.ONLY
        elif s == "never":
            return UseBuildCache.NEVER
        elif s == "auto":
            return UseBuildCache.AUTO
        raise ValueError(f"invalid value for UseBuildCache: {s}")


def _deptypes(use_buildcache: UseBuildCache):
    """What edges should we follow for a given node? If it's a cache-only
    node, then we can drop build type deps."""
    return (
        dt.LINK | dt.RUN if use_buildcache == UseBuildCache.ONLY else dt.BUILD | dt.LINK | dt.RUN
    )


class DepfileNode:
    """Contains a spec, a subset of its dependencies, and a flag whether it should be
    buildcache only/never/auto."""

    def __init__(
        self, target: spack.spec.Spec, prereqs: List[spack.spec.Spec], buildcache: UseBuildCache
    ):
        self.target = MakefileSpec(target)
        self.prereqs = list(MakefileSpec(x) for x in prereqs)
        if buildcache == UseBuildCache.ONLY:
            self.buildcache_flag = "--use-buildcache=only"
        elif buildcache == UseBuildCache.NEVER:
            self.buildcache_flag = "--use-buildcache=never"
        else:
            self.buildcache_flag = ""


class DepfileSpecVisitor:
    """This visitor produces an adjacency list of a (reduced) DAG, which
    is used to generate depfile targets with their prerequisites. Currently
    it only drops build deps when using buildcache only mode.

    Note that the DAG could be reduced even more by dropping build edges of specs
    installed at the moment the depfile is generated, but that would produce
    stateful depfiles that would not fail when the database is wiped later."""

    def __init__(self, pkg_buildcache: UseBuildCache, deps_buildcache: UseBuildCache):
        self.adjacency_list: List[DepfileNode] = []
        self.pkg_buildcache = pkg_buildcache
        self.deps_buildcache = deps_buildcache
        self.depflag_root = _deptypes(pkg_buildcache)
        self.depflag_deps = _deptypes(deps_buildcache)

    def neighbors(self, node):
        """Produce a list of spec to follow from node"""
        depflag = self.depflag_root if node.depth == 0 else self.depflag_deps
        return traverse.sort_edges(node.edge.spec.edges_to_dependencies(depflag=depflag))

    def accept(self, node):
        self.adjacency_list.append(
            DepfileNode(
                target=node.edge.spec,
                prereqs=[edge.spec for edge in self.neighbors(node)],
                buildcache=self.pkg_buildcache if node.depth == 0 else self.deps_buildcache,
            )
        )

        # We already accepted this
        return True


class MakefileSpec(object):
    """Limited interface to spec to help generate targets etc. without
    introducing unwanted special characters.
    """

    _pattern = None

    def __init__(self, spec):
        self.spec = spec

    def safe_name(self):
        return self.safe_format("{name}-{version}-{hash}")

    def spec_hash(self):
        return self.spec.dag_hash()

    def safe_format(self, format_str):
        unsafe_result = self.spec.format(format_str)
        if not MakefileSpec._pattern:
            MakefileSpec._pattern = re.compile(r"[^A-Za-z0-9_.-]")
        return MakefileSpec._pattern.sub("_", unsafe_result)

    def unsafe_format(self, format_str):
        return self.spec.format(format_str)


class MakefileModel:
    """This class produces all data to render a makefile for specs of an environment."""

    def __init__(
        self,
        env: ev.Environment,
        roots: List[spack.spec.Spec],
        adjacency_list: List[DepfileNode],
        make_prefix: Optional[str],
        jobserver: bool,
    ):
        """
        Args:
            env: environment to generate the makefile for
            roots: specs that get built in the default target
            adjacency_list: list of DepfileNode, mapping specs to their dependencies
            make_prefix: prefix for makefile targets
            jobserver: when enabled, make will invoke Spack with jobserver support. For
                dry-run this should be disabled.
        """
        # Currently we can only use depfile with an environment since Spack needs to
        # find the concrete specs somewhere.
        self.env_path = env.path

        # These specs are built in the default target.
        self.roots = list(MakefileSpec(x) for x in roots)

        # The SPACK_PACKAGE_IDS variable is "exported", which can be used when including
        # generated makefiles to add post-install hooks, like pushing to a buildcache,
        # running tests, etc.
        if make_prefix is None:
            self.make_prefix = os.path.join(env.env_subdir_path, "makedeps")
            self.pkg_identifier_variable = "SPACK_PACKAGE_IDS"
        else:
            # NOTE: GNU Make allows directory separators in variable names, so for consistency
            # we can namespace this variable with the same prefix as targets.
            self.make_prefix = make_prefix
            self.pkg_identifier_variable = os.path.join(make_prefix, "SPACK_PACKAGE_IDS")

        # And here we collect a tuple of (target, prereqs, dag_hash, nice_name, buildcache_flag)
        self.make_adjacency_list = [
            (
                item.target.safe_name(),
                " ".join(self._install_target(s.safe_name()) for s in item.prereqs),
                item.target.spec_hash(),
                item.target.unsafe_format(
                    "{name}{@version}{%compiler}{variants}{arch=architecture}"
                ),
                item.buildcache_flag,
            )
            for item in adjacency_list
        ]

        # Root specs without deps are the prereqs for the environment target
        self.root_install_targets = [self._install_target(s.safe_name()) for s in self.roots]

        self.jobserver_support = "+" if jobserver else ""

        # All package identifiers, used to generate the SPACK_PACKAGE_IDS variable
        self.all_pkg_identifiers: List[str] = []

        # All install and install-deps targets
        self.all_install_related_targets: List[str] = []

        # Convenience shortcuts: ensure that `make install/pkg-version-hash` triggers
        # <absolute path to env>/.spack-env/makedeps/install/pkg-version-hash in case
        # we don't have a custom make target prefix.
        self.phony_convenience_targets: List[str] = []

        for node in adjacency_list:
            tgt = node.target.safe_name()
            self.all_pkg_identifiers.append(tgt)
            self.all_install_related_targets.append(self._install_target(tgt))
            self.all_install_related_targets.append(self._install_deps_target(tgt))
            if make_prefix is None:
                self.phony_convenience_targets.append(os.path.join("install", tgt))
                self.phony_convenience_targets.append(os.path.join("install-deps", tgt))

    def _target(self, name: str) -> str:
        # The `all` and `clean` targets are phony. It doesn't make sense to
        # have /abs/path/to/env/metadir/{all,clean} targets. But it *does* make
        # sense to have a prefix like `env/all`, `env/clean` when they are
        # supposed to be included
        if name in ("all", "clean") and os.path.isabs(self.make_prefix):
            return name
        else:
            return os.path.join(self.make_prefix, name)

    def _install_target(self, name: str) -> str:
        return os.path.join(self.make_prefix, "install", name)

    def _install_deps_target(self, name: str) -> str:
        return os.path.join(self.make_prefix, "install-deps", name)

    def to_dict(self):
        return {
            "all_target": self._target("all"),
            "env_target": self._target("env"),
            "clean_target": self._target("clean"),
            "all_install_related_targets": " ".join(self.all_install_related_targets),
            "root_install_targets": " ".join(self.root_install_targets),
            "dirs_target": self._target("dirs"),
            "environment": self.env_path,
            "install_target": self._target("install"),
            "install_deps_target": self._target("install-deps"),
            "any_hash_target": self._target("%"),
            "jobserver_support": self.jobserver_support,
            "spack_script": shlex.quote(spack.paths.spack_script),
            "adjacency_list": self.make_adjacency_list,
            "phony_convenience_targets": " ".join(self.phony_convenience_targets),
            "pkg_ids_variable": self.pkg_identifier_variable,
            "pkg_ids": " ".join(self.all_pkg_identifiers),
        }

    @property
    def empty(self):
        return len(self.roots) == 0

    @staticmethod
    def from_env(
        env: ev.Environment,
        *,
        filter_specs: Optional[List[spack.spec.Spec]] = None,
        pkg_buildcache: UseBuildCache = UseBuildCache.AUTO,
        dep_buildcache: UseBuildCache = UseBuildCache.AUTO,
        make_prefix: Optional[str] = None,
        jobserver: bool = True,
    ) -> "MakefileModel":
        """Produces a MakefileModel from an environment and a list of specs.

        Args:
            env: the environment to use
            filter_specs: if provided, only these specs will be built from the environment,
                otherwise the environment roots are used.
            pkg_buildcache: whether to only use the buildcache for top-level specs.
            dep_buildcache: whether to only use the buildcache for non-top-level specs.
            make_prefix: the prefix for the makefile targets
            jobserver: when enabled, make will invoke Spack with jobserver support. For
                dry-run this should be disabled.
        """
        roots = env.all_matching_specs(*filter_specs) if filter_specs else env.concrete_roots()
        visitor = DepfileSpecVisitor(pkg_buildcache, dep_buildcache)
        traverse.traverse_breadth_first_with_visitor(
            roots, traverse.CoverNodesVisitor(visitor, key=lambda s: s.dag_hash())
        )

        return MakefileModel(env, roots, visitor.adjacency_list, make_prefix, jobserver)
