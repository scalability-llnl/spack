# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.main
import spack.repo
import spack.spec
from spack.installer import PackageInstaller

tags = spack.main.SpackCommand("tags")


def test_tags_bad_options():
    out = tags("-a", "tag1", fail_on_error=False)
    assert "option OR provide" in out


def test_tags_no_installed(install_mockery, mock_fetch):
    out = tags("-i")
    assert "No installed" in out


def test_tags_invalid_tag(mock_packages):
    out = tags("nosuchtag")
    assert "None" in out


def test_tags_all_mock_tags(mock_packages):
    out = tags()
    for tag in ["tag1", "tag2", "tag3"]:
        assert tag in out


def test_tags_all_mock_tag_packages(mock_packages):
    out = tags("-a")
    for pkg in ["mpich\n", "mpich2\n"]:
        assert pkg in out


def test_tags_no_tags(monkeypatch):
    class tag_path:
        tag_index = dict()

    monkeypatch.setattr(spack.repo, "PATH", tag_path)
    out = tags()
    assert "No tagged" in out


def test_tags_installed(install_mockery, mock_fetch):
    s = spack.spec.Spec("mpich").concretized()
    PackageInstaller([s.package], explicit=True, fake=True).install()

    out = tags("-i")
    for tag in ["tag1", "tag2"]:
        assert tag in out

    out = tags("-i", "tag1")
    assert "mpich" in out

    out = tags("-i", "tag3")
    assert "No installed" in out
