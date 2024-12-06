# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack.package import *


class Mujoco(Package):
    """MuJoCo is a physics engine that aims to facilitate research and
    development in robotics, biomechanics, graphics and animation, and
    other areas where fast and accurate simulation is needed."""

    homepage = "https://mujoco.org/"

    mujoco_releases = {
        "2.1.0": {
            "Linux-x86_64": "a436ca2f4144c38b837205635bbd60ffe1162d5b44c87df22232795978d7d012",
            "Darwin-x86_64": "50226f859d9d3742fa57e1a0a92d656197ec5786f75bfa50ae00eb80fae25e90",
        }
    }

    for ver, packages in mujoco_releases.items():
        key = "{0}-{1}".format(platform.system(), platform.machine())
        pkg_sha256 = packages.get(key)
        if pkg_sha256:
            version(ver, sha256=pkg_sha256)

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    def url_for_version(self, version):
        url = "https://mujoco.org/download/mujoco{0}-{1}-x86_64.tar.gz"

        system_map = {"Linux": "linux", "Darwin": "macos"}

        return url.format(version.joined, system_map[platform.system()])

    def install(self, spec, prefix):
        copy_tree(".", prefix)

    def setup_run_environment(self, env):
        env.prepend_path("CPATH", prefix.include)
        env.prepend_path("LD_LIBRARY_PATH", prefix.bin)
        if platform.system() == "Darwin":
            env.prepend_path("DYLD_LIBRARY_PATH", prefix.bin)
