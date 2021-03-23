# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Infrastructure used by tests for mocking packages and repos."""

import ordereddict_backport

import spack.util.naming
import spack.provider_index
from spack.dependency import Dependency
from spack.spec import Spec
from spack.version import Version

__all__ = ["MockPackageMultiRepo"]


class MockPackageBase(object):
    """Internal base class for mocking ``spack.package.PackageBase``.

    Use ``MockPackageMultiRepo.add_package()`` to create new instances.

    """
    virtual = False

    def __init__(self, dependencies, dependency_types,
                 conditions=None, versions=None):
        """Instantiate a new MockPackageBase.

        This is not for general use; it needs to be constructed by a
        ``MockPackageMultiRepo``, as we need to know about *all* packages
        to find possible depenencies.

        """
        self.spec = None
        self._installed_upstream = False

    def provides(self, vname):
        return vname in self.provided

    @property
    def virtuals_provided(self):
        return [v.name for v, c in self.provided]

    @classmethod
    def possible_dependencies(
            cls, transitive=True, deptype='all', visited=None, virtuals=None):
        visited = {} if visited is None else visited

        for name, conditions in cls.dependencies.items():
            # check whether this dependency could be of the type asked for
            types = [dep.type for cond, dep in conditions.items()]
            types = set.union(*types)
            if not any(d in types for d in deptype):
                continue

        visited.setdefault(cls.name, set())
        for dep_name in cls.dependencies:
            if dep_name in visited:
                continue

            visited.setdefault(dep_name, set())

            if not transitive:
                continue

            cls._repo.get(dep_name).possible_dependencies(
                transitive, deptype, visited, virtuals)

        return visited

    def content_hash(self):
        # Unlike real packages, MockPackage doesn't have a corresponding
        # package.py file; in that sense, the content_hash is always the same.
        return self.__class__.__name__


class MockPackageMultiRepo(object):
    """Mock package repository, mimicking ``spack.repo.Repo``."""

    def __init__(self):
        self.spec_to_pkg = {}
        self.namespace = ''
        self.full_namespace = 'spack.pkg.mock'

    def get(self, spec):
        if not isinstance(spec, spack.spec.Spec):
            spec = Spec(spec)
        if spec.name not in self.spec_to_pkg:
            raise spack.repo.UnknownPackageError(spec.fullname)
        return self.spec_to_pkg[spec.name]

    def get_pkg_class(self, name):
        return self.spec_to_pkg[name]

    def exists(self, name):
        return name in self.spec_to_pkg

    def is_virtual(self, name, use_index=True):
        return False

    def repo_for_pkg(self, name):
        import collections
        Repo = collections.namedtuple('Repo', ['namespace'])
        return Repo('mockrepo')

    def __contains__(self, item):
        return item in self.spec_to_pkg

    def add_package(self, name, dependencies=None, dependency_types=None,
                    conditions=None):
        """Factory method for creating mock packages.

        This creates a new subclass of ``MockPackageBase``, ensures that its
        ``name`` and ``__name__`` properties are set up correctly, and
        returns a new instance.

        We use a factory function here because many functions and properties
        of packages need to be class functions.

        Args:
            name (str): name of the new package
            dependencies (list): list of mock packages to be dependencies
                for this new package (optional; no deps if not provided)
            dependency_type (list): list of deptypes for each dependency
                (optional; will be default_deptype if not provided)
            conditions (list): condition specs for each dependency (optional)

        """
        if not dependencies:
            dependencies = []

        if not dependency_types:
            dependency_types = [
                spack.dependency.default_deptype] * len(dependencies)

        assert len(dependencies) == len(dependency_types)

        # new class for the mock package
        class MockPackage(MockPackageBase):
            pass
        MockPackage.__name__ = spack.util.naming.mod_to_class(name)
        MockPackage.name = name
        MockPackage._repo = self

        # set up dependencies
        MockPackage.dependencies = ordereddict_backport.OrderedDict()
        for dep, dtype in zip(dependencies, dependency_types):
            d = Dependency(MockPackage, Spec(dep.name), type=dtype)
            if not conditions or dep.name not in conditions:
                MockPackage.dependencies[dep.name] = {Spec(name): d}
            else:
                dep_conditions = conditions[dep.name]
                dep_conditions = dict(
                    (Spec(x), Dependency(MockPackage, Spec(y), type=dtype))
                    for x, y in dep_conditions.items())
                MockPackage.dependencies[dep.name] = dep_conditions

        # each package has some fake versions
        versions = list(Version(x) for x in [1, 2, 3])
        MockPackage.versions = dict(
            (x, {'preferred': False}) for x in versions
        )

        MockPackage.variants = {}
        MockPackage.provided = {}
        MockPackage.conflicts = {}
        MockPackage.patches = {}

        mock_package = MockPackage(
            dependencies, dependency_types, conditions, versions)
        self.spec_to_pkg[name] = mock_package
        self.spec_to_pkg["mockrepo." + name] = mock_package

        return mock_package

    @property
    def provider_index(self):
        return spack.provider_index.ProviderIndex()
