# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import functools
import operator
import os
import re
import shutil
import stat
from typing import Dict, Iterable, List, Mapping, Optional, Tuple

import archspec

import llnl.util.filesystem as fs
import llnl.util.lang as lang
import llnl.util.tty as tty
from llnl.util.filesystem import HeaderList, LibraryList, join_path

import spack.builder
import spack.config
import spack.deptypes as dt
import spack.detection
import spack.multimethod
import spack.package_base
import spack.platforms
import spack.repo
import spack.spec
import spack.store
from spack.directives import build_system, depends_on, extends
from spack.error import NoHeadersError, NoLibrariesError
from spack.install_test import test_part
from spack.spec import Spec
from spack.util.prefix import Prefix

from ._checks import BaseBuilder, execute_install_time_tests


def _flatten_dict(dictionary: Mapping[str, object]) -> Iterable[str]:
    """Iterable that yields KEY=VALUE paths through a dictionary.

    Args:
        dictionary: Possibly nested dictionary of arbitrary keys and values.

    Yields:
        A single path through the dictionary.
    """
    for key, item in dictionary.items():
        if isinstance(item, dict):
            # Recursive case
            for value in _flatten_dict(item):
                yield f"{key}={value}"
        else:
            # Base case
            yield f"{key}={item}"


class PythonExtension(spack.package_base.PackageBase):
    @property
    def import_modules(self) -> Iterable[str]:
        """Names of modules that the Python package provides.

        These are used to test whether or not the installation succeeded.
        These names generally come from running:

        .. code-block:: python

           >> import setuptools
           >> setuptools.find_packages()

        in the source tarball directory. If the module names are incorrectly
        detected, this property can be overridden by the package.

        Returns:
            List of strings of module names.
        """
        modules = []
        pkg = self.spec["python"].package

        # Packages may be installed in platform-specific or platform-independent
        # site-packages directories
        for directory in {pkg.platlib, pkg.purelib}:
            root = os.path.join(self.prefix, directory)

            # Some Python libraries are packages: collections of modules
            # distributed in directories containing __init__.py files
            for path in fs.find(root, "__init__.py", recursive=True):
                modules.append(
                    path.replace(root + os.sep, "", 1)
                    .replace(os.sep + "__init__.py", "")
                    .replace("/", ".")
                )

            # Some Python libraries are modules: individual *.py files
            # found in the site-packages directory
            for path in fs.find(root, "*.py", recursive=False):
                modules.append(
                    path.replace(root + os.sep, "", 1).replace(".py", "").replace("/", ".")
                )

        modules = [
            mod
            for mod in modules
            if re.match("[a-zA-Z0-9._]+$", mod) and not any(map(mod.startswith, self.skip_modules))
        ]

        tty.debug("Detected the following modules: {0}".format(modules))

        return modules

    @property
    def skip_modules(self) -> Iterable[str]:
        """Names of modules that should be skipped when running tests.

        These are a subset of import_modules. If a module has submodules,
        they are skipped as well (meaning a.b is skipped if a is contained).

        Returns:
            List of strings of module names.
        """
        return []

    @property
    def bindir(self) -> str:
        """Path to Python package's bindir, bin on unix like OS's Scripts on Windows"""
        windows = self.spec.satisfies("platform=windows")
        return join_path(self.spec.prefix, "Scripts" if windows else "bin")

    def view_file_conflicts(self, view, merge_map):
        """Report all file conflicts, excepting special cases for python.
        Specifically, this does not report errors for duplicate
        __init__.py files for packages in the same namespace.
        """
        conflicts = list(dst for src, dst in merge_map.items() if os.path.exists(dst))

        if conflicts and self.py_namespace:
            ext_map = view.extensions_layout.extension_map(self.extendee_spec)
            namespaces = set(x.package.py_namespace for x in ext_map.values())
            namespace_re = r"site-packages/{0}/__init__.py".format(self.py_namespace)
            find_namespace = lang.match_predicate(namespace_re)
            if self.py_namespace in namespaces:
                conflicts = list(x for x in conflicts if not find_namespace(x))

        return conflicts

    def add_files_to_view(self, view, merge_map, skip_if_exists=True):
        # Patch up shebangs if the package extends Python and we put a Python interpreter in the
        # view.
        if not self.extendee_spec:
            return super().add_files_to_view(view, merge_map, skip_if_exists)

        python, *_ = self.spec.dependencies("python-venv") or self.spec.dependencies("python")

        if python.external:
            return super().add_files_to_view(view, merge_map, skip_if_exists)

        # We only patch shebangs in the bin directory.
        copied_files: Dict[Tuple[int, int], str] = {}  # File identifier -> source
        delayed_links: List[Tuple[str, str]] = []  # List of symlinks from merge map
        bin_dir = self.spec.prefix.bin

        for src, dst in merge_map.items():
            if skip_if_exists and os.path.lexists(dst):
                continue

            if not fs.path_contains_subdirectory(src, bin_dir):
                view.link(src, dst)
                continue

            s = os.lstat(src)

            # Symlink is delayed because we may need to re-target if its target is copied in view
            if stat.S_ISLNK(s.st_mode):
                delayed_links.append((src, dst))
                continue

            # If it's executable and has a shebang, copy and patch it.
            if (s.st_mode & 0b111) and fs.has_shebang(src):
                copied_files[(s.st_dev, s.st_ino)] = dst
                shutil.copy2(src, dst)
                fs.filter_file(
                    python.prefix, os.path.abspath(view.get_projection_for_spec(self.spec)), dst
                )
            else:
                view.link(src, dst)

        # Finally re-target the symlinks that point to copied files.
        for src, dst in delayed_links:
            try:
                s = os.stat(src)
                target = copied_files[(s.st_dev, s.st_ino)]
            except (OSError, KeyError):
                target = None
            if target:
                os.symlink(os.path.relpath(target, os.path.dirname(dst)), dst)
            else:
                view.link(src, dst, spec=self.spec)

    def remove_files_from_view(self, view, merge_map):
        ignore_namespace = False
        if self.py_namespace:
            ext_map = view.extensions_layout.extension_map(self.extendee_spec)
            remaining_namespaces = set(
                spec.package.py_namespace for name, spec in ext_map.items() if name != self.name
            )
            if self.py_namespace in remaining_namespaces:
                namespace_init = lang.match_predicate(
                    r"site-packages/{0}/__init__.py".format(self.py_namespace)
                )
                ignore_namespace = True

        bin_dir = self.spec.prefix.bin

        to_remove = []
        for src, dst in merge_map.items():
            if ignore_namespace and namespace_init(dst):
                continue

            if not fs.path_contains_subdirectory(src, bin_dir):
                to_remove.append(dst)
            else:
                os.remove(dst)

        view.remove_files(to_remove)

    def test_imports(self) -> None:
        """Attempts to import modules of the installed package."""

        # Make sure we are importing the installed modules,
        # not the ones in the source directory
        python = self.module.python
        for module in self.import_modules:
            with test_part(
                self,
                f"test_imports_{module}",
                purpose=f"checking import of {module}",
                work_dir="spack-test",
            ):
                python("-c", f"import {module}")

    def update_external_dependencies(self, extendee_spec=None):
        """
        Ensure all external python packages have a python dependency

        If another package in the DAG depends on python, we use that
        python for the dependency of the external. If not, we assume
        that the external PythonPackage is installed into the same
        directory as the python it depends on.
        """
        # TODO: Include this in the solve, rather than instantiating post-concretization
        if "python" not in self.spec:
            if extendee_spec:
                python = extendee_spec
            elif "python" in self.spec.root:
                python = self.spec.root["python"]
            else:
                python = self.get_external_python_for_prefix()
                if not python.concrete:
                    repo = spack.repo.PATH.repo_for_pkg(python)
                    python.namespace = repo.namespace

                    # Ensure architecture information is present
                    if not python.architecture:
                        host_platform = spack.platforms.host()
                        host_os = host_platform.operating_system("default_os")
                        host_target = host_platform.target("default_target")
                        python.architecture = spack.spec.ArchSpec(
                            (str(host_platform), str(host_os), str(host_target))
                        )
                    else:
                        if not python.architecture.platform:
                            python.architecture.platform = spack.platforms.host()
                        if not python.architecture.os:
                            python.architecture.os = "default_os"
                        if not python.architecture.target:
                            python.architecture.target = archspec.cpu.host().family.name

                    # Ensure compiler information is present
                    if not python.compiler:
                        python.compiler = self.spec.compiler

                    python.external_path = self.spec.external_path
                    python._mark_concrete()
            self.spec.add_dependency_edge(python, depflag=dt.BUILD | dt.LINK | dt.RUN, virtuals=())

    def get_external_python_for_prefix(self):
        """
        For an external package that extends python, find the most likely spec for the python
        it depends on.

        First search: an "installed" external that shares a prefix with this package
        Second search: a configured external that shares a prefix with this package
        Third search: search this prefix for a python package

        Returns:
          spack.spec.Spec: The external Spec for python most likely to be compatible with self.spec
        """
        python_externals_installed = [
            s for s in spack.store.STORE.db.query("python") if s.prefix == self.spec.external_path
        ]
        if python_externals_installed:
            return python_externals_installed[0]

        python_external_config = spack.config.get("packages:python:externals", [])
        python_externals_configured = [
            spack.spec.parse_with_version_concrete(item["spec"])
            for item in python_external_config
            if item["prefix"] == self.spec.external_path
        ]
        if python_externals_configured:
            return python_externals_configured[0]

        python_externals_detection = spack.detection.by_path(
            ["python"], path_hints=[self.spec.external_path]
        )

        python_externals_detected = [
            spec
            for spec in python_externals_detection.get("python", [])
            if spec.external_path == self.spec.external_path
        ]
        if python_externals_detected:
            return python_externals_detected[0]

        raise StopIteration("No external python could be detected for %s to depend on" % self.spec)


class PythonPackage(PythonExtension):
    """Specialized class for packages that are built using pip."""

    #: Package name, version, and extension on PyPI
    pypi: Optional[str] = None

    # To be used in UI queries that require to know which
    # build-system class we are using
    build_system_class = "PythonPackage"
    #: Legacy buildsystem attribute used to deserialize and install old specs
    legacy_buildsystem = "python_pip"

    #: Callback names for install-time test
    install_time_test_callbacks = ["test_imports"]

    build_system("python_pip")

    with spack.multimethod.when("build_system=python_pip"):
        extends("python")
        depends_on("py-pip", type="build")
        # FIXME: technically wheel is only needed when building from source, not when
        # installing a downloaded wheel, but I don't want to add wheel as a dep to every
        # package manually
        depends_on("py-wheel", type="build")

    py_namespace: Optional[str] = None

    @lang.classproperty
    def homepage(cls) -> Optional[str]:  # type: ignore[override]
        if cls.pypi:
            name = cls.pypi.split("/")[0]
            return f"https://pypi.org/project/{name}/"
        return None

    @lang.classproperty
    def url(cls) -> Optional[str]:
        if cls.pypi:
            return f"https://files.pythonhosted.org/packages/source/{cls.pypi[0]}/{cls.pypi}"
        return None

    @lang.classproperty
    def list_url(cls) -> Optional[str]:  # type: ignore[override]
        if cls.pypi:
            name = cls.pypi.split("/")[0]
            return f"https://pypi.org/simple/{name}/"
        return None

    @property
    def python_spec(self):
        """Get python-venv if it exists or python otherwise."""
        python, *_ = self.spec.dependencies("python-venv") or self.spec.dependencies("python")
        return python

    @property
    def headers(self) -> HeaderList:
        """Discover header files in platlib."""

        # Remove py- prefix in package name
        name = self.spec.name[3:]

        # Headers should only be in include or platlib, but no harm in checking purelib too
        include = self.prefix.join(self.spec["python"].package.include).join(name)
        python = self.python_spec
        platlib = self.prefix.join(python.package.platlib).join(name)
        purelib = self.prefix.join(python.package.purelib).join(name)

        headers_list = map(fs.find_all_headers, [include, platlib, purelib])
        headers = functools.reduce(operator.add, headers_list)

        if headers:
            return headers

        msg = "Unable to locate {} headers in {}, {}, or {}"
        raise NoHeadersError(msg.format(self.spec.name, include, platlib, purelib))

    @property
    def libs(self) -> LibraryList:
        """Discover libraries in platlib."""

        # Remove py- prefix in package name
        name = self.spec.name[3:]

        # Libraries should only be in platlib, but no harm in checking purelib too
        python = self.python_spec
        platlib = self.prefix.join(python.package.platlib).join(name)
        purelib = self.prefix.join(python.package.purelib).join(name)

        find_all_libraries = functools.partial(fs.find_all_libraries, recursive=True)
        libs_list = map(find_all_libraries, [platlib, purelib])
        libs = functools.reduce(operator.add, libs_list)

        if libs:
            return libs

        msg = "Unable to recursively locate {} libraries in {} or {}"
        raise NoLibrariesError(msg.format(self.spec.name, platlib, purelib))


@spack.builder.builder("python_pip")
class PythonPipBuilder(BaseBuilder):
    phases = ("install",)

    #: Names associated with package methods in the old build-system format
    legacy_methods = ("test_imports",)

    #: Same as legacy_methods, but the signature is different
    legacy_long_methods = ("install_options", "global_options", "config_settings")

    #: Names associated with package attributes in the old build-system format
    legacy_attributes = ("archive_files", "build_directory", "install_time_test_callbacks")

    #: Callback names for install-time test
    install_time_test_callbacks = ["test_imports"]

    @staticmethod
    def std_args(cls) -> List[str]:
        return [
            # Verbose
            "-vvv",
            # Disable prompting for input
            "--no-input",
            # Disable the cache
            "--no-cache-dir",
            # Don't check to see if pip is up-to-date
            "--disable-pip-version-check",
            # Install packages
            "install",
            # Don't install package dependencies
            "--no-deps",
            # Overwrite existing packages
            "--ignore-installed",
            # Use env vars like PYTHONPATH
            "--no-build-isolation",
            # Don't warn that prefix.bin is not in PATH
            "--no-warn-script-location",
            # Ignore the PyPI package index
            "--no-index",
        ]

    @property
    def build_directory(self) -> str:
        """The root directory of the Python package.

        This is usually the directory containing one of the following files:

        * ``pyproject.toml``
        * ``setup.cfg``
        * ``setup.py``
        """
        return self.pkg.stage.source_path

    def config_settings(self, spec: Spec, prefix: Prefix) -> Mapping[str, object]:
        """Configuration settings to be passed to the PEP 517 build backend.

        Requires pip 22.1 or newer for keys that appear only a single time,
        or pip 23.1 or newer if the same key appears multiple times.

        Args:
            spec: Build spec.
            prefix: Installation prefix.

        Returns:
            Possibly nested dictionary of KEY, VALUE settings.
        """
        return {}

    def install_options(self, spec: Spec, prefix: Prefix) -> Iterable[str]:
        """Extra arguments to be supplied to the setup.py install command.

        Requires pip 23.0 or older.

        Args:
            spec: Build spec.
            prefix: Installation prefix.

        Returns:
            List of options.
        """
        return []

    def global_options(self, spec: Spec, prefix: Prefix) -> Iterable[str]:
        """Extra global options to be supplied to the setup.py call before the install
        or bdist_wheel command.

        Deprecated in pip 23.1.

        Args:
            spec: Build spec.
            prefix: Installation prefix.

        Returns:
            List of options.
        """
        return []

    def install(self, pkg: PythonPackage, spec: Spec, prefix: Prefix) -> None:
        """Install everything from build directory."""
        pip = spec["python"].command
        pip.add_default_arg("-m", "pip")

        args = PythonPipBuilder.std_args(pkg) + [f"--prefix={prefix}"]

        for setting in _flatten_dict(self.config_settings(spec, prefix)):
            args.append(f"--config-settings={setting}")
        for option in self.install_options(spec, prefix):
            args.append(f"--install-option={option}")
        for option in self.global_options(spec, prefix):
            args.append(f"--global-option={option}")

        if pkg.stage.archive_file and pkg.stage.archive_file.endswith(".whl"):
            args.append(pkg.stage.archive_file)
        else:
            args.append(".")

        with fs.working_dir(self.build_directory):
            pip(*args)

    spack.builder.run_after("install")(execute_install_time_tests)
