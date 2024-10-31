# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.util.executable import which_string


class NinjaFortran(Package):
    """A Fortran capable fork of ninja."""

    homepage = "https://github.com/Kitware/ninja"
    url = "https://github.com/Kitware/ninja/archive/v1.9.0.g99df1.kitware.dyndep-1.jobserver-1.tar.gz"

    license("Apache-2.0")

    # Each version is a fork off of a specific commit of ninja
    # Hashes don't sort properly, so added "artificial" tweak-level version
    # number prior to the hashes for sorting puposes
    version(
        "1.9.0.2.g99df1", sha256="b7bc3d91e906b92d2e0887639e8ed6b0c45b28e339dda2dbb66c1388c86a9fcf"
    )
    version(
        "1.9.0.1.g5b44b", sha256="449359a402c3adccd37f6fece19ce7d7cda586e837fdf50eb7d53597b7f1ce90"
    )
    version(
        "1.9.0.0.gad558", sha256="ab486a3ccfb38636bfa61fefb976ddf9a7652f4bf12495a77718b35cc3db61ee"
    )
    version(
        "1.8.2.2.g81279", sha256="744a13475ace2c0ff8c8edaf95eb73edf3daf8805e4060b60d18ad4f55bb98aa"
    )
    version(
        "1.8.2.1.g3bbbe", sha256="121c432cec32c8aea730a71a256a81442ac8446c6f0e7652ea3121da9e0d482d"
    )
    version(
        "1.8.2.0.g972a7", sha256="127db130cb1c711ac4a5bb93d2f2665d304cff5206283332b50bc8ba2eb70d2e"
    )
    version(
        "1.7.2.1.gaad58", sha256="fac971edef78fc9f52e47365facb88c5c1c85d6d9c15f4356a1b97352c9ae5f8"
    )
    version(
        "1.7.2.0.gcc0ea", sha256="6afa570fa9300833f76e56fa5b01f5a3b7d8a7108f6ad368b067a003d25ef18b"
    )
    version(
        "1.7.1.0.g7ca7f", sha256="53472d0c3cf9c1cff7e991699710878be55d21a1c229956dea6a2c3e44edee80"
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("python", type="build")

    phases = ["configure", "install"]

    def url_for_version(self, version):
        # for some reason the hashes are being stripped from incomming
        # version, so find the incomming version in all package versions
        for ver in self.versions:
            if str(version) in str(ver):
                break

        # remove the "artificial" tweak-level
        split_ver = str(ver).split(".")
        url_version = ".".join(split_ver[:3]) + "." + split_ver[4]

        if version < spack.version.Version("1.8.2.1"):
            url = "https://github.com/Kitware/ninja/archive/v{0}.kitware.dyndep-1.tar.gz"
        else:
            url = (
                "https://github.com/Kitware/ninja/archive/v{0}.kitware.dyndep-1.jobserver-1.tar.gz"
            )
        return url.format(url_version)

    def configure(self, spec, prefix):
        python("configure.py", "--bootstrap")

    @run_after("configure")
    @on_package_attributes(run_tests=True)
    def configure_test(self):
        ninja = Executable("./ninja")
        ninja(f"-j{make_jobs}", "ninja_test")
        ninja_test = Executable("./ninja_test")
        ninja_test()

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("ninja", prefix.bin)
        install_tree("misc", prefix.misc)

        # Some distros like Fedora install a 'ninja-build' executable
        # instead of 'ninja'. Install both for uniformity.
        with working_dir(prefix.bin):
            symlink("ninja", "ninja-build")

    def setup_dependent_package(self, module, dspec):
        name = "ninja"

        module.ninja = MakeExecutable(
            which_string(name, path=[self.spec.prefix.bin], required=True),
            determine_number_of_jobs(parallel=dspec.package.parallel),
            supports_jobserver=True,  # This fork supports jobserver
        )
