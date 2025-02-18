# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Libgpiod(AutotoolsPackage):
    """C library and tools for interacting with the linux GPIO character device
    (gpiod stands for GPIO device)"""

    homepage = "https://git.kernel.org/pub/scm/libs/libgpiod/libgpiod.git/about/"
    git = "https://git.kernel.org/pub/scm/libs/libgpiod/libgpiod"

    maintainers("davekeeshan")

    license("LGPL-2.1-or-later")

    version("master", branch="master")
    version("2.2.0", sha256="ae35329db7027c740e90c883baf27c26311f0614e6a7b115771b28188b992aec")
    version("2.1.3", sha256="8d80ea022ae78122aa525308e7423b83064bff278fcd9cd045b94b4f81f8057d")
    version("2.1.2", sha256="b1bdf1e3f75238695f93e442062bafc069170f2bf4f0cd4b8e049ca67131a1f0")
    version("2.1.1", sha256="0af43a6089d69f9d075cf67ca2ae5972b9081e38e6b3d46cea37d67e2df6fb9b")
    version("2.1.0", sha256="fd6ed4b2c674fe6cc3b481880f6cde1eea79e296e95a139b85401eaaea6de3fc")
    version("2.0.2", sha256="3532e1dbaffdc2c5965a761a0750f2691ee49aad273ddbbd93acf6a727b1b65c")
    version("2.0.1", sha256="b6eda55356160a8e73906e3d48e959ef81296787d764975b10f257e9660668e9")
    version("2.0.0", sha256="62071ac22872d9b936408e4a067d15edcdd61dce864ace8725eacdaefe23b898")
    version("1.6.5", sha256="1473d3035b506065393a4569763cf6b5c98e59c8f865326374ebadffa2578f3a")
    version("1.6.4", sha256="829d4ac268df07853609d67cfc7f476e9aa736cb2a68a630be99e8fad197be0a")
    version("1.6.3", sha256="eb446070be1444fd7d32d32bbca53c2f3bbb0a21193db86198cf6050b7a28441")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("autoconf-archive", type="build")
    depends_on("automake", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("libtool", type="build")

    def autoreconf(self, spec, prefix):
        Executable("./autogen.sh")()

    def url_for_version(self, version):
        url = "https://git.kernel.org/pub/scm/libs/libgpiod/libgpiod.git/snapshot/libgpiod-{0}.tar.gz"
        if version[2] == 0:
            return url.format(version.up_to(1))
        else:
            return url.format(version)
