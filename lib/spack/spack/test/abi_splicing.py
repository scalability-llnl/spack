# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
""" Test ABI-based splicing of dependencies """

from typing import List

import pytest

import spack.concretize
import spack.config
import spack.deptypes as dt
from spack.installer import PackageInstaller
from spack.solver.asp import SolverError
from spack.spec import Spec


def _make_specs_non_buildable(specs: List[str]):
    output_config = {}
    for spec in specs:
        output_config[spec] = {"buildable": False}
    return output_config


@pytest.fixture
def install_specs(
    mutable_database,
    mock_packages,
    mutable_config,
    do_not_check_runtimes_on_reuse,
    install_mockery,
):
    """Returns a function that concretizes and installs a list of abstract specs"""
    mutable_config.set("concretizer:reuse", True)

    def _impl(*specs_str):
        concrete_specs = [Spec(s).concretized() for s in specs_str]
        PackageInstaller([s.package for s in concrete_specs], fake=True, explicit=True).install()
        return concrete_specs

    return _impl


def _enable_splicing():
    spack.config.set("concretizer:splice", {"automatic": True})


@pytest.mark.parametrize("spec_str", ["splice-z", "splice-h@1"])
def test_spec_reuse(spec_str, install_specs, mutable_config):
    """Tests reuse of splice-z, without splicing, as a root and as a dependency of splice-h"""
    splice_z = install_specs("splice-z@1.0.0+compat")[0]
    mutable_config.set("packages", _make_specs_non_buildable(["splice-z"]))
    concrete = spack.concretize.concretize_one(spec_str)
    assert concrete["splice-z"].satisfies(splice_z)


@pytest.mark.regression("48578")
def test_splice_installed_hash(install_specs, mutable_config):
    """Tests splicing the dependency of an installed spec, for another installed spec"""
    splice_t, splice_h = install_specs(
        "splice-t@1 ^splice-h@1.0.0+compat ^splice-z@1.0.0",
        "splice-h@1.0.2+compat ^splice-z@1.0.0",
    )
    packages_config = _make_specs_non_buildable(["splice-t", "splice-h"])
    mutable_config.set("packages", packages_config)

    goal_spec = "splice-t@1 ^splice-h@1.0.2+compat ^splice-z@1.0.0"
    with pytest.raises(SolverError):
        spack.concretize.concretize_one(goal_spec)
    _enable_splicing()
    concrete = spack.concretize.concretize_one(goal_spec)

    # splice-t has a dependency that is changing, thus its hash should be different
    assert concrete.dag_hash() != splice_t.dag_hash()
    assert concrete.build_spec.satisfies(splice_t)
    assert not concrete.satisfies(splice_t)

    # splice-h is reused, so the hash should stay the same
    assert concrete["splice-h"].satisfies(splice_h)
    assert concrete["splice-h"].build_spec.satisfies(splice_h)
    assert concrete["splice-h"].dag_hash() == splice_h.dag_hash()


def test_splice_build_splice_node(install_specs, mutable_config):
    """Tests splicing the dependency of an installed spec, for a spec that is yet to be built"""
    splice_t = install_specs("splice-t@1 ^splice-h@1.0.0+compat ^splice-z@1.0.0+compat")[0]
    mutable_config.set("packages", _make_specs_non_buildable(["splice-t"]))

    goal_spec = "splice-t@1 ^splice-h@1.0.2+compat ^splice-z@1.0.0+compat"
    with pytest.raises(SolverError):
        spack.concretize.concretize_one(goal_spec)

    _enable_splicing()
    concrete = spack.concretize.concretize_one(goal_spec)

    # splice-t has a dependency that is changing, thus its hash should be different
    assert concrete.dag_hash() != splice_t.dag_hash()
    assert concrete.build_spec.satisfies(splice_t)
    assert not concrete.satisfies(splice_t)

    # splice-h should be different
    assert concrete["splice-h"].dag_hash() != splice_t["splice-h"].dag_hash()
    assert concrete["splice-h"].build_spec.dag_hash() == concrete["splice-h"].dag_hash()


def test_double_splice(install_specs, mutable_config):
    """Tests splicing two dependencies of an installed spec, for other installed specs"""
    splice_t, splice_h, splice_z = install_specs(
        "splice-t@1 ^splice-h@1.0.0+compat ^splice-z@1.0.0+compat",
        "splice-h@1.0.2+compat ^splice-z@1.0.1+compat",
        "splice-z@1.0.2+compat",
    )
    mutable_config.set("packages", _make_specs_non_buildable(["splice-t", "splice-h", "splice-z"]))

    goal_spec = "splice-t@1 ^splice-h@1.0.2+compat ^splice-z@1.0.2+compat"
    with pytest.raises(SolverError):
        spack.concretize.concretize_one(goal_spec)

    _enable_splicing()
    concrete = spack.concretize.concretize_one(goal_spec)

    # splice-t and splice-h have a dependency that is changing, thus its hash should be different
    assert concrete.dag_hash() != splice_t.dag_hash()
    assert concrete.build_spec.satisfies(splice_t)
    assert not concrete.satisfies(splice_t)

    assert concrete["splice-h"].dag_hash() != splice_h.dag_hash()
    assert concrete["splice-h"].build_spec.satisfies(splice_h)
    assert not concrete["splice-h"].satisfies(splice_h)

    # splice-z is reused, so the hash should stay the same
    assert concrete["splice-z"].dag_hash() == splice_z.dag_hash()


@pytest.mark.parametrize(
    "original_spec,goal_spec",
    [
        # `virtual-abi-1` can be spliced for `virtual-abi-multi abi=one` and vice-versa
        (
            "depends-on-virtual-with-abi ^virtual-abi-1",
            "depends-on-virtual-with-abi ^virtual-abi-multi abi=one",
        ),
        (
            "depends-on-virtual-with-abi ^virtual-abi-multi abi=one",
            "depends-on-virtual-with-abi ^virtual-abi-1",
        ),
        # `virtual-abi-2` can be spliced for `virtual-abi-multi abi=two` and vice-versa
        (
            "depends-on-virtual-with-abi ^virtual-abi-2",
            "depends-on-virtual-with-abi ^virtual-abi-multi abi=two",
        ),
        (
            "depends-on-virtual-with-abi ^virtual-abi-multi abi=two",
            "depends-on-virtual-with-abi ^virtual-abi-2",
        ),
    ],
)
def test_virtual_multi_splices_in(original_spec, goal_spec, install_specs, mutable_config):
    """Tests that we can splice a virtual dependency with a different, but compatible, provider."""
    original = install_specs(original_spec)[0]
    mutable_config.set("packages", _make_specs_non_buildable(["depends-on-virtual-with-abi"]))

    with pytest.raises(SolverError):
        spack.concretize.concretize_one(goal_spec)

    _enable_splicing()
    spliced = spack.concretize.concretize_one(goal_spec)

    assert spliced.dag_hash() != original.dag_hash()
    assert spliced.build_spec.dag_hash() == original.dag_hash()
    assert spliced["virtual-with-abi"].name != spliced.build_spec["virtual-with-abi"].name


def test_manyvariant_star_matching_variant_splice(install_specs, mutable_config):
    goal_specs = [
        Spec("depends-on-manyvariants ^manyvariants@1.0.1+a+b c=v1 d=v2"),
        Spec("depends-on-manyvariants ^manyvariants@1.0.1~a~b c=v3 d=v3"),
    ]
    install_specs(
        # can_splice("manyvariants@1.0.0", when="@1.0.1", match_variants="*")
        "depends-on-manyvariants ^manyvariants@1.0.0+a+b c=v1 d=v2",
        "depends-on-manyvariants ^manyvariants@1.0.0~a~b c=v3 d=v3",
    )
    freeze_build_config = {"depends-on-manyvariants": {"buildable": False}}
    mutable_config.set("packages", freeze_build_config)

    for goal in goal_specs:
        with pytest.raises(SolverError):
            spack.concretize.concretize_one(goal)

    _enable_splicing()
    for goal in goal_specs:
        assert spack.concretize.concretize_one(goal).satisfies(goal)


def test_manyvariant_limited_matching(install_specs, mutable_config):
    goal_specs = [
        Spec("depends-on-manyvariants@2.0 ^manyvariants@2.0.1~a+b c=v3 d=v2"),
        Spec("depends-on-manyvariants@2.0 ^manyvariants@2.0.1+a+b c=v3 d=v3"),
    ]
    install_specs(
        # can_splice("manyvariants@2.0.0+a~b", when="@2.0.1~a+b", match_variants=["c", "d"])
        "depends-on-manyvariants@2.0 ^manyvariants@2.0.0+a~b c=v3 d=v2",
        # can_splice("manyvariants@2.0.0 c=v1 d=v1", when="@2.0.1+a+b")
        "depends-on-manyvariants@2.0 ^manyvariants@2.0.0~a~b c=v1 d=v1",
    )
    freeze_build_config = {"depends-on-manyvariants": {"buildable": False}}
    mutable_config.set("packages", freeze_build_config)

    for s in goal_specs:
        with pytest.raises(SolverError):
            spack.concretize.concretize_one(s)

    _enable_splicing()
    for s in goal_specs:
        assert spack.concretize.concretize_one(s).satisfies(s)


def test_external_splice_same_name(install_specs, mutable_config):
    goal_specs = [
        Spec("splice-h@1.0.0 ^splice-z@1.0.2"),
        Spec("splice-t@1.0 ^splice-h@1.0.1 ^splice-z@1.0.2"),
    ]
    install_specs(
        "splice-h@1.0.0 ^splice-z@1.0.0+compat",
        "splice-t@1.0 ^splice-h@1.0.1 ^splice-z@1.0.1+compat",
    )
    mutable_config.set(
        "packages",
        {"splice-z": {"externals": [{"spec": "splice-z@1.0.2+compat", "prefix": "/usr"}]}},
    )

    _enable_splicing()
    for s in goal_specs:
        assert spack.concretize.concretize_one(s).satisfies(s)


def test_spliced_build_deps_only_in_build_spec(install_specs):
    goal_spec = Spec("splice-t@1.0 ^splice-h@1.0.2 ^splice-z@1.0.0")
    install_specs("splice-t@1.0 ^splice-h@1.0.1 ^splice-z@1.0.0")

    _enable_splicing()
    concr_goal = spack.concretize.concretize_one(goal_spec)
    build_spec = concr_goal._build_spec
    # Spec has been spliced
    assert build_spec is not None
    # Build spec has spliced build dependencies
    assert build_spec.dependencies("splice-h", dt.BUILD)
    assert build_spec.dependencies("splice-z", dt.BUILD)
    # Spliced build dependencies are removed
    assert len(concr_goal.dependencies(None, dt.BUILD)) == 0


def test_spliced_transitive_dependency(install_specs, mutable_config):
    goal_spec = Spec("splice-depends-on-t^splice-h@1.0.2")
    install_specs("splice-depends-on-t@1.0 ^splice-h@1.0.1")
    mutable_config.set("packages", _make_specs_non_buildable(["splice-depends-on-t"]))

    _enable_splicing()
    concr_goal = spack.concretize.concretize_one(goal_spec)
    # Spec has been spliced
    assert concr_goal._build_spec is not None
    assert concr_goal["splice-t"]._build_spec is not None
    assert concr_goal.satisfies(goal_spec)
    # Spliced build dependencies are removed
    assert len(concr_goal.dependencies(None, dt.BUILD)) == 0
