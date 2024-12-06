# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Tools to produce reports of spec installations"""
import collections
import contextlib
import functools
import gzip
import os
import time
import traceback
from typing import Any, Callable, Dict, List, Type

import llnl.util.lang

import spack.build_environment
import spack.install_test
import spack.installer
import spack.package_base
import spack.reporters
import spack.spec


class InfoCollector:
    """Base class for context manager objects that collect information during the execution of
    certain package functions.

    The data collected is available through the ``specs`` attribute once exited, and it's
    organized as a list where each item represents the installation of one spec.

    """

    wrap_class: Type
    do_fn: str
    _backup_do_fn: Callable
    input_specs: List[spack.spec.Spec]
    specs: List[Dict[str, Any]]

    def __init__(self, wrap_class: Type, do_fn: str, specs: List[spack.spec.Spec]):
        #: Class for which to wrap a function
        self.wrap_class = wrap_class
        #: Action to be reported on
        self.do_fn = do_fn
        #: Backup of the wrapped class function
        self._backup_do_fn = getattr(self.wrap_class, do_fn)
        #: Specs that will be acted on
        self.input_specs = specs
        #: This is where we record the data that will be included in our report
        self.specs: List[Dict[str, Any]] = []

    def fetch_log(self, pkg: spack.package_base.PackageBase) -> str:
        """Return the stdout log associated with the function being monitored

        Args:
            pkg: package under consideration
        """
        raise NotImplementedError("must be implemented by derived classes")

    def extract_package_from_signature(self, instance, *args, **kwargs):
        """Return the package instance, given the signature of the wrapped function."""
        raise NotImplementedError("must be implemented by derived classes")

    def __enter__(self):
        # Initialize the spec report with the data that is available upfront.
        Property = collections.namedtuple("Property", ["name", "value"])
        for input_spec in self.input_specs:
            name_fmt = "{0}_{1}"
            name = name_fmt.format(input_spec.name, input_spec.dag_hash(length=7))
            spec_record = {
                "name": name,
                "nerrors": None,
                "nfailures": None,
                "npackages": None,
                "time": None,
                "timestamp": time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime()),
                "properties": [],
                "packages": [],
            }
            spec_record["properties"].append(Property("architecture", input_spec.architecture))
            spec_record["properties"].append(Property("compiler", input_spec.compiler))
            self.init_spec_record(input_spec, spec_record)
            self.specs.append(spec_record)

        def gather_info(wrapped_fn):
            """Decorates a function to gather useful information for a CI report."""

            @functools.wraps(wrapped_fn)
            def wrapper(instance, *args, **kwargs):
                pkg = self.extract_package_from_signature(instance, *args, **kwargs)

                package = {
                    "name": pkg.name,
                    "id": pkg.spec.dag_hash(),
                    "elapsed_time": None,
                    "result": None,
                    "message": None,
                    "installed_from_binary_cache": False,
                }

                # Append the package to the correct spec report. In some
                # cases it may happen that a spec that is asked to be
                # installed explicitly will also be installed as a
                # dependency of another spec. In this case append to both
                # spec reports.
                for current_spec in llnl.util.lang.dedupe([pkg.spec.root, pkg.spec]):
                    name = name_fmt.format(current_spec.name, current_spec.dag_hash(length=7))
                    try:
                        item = next((x for x in self.specs if x["name"] == name))
                        item["packages"].append(package)
                    except StopIteration:
                        pass

                start_time = time.time()
                try:
                    value = wrapped_fn(instance, *args, **kwargs)
                    package["stdout"] = self.fetch_log(pkg)
                    package["installed_from_binary_cache"] = pkg.installed_from_binary_cache
                    self.on_success(pkg, kwargs, package)
                    return value

                except spack.build_environment.InstallError as exc:
                    # An InstallError is considered a failure (the recipe
                    # didn't work correctly)
                    package["result"] = "failure"
                    package["message"] = exc.message or "Installation failure"
                    package["stdout"] = self.fetch_log(pkg)
                    package["stdout"] += package["message"]
                    package["exception"] = exc.traceback
                    raise

                except (Exception, BaseException) as exc:
                    # Everything else is an error (the installation
                    # failed outside of the child process)
                    package["result"] = "error"
                    package["message"] = str(exc) or "Unknown error"
                    package["stdout"] = self.fetch_log(pkg)
                    package["stdout"] += package["message"]
                    package["exception"] = traceback.format_exc()
                    raise

                finally:
                    package["elapsed_time"] = time.time() - start_time

            return wrapper

        setattr(self.wrap_class, self.do_fn, gather_info(getattr(self.wrap_class, self.do_fn)))

    def on_success(self, pkg: spack.package_base.PackageBase, kwargs, package_record):
        """Add additional properties on function call success."""
        raise NotImplementedError("must be implemented by derived classes")

    def init_spec_record(self, input_spec: spack.spec.Spec, record):
        """Add additional entries to a spec record when entering the collection context."""

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Restore the original method in PackageBase
        setattr(self.wrap_class, self.do_fn, self._backup_do_fn)
        for spec in self.specs:
            spec["npackages"] = len(spec["packages"])
            spec["nfailures"] = len([x for x in spec["packages"] if x["result"] == "failure"])
            spec["nerrors"] = len([x for x in spec["packages"] if x["result"] == "error"])
            spec["time"] = sum(float(x["elapsed_time"]) for x in spec["packages"])


class BuildInfoCollector(InfoCollector):
    """Collect information for the PackageInstaller._install_task method.

    Args:
        specs: specs whose install information will be recorded
    """

    def __init__(self, specs: List[spack.spec.Spec]):
        super().__init__(spack.installer.PackageInstaller, "_install_task", specs)

    def init_spec_record(self, input_spec, record):
        # Check which specs are already installed and mark them as skipped
        for dep in filter(lambda x: x.installed, input_spec.traverse()):
            package = {
                "name": dep.name,
                "id": dep.dag_hash(),
                "elapsed_time": "0.0",
                "result": "skipped",
                "message": "Spec already installed",
            }
            record["packages"].append(package)

    def on_success(self, pkg, kwargs, package_record):
        package_record["result"] = "success"

    def fetch_log(self, pkg):
        try:
            if os.path.exists(pkg.install_log_path):
                stream = gzip.open(pkg.install_log_path, "rt")
            else:
                stream = open(pkg.log_path)
            with stream as f:
                return f.read()
        except OSError:
            return f"Cannot open log for {pkg.spec.cshort_spec}"

    def extract_package_from_signature(self, instance, *args, **kwargs):
        return args[0].pkg


class TestInfoCollector(InfoCollector):
    """Collect information for the PackageBase.do_test method.

    Args:
        specs: specs whose install information will be recorded
        record_directory: record directory for test log paths
    """

    dir: str

    def __init__(self, specs: List[spack.spec.Spec], record_directory: str):
        super().__init__(spack.package_base.PackageBase, "do_test", specs)
        self.dir = record_directory

    def on_success(self, pkg, kwargs, package_record):
        externals = kwargs.get("externals", False)
        skip_externals = pkg.spec.external and not externals
        if skip_externals:
            package_record["result"] = "skipped"
        package_record["result"] = "success"

    def fetch_log(self, pkg: spack.package_base.PackageBase):
        log_file = os.path.join(self.dir, spack.install_test.TestSuite.test_log_name(pkg.spec))
        try:
            with open(log_file, "r", encoding="utf-8") as stream:
                return "".join(stream.readlines())
        except Exception:
            return f"Cannot open log for {pkg.spec.cshort_spec}"

    def extract_package_from_signature(self, instance, *args, **kwargs):
        return instance


@contextlib.contextmanager
def build_context_manager(
    reporter: spack.reporters.Reporter, filename: str, specs: List[spack.spec.Spec]
):
    """Decorate a package to generate a report after the installation function is executed.

    Args:
        reporter: object that generates the report
        filename:  filename for the report
        specs: specs that need reporting
    """
    collector = BuildInfoCollector(specs)
    try:
        with collector:
            yield
    finally:
        reporter.build_report(filename, specs=collector.specs)


@contextlib.contextmanager
def test_context_manager(
    reporter: spack.reporters.Reporter,
    filename: str,
    specs: List[spack.spec.Spec],
    raw_logs_dir: str,
):
    """Decorate a package to generate a report after the test function is executed.

    Args:
        reporter: object that generates the report
        filename:  filename for the report
        specs: specs that need reporting
        raw_logs_dir: record directory for test log paths
    """
    collector = TestInfoCollector(specs, raw_logs_dir)
    try:
        with collector:
            yield
    finally:
        reporter.test_report(filename, specs=collector.specs)
