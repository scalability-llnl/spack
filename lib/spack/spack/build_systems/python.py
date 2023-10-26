# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import inspect
import os
import re
import shutil
import stat
from typing import Optional

import archspec

import llnl.util.filesystem as fs
import llnl.util.lang as lang
import llnl.util.tty as tty

import spack.builder
import spack.config
import spack.deptypes as dt
import spack.detection
import spack.multimethod
import spack.package_base
import spack.spec
import spack.store
from spack.directives import build_system, depends_on, extends, maintainers
from spack.error import NoHeadersError, NoLibrariesError
from spack.install_test import test_part
from spack.util.executable import Executable

from ._checks import BaseBuilder, execute_install_time_tests


def _flatten_dict(dictionary):
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
    maintainers("adamjstewart")

    @property
    def import_modules(self):
        """Names of modules that the Python package provides.

        These are used to test whether or not the installation succeeded.
        These names generally come from running:

        .. code-block:: python

           >> import setuptools
           >> setuptools.find_packages()

        in the source tarball directory. If the module names are incorrectly
        detected, this property can be overridden by the package.

        Returns:
            list: list of strings of module names
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
    def skip_modules(self):
        """Names of modules that should be skipped when running tests.

        These are a subset of import_modules. If a module has submodules,
        they are skipped as well (meaning a.b is skipped if a is contained).

        Returns:
            list: list of strings of module names
        """
        return []

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
        if not self.extendee_spec:
            return super().add_files_to_view(view, merge_map, skip_if_exists)

        bin_dir = self.spec.prefix.bin
        python_prefix = self.extendee_spec.prefix
        python_is_external = self.extendee_spec.external
        global_view = fs.same_path(python_prefix, view.get_projection_for_spec(self.spec))
        for src, dst in merge_map.items():
            if os.path.exists(dst):
                continue
            elif global_view or not fs.path_contains_subdirectory(src, bin_dir):
                view.link(src, dst)
            elif not os.path.islink(src):
                shutil.copy2(src, dst)
                is_script = fs.is_nonsymlink_exe_with_shebang(src)
                if is_script and not python_is_external:
                    fs.filter_file(
                        python_prefix,
                        os.path.abspath(view.get_projection_for_spec(self.spec)),
                        dst,
                    )
            else:
                orig_link_target = os.path.realpath(src)
                new_link_target = os.path.abspath(merge_map[orig_link_target])
                view.link(new_link_target, dst)

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
        global_view = self.extendee_spec.prefix == view.get_projection_for_spec(self.spec)

        to_remove = []
        for src, dst in merge_map.items():
            if ignore_namespace and namespace_init(dst):
                continue

            if global_view or not fs.path_contains_subdirectory(src, bin_dir):
                to_remove.append(dst)
            else:
                os.remove(dst)

        view.remove_files(to_remove)

    def test_imports(self):
        """Attempts to import modules of the installed package."""

        # Make sure we are importing the installed modules,
        # not the ones in the source directory
        python = inspect.getmodule(self).python
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
            d.spec
            for d in python_externals_detection.get("python", [])
            if d.prefix == self.spec.external_path
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
    install_time_test_callbacks = ["test"]

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
    def homepage(cls):
        if cls.pypi:
            name = cls.pypi.split("/")[0]
            return "https://pypi.org/project/" + name + "/"

    @lang.classproperty
    def url(cls):
        if cls.pypi:
            return "https://files.pythonhosted.org/packages/source/" + cls.pypi[0] + "/" + cls.pypi

    @lang.classproperty
    def list_url(cls):
        if cls.pypi:
            name = cls.pypi.split("/")[0]
            return "https://pypi.org/simple/" + name + "/"

    @property
    def headers(self):
        """Discover header files in platlib."""

        # Remove py- prefix in package name
        name = self.spec.name[3:]

        # Headers may be in either location
        include = self.prefix.join(self.spec["python"].package.include).join(name)
        platlib = self.prefix.join(self.spec["python"].package.platlib).join(name)
        headers = fs.find_all_headers(include) + fs.find_all_headers(platlib)

        if headers:
            return headers

        msg = "Unable to locate {} headers in {} or {}"
        raise NoHeadersError(msg.format(self.spec.name, include, platlib))

    @property
    def libs(self):
        """Discover libraries in platlib."""

        # Remove py- prefix in package name
        name = self.spec.name[3:]

        root = self.prefix.join(self.spec["python"].package.platlib).join(name)

        libs = fs.find_all_libraries(root, recursive=True)

        if libs:
            return libs

        msg = "Unable to recursively locate {} libraries in {}"
        raise NoLibrariesError(msg.format(self.spec.name, root))


def fixup_shebangs(path: str, old_interpreter: bytes, new_interpreter: bytes):
    # Recurse into the install prefix and fixup shebangs
    exe = stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
    dirs = [path]
    hardlinks = set()

    while dirs:
        with os.scandir(dirs.pop()) as entries:
            for entry in entries:
                if entry.is_dir(follow_symlinks=False):
                    dirs.append(entry.path)
                    continue

                # Only consider files, not symlinks
                if not entry.is_file(follow_symlinks=False):
                    continue

                lstat = entry.stat(follow_symlinks=False)

                # Skip over files that are not executable
                if not (lstat.st_mode & exe):
                    continue

                # Don't modify hardlinks more than once
                if lstat.st_nlink > 1:
                    key = (lstat.st_ino, lstat.st_dev)
                    if key in hardlinks:
                        continue
                    hardlinks.add(key)

                # Finally replace shebangs if any.
                with open(entry.path, "rb+") as f:
                    contents = f.read(2)
                    if contents != b"#!":
                        continue
                    contents += f.read()

                    if old_interpreter not in contents:
                        continue

                    f.seek(0)
                    f.write(contents.replace(old_interpreter, new_interpreter))
                    f.truncate()


@spack.builder.builder("python_pip")
class PythonPipBuilder(BaseBuilder):
    phases = ("install",)

    #: Names associated with package methods in the old build-system format
    legacy_methods = ("test",)

    #: Same as legacy_methods, but the signature is different
    legacy_long_methods = ("install_options", "global_options", "config_settings")

    #: Names associated with package attributes in the old build-system format
    legacy_attributes = ("build_directory", "install_time_test_callbacks")

    #: Callback names for install-time test
    install_time_test_callbacks = ["test"]

    @staticmethod
    def std_args(cls):
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
    def build_directory(self):
        """The root directory of the Python package.

        This is usually the directory containing one of the following files:

        * ``pyproject.toml``
        * ``setup.cfg``
        * ``setup.py``
        """
        return self.pkg.stage.source_path

    def config_settings(self, spec, prefix):
        """Configuration settings to be passed to the PEP 517 build backend.

        Requires pip 22.1 or newer for keys that appear only a single time,
        or pip 23.1 or newer if the same key appears multiple times.

        Args:
            spec (spack.spec.Spec): build spec
            prefix (spack.util.prefix.Prefix): installation prefix

        Returns:
            dict: Possibly nested dictionary of KEY, VALUE settings
        """
        return {}

    def install_options(self, spec, prefix):
        """Extra arguments to be supplied to the setup.py install command.

        Requires pip 23.0 or older.

        Args:
            spec (spack.spec.Spec): build spec
            prefix (spack.util.prefix.Prefix): installation prefix

        Returns:
            list: list of options
        """
        return []

    def global_options(self, spec, prefix):
        """Extra global options to be supplied to the setup.py call before the install
        or bdist_wheel command.

        Deprecated in pip 23.1.

        Args:
            spec (spack.spec.Spec): build spec
            prefix (spack.util.prefix.Prefix): installation prefix

        Returns:
            list: list of options
        """
        return []

    @property
    def _build_venv_path(self):
        """Return the path to the virtual environment used for building when
        python is external."""
        return os.path.join(self.spec.package.stage.path, "build_env")

    @property
    def _build_venv_python(self) -> Executable:
        """Return the Python executable in the build virtual environment when
        python is external."""
        return Executable(os.path.join(self._build_venv_path, "bin", "python"))

    def install(self, pkg, spec, prefix):
        """Install everything from build directory."""
        python: Executable = spec["python"].command
        # Since we invoke pip with --no-build-isolation, we have to make sure that pip cannot
        # execute hooks from user and system site-packages.
        if spec["python"].external:
            # There are no environment variables to disable the system site-packages, so we use a
            # virtual environment instead. The downside of this approach is that pip produces
            # incorrect shebangs that refer to the virtual environment, which we have to fix up.
            python("-m", "venv", "--without-pip", self._build_venv_path)
            pip = self._build_venv_python
        else:
            # For a Spack managed Python, system site-packages is empty/unused by design, so it
            # suffices to disable user site-packages, for which there is an environment variable.
            pip = python
            pip.add_default_env("PYTHONNOUSERSITE", "1")
        pip.add_default_arg("-m")
        pip.add_default_arg("pip")

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

    @spack.builder.run_after("install")
    def fixup_shebangs_pointing_to_build(self):
        """When installing a package using an external python, we use a temporary virtual
        environment which improves build isolation. The downside is that pip produces shebangs
        that point to the temporary virtual environment. This method fixes them up to point to the
        underlying Python."""
        # No need to fixup shebangs if no build venv was used. (this post install function also
        # runs when install was overridden in another package, so check existence of the venv path)
        if not os.path.exists(self._build_venv_path):
            return

        # Use sys.executable, since that's what pip uses.
        interpreter = (
            lambda python: python("-c", "import sys; print(sys.executable)", output=str)
            .strip()
            .encode("utf-8")
        )

        fixup_shebangs(
            path=self.spec.prefix,
            old_interpreter=interpreter(self._build_venv_python),
            new_interpreter=interpreter(self.spec["python"].command),
        )

    spack.builder.run_after("install")(execute_install_time_tests)
