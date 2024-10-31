# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pathlib

import pytest

import spack.config
import spack.environment as ev
import spack.repo
import spack.util.spack_yaml as syaml
from spack.spec import Spec

"""
These tests include the following package DAGs:

Firstly, w, x, y where w and x apply cflags to y.

w
|\
x |
|/
y

Secondly, v, y which where v does not apply cflags to y - this is for testing
mixing with compiler flag propagation in the absence of compiler flags applied
by dependents.

v
|
y

Finally, a diamond dag to check that the topological order is resolved into
a total order:

t
|\
u x
|/
y
"""


@pytest.fixture
def test_repo(mutable_config, monkeypatch, mock_stage):
    repo_dir = pathlib.Path(spack.paths.repos_path) / "flags.test"
    with spack.repo.use_repositories(str(repo_dir)) as mock_repo_path:
        yield mock_repo_path


def update_concretize_scope(conf_str, section):
    conf = syaml.load_config(conf_str)
    spack.config.set(section, conf[section], scope="concretize")


def test_mix_spec_and_requirements(concretize_scope, test_repo):
    conf_str = """\
packages:
  y:
    require: cflags="-c"
"""
    update_concretize_scope(conf_str, "packages")

    s1 = Spec('y cflags="-a"').concretized()
    assert s1.satisfies('cflags="-a -c"')


def test_mix_spec_and_dependent(concretize_scope, test_repo):
    s1 = Spec('x ^y cflags="-a"').concretized()
    assert s1["y"].satisfies('cflags="-a -d1"')


def _compiler_cfg_one_entry_with_cflags(cflags):
    return f"""\
compilers::
- compiler:
    spec: gcc@12.100.100
    paths:
      cc: /usr/bin/fake-gcc
      cxx: /usr/bin/fake-g++
      f77: null
      fc: null
    flags:
      cflags: {cflags}
    operating_system: debian6
    modules: []
"""


def test_mix_spec_and_compiler_cfg(concretize_scope, test_repo):
    conf_str = _compiler_cfg_one_entry_with_cflags("-Wall")
    update_concretize_scope(conf_str, "compilers")

    s1 = Spec('y %gcc@12.100.100 cflags="-O2"').concretized()
    assert s1.satisfies('cflags="-Wall -O2"')


@pytest.mark.parametrize(
    "cmd_flags,req_flags,cmp_flags,dflags,expected_order",
    [
        ("-a -b", "-c", None, False, "-c -a -b"),
        ("-x7 -x4", "-x5 -x6", None, False, "-x5 -x6 -x7 -x4"),
        ("-x7 -x4", "-x5 -x6", "-x3 -x8", False, "-x3 -x8 -x5 -x6 -x7 -x4"),
        ("-x7 -x4", "-x5 -x6", "-x3 -x8", True, "-x3 -x8 -d1 -d2 -x5 -x6 -x7 -x4"),
        ("-x7 -x4", None, "-x3 -x8", False, "-x3 -x8 -x7 -x4"),
        ("-x7 -x4", None, "-x3 -x8", True, "-x3 -x8 -d1 -d2 -x7 -x4"),
        # The remaining test cover cases of intersection
        ("-a -b", "-a -c", None, False, "-c -a -b"),
        ("-a -b", None, "-a -c", False, "-c -a -b"),
        ("-a -b", "-a -c", "-a -d", False, "-d -c -a -b"),
        ("-a -d2 -d1", "-d2 -c", "-d1 -b", True, "-b -c -a -d2 -d1"),
        ("-a", "-d0 -d2 -c", "-d1 -b", True, "-b -d1 -d0 -d2 -c -a"),
    ],
)
def test_flag_order_and_grouping(
    concretize_scope, test_repo, cmd_flags, req_flags, cmp_flags, dflags, expected_order
):
    """Check consistent flag ordering and grouping on a package "y"
    with flags introduced from a variety of sources.

    The ordering rules are explained in ``asp.SpecBuilder.reorder_flags``.
    """
    if req_flags:
        conf_str = f"""\
packages:
  y:
    require: cflags="{req_flags}"
"""
        update_concretize_scope(conf_str, "packages")

    if cmp_flags:
        conf_str = _compiler_cfg_one_entry_with_cflags(cmp_flags)
        update_concretize_scope(conf_str, "compilers")

    compiler_spec = ""
    if cmp_flags:
        compiler_spec = "%gcc@12.100.100"

    if dflags:
        spec_str = f"x+activatemultiflag {compiler_spec} ^y"
        expected_dflags = "-d1 -d2"
    else:
        spec_str = f"y {compiler_spec}"
        expected_dflags = None

    if cmd_flags:
        spec_str += f' cflags="{cmd_flags}"'

    root_spec = Spec(spec_str).concretized()
    spec = root_spec["y"]
    satisfy_flags = " ".join(x for x in [cmd_flags, req_flags, cmp_flags, expected_dflags] if x)
    assert spec.satisfies(f'cflags="{satisfy_flags}"')
    assert spec.compiler_flags["cflags"] == expected_order.split()


def test_two_dependents_flag_mixing(concretize_scope, test_repo):
    root_spec1 = Spec("w~moveflaglater").concretized()
    spec1 = root_spec1["y"]
    assert spec1.compiler_flags["cflags"] == "-d0 -d1 -d2".split()

    root_spec2 = Spec("w+moveflaglater").concretized()
    spec2 = root_spec2["y"]
    assert spec2.compiler_flags["cflags"] == "-d3 -d1 -d2".split()


def test_propagate_and_compiler_cfg(concretize_scope, test_repo):
    conf_str = _compiler_cfg_one_entry_with_cflags("-f2")
    update_concretize_scope(conf_str, "compilers")

    root_spec = Spec("v %gcc@12.100.100 cflags=='-f1'").concretized()
    assert root_spec["y"].satisfies("cflags='-f1 -f2'")


# Note: setting flags on a dependency overrides propagation, which
# is tested in test/concretize.py:test_compiler_flag_propagation


def test_propagate_and_pkg_dep(concretize_scope, test_repo):
    root_spec1 = Spec("x ~activatemultiflag cflags=='-f1'").concretized()
    assert root_spec1["y"].satisfies("cflags='-f1 -d1'")


def test_propagate_and_require(concretize_scope, test_repo):
    conf_str = """\
packages:
  y:
    require: cflags="-f2"
"""
    update_concretize_scope(conf_str, "packages")

    root_spec1 = Spec("v cflags=='-f1'").concretized()
    assert root_spec1["y"].satisfies("cflags='-f1 -f2'")

    # Next, check that a requirement does not "undo" a request for
    # propagation from the command-line spec
    conf_str = """\
packages:
  v:
    require: cflags="-f1"
"""
    update_concretize_scope(conf_str, "packages")

    root_spec2 = Spec("v cflags=='-f1'").concretized()
    assert root_spec2["y"].satisfies("cflags='-f1'")

    # Note: requirements cannot enforce propagation: any attempt to do
    # so will generate a concretization error; this likely relates to
    # the note about #37180 in concretize.lp


def test_dev_mix_flags(tmp_path, concretize_scope, mutable_mock_env_path, test_repo):
    src_dir = tmp_path / "x-src"

    env_content = f"""\
spack:
  specs:
  - y %gcc@12.100.100 cflags=='-fsanitize=address'
  develop:
    y:
      spec: y cflags=='-fsanitize=address'
      path: {src_dir}
"""

    conf_str = _compiler_cfg_one_entry_with_cflags("-f1")
    update_concretize_scope(conf_str, "compilers")

    manifest_file = tmp_path / ev.manifest_name
    manifest_file.write_text(env_content)
    e = ev.create("test", manifest_file)
    with e:
        e.concretize()
    e.write()

    (result,) = list(j for i, j in e.concretized_specs() if j.name == "y")

    assert result["y"].satisfies("cflags='-fsanitize=address -f1'")


def test_diamond_dep_flag_mixing(concretize_scope, test_repo):
    """A diamond where each dependent applies flags to the bottom
    dependency. The goal is to ensure that the flag ordering is
    (a) topological and (b) repeatable for elements not subject to
    this partial ordering (i.e. the flags for the left and right
    nodes of the diamond always appear in the same order).
    `Spec.traverse` is responsible for handling both of these needs.
    """
    root_spec1 = Spec("t").concretized()
    spec1 = root_spec1["y"]
    assert spec1.satisfies('cflags="-c1 -c2 -d1 -d2 -e1 -e2"')
    assert spec1.compiler_flags["cflags"] == "-c1 -c2 -e1 -e2 -d1 -d2".split()
