# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os.path

import pytest

from llnl.util.filesystem import touch

import spack.builder
import spack.paths
import spack.repo
import spack.spec


@pytest.fixture()
def builder_test_repository():
    builder_test_path = os.path.join(spack.paths.repos_path, "builder.test")
    with spack.repo.use_repositories(builder_test_path) as mock_repo:
        yield mock_repo


@pytest.mark.parametrize(
    "spec_str,expected_values",
    [
        (
            "callbacks@2.0",
            [
                ("BEFORE_INSTALL_1_CALLED", "1"),
                ("BEFORE_INSTALL_2_CALLED", "1"),
                ("CALLBACKS_INSTALL_CALLED", "1"),
                ("AFTER_INSTALL_1_CALLED", "1"),
                ("TEST_VALUE", "3"),
                ("INSTALL_VALUE", "CALLBACKS"),
            ],
        ),
        # The last callback is conditional on "@1.0", check it's being executed
        (
            "callbacks@1.0",
            [
                ("BEFORE_INSTALL_1_CALLED", "1"),
                ("BEFORE_INSTALL_2_CALLED", "1"),
                ("CALLBACKS_INSTALL_CALLED", "1"),
                ("AFTER_INSTALL_1_CALLED", "1"),
                ("AFTER_INSTALL_2_CALLED", "1"),
                ("TEST_VALUE", "4"),
                ("INSTALL_VALUE", "CALLBACKS"),
            ],
        ),
        # The package below adds to "callbacks" using inheritance, test that using super()
        # works with builder hierarchies
        (
            "inheritance@1.0",
            [
                ("DERIVED_BEFORE_INSTALL_CALLED", "1"),
                ("BEFORE_INSTALL_1_CALLED", "1"),
                ("BEFORE_INSTALL_2_CALLED", "1"),
                ("CALLBACKS_INSTALL_CALLED", "1"),
                ("INHERITANCE_INSTALL_CALLED", "1"),
                ("AFTER_INSTALL_1_CALLED", "1"),
                ("AFTER_INSTALL_2_CALLED", "1"),
                ("TEST_VALUE", "4"),
                ("INSTALL_VALUE", "INHERITANCE"),
            ],
        ),
        # Generate custom phases using a GenericBuilder
        (
            "custom-phases",
            [("CONFIGURE_CALLED", "1"), ("INSTALL_CALLED", "1"), ("LAST_PHASE", "INSTALL")],
        ),
        # Old-style package, with phase defined in base builder
        ("old-style-autotools@1.0", [("AFTER_AUTORECONF_1_CALLED", "1")]),
        ("old-style-autotools@2.0", [("AFTER_AUTORECONF_2_CALLED", "1")]),
        ("old-style-custom-phases", [("AFTER_CONFIGURE_CALLED", "1"), ("TEST_VALUE", "0")]),
    ],
)
@pytest.mark.usefixtures("builder_test_repository", "config")
@pytest.mark.disable_clean_stage_check
def test_callbacks_and_installation_procedure(spec_str, expected_values, working_env):
    """Test the correct execution of callbacks and installation procedures for packages."""
    s = spack.spec.Spec(spec_str).concretized()
    builder = spack.builder.create(s.package)
    for phase_fn in builder:
        phase_fn.execute()

    # Check calls have produced the expected side effects
    for var_name, expected in expected_values:
        assert os.environ[var_name] == expected, os.environ


@pytest.mark.usefixtures("builder_test_repository", "config")
@pytest.mark.parametrize(
    "spec_str,method_name,expected",
    [
        # Call a function defined on the package, which calls the same function defined
        # on the super(builder)
        ("old-style-autotools", "configure_args", ["--with-foo"]),
        # Call a function defined on the package, which calls the same function defined on the
        # super(pkg), which calls the same function defined in the super(builder)
        ("old-style-derived", "configure_args", ["--with-bar", "--with-foo"]),
    ],
)
def test_old_style_compatibility_with_super(spec_str, method_name, expected):
    s = spack.spec.Spec(spec_str).concretized()
    builder = spack.builder.create(s.package)
    value = getattr(builder, method_name)()
    assert value == expected


@pytest.mark.not_on_windows("log_ouput cannot currently be used outside of subprocess on Windows")
@pytest.mark.regression("33928")
@pytest.mark.usefixtures("builder_test_repository", "config", "working_env")
@pytest.mark.disable_clean_stage_check
def test_build_time_tests_are_executed_from_default_builder():
    s = spack.spec.Spec("old-style-autotools").concretized()
    builder = spack.builder.create(s.package)
    builder.pkg.run_tests = True
    for phase_fn in builder:
        phase_fn.execute()

    assert os.environ.get("CHECK_CALLED") == "1", "Build time tests not executed"
    assert os.environ.get("INSTALLCHECK_CALLED") == "1", "Install time tests not executed"


@pytest.mark.regression("34518")
@pytest.mark.usefixtures("builder_test_repository", "config", "working_env")
def test_monkey_patching_wrapped_pkg():
    """Confirm 'run_tests' is accessible through wrappers."""
    s = spack.spec.Spec("old-style-autotools").concretized()
    builder = spack.builder.create(s.package)
    assert s.package.run_tests is False
    assert builder.pkg.run_tests is False
    assert builder.pkg_with_dispatcher.run_tests is False

    s.package.run_tests = True
    assert builder.pkg.run_tests is True
    assert builder.pkg_with_dispatcher.run_tests is True


@pytest.mark.regression("34440")
@pytest.mark.usefixtures("builder_test_repository", "config", "working_env")
def test_monkey_patching_test_log_file():
    """Confirm 'test_log_file' is accessible through wrappers."""
    s = spack.spec.Spec("old-style-autotools").concretized()
    builder = spack.builder.create(s.package)

    s.package.tester.test_log_file = "/some/file"
    assert builder.pkg.tester.test_log_file == "/some/file"
    assert builder.pkg_with_dispatcher.tester.test_log_file == "/some/file"


# Windows context manager's __exit__ fails with ValueError ("I/O operation
# on closed file").
@pytest.mark.not_on_windows("Does not run on windows")
def test_install_time_test_callback(tmpdir, config, mock_packages, mock_stage):
    """Confirm able to run stand-alone test as a post-install callback."""
    s = spack.spec.Spec("py-test-callback").concretized()
    builder = spack.builder.create(s.package)
    builder.pkg.run_tests = True
    s.package.tester.test_log_file = tmpdir.join("install_test.log")
    touch(s.package.tester.test_log_file)

    for phase_fn in builder:
        phase_fn.execute()

    with open(s.package.tester.test_log_file, "r") as f:
        results = f.read().replace("\n", " ")
        assert "PyTestCallback test" in results


@pytest.mark.regression("43097")
@pytest.mark.usefixtures("builder_test_repository", "config")
def test_mixins_with_builders(working_env):
    """Tests that run_after and run_before callbacks are accumulated correctly,
    when mixins are used with builders.
    """
    s = spack.spec.Spec("builder-and-mixins").concretized()
    builder = spack.builder.create(s.package)

    # Check that callbacks added by the mixin are in the list
    assert any(fn.__name__ == "before_install" for _, fn in builder.run_before_callbacks)
    assert any(fn.__name__ == "after_install" for _, fn in builder.run_after_callbacks)

    # Check that callback from the GenericBuilder are in the list too
    assert any(fn.__name__ == "sanity_check_prefix" for _, fn in builder.run_after_callbacks)
