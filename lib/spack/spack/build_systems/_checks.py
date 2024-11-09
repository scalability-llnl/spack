# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
from typing import List

import llnl.util.lang

import spack.builder
import spack.error
import spack.relocate
import spack.spec
import spack.store


def sanity_check_prefix(builder: spack.builder.Builder):
    """Check that specific directories and files are created after installation.

    The files to be checked are in the ``sanity_check_is_file`` attribute of the
    package object, while the directories are in the ``sanity_check_is_dir``.

    Args:
        builder: builder that installed the package
    """
    pkg = builder.pkg

    def check_paths(path_list, filetype, predicate):
        if isinstance(path_list, str):
            path_list = [path_list]

        for path in path_list:
            abs_path = os.path.join(pkg.prefix, path)
            if not predicate(abs_path):
                msg = "Install failed for {0}. No such {1} in prefix: {2}"
                msg = msg.format(pkg.name, filetype, path)
                raise spack.error.InstallError(msg)

    check_paths(pkg.sanity_check_is_file, "file", os.path.isfile)
    check_paths(pkg.sanity_check_is_dir, "directory", os.path.isdir)

    ignore_file = llnl.util.lang.match_predicate(spack.store.STORE.layout.hidden_file_regexes)
    if all(map(ignore_file, os.listdir(pkg.prefix))):
        msg = "Install failed for {0}.  Nothing was installed!"
        raise spack.error.InstallError(msg.format(pkg.name))


def apply_macos_rpath_fixups(builder: spack.builder.Builder):
    """On Darwin, make installed libraries more easily relocatable.

    Some build systems (handrolled, autotools, makefiles) can set their own
    rpaths that are duplicated by spack's compiler wrapper. This fixup
    interrogates, and postprocesses if necessary, all libraries installed
    by the code.

    It should be added as a @run_after to packaging systems (or individual
    packages) that do not install relocatable libraries by default.

    Args:
        builder: builder that installed the package
    """
    spack.relocate.fixup_macos_rpaths(builder.spec)


def ensure_build_dependencies_or_raise(
    spec: spack.spec.Spec, dependencies: List[spack.spec.Spec], error_msg: str
):
    """Ensure that some build dependencies are present in the concrete spec.

    If not, raise a RuntimeError with a helpful error message.

    Args:
        spec: concrete spec to be checked.
        dependencies: list of abstract specs to be satisfied
        error_msg: brief error message to be prepended to a longer description

    Raises:
          RuntimeError: when the required build dependencies are not found
    """
    assert spec.concrete, "Can ensure build dependencies only on concrete specs"
    build_deps = [d.name for d in spec.dependencies(deptype="build")]
    missing_deps = [x for x in dependencies if x not in build_deps]

    if not missing_deps:
        return

    # Raise an exception on missing deps.
    msg = (
        "{0}: missing dependencies: {1}.\n\nPlease add "
        "the following lines to the package:\n\n".format(
            error_msg, ", ".join(str(d) for d in missing_deps)
        )
    )

    for dep in missing_deps:
        msg += '    depends_on("{0}", type="build", when="@{1} {2}")\n'.format(
            dep, spec.version, "build_system=autotools"
        )

    msg += '\nUpdate the version (when="@{0}") as needed.'.format(spec.version)
    raise RuntimeError(msg)


def execute_build_time_tests(builder: spack.builder.Builder):
    """Execute the build-time tests prescribed by builder.

    Args:
        builder: builder prescribing the test callbacks. The name of the callbacks is
            stored as a list of strings in the ``build_time_test_callbacks`` attribute.
    """
    if not builder.pkg.run_tests or not builder.build_time_test_callbacks:
        return

    builder.pkg.tester.phase_tests(builder, "build", builder.build_time_test_callbacks)


def execute_install_time_tests(builder: spack.builder.Builder):
    """Execute the install-time tests prescribed by builder.

    Args:
        builder: builder prescribing the test callbacks. The name of the callbacks is
            stored as a list of strings in the ``install_time_test_callbacks`` attribute.
    """
    if not builder.pkg.run_tests or not builder.install_time_test_callbacks:
        return

    builder.pkg.tester.phase_tests(builder, "install", builder.install_time_test_callbacks)


class BaseBuilder(spack.builder.Builder):
    """Base class for builders to register common checks"""

    # Check that self.prefix is there after installation
    spack.builder.run_after("install")(sanity_check_prefix)
