# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import collections

import spack.config
import spack.detection
import spack.detection.common
import spack.detection.path
import spack.spec


def test_detection_update_config(mutable_config):
    # mock detected package
    detected_packages = collections.defaultdict(list)
    detected_packages["cmake"] = [spack.spec.Spec("cmake@3.27.5", external_path="/usr/bin")]

    # update config for new package
    spack.detection.common.update_configuration(detected_packages)
    # Check entries in 'packages.yaml'
    packages_yaml = spack.config.get("packages")
    assert "cmake" in packages_yaml
    assert "externals" in packages_yaml["cmake"]
    externals = packages_yaml["cmake"]["externals"]
    assert len(externals) == 1
    external_gcc = externals[0]
    assert external_gcc["spec"] == "cmake@3.27.5"
    assert external_gcc["prefix"] == "/usr/bin"


def test_dedupe_paths(tmp_path):
    """Test that ``dedupe_paths`` deals with symlinked directories, retaining the target"""
    x = tmp_path / "x"
    y = tmp_path / "y"
    z = tmp_path / "z"

    x.mkdir()
    y.mkdir()
    z.symlink_to("x", target_is_directory=True)

    # dedupe repeated dirs, should preserve order
    assert spack.detection.path.dedupe_paths([str(x), str(y), str(x)]) == [str(x), str(y)]
    assert spack.detection.path.dedupe_paths([str(y), str(x), str(y)]) == [str(y), str(x)]

    # dedupe repeated symlinks
    assert spack.detection.path.dedupe_paths([str(z), str(y), str(z)]) == [str(z), str(y)]
    assert spack.detection.path.dedupe_paths([str(y), str(z), str(y)]) == [str(y), str(z)]

    # when both symlink and target are present, only target is retained, and it comes at the
    # priority of the first occurrence.
    assert spack.detection.path.dedupe_paths([str(x), str(y), str(z)]) == [str(x), str(y)]
    assert spack.detection.path.dedupe_paths([str(z), str(y), str(x)]) == [str(x), str(y)]
    assert spack.detection.path.dedupe_paths([str(y), str(z), str(x)]) == [str(y), str(x)]
