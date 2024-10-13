# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Test environment internals without CLI"""
import filecmp
import os
import pickle

import pytest

import llnl.util.filesystem as fs

import spack.config
import spack.environment as ev
import spack.solver.asp
import spack.spec
from spack.environment.environment import (
    EnvironmentManifestFile,
    SpackEnvironmentViewError,
    _error_on_nonempty_view_dir,
)
from spack.spec_list import UndefinedReferenceError

pytestmark = pytest.mark.not_on_windows("Envs are not supported on windows")


class TestDirectoryInitialization:
    def test_environment_dir_from_name(self, mutable_mock_env_path):
        """Test the function mapping a managed environment name to its folder."""
        env = ev.create("test")
        environment_dir = ev.environment_dir_from_name("test")
        assert env.path == environment_dir
        with pytest.raises(ev.SpackEnvironmentError, match="environment already exists"):
            ev.environment_dir_from_name("test", exists_ok=False)


def test_hash_change_no_rehash_concrete(tmp_path, mock_packages, config):
    # create an environment
    env_path = tmp_path / "env_dir"
    env_path.mkdir(exist_ok=False)
    env = ev.create_in_dir(env_path)
    env.write()

    # add a spec with a rewritten build hash
    spec = spack.spec.Spec("mpileaks")
    env.add(spec)
    env.concretize()

    # rewrite the hash
    old_hash = env.concretized_order[0]
    new_hash = "abc"
    env.specs_by_hash[old_hash]._hash = new_hash
    env.concretized_order[0] = new_hash
    env.specs_by_hash[new_hash] = env.specs_by_hash[old_hash]
    del env.specs_by_hash[old_hash]
    env.write()

    # Read environment
    read_in = ev.Environment(env_path)

    # Ensure read hashes are used (rewritten hash seen on read)
    assert read_in.concretized_order
    assert read_in.concretized_order[0] in read_in.specs_by_hash
    assert read_in.specs_by_hash[read_in.concretized_order[0]]._hash == new_hash


def test_env_change_spec(tmp_path, mock_packages, config):
    env_path = tmp_path / "env_dir"
    env_path.mkdir(exist_ok=False)
    env = ev.create_in_dir(env_path)
    env.write()

    spec = spack.spec.Spec("mpileaks@2.1~shared+debug")
    env.add(spec)
    env.write()

    change_spec = spack.spec.Spec("mpileaks@2.2")
    env.change_existing_spec(change_spec)
    (spec,) = env.added_specs()
    assert spec == spack.spec.Spec("mpileaks@2.2~shared+debug")

    change_spec = spack.spec.Spec("mpileaks~debug")
    env.change_existing_spec(change_spec)
    (spec,) = env.added_specs()
    assert spec == spack.spec.Spec("mpileaks@2.2~shared~debug")


_test_matrix_yaml = """\
spack:
  definitions:
  - compilers: ["%gcc", "%clang"]
  - desired_specs: ["mpileaks@2.1"]
  specs:
  - matrix:
    - [$compilers]
    - [$desired_specs]
"""


def test_env_change_spec_in_definition(tmp_path, mock_packages, mutable_mock_env_path):
    manifest_file = tmp_path / ev.manifest_name
    manifest_file.write_text(_test_matrix_yaml)
    e = ev.create("test", manifest_file)
    e.concretize()
    e.write()

    assert any(x.intersects("mpileaks@2.1%gcc") for x in e.user_specs)

    e.change_existing_spec(spack.spec.Spec("mpileaks@2.2"), list_name="desired_specs")
    e.write()

    # Ensure changed specs are in memory
    assert any(x.intersects("mpileaks@2.2%gcc") for x in e.user_specs)
    assert not any(x.intersects("mpileaks@2.1%gcc") for x in e.user_specs)

    # Now make sure the changes can be read from the modified config
    e = ev.read("test")
    assert any(x.intersects("mpileaks@2.2%gcc") for x in e.user_specs)
    assert not any(x.intersects("mpileaks@2.1%gcc") for x in e.user_specs)


def test_env_change_spec_in_matrix_raises_error(tmp_path, mock_packages, mutable_mock_env_path):
    manifest_file = tmp_path / ev.manifest_name
    manifest_file.write_text(_test_matrix_yaml)
    e = ev.create("test", manifest_file)
    e.concretize()
    e.write()

    with pytest.raises(spack.environment.SpackEnvironmentError) as error:
        e.change_existing_spec(spack.spec.Spec("mpileaks@2.2"))
    assert "Cannot directly change specs in matrices" in str(error)


def test_activate_should_require_an_env():
    with pytest.raises(TypeError):
        ev.activate(env="name")

    with pytest.raises(TypeError):
        ev.activate(env=None)


def test_user_view_path_is_not_canonicalized_in_yaml(tmpdir, config):
    # When spack.yaml files are checked into version control, we
    # don't want view: ./relative to get canonicalized on disk.

    # We create a view in <tmpdir>/env_dir
    env_path = tmpdir.mkdir("env_dir").strpath

    # And use a relative path to specify the view dir
    view = os.path.join(".", "view")

    # Which should always resolve to the following independent of cwd.
    absolute_view = os.path.join(env_path, "view")

    # Serialize environment with relative view path
    with fs.working_dir(str(tmpdir)):
        fst = ev.create_in_dir(env_path, with_view=view)
        fst.regenerate_views()

    # The view link should be created
    assert os.path.isdir(absolute_view)

    # Deserialize and check if the view path is still relative in yaml
    # and also check that the getter is pointing to the right dir.
    with fs.working_dir(str(tmpdir)):
        snd = ev.Environment(env_path)
        assert snd.manifest["spack"]["view"] == view
        assert os.path.samefile(snd.default_view.root, absolute_view)


def test_environment_cant_modify_environments_root(tmpdir):
    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(
            """\
 spack:
   config:
     environments_root: /a/black/hole
   view: false
   specs: []
 """
        )
    with tmpdir.as_cwd():
        with pytest.raises(ev.SpackEnvironmentError):
            e = ev.Environment(tmpdir.strpath)
            ev.activate(e)


@pytest.mark.regression("35420")
@pytest.mark.parametrize(
    "original_content",
    [
        (
            """\
spack:
  specs:
  - matrix:
    # test
    - - a
  concretizer:
    unify: false"""
        )
    ],
)
def test_roundtrip_spack_yaml_with_comments(original_content, mock_packages, config, tmp_path):
    """Ensure that round-tripping a spack.yaml file doesn't change its content."""
    spack_yaml = tmp_path / "spack.yaml"
    spack_yaml.write_text(original_content)

    e = ev.Environment(tmp_path)
    e.manifest.flush()

    content = spack_yaml.read_text()
    assert content == original_content


def test_adding_anonymous_specs_to_env_fails(tmp_path):
    """Tests that trying to add an anonymous spec to the 'specs' section of an environment
    raises an exception
    """
    env = ev.create_in_dir(tmp_path)
    with pytest.raises(ev.SpackEnvironmentError, match="cannot add anonymous"):
        env.add("%gcc")


def test_removing_from_non_existing_list_fails(tmp_path):
    """Tests that trying to remove a spec from a non-existing definition fails."""
    env = ev.create_in_dir(tmp_path)
    with pytest.raises(ev.SpackEnvironmentError, match="'bar' does not exist"):
        env.remove("%gcc", list_name="bar")


@pytest.mark.parametrize(
    "init_view,update_value",
    [
        (True, False),
        (True, "./view"),
        (False, True),
        ("./view", True),
        ("./view", False),
        (True, True),
        (False, False),
    ],
)
def test_update_default_view(init_view, update_value, tmp_path, mock_packages, config):
    """Tests updating the default view with different values."""
    env = ev.create_in_dir(tmp_path, with_view=init_view)
    env.update_default_view(update_value)
    env.write(regenerate=True)
    if not isinstance(update_value, bool):
        assert env.default_view.raw_root == update_value

    expected_value = update_value
    if isinstance(init_view, str) and update_value is True:
        expected_value = init_view

    assert env.manifest.yaml_content["spack"]["view"] == expected_value


@pytest.mark.parametrize(
    "initial_content,update_value,expected_view",
    [
        (
            """
spack:
  specs:
  - mpileaks
  view:
    default:
      root: ./view-gcc
      select: ['%gcc']
      link_type: symlink
""",
            "./another-view",
            {"root": "./another-view", "select": ["%gcc"], "link_type": "symlink"},
        ),
        (
            """
spack:
  specs:
  - mpileaks
  view:
    default:
      root: ./view-gcc
      select: ['%gcc']
      link_type: symlink
""",
            True,
            {"root": "./view-gcc", "select": ["%gcc"], "link_type": "symlink"},
        ),
    ],
)
def test_update_default_complex_view(
    initial_content, update_value, expected_view, tmp_path, mock_packages, config
):
    spack_yaml = tmp_path / "spack.yaml"
    spack_yaml.write_text(initial_content)

    env = ev.Environment(tmp_path)
    env.update_default_view(update_value)
    env.write(regenerate=True)

    assert env.default_view.to_dict() == expected_view


@pytest.mark.parametrize("filename", [ev.manifest_name, ev.lockfile_name])
def test_cannot_initialize_in_dir_with_init_file(tmp_path, filename):
    """Tests that initializing an environment in a directory with an already existing
    spack.yaml or spack.lock raises an exception.
    """
    init_file = tmp_path / filename
    init_file.touch()
    with pytest.raises(ev.SpackEnvironmentError, match="cannot initialize"):
        ev.create_in_dir(tmp_path)


def test_cannot_initiliaze_if_dirname_exists_as_a_file(tmp_path):
    """Tests that initializing an environment using as a location an existing file raises
    an error.
    """
    dir_name = tmp_path / "dir"
    dir_name.touch()
    with pytest.raises(ev.SpackEnvironmentError, match="cannot initialize"):
        ev.create_in_dir(dir_name)


def test_cannot_initialize_if_init_file_does_not_exist(tmp_path):
    """Tests that initializing an environment passing a non-existing init file raises an error."""
    init_file = tmp_path / ev.manifest_name
    with pytest.raises(ev.SpackEnvironmentError, match="cannot initialize"):
        ev.create_in_dir(tmp_path, init_file=init_file)


def test_environment_pickle(tmp_path):
    env1 = ev.create_in_dir(tmp_path)
    obj = pickle.dumps(env1)
    env2 = pickle.loads(obj)
    assert isinstance(env2, ev.Environment)


def test_error_on_nonempty_view_dir(tmpdir):
    """Error when the target is not an empty dir"""
    with tmpdir.as_cwd():
        os.mkdir("empty_dir")
        os.mkdir("nonempty_dir")
        with open(os.path.join("nonempty_dir", "file"), "wb"):
            pass
        os.symlink("empty_dir", "symlinked_empty_dir")
        os.symlink("does_not_exist", "broken_link")
        os.symlink("broken_link", "file")

        # This is OK.
        _error_on_nonempty_view_dir("empty_dir")

        # This is not OK.
        with pytest.raises(SpackEnvironmentViewError):
            _error_on_nonempty_view_dir("nonempty_dir")

        with pytest.raises(SpackEnvironmentViewError):
            _error_on_nonempty_view_dir("symlinked_empty_dir")

        with pytest.raises(SpackEnvironmentViewError):
            _error_on_nonempty_view_dir("broken_link")

        with pytest.raises(SpackEnvironmentViewError):
            _error_on_nonempty_view_dir("file")


def test_can_add_specs_to_environment_without_specs_attribute(tmp_path, mock_packages, config):
    """Sometimes users have template manifest files, and save one line in the YAML file by
    removing the empty 'specs: []' attribute. This test ensures that adding a spec to an
    environment without the 'specs' attribute, creates the attribute first instead of returning
    an error.
    """
    spack_yaml = tmp_path / "spack.yaml"
    spack_yaml.write_text(
        """
spack:
  view: true
  concretizer:
    unify: true
    """
    )
    env = ev.Environment(tmp_path)
    env.add("pkg-a")

    assert len(env.user_specs) == 1
    assert env.manifest.yaml_content["spack"]["specs"] == ["pkg-a"]


@pytest.mark.parametrize(
    "original_yaml,new_spec,expected_yaml",
    [
        (
            """spack:
  specs:
  # baz
  - zlib
""",
            "libpng",
            """spack:
  specs:
  # baz
  - zlib
  - libpng
""",
        )
    ],
)
def test_preserving_comments_when_adding_specs(
    original_yaml, new_spec, expected_yaml, config, tmp_path
):
    """Ensure that round-tripping a spack.yaml file doesn't change its content."""
    spack_yaml = tmp_path / "spack.yaml"
    spack_yaml.write_text(original_yaml)

    e = ev.Environment(str(tmp_path))
    e.add(new_spec)
    e.write()

    content = spack_yaml.read_text()
    assert content == expected_yaml


@pytest.mark.parametrize("filename", [ev.lockfile_name, "as9582g54.lock", "m3ia54s.json"])
@pytest.mark.regression("37410")
def test_initialize_from_lockfile(tmp_path, filename):
    """Some users have workflows where they store multiple lockfiles in the
    same directory, and pick one of them to create an environment depending
    on external parameters e.g. while running CI jobs. This test ensures that
    Spack can create environments from lockfiles that are not necessarily named
    'spack.lock' and can thus coexist in the same directory.
    """

    init_file = tmp_path / filename
    env_dir = tmp_path / "env_dir"
    init_file.write_text('{ "roots": [] }\n')
    ev.initialize_environment_dir(env_dir, init_file)

    assert os.path.exists(env_dir / ev.lockfile_name)
    assert filecmp.cmp(env_dir / ev.lockfile_name, init_file, shallow=False)


def test_cannot_initialize_from_bad_lockfile(tmp_path):
    """Test that we fail on an incorrectly constructed lockfile"""

    init_file = tmp_path / ev.lockfile_name
    env_dir = tmp_path / "env_dir"

    init_file.write_text("Not a legal JSON file\n")

    with pytest.raises(ev.SpackEnvironmentError, match="from lockfile"):
        ev.initialize_environment_dir(env_dir, init_file)


@pytest.mark.parametrize("filename", ["random.txt", "random.yaml", ev.manifest_name])
@pytest.mark.regression("37410")
def test_initialize_from_random_file_as_manifest(tmp_path, filename):
    """Some users have workflows where they store multiple lockfiles in the
    same directory, and pick one of them to create an environment depending
    on external parameters e.g. while running CI jobs. This test ensures that
    Spack can create environments from manifest that are not necessarily named
    'spack.yaml' and can thus coexist in the same directory.
    """

    init_file = tmp_path / filename
    env_dir = tmp_path / "env_dir"

    init_file.write_text(
        """\
spack:
  view: true
  concretizer:
    unify: true
  specs: []
"""
    )

    ev.create_in_dir(env_dir, init_file)

    assert not os.path.exists(env_dir / ev.lockfile_name)
    assert os.path.exists(env_dir / ev.manifest_name)
    assert filecmp.cmp(env_dir / ev.manifest_name, init_file, shallow=False)


def test_error_message_when_using_too_new_lockfile(tmp_path):
    """Sometimes the lockfile format needs to be bumped. When that happens, we have forward
    incompatibilities that need to be reported in a clear way to the user, in case we moved
    back to an older version of Spack. This test ensures that the error message for a too
    new lockfile version stays comprehensible across refactoring of the environment code.
    """
    init_file = tmp_path / ev.lockfile_name
    env_dir = tmp_path / "env_dir"
    init_file.write_text(
        """
{
    "_meta": {
        "file-type": "spack-lockfile",
        "lockfile-version": 100,
        "specfile-version": 3
    },
    "roots": [],
    "concrete_specs": {}
}\n
"""
    )
    ev.initialize_environment_dir(env_dir, init_file)
    with pytest.raises(ev.SpackEnvironmentError, match="You need to use a newer Spack version."):
        ev.Environment(env_dir)


@pytest.mark.regression("38240")
@pytest.mark.parametrize(
    "unify_in_lower_scope,unify_in_spack_yaml",
    [
        (True, False),
        (True, "when_possible"),
        (False, True),
        (False, "when_possible"),
        ("when_possible", False),
        ("when_possible", True),
    ],
)
def test_environment_concretizer_scheme_used(tmp_path, unify_in_lower_scope, unify_in_spack_yaml):
    """Tests that "unify" settings in spack.yaml always take precedence over settings in lower
    configuration scopes.
    """
    manifest = tmp_path / "spack.yaml"
    manifest.write_text(
        f"""\
spack:
  specs:
  - mpileaks
  concretizer:
    unify: {str(unify_in_spack_yaml).lower()}
"""
    )

    with spack.config.override("concretizer:unify", unify_in_lower_scope):
        with ev.Environment(manifest.parent) as e:
            assert e.unify == unify_in_spack_yaml


@pytest.mark.parametrize("unify_in_config", [True, False, "when_possible"])
def test_environment_config_scheme_used(tmp_path, unify_in_config):
    """Tests that "unify" settings in lower configuration scopes is taken into account,
    if absent in spack.yaml.
    """
    manifest = tmp_path / "spack.yaml"
    manifest.write_text(
        """\
spack:
  specs:
  - mpileaks
"""
    )

    with spack.config.override("concretizer:unify", unify_in_config):
        with ev.Environment(manifest.parent) as e:
            assert e.unify == unify_in_config


@pytest.mark.parametrize(
    "spec_str,expected_raise,expected_spec",
    [
        # vendorsb vendors "b" only when @=1.1
        ("vendorsb", False, "vendorsb@=1.0"),
        ("vendorsb@=1.1", True, None),
    ],
)
def test_conflicts_with_packages_that_are_not_dependencies(
    spec_str, expected_raise, expected_spec, tmp_path, mock_packages, config
):
    """Tests that we cannot concretize two specs together, if one conflicts with the other,
    even though they don't have a dependency relation.
    """
    manifest = tmp_path / "spack.yaml"
    manifest.write_text(
        f"""\
spack:
  specs:
  - {spec_str}
  - pkg-b
  concretizer:
    unify: true
"""
    )
    with ev.Environment(manifest.parent) as e:
        if expected_raise:
            with pytest.raises(spack.solver.asp.UnsatisfiableSpecError):
                e.concretize()
        else:
            e.concretize()
            assert any(s.satisfies(expected_spec) for s in e.concrete_roots())


@pytest.mark.regression("39455")
@pytest.mark.parametrize(
    "possible_mpi_spec,unify", [("mpich", False), ("mpich", True), ("zmpi", False), ("zmpi", True)]
)
def test_requires_on_virtual_and_potential_providers(
    possible_mpi_spec, unify, tmp_path, mock_packages, config
):
    """Tests that in an environment we can add packages explicitly, even though they provide
    a virtual package, and we require the provider of the same virtual to be another package,
    if they are added explicitly by their name.
    """
    manifest = tmp_path / "spack.yaml"
    manifest.write_text(
        f"""\
    spack:
      specs:
      - {possible_mpi_spec}
      - mpich2
      - mpileaks
      packages:
        mpi:
          require: mpich2
      concretizer:
        unify: {unify}
    """
    )
    with ev.Environment(manifest.parent) as e:
        e.concretize()
        assert e.matching_spec(possible_mpi_spec)
        assert e.matching_spec("mpich2")

        mpileaks = e.matching_spec("mpileaks")
        assert mpileaks.satisfies("^mpich2")
        assert mpileaks["mpi"].satisfies("mpich2")
        assert not mpileaks.satisfies(f"^{possible_mpi_spec}")


@pytest.mark.regression("39387")
@pytest.mark.parametrize(
    "spec_str", ["mpileaks +opt", "mpileaks  +opt   ~shared", "mpileaks  ~shared   +opt"]
)
def test_manifest_file_removal_works_if_spec_is_not_normalized(tmp_path, spec_str):
    """Tests that we can remove a spec from a manifest file even if its string
    representation is not normalized.
    """
    manifest = tmp_path / "spack.yaml"
    manifest.write_text(
        f"""\
spack:
  specs:
  - {spec_str}
"""
    )
    s = spack.spec.Spec(spec_str)
    spack_yaml = EnvironmentManifestFile(tmp_path)
    # Doing a round trip str -> Spec -> str normalizes the representation
    spack_yaml.remove_user_spec(str(s))
    spack_yaml.flush()

    assert spec_str not in manifest.read_text()


@pytest.mark.regression("39387")
@pytest.mark.parametrize(
    "duplicate_specs,expected_number",
    [
        # Swap variants, versions, etc. add spaces
        (["foo +bar ~baz", "foo ~baz    +bar"], 3),
        (["foo @1.0 ~baz %gcc", "foo ~baz @1.0%gcc"], 3),
        # Item 1 and 3 are exactly the same
        (["zlib +shared", "zlib      +shared", "zlib +shared"], 4),
    ],
)
def test_removing_spec_from_manifest_with_exact_duplicates(
    duplicate_specs, expected_number, tmp_path
):
    """Tests that we can remove exact duplicates from a manifest file.

    Note that we can't get in a state with duplicates using only CLI, but this might happen
    on user edited spack.yaml files.
    """
    manifest = tmp_path / "spack.yaml"
    manifest.write_text(
        f"""\
    spack:
      specs: [{", ".join(duplicate_specs)} , "zlib"]
    """
    )

    with ev.Environment(tmp_path) as env:
        assert len(env.user_specs) == expected_number
        env.remove(duplicate_specs[0])
        env.write()

    assert "+shared" not in manifest.read_text()
    assert "zlib" in manifest.read_text()
    with ev.Environment(tmp_path) as env:
        assert len(env.user_specs) == 1


@pytest.mark.regression("35298")
def test_variant_propagation_with_unify_false(tmp_path, mock_packages, config):
    """Spack distributes concretizations to different processes, when unify:false is selected and
    the number of roots is 2 or more. When that happens, the specs to be concretized need to be
    properly reconstructed on the worker process, if variant propagation was requested.
    """
    manifest = tmp_path / "spack.yaml"
    manifest.write_text(
        """
    spack:
      specs:
      - parent-foo ++foo
      - pkg-c
      concretizer:
        unify: false
    """
    )
    with ev.Environment(tmp_path) as env:
        env.concretize()

    root = env.matching_spec("parent-foo")
    for node in root.traverse():
        assert node.satisfies("+foo")


def test_env_with_include_defs(mutable_mock_env_path, mock_packages):
    """Test environment with included definitions file."""
    env_path = mutable_mock_env_path
    env_path.mkdir()
    defs_file = env_path / "definitions.yaml"
    defs_file.write_text(
        """definitions:
- core_specs: [libdwarf, libelf]
- compilers: ['%gcc']
"""
    )

    spack_yaml = env_path / ev.manifest_name
    spack_yaml.write_text(
        f"""spack:
  include:
  - file://{defs_file}

  definitions:
  - my_packages: [zlib]

  specs:
  - matrix:
    - [$core_specs]
    - [$compilers]
  - $my_packages
"""
    )

    e = ev.Environment(env_path)
    with e:
        e.concretize()


def test_env_with_include_def_missing(mutable_mock_env_path, mock_packages):
    """Test environment with included definitions file that is missing a definition."""
    env_path = mutable_mock_env_path
    env_path.mkdir()
    filename = "missing-def.yaml"
    defs_file = env_path / filename
    defs_file.write_text("definitions:\n- my_compilers: ['%gcc']\n")

    spack_yaml = env_path / ev.manifest_name
    spack_yaml.write_text(
        f"""spack:
  include:
  - file://{defs_file}

  specs:
  - matrix:
    - [$core_specs]
    - [$my_compilers]
"""
    )

    e = ev.Environment(env_path)
    with e:
        with pytest.raises(UndefinedReferenceError, match=r"which does not appear"):
            e.concretize()


@pytest.mark.regression("41292")
def test_deconcretize_then_concretize_does_not_error(mutable_mock_env_path, mock_packages):
    """Tests that, after having deconcretized a spec, we can reconcretize an environment which
    has 2 or more user specs mapping to the same concrete spec.
    """
    mutable_mock_env_path.mkdir()
    spack_yaml = mutable_mock_env_path / ev.manifest_name
    spack_yaml.write_text(
        """spack:
      specs:
      # These two specs concretize to the same hash
      - pkg-c
      - pkg-c@1.0
      # Spec used to trigger the bug
      - pkg-a
      concretizer:
        unify: true
    """
    )
    e = ev.Environment(mutable_mock_env_path)
    with e:
        e.concretize()
        e.deconcretize(spack.spec.Spec("pkg-a"), concrete=False)
        e.concretize()
    assert len(e.concrete_roots()) == 3
    all_root_hashes = {x.dag_hash() for x in e.concrete_roots()}
    assert len(all_root_hashes) == 2


@pytest.mark.regression("44216")
def test_root_version_weights_for_old_versions(mutable_mock_env_path, mock_packages):
    """Tests that, when we select two old versions of root specs that have the same version
    optimization penalty, both are considered.
    """
    mutable_mock_env_path.mkdir()
    spack_yaml = mutable_mock_env_path / ev.manifest_name
    spack_yaml.write_text(
        """spack:
      specs:
      # allow any version, but the most recent
      - bowtie@:1.3
      # allows only the third most recent, so penalty is 2
      - gcc@1
      concretizer:
        unify: true
    """
    )
    e = ev.Environment(mutable_mock_env_path)
    with e:
        e.concretize()

    bowtie = [x for x in e.concrete_roots() if x.name == "bowtie"][0]
    gcc = [x for x in e.concrete_roots() if x.name == "gcc"][0]

    assert bowtie.satisfies("@=1.3.0")
    assert gcc.satisfies("@=1.0")


def test_env_view_on_empty_dir_is_fine(tmp_path, config, mock_packages, temporary_store):
    """Tests that creating a view pointing to an empty dir is not an error."""
    view_dir = tmp_path / "view"
    view_dir.mkdir()
    env = ev.create_in_dir(tmp_path, with_view="view")
    env.add("mpileaks")
    env.concretize()
    env.install_all(fake=True)
    env.regenerate_views()
    assert view_dir.is_symlink()


def test_env_view_on_non_empty_dir_errors(tmp_path, config, mock_packages, temporary_store):
    """Tests that creating a view pointing to a non-empty dir errors."""
    view_dir = tmp_path / "view"
    view_dir.mkdir()
    (view_dir / "file").write_text("")
    env = ev.create_in_dir(tmp_path, with_view="view")
    env.add("mpileaks")
    env.concretize()
    env.install_all(fake=True)
    with pytest.raises(ev.SpackEnvironmentError, match="because it is a non-empty dir"):
        env.regenerate_views()


@pytest.mark.parametrize(
    "matrix_line", [("^zmpi", "^mpich"), ("~shared", "+shared"), ("shared=False", "+shared-libs")]
)
@pytest.mark.regression("40791")
def test_stack_enforcement_is_strict(tmp_path, matrix_line, config, mock_packages):
    """Ensure that constraints in matrices are applied strictly after expansion, to avoid
    inconsistencies between abstract user specs and concrete specs.
    """
    manifest = tmp_path / "spack.yaml"
    manifest.write_text(
        f"""\
spack:
  definitions:
    - packages: [libelf, mpileaks]
    - install:
        - matrix:
            - [$packages]
            - [{", ".join(item for item in matrix_line)}]
  specs:
    - $install
  concretizer:
    unify: false
"""
    )
    # Here we raise different exceptions depending on whether we solve serially or not
    with pytest.raises(Exception):
        with ev.Environment(tmp_path) as e:
            e.concretize()
