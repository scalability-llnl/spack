# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import spack.binary_distribution as bd
import spack.concretize
import spack.mirrors.mirror
from spack.installer import PackageInstaller


def test_build_tarball_overwrite(install_mockery, mock_fetch, monkeypatch, tmp_path):
    spec = spack.concretize.concretize_one("trivial-install-test-package")
    PackageInstaller([spec.package], fake=True).install()

    specs = [spec]

    # populate cache, everything is new
    mirror = spack.mirrors.mirror.Mirror.from_local_path(str(tmp_path))
    with bd.make_uploader(mirror) as uploader:
        skipped = uploader.push_or_raise(specs)
        assert not skipped

    # should skip all
    with bd.make_uploader(mirror) as uploader:
        skipped = uploader.push_or_raise(specs)
        assert skipped == specs

    # with force=True none should be skipped
    with bd.make_uploader(mirror, force=True) as uploader:
        skipped = uploader.push_or_raise(specs)
        assert not skipped

    # Remove the tarball, which should cause push to push.
    os.remove(
        tmp_path
        / bd.BUILD_CACHE_RELATIVE_PATH
        / bd.tarball_directory_name(spec)
        / bd.tarball_name(spec, ".spack")
    )

    with bd.make_uploader(mirror) as uploader:
        skipped = uploader.push_or_raise(specs)
        assert not skipped
