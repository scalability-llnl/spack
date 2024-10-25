# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import pathlib

import pytest

import spack.config
import spack.error
import spack.package_base
import spack.repo
import spack.solver.asp
import spack.util.spack_yaml as syaml
import spack.version
from spack.installer import PackageInstaller
from spack.solver.asp import InternalConcretizerError, UnsatisfiableSpecError
from spack.spec import Spec
from spack.util.url import path_to_file_url


def update_packages_config(conf_str):
    conf = syaml.load_config(conf_str)
    spack.config.set("packages", conf["packages"], scope="concretize")


@pytest.fixture
def test_repo(mutable_config, monkeypatch, mock_stage):
    repo_dir = pathlib.Path(spack.paths.repos_path) / "requirements.test"
    with spack.repo.use_repositories(str(repo_dir)) as mock_repo_path:
        yield mock_repo_path


def test_one_package_multiple_reqs(concretize_scope, test_repo):
    conf_str = """\
packages:
  y:
    require:
    - "@2.4"
    - "~shared"
"""
    update_packages_config(conf_str)
    y_spec = Spec("y").concretized()
    assert y_spec.satisfies("@2.4~shared")


def test_requirement_isnt_optional(concretize_scope, test_repo):
    """If a user spec requests something that directly conflicts
    with a requirement, make sure we get an error.
    """
    conf_str = """\
packages:
  x:
    require: "@1.0"
"""
    update_packages_config(conf_str)
    with pytest.raises(UnsatisfiableSpecError):
        Spec("x@1.1").concretize()


def test_require_undefined_version(concretize_scope, test_repo):
    """If a requirement specifies a numbered version that isn't in
    the associated package.py and isn't part of a Git hash
    equivalence (hash=number), then Spack should raise an error
    (it is assumed this is a typo, and raising the error here
    avoids a likely error when Spack attempts to fetch the version).
    """
    conf_str = """\
packages:
  x:
    require: "@1.2"
"""
    update_packages_config(conf_str)
    with pytest.raises(spack.error.ConfigError):
        Spec("x").concretize()


def test_require_truncated(concretize_scope, test_repo):
    """A requirement specifies a version range, with satisfying
    versions defined in the package.py. Make sure we choose one
    of the defined versions (vs. allowing the requirement to
    define a new version).
    """
    conf_str = """\
packages:
  x:
    require: "@1"
"""
    update_packages_config(conf_str)
    xspec = Spec("x").concretized()
    assert xspec.satisfies("@1.1")


def test_git_user_supplied_reference_satisfaction(
    concretize_scope, test_repo, mock_git_version_info, monkeypatch
):
    repo_path, filename, commits = mock_git_version_info

    monkeypatch.setattr(
        spack.package_base.PackageBase, "git", path_to_file_url(repo_path), raising=False
    )

    hash_eq_ver = Spec(f"v@{commits[0]}=2.2")
    hash_eq_ver_copy = Spec(f"v@{commits[0]}=2.2")
    just_hash = Spec(f"v@{commits[0]}")
    just_ver = Spec("v@=2.2")
    hash_eq_other_ver = Spec(f"v@{commits[0]}=2.3")

    assert not hash_eq_ver == just_hash
    assert not hash_eq_ver.satisfies(just_hash)
    assert not hash_eq_ver.intersects(just_hash)

    # Git versions and literal versions are distinct versions, like
    # pkg@10.1.0 and pkg@10.1.0-suffix are distinct versions.
    assert not hash_eq_ver.satisfies(just_ver)
    assert not just_ver.satisfies(hash_eq_ver)
    assert not hash_eq_ver.intersects(just_ver)
    assert hash_eq_ver != just_ver
    assert just_ver != hash_eq_ver
    assert not hash_eq_ver == just_ver
    assert not just_ver == hash_eq_ver

    # When a different version is associated, they're not equal
    assert not hash_eq_ver.satisfies(hash_eq_other_ver)
    assert not hash_eq_other_ver.satisfies(hash_eq_ver)
    assert not hash_eq_ver.intersects(hash_eq_other_ver)
    assert not hash_eq_other_ver.intersects(hash_eq_ver)
    assert hash_eq_ver != hash_eq_other_ver
    assert hash_eq_other_ver != hash_eq_ver
    assert not hash_eq_ver == hash_eq_other_ver
    assert not hash_eq_other_ver == hash_eq_ver

    # These should be equal
    assert hash_eq_ver == hash_eq_ver_copy
    assert not hash_eq_ver != hash_eq_ver_copy
    assert hash_eq_ver.satisfies(hash_eq_ver_copy)
    assert hash_eq_ver_copy.satisfies(hash_eq_ver)
    assert hash_eq_ver.intersects(hash_eq_ver_copy)
    assert hash_eq_ver_copy.intersects(hash_eq_ver)


def test_requirement_adds_new_version(
    concretize_scope, test_repo, mock_git_version_info, monkeypatch
):
    repo_path, filename, commits = mock_git_version_info
    monkeypatch.setattr(
        spack.package_base.PackageBase, "git", path_to_file_url(repo_path), raising=False
    )

    a_commit_hash = commits[0]
    conf_str = """\
packages:
  v:
    require: "@{0}=2.2"
""".format(
        a_commit_hash
    )
    update_packages_config(conf_str)

    s1 = Spec("v").concretized()
    assert s1.satisfies("@2.2")
    # Make sure the git commit info is retained
    assert isinstance(s1.version, spack.version.GitVersion)
    assert s1.version.ref == a_commit_hash


def test_requirement_adds_version_satisfies(
    concretize_scope, test_repo, mock_git_version_info, monkeypatch
):
    """Make sure that new versions added by requirements are factored into
    conditions. In this case create a new version that satisfies a
    depends_on condition and make sure it is triggered (i.e. the
    dependency is added).
    """
    repo_path, filename, commits = mock_git_version_info
    monkeypatch.setattr(
        spack.package_base.PackageBase, "git", path_to_file_url(repo_path), raising=False
    )

    # Sanity check: early version of T does not include U
    s0 = Spec("t@2.0").concretized()
    assert not ("u" in s0)

    conf_str = """\
packages:
  t:
    require: "@{0}=2.2"
""".format(
        commits[0]
    )
    update_packages_config(conf_str)

    s1 = Spec("t").concretized()
    assert "u" in s1
    assert s1.satisfies("@2.2")


@pytest.mark.parametrize("require_checksum", (True, False))
def test_requirement_adds_git_hash_version(
    require_checksum, concretize_scope, test_repo, mock_git_version_info, monkeypatch, working_env
):
    # A full commit sha is a checksummed version, so this test should pass in both cases
    if require_checksum:
        os.environ["SPACK_CONCRETIZER_REQUIRE_CHECKSUM"] = "yes"

    repo_path, filename, commits = mock_git_version_info
    monkeypatch.setattr(
        spack.package_base.PackageBase, "git", path_to_file_url(repo_path), raising=False
    )

    a_commit_hash = commits[0]
    conf_str = f"""\
packages:
  v:
    require: "@{a_commit_hash}"
"""
    update_packages_config(conf_str)

    s1 = Spec("v").concretized()
    assert isinstance(s1.version, spack.version.GitVersion)
    assert s1.satisfies(f"v@{a_commit_hash}")


def test_requirement_adds_multiple_new_versions(
    concretize_scope, test_repo, mock_git_version_info, monkeypatch
):
    repo_path, filename, commits = mock_git_version_info
    monkeypatch.setattr(
        spack.package_base.PackageBase, "git", path_to_file_url(repo_path), raising=False
    )

    conf_str = f"""\
packages:
  v:
    require:
    - one_of: ["@{commits[0]}=2.2", "@{commits[1]}=2.3"]
"""
    update_packages_config(conf_str)

    assert Spec("v").concretized().satisfies(f"@{commits[0]}=2.2")
    assert Spec("v@2.3").concretized().satisfies(f"v@{commits[1]}=2.3")


# TODO: this belongs in the concretize_preferences test module but uses
# fixtures defined only here
def test_preference_adds_new_version(
    concretize_scope, test_repo, mock_git_version_info, monkeypatch
):
    """Normally a preference cannot define a new version, but that constraint
    is ignored if the version is a Git hash-based version.
    """
    repo_path, filename, commits = mock_git_version_info
    monkeypatch.setattr(
        spack.package_base.PackageBase, "git", path_to_file_url(repo_path), raising=False
    )

    conf_str = f"""\
packages:
  v:
    version: ["{commits[0]}=2.2", "{commits[1]}=2.3"]
"""
    update_packages_config(conf_str)

    assert Spec("v").concretized().satisfies(f"@{commits[0]}=2.2")
    assert Spec("v@2.3").concretized().satisfies(f"@{commits[1]}=2.3")

    # When installing by hash, a lookup is triggered, so it's not mapped to =2.3.
    s3 = Spec(f"v@{commits[1]}").concretized()
    assert s3.satisfies(f"v@{commits[1]}")
    assert not s3.satisfies("@2.3")


def test_external_adds_new_version_that_is_preferred(concretize_scope, test_repo):
    """Test that we can use a version, not declared in package recipe, as the
    preferred version if that version appears in an external spec.
    """
    conf_str = """\
packages:
  y:
    version: ["2.7"]
    externals:
    - spec: y@2.7 # Not defined in y
      prefix: /fake/nonexistent/path/
    buildable: false
"""
    update_packages_config(conf_str)

    spec = Spec("x").concretized()
    assert spec["y"].satisfies("@2.7")
    assert spack.version.Version("2.7") not in spec["y"].package.versions


def test_requirement_is_successfully_applied(concretize_scope, test_repo):
    """If a simple requirement can be satisfied, make sure the
    concretization succeeds and the requirement spec is applied.
    """
    s1 = Spec("x").concretized()
    # Without any requirements/preferences, the later version is preferred
    assert s1.satisfies("@1.1")

    conf_str = """\
packages:
  x:
    require: "@1.0"
"""
    update_packages_config(conf_str)
    s2 = Spec("x").concretized()
    # The requirement forces choosing the eariler version
    assert s2.satisfies("@1.0")


def test_multiple_packages_requirements_are_respected(concretize_scope, test_repo):
    """Apply requirements to two packages; make sure the concretization
    succeeds and both requirements are respected.
    """
    conf_str = """\
packages:
  x:
    require: "@1.0"
  y:
    require: "@2.4"
"""
    update_packages_config(conf_str)
    spec = Spec("x").concretized()
    assert spec["x"].satisfies("@1.0")
    assert spec["y"].satisfies("@2.4")


def test_oneof(concretize_scope, test_repo):
    """'one_of' allows forcing the concretizer to satisfy one of
    the specs in the group (but not all have to be satisfied).
    """
    conf_str = """\
packages:
  y:
    require:
    - one_of: ["@2.4", "~shared"]
"""
    update_packages_config(conf_str)
    spec = Spec("x").concretized()
    # The concretizer only has to satisfy one of @2.4/~shared, and @2.4
    # comes first so it is prioritized
    assert spec["y"].satisfies("@2.4+shared")


def test_one_package_multiple_oneof_groups(concretize_scope, test_repo):
    """One package has two 'one_of' groups; check that both are
    applied.
    """
    conf_str = """\
packages:
  y:
    require:
    - one_of: ["@2.4%gcc", "@2.5%clang"]
    - one_of: ["@2.5~shared", "@2.4+shared"]
"""
    update_packages_config(conf_str)

    s1 = Spec("y@2.5").concretized()
    assert s1.satisfies("%clang~shared")

    s2 = Spec("y@2.4").concretized()
    assert s2.satisfies("%gcc+shared")


@pytest.mark.regression("34241")
def test_require_cflags(concretize_scope, mock_packages):
    """Ensures that flags can be required from configuration."""
    conf_str = """\
packages:
  mpich2:
    require: cflags="-g"
  mpi:
    require: mpich cflags="-O1"
"""
    update_packages_config(conf_str)

    spec_mpich2 = Spec("mpich2").concretized()
    assert spec_mpich2.satisfies("cflags=-g")

    spec_mpi = Spec("mpi").concretized()
    assert spec_mpi.satisfies("mpich cflags=-O1")


def test_requirements_for_package_that_is_not_needed(concretize_scope, test_repo):
    """Specify requirements for specs that are not concretized or
    a dependency of a concretized spec (in other words, none of
    the requirements are used for the requested spec).
    """
    # Note that the exact contents aren't important since this isn't
    # intended to be used, but the important thing is that a number of
    # packages have requirements applied
    conf_str = """\
packages:
  x:
    require: "@1.0"
  y:
    require:
    - one_of: ["@2.4%gcc", "@2.5%clang"]
    - one_of: ["@2.5~shared", "@2.4+shared"]
"""
    update_packages_config(conf_str)

    s1 = Spec("v").concretized()
    assert s1.satisfies("@2.1")


def test_oneof_ordering(concretize_scope, test_repo):
    """Ensure that earlier elements of 'one_of' have higher priority.
    This priority should override default priority (e.g. choosing
    later versions).
    """
    conf_str = """\
packages:
  y:
    require:
    - one_of: ["@2.4", "@2.5"]
"""
    update_packages_config(conf_str)

    s1 = Spec("y").concretized()
    assert s1.satisfies("@2.4")

    s2 = Spec("y@2.5").concretized()
    assert s2.satisfies("@2.5")


def test_reuse_oneof(concretize_scope, test_repo, tmp_path, mock_fetch):
    conf_str = """\
packages:
  y:
    require:
    - one_of: ["@2.5", "~shared"]
"""

    store_dir = tmp_path / "store"
    with spack.store.use_store(str(store_dir)):
        s1 = Spec("y@2.5 ~shared").concretized()
        PackageInstaller([s1.package], fake=True, explicit=True).install()

        update_packages_config(conf_str)

        with spack.config.override("concretizer:reuse", True):
            s2 = Spec("y").concretized()
            assert not s2.satisfies("@2.5 ~shared")


@pytest.mark.parametrize(
    "allow_deprecated,expected,not_expected",
    [(True, ["@=2.3", "%gcc"], []), (False, ["%gcc"], ["@=2.3"])],
)
def test_requirements_and_deprecated_versions(
    allow_deprecated, expected, not_expected, concretize_scope, test_repo
):
    """Tests the expected behavior of requirements and deprecated versions.

    If deprecated versions are not allowed, concretization should just pick
    the other requirement.

    If deprecated versions are allowed, both requirements are honored.
    """
    # 2.3 is a deprecated versions. Ensure that any_of picks both constraints,
    # since they are possible
    conf_str = """\
packages:
  y:
    require:
    - any_of: ["@=2.3", "%gcc"]
"""
    update_packages_config(conf_str)

    with spack.config.override("config:deprecated", allow_deprecated):
        s1 = Spec("y").concretized()
        for constrain in expected:
            assert s1.satisfies(constrain)

        for constrain in not_expected:
            assert not s1.satisfies(constrain)


@pytest.mark.parametrize("spec_str,requirement_str", [("x", "%gcc"), ("x", "%clang")])
def test_default_requirements_with_all(spec_str, requirement_str, concretize_scope, test_repo):
    """Test that default requirements are applied to all packages."""
    conf_str = f"""\
packages:
  all:
    require: "{requirement_str}"
"""
    update_packages_config(conf_str)

    spec = Spec(spec_str).concretized()
    for s in spec.traverse():
        assert s.satisfies(requirement_str)


@pytest.mark.parametrize(
    "requirements,expectations",
    [
        (("%gcc", "%clang"), ("%gcc", "%clang")),
        (("%gcc ~shared", "@1.0"), ("%gcc ~shared", "@1.0 +shared")),
    ],
)
def test_default_and_package_specific_requirements(
    concretize_scope, requirements, expectations, test_repo
):
    """Test that specific package requirements override default package requirements."""
    generic_req, specific_req = requirements
    generic_exp, specific_exp = expectations
    conf_str = f"""\
packages:
  all:
    require: "{generic_req}"
  x:
    require: "{specific_req}"
"""
    update_packages_config(conf_str)

    spec = Spec("x").concretized()
    assert spec.satisfies(specific_exp)
    for s in spec.traverse(root=False):
        assert s.satisfies(generic_exp)


@pytest.mark.parametrize("mpi_requirement", ["mpich", "mpich2", "zmpi"])
def test_requirements_on_virtual(mpi_requirement, concretize_scope, mock_packages):
    conf_str = f"""\
packages:
  mpi:
    require: "{mpi_requirement}"
"""
    update_packages_config(conf_str)

    spec = Spec("callpath").concretized()
    assert "mpi" in spec
    assert mpi_requirement in spec


@pytest.mark.parametrize(
    "mpi_requirement,specific_requirement",
    [("mpich", "@3.0.3"), ("mpich2", "%clang"), ("zmpi", "%gcc")],
)
def test_requirements_on_virtual_and_on_package(
    mpi_requirement, specific_requirement, concretize_scope, mock_packages
):
    conf_str = f"""\
packages:
  mpi:
    require: "{mpi_requirement}"
  {mpi_requirement}:
    require: "{specific_requirement}"
"""
    update_packages_config(conf_str)

    spec = Spec("callpath").concretized()
    assert "mpi" in spec
    assert mpi_requirement in spec
    assert spec["mpi"].satisfies(specific_requirement)


def test_incompatible_virtual_requirements_raise(concretize_scope, mock_packages):
    conf_str = """\
    packages:
      mpi:
        require: "mpich"
    """
    update_packages_config(conf_str)

    spec = Spec("callpath ^zmpi")
    # TODO (multiple nodes): recover a better error message later
    with pytest.raises((UnsatisfiableSpecError, InternalConcretizerError)):
        spec.concretize()


def test_non_existing_variants_under_all(concretize_scope, mock_packages):
    conf_str = """\
    packages:
      all:
        require:
        - any_of: ["~foo", "@:"]
    """
    update_packages_config(conf_str)

    spec = Spec("callpath ^zmpi").concretized()
    assert "~foo" not in spec


@pytest.mark.parametrize(
    "packages_yaml,spec_str,expected_satisfies",
    [
        # In the tests below we set the compiler preference to "gcc" to be explicit on the
        # fact that "clang" is not the preferred compiler. That helps making more robust the
        # tests that verify enforcing "%clang" as a requirement.
        (
            """\
    packages:
      all:
        compiler: ["gcc", "clang"]

      libelf:
        require:
        - one_of: ["%clang"]
          when: "@0.8.13"
""",
            "libelf",
            [("@0.8.13%clang", True), ("%gcc", False)],
        ),
        (
            """\
    packages:
      all:
        compiler: ["gcc", "clang"]

      libelf:
        require:
        - one_of: ["%clang"]
          when: "@0.8.13"
""",
            "libelf@0.8.12",
            [("%clang", False), ("%gcc", True)],
        ),
        (
            """\
    packages:
      all:
        compiler: ["gcc", "clang"]

      libelf:
        require:
        - spec: "%clang"
          when: "@0.8.13"
""",
            "libelf@0.8.12",
            [("%clang", False), ("%gcc", True)],
        ),
        (
            """\
    packages:
      all:
        compiler: ["gcc", "clang"]

      libelf:
        require:
        - spec: "@0.8.13"
          when: "%clang"
""",
            "libelf@0.8.13%gcc",
            [("%clang", False), ("%gcc", True), ("@0.8.13", True)],
        ),
    ],
)
def test_conditional_requirements_from_packages_yaml(
    packages_yaml, spec_str, expected_satisfies, concretize_scope, mock_packages
):
    """Test that conditional requirements are required when the condition is met,
    and optional when the condition is not met.
    """
    update_packages_config(packages_yaml)
    spec = Spec(spec_str).concretized()
    for match_str, expected in expected_satisfies:
        assert spec.satisfies(match_str) is expected


@pytest.mark.parametrize(
    "packages_yaml,spec_str,expected_message",
    [
        (
            """\
    packages:
      mpileaks:
        require:
        - one_of: ["~debug"]
          message: "debug is not allowed"
""",
            "mpileaks+debug",
            "debug is not allowed",
        ),
        (
            """\
    packages:
      libelf:
        require:
        - one_of: ["%clang"]
          message: "can only be compiled with clang"
""",
            "libelf%gcc",
            "can only be compiled with clang",
        ),
        (
            """\
        packages:
          libelf:
            require:
            - one_of: ["%clang"]
              when: platform=test
              message: "can only be compiled with clang on the test platform"
    """,
            "libelf%gcc",
            "can only be compiled with clang on ",
        ),
        (
            """\
            packages:
              libelf:
                require:
                - spec: "%clang"
                  when: platform=test
                  message: "can only be compiled with clang on the test platform"
        """,
            "libelf%gcc",
            "can only be compiled with clang on ",
        ),
        (
            """\
        packages:
          libelf:
            require:
            - one_of: ["%clang", "%intel"]
              when: platform=test
              message: "can only be compiled with clang or intel on the test platform"
    """,
            "libelf%gcc",
            "can only be compiled with clang or intel",
        ),
    ],
)
def test_requirements_fail_with_custom_message(
    packages_yaml, spec_str, expected_message, concretize_scope, mock_packages
):
    """Test that specs failing due to requirements not being satisfiable fail with a
    custom error message.
    """
    update_packages_config(packages_yaml)
    with pytest.raises(spack.error.SpackError, match=expected_message):
        Spec(spec_str).concretized()


def test_skip_requirement_when_default_requirement_condition_cannot_be_met(
    concretize_scope, mock_packages
):
    """Tests that we can express a requirement condition under 'all' also in cases where
    the corresponding condition spec mentions variants or versions that don't exist in the
    package. For those packages the requirement rule is not emitted, since it can be
    determined to be always false.
    """
    packages_yaml = """
        packages:
          all:
            require:
            - one_of: ["%clang"]
              when: "+shared"
    """
    update_packages_config(packages_yaml)
    s = Spec("mpileaks").concretized()

    assert s.satisfies("%clang +shared")
    # Sanity checks that 'callpath' doesn't have the shared variant, but that didn't
    # cause failures during concretization.
    assert "shared" not in s["callpath"].variants


def test_requires_directive(concretize_scope, mock_packages):
    compilers_yaml = pathlib.Path(concretize_scope) / "compilers.yaml"

    # NOTE: target is omitted here so that the test works on aarch64, as well.
    compilers_yaml.write_text(
        """
compilers::
- compiler:
    spec: gcc@12.0.0
    paths:
      cc: /usr/bin/clang-12
      cxx: /usr/bin/clang++-12
      f77: null
      fc: null
    operating_system: debian6
    modules: []
"""
    )
    spack.config.CONFIG.clear_caches()

    # This package requires either clang or gcc
    s = Spec("requires_clang_or_gcc").concretized()
    assert s.satisfies("%gcc@12.0.0")

    # This package can only be compiled with clang
    with pytest.raises(spack.error.SpackError, match="can only be compiled with Clang"):
        Spec("requires_clang").concretized()


@pytest.mark.parametrize(
    "packages_yaml",
    [
        # Simple string
        """
        packages:
          all:
            require: "+shared"
    """,
        # List of strings
        """
        packages:
          all:
            require:
            - "+shared"
    """,
        # Objects with attributes
        """
        packages:
          all:
            require:
            - spec: "+shared"
    """,
        """
        packages:
          all:
            require:
            - one_of: ["+shared"]
    """,
    ],
)
def test_default_requirements_semantic(packages_yaml, concretize_scope, mock_packages):
    """Tests that requirements under 'all:' are by default applied only if the variant/property
    required exists, but are strict otherwise.

    For example:

      packages:
        all:
          require: "+shared"

    should enforce the value of "+shared" when a Boolean variant named "shared" exists. This is
    not overridable from the command line, so with the configuration above:

    > spack spec zlib~shared

    is unsatisfiable.
    """
    update_packages_config(packages_yaml)

    # Regular zlib concretize to +shared
    s = Spec("zlib").concretized()
    assert s.satisfies("+shared")

    # If we specify the variant we can concretize only the one matching the constraint
    s = Spec("zlib +shared").concretized()
    assert s.satisfies("+shared")
    with pytest.raises(UnsatisfiableSpecError):
        Spec("zlib ~shared").concretized()

    # A spec without the shared variant still concretize
    s = Spec("pkg-a").concretized()
    assert not s.satisfies("pkg-a +shared")
    assert not s.satisfies("pkg-a ~shared")


@pytest.mark.parametrize(
    "packages_yaml,spec_str,expected,not_expected",
    [
        # The package has a 'libs' mv variant defaulting to 'libs=shared'
        (
            """
        packages:
          all:
            require: "+libs"
    """,
            "multivalue-variant",
            ["libs=shared"],
            ["libs=static", "+libs"],
        ),
        (
            """
        packages:
          all:
            require: "libs=foo"
    """,
            "multivalue-variant",
            ["libs=shared"],
            ["libs=static", "libs=foo"],
        ),
        (
            # (TODO): revisit this case when we'll have exact value semantic for mv variants
            """
        packages:
          all:
            require: "libs=static"
    """,
            "multivalue-variant",
            ["libs=static", "libs=shared"],
            [],
        ),
        (
            # Constraint apply as a whole, so having a non-existing variant
            # invalidate the entire constraint
            """
        packages:
          all:
            require: "libs=static +feefoo"
    """,
            "multivalue-variant",
            ["libs=shared"],
            ["libs=static"],
        ),
    ],
)
def test_default_requirements_semantic_with_mv_variants(
    packages_yaml, spec_str, expected, not_expected, concretize_scope, mock_packages
):
    """Tests that requirements under 'all:' are behaving correctly under cases that could stem
    from MV variants.
    """
    update_packages_config(packages_yaml)
    s = Spec(spec_str).concretized()

    for constraint in expected:
        assert s.satisfies(constraint), constraint

    for constraint in not_expected:
        assert not s.satisfies(constraint), constraint


@pytest.mark.regression("42084")
def test_requiring_package_on_multiple_virtuals(concretize_scope, mock_packages):
    update_packages_config(
        """
    packages:
      all:
        providers:
          scalapack: [netlib-scalapack]
      blas:
        require: intel-parallel-studio
      lapack:
        require: intel-parallel-studio
      scalapack:
        require: intel-parallel-studio
    """
    )
    s = Spec("dla-future").concretized()

    assert s["blas"].name == "intel-parallel-studio"
    assert s["lapack"].name == "intel-parallel-studio"
    assert s["scalapack"].name == "intel-parallel-studio"


@pytest.mark.parametrize(
    "packages_yaml,spec_str,expected,not_expected",
    [
        (
            """
        packages:
          all:
            prefer:
            - "%clang"
            compiler: [gcc]
    """,
            "multivalue-variant",
            ["%clang"],
            ["%gcc"],
        ),
        (
            """
            packages:
              all:
                prefer:
                - "%clang"
        """,
            "multivalue-variant %gcc",
            ["%gcc"],
            ["%clang"],
        ),
        # Test parsing objects instead of strings
        (
            """
            packages:
              all:
                prefer:
                - spec: "%clang"
                compiler: [gcc]
        """,
            "multivalue-variant",
            ["%clang"],
            ["%gcc"],
        ),
    ],
)
def test_strong_preferences_packages_yaml(
    packages_yaml, spec_str, expected, not_expected, concretize_scope, mock_packages
):
    """Tests that "preferred" specs are stronger than usual preferences, but can be overridden."""
    update_packages_config(packages_yaml)
    s = Spec(spec_str).concretized()

    for constraint in expected:
        assert s.satisfies(constraint), constraint

    for constraint in not_expected:
        assert not s.satisfies(constraint), constraint


@pytest.mark.parametrize(
    "packages_yaml,spec_str",
    [
        (
            """
        packages:
          all:
            conflict:
            - "%clang"
    """,
            "multivalue-variant %clang",
        ),
        # Use an object instead of a string in configuration
        (
            """
        packages:
          all:
            conflict:
            - spec: "%clang"
              message: "cannot use clang"
    """,
            "multivalue-variant %clang",
        ),
        (
            """
            packages:
              multivalue-variant:
                conflict:
                - spec: "%clang"
                  when: "@2"
                  message: "cannot use clang with version 2"
        """,
            "multivalue-variant@=2.3 %clang",
        ),
    ],
)
def test_conflict_packages_yaml(packages_yaml, spec_str, concretize_scope, mock_packages):
    """Tests conflicts that are specified from configuration files."""
    update_packages_config(packages_yaml)
    with pytest.raises(UnsatisfiableSpecError):
        Spec(spec_str).concretized()


@pytest.mark.parametrize(
    "spec_str,expected,not_expected",
    [
        (
            "forward-multi-value +cuda cuda_arch=10 ^dependency-mv~cuda",
            ["cuda_arch=10", "^dependency-mv~cuda"],
            ["cuda_arch=11", "^dependency-mv cuda_arch=10", "^dependency-mv cuda_arch=11"],
        ),
        (
            "forward-multi-value +cuda cuda_arch=10 ^dependency-mv+cuda",
            ["cuda_arch=10", "^dependency-mv cuda_arch=10"],
            ["cuda_arch=11", "^dependency-mv cuda_arch=11"],
        ),
        (
            "forward-multi-value +cuda cuda_arch=11 ^dependency-mv+cuda",
            ["cuda_arch=11", "^dependency-mv cuda_arch=11"],
            ["cuda_arch=10", "^dependency-mv cuda_arch=10"],
        ),
        (
            "forward-multi-value +cuda cuda_arch=10,11 ^dependency-mv+cuda",
            ["cuda_arch=10,11", "^dependency-mv cuda_arch=10,11"],
            [],
        ),
    ],
)
def test_forward_multi_valued_variant_using_requires(
    spec_str, expected, not_expected, config, mock_packages
):
    """Tests that a package can forward multivalue variants to dependencies, using
    `requires` directives of the form:

        for _val in ("shared", "static"):
            requires(f"^some-virtual-mv libs={_val}", when=f"libs={_val} ^some-virtual-mv")
    """
    s = Spec(spec_str).concretized()

    for constraint in expected:
        assert s.satisfies(constraint)

    for constraint in not_expected:
        assert not s.satisfies(constraint)


def test_strong_preferences_higher_priority_than_reuse(concretize_scope, mock_packages):
    """Tests that strong preferences have a higher priority than reusing specs."""
    reused_spec = Spec("adios2~bzip2").concretized()
    reuse_nodes = list(reused_spec.traverse())
    root_specs = [Spec("ascent+adios2")]

    # Check that without further configuration adios2 is reused
    with spack.config.override("concretizer:reuse", True):
        solver = spack.solver.asp.Solver()
        setup = spack.solver.asp.SpackSolverSetup()
        result, _, _ = solver.driver.solve(setup, root_specs, reuse=reuse_nodes)
        ascent = result.specs[0]
    assert ascent["adios2"].dag_hash() == reused_spec.dag_hash(), ascent

    # If we stick a preference, adios2 is not reused
    update_packages_config(
        """
    packages:
      adios2:
        prefer:
        - "+bzip2"
"""
    )
    with spack.config.override("concretizer:reuse", True):
        solver = spack.solver.asp.Solver()
        setup = spack.solver.asp.SpackSolverSetup()
        result, _, _ = solver.driver.solve(setup, root_specs, reuse=reuse_nodes)
        ascent = result.specs[0]

    assert ascent["adios2"].dag_hash() != reused_spec.dag_hash()
    assert ascent["adios2"].satisfies("+bzip2")

    # A preference is still preference, so we can override from input
    with spack.config.override("concretizer:reuse", True):
        solver = spack.solver.asp.Solver()
        setup = spack.solver.asp.SpackSolverSetup()
        result, _, _ = solver.driver.solve(
            setup, [Spec("ascent+adios2 ^adios2~bzip2")], reuse=reuse_nodes
        )
        ascent = result.specs[0]
    assert ascent["adios2"].dag_hash() == reused_spec.dag_hash(), ascent
