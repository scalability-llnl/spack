# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Test the Environment class"""

import spack.database
import spack.environment as ev
from spack.main import SpackCommand

env = SpackCommand("env")
add = SpackCommand("add")
develop = SpackCommand("develop")


def test_dev_use_git(tmpdir, mock_packages, mutable_database, mutable_mock_env_path, monkeypatch):
    existing_dev_path = tmpdir.ensure("dev-path", dir=True)
    spack_yaml = str(tmpdir.ensure("spack.yaml"))

    with open(spack_yaml, "w") as f:
        f.write(
            """\
spack:
    detect-changes-with-git: true
    view: false
    specs: []
"""
        )

    env("create", "test", spack_yaml)
    with ev.read("test") as e:
        add("dependent-of-dev-build")
        develop(f"--path={str(existing_dev_path)}", "dev-build-test-install@=0.0.0")
        e.concretize()

        user_to_concretized = list(e.concretized_specs())
        root = user_to_concretized[0][1]
        dependent = root["dependent-of-dev-build"]
        child = root["dev-build-test-install"]

        db = spack.database.Database(tmpdir.join("db"), lock_cfg=spack.database.NO_LOCK)
        db._add(root)

        class MockGitChangeDetector:
            def update_current(self):
                # Always indicate that a rebuild is required
                return True

        def mock_git_checker(git_dir):
            return MockGitChangeDetector()

        needs_reinstall, git_states = e._dev_specs_that_need_overwrite(
            _database=db, _git_checker=mock_git_checker
        )
        assert set(needs_reinstall) == set([dependent.dag_hash(), child.dag_hash()])
