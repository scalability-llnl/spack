# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.singularityce import SingularityBase


class Singularity(SingularityBase):
    """Singularity is a container technology focused on building portable
    encapsulated environments to support "Mobility of Compute" For older
    versions of Singularity (pre 3.0) you should use singularity-legacy,
    which has a different install base (Autotools).

    Needs post-install chmod/chown steps to enable full functionality.
    See package definition or `spack-build-out.txt` build log for details,
    e.g.

    tail -15 $(spack location -i singularity)/.spack/spack-build-out.txt
    """

    homepage = "https://singularity.hpcng.org/"
    git = "https://github.com/hpcng/singularity.git"
    url = "https://github.com/hpcng/singularity/releases/download/v3.8.5/singularity-3.8.5.tar.gz"

    license("BSD-3-Clause AND BSD-3-Clause-LBNL")

    version(
        "3.8.7",
        sha256="3329f2e583f84a8343cb2c0380a1d6cbceafae7d1e633b5cbcadf7143eac859b",
        deprecated=True,
    )
    version(
        "3.8.6",
        sha256="bb5a3b7670ac9c7a4b3ce5b2c9f3d6b5be60e21b08d338c9dfdabb7b2a99f528",
        deprecated=True,
    )
    version(
        "3.8.5",
        sha256="7fff78b5c07b5d4d08269bd267ac5e994390f933321e54efd6b7c86683153ce4",
        deprecated=True,
    )
    version(
        "3.8.3",
        sha256="2e22eb9ee1b73fdd51b8783149f0e4d83c0d2d8a0c1edf6034157d50eeefb835",
        deprecated=True,
    )
    version(
        "3.8.0",
        sha256="e9608b0e0a8c805218bbe795e9176484837b2f7fcb95e5469b853b3809a2412e",
        deprecated=True,
    )
    version(
        "3.7.4",
        sha256="c266369a8bf2747f44e0759858c3fc3b2325b975a8818b2668f0b97b124d0164",
        deprecated=True,
    )
    version(
        "3.7.3",
        sha256="6667eb8875d2b66d73504f40c956b42b1351744f488d164204376215d885da5c",
        deprecated=True,
    )
    version(
        "3.7.2",
        sha256="36916222e26fb934404f0766e0ff368edac36d7fc31ca571f5f609466609066b",
        deprecated=True,
    )
    version(
        "3.7.1",
        sha256="82d2c65063560195ec34551931be3c325b95e8e2009e92755fd7daad346e083c",
        deprecated=True,
    )
    version(
        "3.7.0",
        sha256="fb96aaf5f462a56a4a5bd2951287bcbbefe8cf543e228e4e955428f386a8d478",
        deprecated=True,
    )
    version(
        "3.6.4",
        sha256="71233a81d6bb4d686d8dc636b3e3e962a372f54001921c89a12b062cefd9e79f",
        deprecated=True,
    )
    version(
        "3.6.3",
        sha256="b1a985757a9907d8db0f102fc170a25387e715f7ff31957be964bf47914ea2fd",
        deprecated=True,
    )
    version(
        "3.6.2",
        sha256="dfd7ec7376ca0321c47787388fb3e781034edf99068f66efc36109e516024d9b",
        deprecated=True,
    )
    version(
        "3.6.1",
        sha256="6cac56106ee7f209150aaee9f8788d03b58796af1b767245d343f0b8a691121c",
        deprecated=True,
    )
    version(
        "3.5.3",
        sha256="0c76f1e3808bf4c10e92b17150314b2b816be79f8101be448a6e9d7a96c9e486",
        deprecated=True,
    )
    version(
        "3.5.2",
        sha256="f9c21e289377a4c40ed7a78a0c95e1ff416dec202ed49a6c616dd2c37700eab8",
        deprecated=True,
    )
    version(
        "3.4.1",
        sha256="638fd7cc5ab2a20e779b8768f73baf21909148339d6c4edf6ff61349c53a70c2",
        deprecated=True,
    )
    version(
        "3.4.0",
        sha256="eafb27f1ffbed427922ebe2b5b95d1c9c09bfeb897518867444fe230e3e35e41",
        deprecated=True,
    )
    version(
        "3.3.0",
        sha256="070530a472e7e78492f1f142c8d4b77c64de4626c4973b0589f0d18e1fcf5b4f",
        deprecated=True,
    )
    version(
        "3.2.1",
        sha256="d4388fb5f7e0083f0c344354c9ad3b5b823e2f3f27980e56efa7785140c9b616",
        deprecated=True,
    )
    version(
        "3.1.1",
        sha256="7f0df46458d8894ba0c2071b0848895304ae6b1137d3d4630f1600ed8eddf1a4",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated

    patch("singularity_v3.4.0_remove_root_check.patch", level=0, when="@3.4.0:3.4.1")
