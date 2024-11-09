# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import pytest

from spack.directory_layout import DirectoryLayout
from spack.filesystem_view import SimpleFilesystemView, YamlFilesystemView
from spack.installer import PackageInstaller
from spack.spec import Spec


def test_remove_extensions_ordered(install_mockery, mock_fetch, tmpdir):
    view_dir = str(tmpdir.join("view"))
    layout = DirectoryLayout(view_dir)
    view = YamlFilesystemView(view_dir, layout)
    e2 = Spec("extension2").concretized()
    PackageInstaller([e2.package], explicit=True).install()
    view.add_specs(e2)

    e1 = e2["extension1"]
    view.remove_specs(e1, e2)


@pytest.mark.regression("32456")
def test_view_with_spec_not_contributing_files(mock_packages, tmpdir):
    view_dir = os.path.join(str(tmpdir), "view")
    os.mkdir(view_dir)

    layout = DirectoryLayout(view_dir)
    view = SimpleFilesystemView(view_dir, layout)

    a = Spec("pkg-a")
    b = Spec("pkg-b")
    a.prefix = os.path.join(tmpdir, "a")
    b.prefix = os.path.join(tmpdir, "b")
    a._mark_concrete()
    b._mark_concrete()

    # Create directory structure for a and b, and view
    os.makedirs(a.prefix.subdir)
    os.makedirs(b.prefix.subdir)
    os.makedirs(os.path.join(a.prefix, ".spack"))
    os.makedirs(os.path.join(b.prefix, ".spack"))

    # Add files to b's prefix, but not to a's
    with open(b.prefix.file, "w") as f:
        f.write("file 1")

    with open(b.prefix.subdir.file, "w") as f:
        f.write("file 2")

    # In previous versions of Spack we incorrectly called add_files_to_view
    # with b's merge map. It shouldn't be called at all, since a has no
    # files to add to the view.
    def pkg_a_add_files_to_view(view, merge_map, skip_if_exists=True):
        assert False, "There shouldn't be files to add"

    a.package.add_files_to_view = pkg_a_add_files_to_view

    # Create view and see if files are linked.
    view.add_specs(a, b)
    assert os.path.lexists(os.path.join(view_dir, "file"))
    assert os.path.lexists(os.path.join(view_dir, "subdir", "file"))
