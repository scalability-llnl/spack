# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.environment as ev
import spack.spec
from spack.main import SpackCommand

undevelop = SpackCommand("undevelop")
env = SpackCommand("env")
concretize = SpackCommand("concretize")


def test_undevelop(tmpdir, mutable_config, mock_packages, mutable_mock_env_path):
    # setup environment
    envdir = tmpdir.mkdir("env")
    with envdir.as_cwd():
        with open("spack.yaml", "w") as f:
            f.write(
                """\
spack:
  specs:
  - mpich

  develop:
    mpich:
      spec: mpich@1.0
      path: /fake/path
"""
            )

        env("create", "test", "./spack.yaml")
        with ev.read("test"):
            before = spack.spec.Spec("mpich").concretized()
            undevelop("mpich")
            after = spack.spec.Spec("mpich").concretized()

    # Removing dev spec from environment changes concretization
    assert before.satisfies("dev_path=*")
    assert not after.satisfies("dev_path=*")


def test_undevelop_nonexistent(tmpdir, mutable_config, mock_packages, mutable_mock_env_path):
    # setup environment
    envdir = tmpdir.mkdir("env")
    with envdir.as_cwd():
        with open("spack.yaml", "w") as f:
            f.write(
                """\
spack:
  specs:
  - mpich

  develop:
    mpich:
      spec: mpich@1.0
      path: /fake/path
"""
            )

        env("create", "test", "./spack.yaml")
        with ev.read("test") as e:
            concretize()
            before = e.specs_by_hash
            undevelop("package-not-in-develop")  # does nothing
            concretize("-f")
            after = e.specs_by_hash

    # nothing should have changed
    assert before == after
