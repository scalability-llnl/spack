# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import spack.bootstrap
import spack.bootstrap.config
import spack.bootstrap.core
import spack.compilers
import spack.config
import spack.environment
import spack.store
import spack.util.path


@pytest.fixture
def active_mock_environment(mutable_config, mutable_mock_env_path):
    with spack.environment.create("bootstrap-test") as env:
        yield env


@pytest.mark.regression("22294")
def test_store_is_restored_correctly_after_bootstrap(mutable_config, tmpdir):
    """Tests that the store is correctly swapped during bootstrapping, and restored afterward."""
    user_path = str(tmpdir.join("store"))
    with spack.store.use_store(user_path):
        assert spack.store.STORE.root == user_path
        assert spack.config.CONFIG.get("config:install_tree:root") == user_path
        with spack.bootstrap.ensure_bootstrap_configuration():
            assert spack.store.STORE.root == spack.bootstrap.config.store_path()
        assert spack.store.STORE.root == user_path
        assert spack.config.CONFIG.get("config:install_tree:root") == user_path


@pytest.mark.regression("38963")
def test_store_padding_length_is_zero_during_bootstrapping(mutable_config, tmpdir):
    """Tests that, even though padded length is set in user config, the bootstrap store maintains
    a padded length of zero.
    """
    user_path = str(tmpdir.join("store"))
    with spack.store.use_store(user_path, extra_data={"padded_length": 512}):
        assert spack.config.CONFIG.get("config:install_tree:padded_length") == 512
        with spack.bootstrap.ensure_bootstrap_configuration():
            assert spack.store.STORE.root == spack.bootstrap.config.store_path()
            assert spack.config.CONFIG.get("config:install_tree:padded_length") == 0
        assert spack.config.CONFIG.get("config:install_tree:padded_length") == 512


@pytest.mark.regression("38963")
def test_install_tree_customization_is_respected(mutable_config, tmp_path):
    """Tests that a custom user store is respected when we exit the bootstrapping
    environment.
    """
    spack.store.reinitialize()
    store_dir = tmp_path / "store"
    spack.config.CONFIG.set("config:install_tree:root", str(store_dir))
    with spack.bootstrap.ensure_bootstrap_configuration():
        assert spack.store.STORE.root == spack.bootstrap.config.store_path()
        assert (
            spack.config.CONFIG.get("config:install_tree:root")
            == spack.bootstrap.config.store_path()
        )
        assert spack.config.CONFIG.get("config:install_tree:padded_length") == 0
    assert spack.config.CONFIG.get("config:install_tree:root") == str(store_dir)
    assert spack.store.STORE.root == str(store_dir)


@pytest.mark.parametrize(
    "config_value,expected",
    [
        # Absolute path without expansion
        ("/opt/spack/bootstrap", "/opt/spack/bootstrap/store"),
        # Path with placeholder
        ("$spack/opt/bootstrap", "$spack/opt/bootstrap/store"),
    ],
)
def test_store_path_customization(config_value, expected, mutable_config):
    # Set the current configuration to a specific value
    spack.config.set("bootstrap:root", config_value)

    # Check the store path
    current = spack.bootstrap.config.store_path()
    assert current == spack.util.path.canonicalize_path(expected)


def test_raising_exception_if_bootstrap_disabled(mutable_config):
    # Disable bootstrapping in config.yaml
    spack.config.set("bootstrap:enable", False)

    # Check the correct exception is raised
    with pytest.raises(RuntimeError, match="bootstrapping is currently disabled"):
        spack.bootstrap.config.store_path()


def test_raising_exception_module_importable():
    with pytest.raises(ImportError, match='cannot bootstrap the "asdf" Python module'):
        spack.bootstrap.core.ensure_module_importable_or_raise("asdf")


def test_raising_exception_executables_in_path():
    with pytest.raises(RuntimeError, match="cannot bootstrap any of the asdf, fdsa executables"):
        spack.bootstrap.core.ensure_executables_in_path_or_raise(["asdf", "fdsa"], "python")


@pytest.mark.regression("25603")
def test_bootstrap_deactivates_environments(active_mock_environment):
    assert spack.environment.active_environment() == active_mock_environment
    with spack.bootstrap.ensure_bootstrap_configuration():
        assert spack.environment.active_environment() is None
    assert spack.environment.active_environment() == active_mock_environment


@pytest.mark.regression("25805")
def test_bootstrap_disables_modulefile_generation(mutable_config):
    # Be sure to enable both lmod and tcl in modules.yaml
    spack.config.set("modules:default:enable", ["tcl", "lmod"])

    assert "tcl" in spack.config.get("modules:default:enable")
    assert "lmod" in spack.config.get("modules:default:enable")
    with spack.bootstrap.ensure_bootstrap_configuration():
        assert "tcl" not in spack.config.get("modules:default:enable")
        assert "lmod" not in spack.config.get("modules:default:enable")
    assert "tcl" in spack.config.get("modules:default:enable")
    assert "lmod" in spack.config.get("modules:default:enable")


@pytest.mark.regression("25992")
@pytest.mark.requires_executables("gcc")
def test_bootstrap_search_for_compilers_with_no_environment(no_compilers_yaml):
    assert not spack.compilers.all_compiler_specs(init_config=False)
    with spack.bootstrap.ensure_bootstrap_configuration():
        assert spack.compilers.all_compiler_specs(init_config=False)
    assert not spack.compilers.all_compiler_specs(init_config=False)


@pytest.mark.regression("25992")
@pytest.mark.requires_executables("gcc")
def test_bootstrap_search_for_compilers_with_environment_active(
    no_compilers_yaml, active_mock_environment
):
    assert not spack.compilers.all_compiler_specs(init_config=False)
    with spack.bootstrap.ensure_bootstrap_configuration():
        assert spack.compilers.all_compiler_specs(init_config=False)
    assert not spack.compilers.all_compiler_specs(init_config=False)


@pytest.mark.regression("26189")
def test_config_yaml_is_preserved_during_bootstrap(mutable_config):
    expected_dir = "/tmp/test"
    spack.config.set("config:test_stage", expected_dir, scope="command_line")

    assert spack.config.get("config:test_stage") == expected_dir
    with spack.bootstrap.ensure_bootstrap_configuration():
        assert spack.config.get("config:test_stage") == expected_dir
    assert spack.config.get("config:test_stage") == expected_dir


@pytest.mark.regression("26548")
def test_bootstrap_custom_store_in_environment(mutable_config, tmpdir):
    # Test that the custom store in an environment is taken into account
    # during bootstrapping
    spack_yaml = tmpdir.join("spack.yaml")
    install_root = tmpdir.join("store")
    spack_yaml.write(
        """
spack:
  specs:
  - libelf
  config:
    install_tree:
      root: {0}
""".format(
            install_root
        )
    )
    with spack.environment.Environment(str(tmpdir)):
        assert spack.environment.active_environment()
        assert spack.config.get("config:install_tree:root") == install_root
        # Don't trigger evaluation here
        with spack.bootstrap.ensure_bootstrap_configuration():
            pass
        assert str(spack.store.STORE.root) == install_root


def test_nested_use_of_context_manager(mutable_config):
    """Test nested use of the context manager"""
    user_config = spack.config.CONFIG
    with spack.bootstrap.ensure_bootstrap_configuration():
        assert spack.config.CONFIG != user_config
        with spack.bootstrap.ensure_bootstrap_configuration():
            assert spack.config.CONFIG != user_config
    assert spack.config.CONFIG == user_config


@pytest.mark.parametrize("expected_missing", [False, True])
def test_status_function_find_files(
    mutable_config, mock_executable, tmpdir, monkeypatch, expected_missing
):
    import spack.bootstrap.status

    if not expected_missing:
        mock_executable("foo", "echo Hello WWorld!")

    monkeypatch.setattr(
        spack.bootstrap.status,
        "_optional_requirements",
        lambda: [spack.bootstrap.status._required_system_executable("foo", "NOT FOUND")],
    )
    monkeypatch.setenv("PATH", str(tmpdir.join("bin")))

    _, missing = spack.bootstrap.status_message("optional")
    assert missing is expected_missing


@pytest.mark.regression("31042")
def test_source_is_disabled(mutable_config):
    # Get the configuration dictionary of the current bootstrapping source
    conf = next(iter(spack.bootstrap.core.bootstrapping_sources()))

    # The source is not explicitly enabled or disabled, so the following
    # call should raise to skip using it for bootstrapping
    with pytest.raises(ValueError):
        spack.bootstrap.core.source_is_enabled_or_raise(conf)

    # Try to explicitly disable the source and verify that the behavior
    # is the same as above
    spack.config.add("bootstrap:trusted:{0}:{1}".format(conf["name"], False))
    with pytest.raises(ValueError):
        spack.bootstrap.core.source_is_enabled_or_raise(conf)


@pytest.mark.regression("45247")
def test_use_store_does_not_try_writing_outside_root(tmp_path, monkeypatch, mutable_config):
    """Tests that when we use the 'use_store' context manager, there is no attempt at creating
    a Store outside the given root.
    """
    initial_store = mutable_config.get("config:install_tree:root")
    user_store = tmp_path / "store"

    fn = spack.store.Store.__init__

    def _checked_init(self, root, *args, **kwargs):
        fn(self, root, *args, **kwargs)
        assert self.root == str(user_store)

    monkeypatch.setattr(spack.store.Store, "__init__", _checked_init)

    spack.store.reinitialize()
    with spack.store.use_store(user_store):
        assert spack.config.CONFIG.get("config:install_tree:root") == str(user_store)
    assert spack.config.CONFIG.get("config:install_tree:root") == initial_store
