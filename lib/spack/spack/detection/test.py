# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Create and run mock e2e tests for package detection."""
import collections
import contextlib
import pathlib
import tempfile
from typing import Any, Deque, Dict, Generator, List, NamedTuple, Tuple

from llnl.util import filesystem

import spack.platforms
import spack.repo
import spack.spec
from spack.util import spack_yaml

from .path import by_path


class MockExecutables(NamedTuple):
    """Mock executables to be used in detection tests"""

    #: Relative paths for mock executables to be created
    executables: List[str]
    #: Shell script for the mock executable
    script: str


class ExpectedTestResult(NamedTuple):
    """Data structure to model assertions on detection tests"""

    #: Spec to be detected
    spec: str
    #: Attributes expected in the external spec
    extra_attributes: Dict[str, str]


class DetectionTest(NamedTuple):
    """Data structure to construct detection tests by PATH inspection.

    Packages may have a YAML file containing the description of one or more detection tests
    to be performed. Each test creates a few mock executable scripts in a temporary folder,
    and checks that detection by PATH gives the expected results.
    """

    pkg_name: str
    layout: List[MockExecutables]
    results: List[ExpectedTestResult]


class Runner:
    """Runs an external detection test"""

    def __init__(self, *, test: DetectionTest, repository: spack.repo.RepoPath) -> None:
        self.test = test
        self.repository = repository
        self.tmpdir = tempfile.TemporaryDirectory()

    def execute(self) -> List[spack.spec.Spec]:
        """Executes a test and returns the specs that have been detected.

        This function sets-up a test in a temporary directory, according to the prescriptions
        in the test layout, then performs a detection by executables and returns the specs that
        have been detected.
        """
        with self._mock_layout() as path_hints:
            entries = by_path([self.test.pkg_name], path_hints=path_hints)
            _, unqualified_name = spack.repo.partition_package_name(self.test.pkg_name)
            specs = set(entries[unqualified_name])
        return list(specs)

    @contextlib.contextmanager
    def _mock_layout(self) -> Generator[List[str], None, None]:
        hints = set()
        try:
            for entry in self.test.layout:
                exes = self._create_executable_scripts(entry)

                for mock_executable in exes:
                    hints.add(str(mock_executable.parent))

            yield list(hints)
        finally:
            self.tmpdir.cleanup()

    def _create_executable_scripts(self, mock_executables: MockExecutables) -> List[pathlib.Path]:
        import jinja2

        relative_paths = mock_executables.executables
        script = mock_executables.script
        script_template = jinja2.Template("#!/bin/bash\n{{ script }}\n")
        result = []
        for mock_exe_path in relative_paths:
            rel_path = pathlib.Path(mock_exe_path)
            abs_path = pathlib.Path(self.tmpdir.name) / rel_path
            abs_path.parent.mkdir(parents=True, exist_ok=True)
            abs_path.write_text(script_template.render(script=script))
            filesystem.set_executable(abs_path)
            result.append(abs_path)
        return result

    @property
    def expected_specs(self) -> List[spack.spec.Spec]:
        return [
            spack.spec.Spec.from_detection(
                item.spec, external_path=self.tmpdir.name, extra_attributes=item.extra_attributes
            )
            for item in self.test.results
        ]


def detection_tests(pkg_name: str, repository: spack.repo.RepoPath) -> List[Runner]:
    """Returns a list of test runners for a given package.

    Currently, detection tests are specified in a YAML file, called ``detection_test.yaml``,
    alongside the ``package.py`` file.

    This function reads that file to create a bunch of ``Runner`` objects.

    Args:
        pkg_name: name of the package to test
        repository: repository where the package lives
    """
    result = []
    detection_tests_content = read_detection_tests(pkg_name, repository)
    current_platform = str(spack.platforms.host())

    tests_by_path = detection_tests_content.get("paths", [])
    for single_test_data in tests_by_path:
        if current_platform not in single_test_data.get("platforms", [current_platform]):
            continue

        mock_executables = []
        for layout in single_test_data["layout"]:
            mock_executables.append(
                MockExecutables(executables=layout["executables"], script=layout["script"])
            )
        expected_results = []
        for assertion in single_test_data["results"]:
            expected_results.append(
                ExpectedTestResult(
                    spec=assertion["spec"], extra_attributes=assertion.get("extra_attributes", {})
                )
            )

        current_test = DetectionTest(
            pkg_name=pkg_name, layout=mock_executables, results=expected_results
        )
        result.append(Runner(test=current_test, repository=repository))

    return result


def read_detection_tests(pkg_name: str, repository: spack.repo.RepoPath) -> Dict[str, Any]:
    """Returns the normalized content of the detection_tests.yaml associated with the package
    passed in input.

    The content is merged with that of any package that is transitively included using the
    "includes" attribute.

    Args:
        pkg_name: name of the package to test
        repository: repository in which to search for packages
    """
    content_stack, seen = [], set()
    included_packages: Deque[str] = collections.deque()

    root_detection_yaml, result = _detection_tests_yaml(pkg_name, repository)
    included_packages.extend(result.get("includes", []))
    seen |= set(result.get("includes", []))

    while included_packages:
        current_package = included_packages.popleft()
        try:
            current_detection_yaml, content = _detection_tests_yaml(current_package, repository)
        except FileNotFoundError as e:
            msg = (
                f"cannot read the detection tests from the '{current_package}' package, "
                f"included by {root_detection_yaml}"
            )
            raise FileNotFoundError(msg + f"\n\n\t{e}\n")

        content_stack.append((current_package, content))
        included_packages.extend(x for x in content.get("includes", []) if x not in seen)
        seen |= set(content.get("includes", []))

    result.setdefault("paths", [])
    for pkg_name, content in content_stack:
        result["paths"].extend(content.get("paths", []))

    return result


def _detection_tests_yaml(
    pkg_name: str, repository: spack.repo.RepoPath
) -> Tuple[pathlib.Path, Dict[str, Any]]:
    pkg_dir = pathlib.Path(repository.filename_for_package_name(pkg_name)).parent
    detection_tests_yaml = pkg_dir / "detection_test.yaml"
    with open(str(detection_tests_yaml)) as f:
        content = spack_yaml.load(f)
    return detection_tests_yaml, content
