# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack.package import *


class Patchelf(AutotoolsPackage):
    """PatchELF is a small utility to modify the dynamic linker and RPATH of
    ELF executables."""

    homepage = "https://nixos.org/patchelf.html"
    url = "https://github.com/NixOS/patchelf/releases/download/0.12/patchelf-0.12.tar.bz2"
    list_url = "https://nixos.org/releases/patchelf/"
    list_depth = 1

    maintainers("haampie")

    license("GPL-3.0-or-later")

    version("0.18.0", sha256="64de10e4c6b8b8379db7e87f58030f336ea747c0515f381132e810dbf84a86e7")
    # patchelf 0.18 breaks libraries:
    # https://github.com/spack/spack/issues/39252
    # https://github.com/spack/spack/pull/40938
    version(
        "0.17.2",
        sha256="20427b718dd130e4b66d95072c2a2bd5e17232e20dad58c1bea9da81fae330e0",
        preferred=True,
    )
    version("0.16.1", sha256="1a562ed28b16f8a00456b5f9ee573bb1af7c39c1beea01d94fc0c7b3256b0406")
    version("0.15.0", sha256="53a8d58ed4e060412b8fdcb6489562b3c62be6f65cee5af30eba60f4423bfa0f")
    version("0.14.5", sha256="113ada3f1ace08f0a7224aa8500f1fa6b08320d8f7df05ff58585286ec5faa6f")
    version("0.14.3", sha256="8fabf4210499744ced101612cd5c9fd12b94af67a16297cb5d3ff682c007ffdb")
    version("0.14.2", sha256="3dbced63d02076221397d3fa45ef6cf6776e7c6d45ea5c4e86c91604dfc87a80")
    version("0.14.1", sha256="7a1506caf6873a2b60e7bebc35e1671fa232ee075642b074106b0d0636417466")
    version("0.14", sha256="a31f2bff841dffa896317d3837bc2877c1f79da0744d88e459662d8e7fe7897c")
    version("0.13.1", sha256="08c0237e89be74d61ddf8f6ff218439cdd62af572d568fb38913b53e222831de")
    version("0.13", sha256="4c7ed4bcfc1a114d6286e4a0d3c1a90db147a4c3adda1814ee0eee0f9ee917ed")
    version("0.12", sha256="699a31cf52211cf5ad6e35a8801eb637bc7f3c43117140426400d67b7babd792")
    version("0.11", sha256="e52378cc2f9379c6e84a04ac100a3589145533a7b0cd26ef23c79dfd8a9038f9")
    version("0.10", sha256="b2deabce05c34ce98558c0efb965f209de592197b2c88e930298d740ead09019")
    version("0.9", sha256="f2aa40a6148cb3b0ca807a1bf836b081793e55ec9e5540a5356d800132be7e0a")
    version("0.8", sha256="14af06a2da688d577d64ff8dac065bb8903bbffbe01d30c62df7af9bf4ce72fe")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    conflicts("%gcc@:4.6", when="@0.10:", msg="Requires C++11 support")
    conflicts("%gcc@:6", when="@0.14:", msg="Requires C++17 support")
    conflicts("%clang@:3", when="@0.14:", msg="Requires C++17 support")

    # GCC 7.5 doesn't have __cpp_deduction_guides >= 201606
    patch("513.patch", when="@0.18: %gcc@:7")

    def url_for_version(self, version):
        if version < Version("0.12"):
            return "https://nixos.org/releases/patchelf/patchelf-{0}/patchelf-{1}.tar.gz".format(
                version, version
            )

        # Prefer gz over bz2
        if version >= Version("0.13.1"):
            return "https://github.com/NixOS/patchelf/releases/download/{0}/patchelf-{1}.tar.gz".format(
                version, version
            )

        return (
            "https://github.com/NixOS/patchelf/releases/download/{0}/patchelf-{1}.tar.bz2".format(
                version, version
            )
        )

    def test_version(self):
        """ensure patchelf version match"""
        # Check patchelf in prefix and reports the correct version
        patchelf = which(self.prefix.bin.patchelf)
        out = patchelf("--version", output=str.split, error=str.split)
        expected = f"patchelf {self.spec.version}"
        assert expected in out, f"Expected '{expected}' in output"

    def test_rpath_change(self):
        """ensure patchelf can change rpath"""
        currdir = os.getcwd()
        hello_file = self.test_suite.current_test_data_dir.join("hello")

        patchelf = which(self.prefix.bin.patchelf)
        patchelf("--set-rpath", currdir, hello_file)
        out = patchelf("--print-rpath", hello_file, output=str.split, error=str.split)
        assert currdir in out, f"Expected '{currdir}' in output"
