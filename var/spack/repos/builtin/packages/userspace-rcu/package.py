# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class UserspaceRcu(AutotoolsPackage):
    """liburcu is a LGPLv2.1 userspace RCU (read-copy-update) library. This
    data synchronization library provides read-side access which scales
    linearly with the number of cores."""

    homepage = "https://liburcu.org/"
    url = "https://github.com/urcu/userspace-rcu/archive/v0.11.1.tar.gz"

    license("LGPL-2.1-or-later")

    version("0.13.1", sha256="b810481f0c859a5859d82e23eddd2856b410802009f94663d64c330dc2f4403e")
    version("0.13.0", sha256="c457d17ec9dff7db0e90b103ef1a03737efdeaec13098af82f83a03091c835b5")
    version("0.12.3", sha256="a61b5aca001f70cb576505cc4869bd74a758484343466cc49cb1342c67028a54")
    version("0.12.2", sha256="d282169cdfa9fcc4cfbacab3757bb739debf4559a7f9ad537bb8b2061e98351a")
    version("0.12.1", sha256="19f31563db5078f47cabbb06bd7a3935a0964e31449efedd267f311ae79443c6")
    version("0.12.0", sha256="6b0cdee07a651c56daea8d03285f379afab898ebc83c785a23927320e45a3012")
    version("0.11.4", sha256="d995598482221587ff6753d2a8da6ac74ff0fa79fbea29ccee196f295834531d")
    version("0.11.3", sha256="fa7a3be0fe1bb000be0a5b28c5b33fdbc13d7cf5a4816b9bcbc60e2adf8ec8d5")
    version("0.11.2", sha256="072da1b9cf864a4cb9f7b9bb6c208979682ce018cbd1ead0ee84e294e3035cbd")
    version("0.11.1", sha256="a0ed8995edfbeac5f5eb2f152a8f3654040ecfc99a746bfe3da3bccf435b7d5d")
    version("0.11.0", sha256="7834e4692565b491b9d2d258095d6c05089c9bae8a1bef280c338d15ba02e9ac")
    version("0.10.2", sha256="e117c416fced894e24720cc1b38247074a13020f19d6704b38e554cbcb993d06")
    version("0.9.6", sha256="4d9e4ca40c079e0b0e9f912a9092589b97fbaf80eb6537e9ae70d48c09472efa")

    depends_on("c", type="build")  # generated

    depends_on("m4", type="build")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")

    patch(
        "examples.patch", sha256="49aa8fa99d3a1315c639d2a90014079c34a7d0a6dde110b6cbb7b02f87324742"
    )

    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("./bootstrap")
