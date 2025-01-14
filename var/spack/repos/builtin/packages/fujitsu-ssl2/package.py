# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from llnl.util.filesystem import HeaderList, LibraryList

from spack.package import *


class FugakuClangLinkFlags(LibraryList):
    """Provides *_flags for custom LLVM wrappers which take care of SSL2"""

    def __init__(self, flags=[]):
        self.files = list()
        self.fugaku_clang_flags = flags

    @property
    def libraries(self):
        return self.files

    @property
    def names(self):
        libslist = []
        if "-SSL2BLAMP" in self.fugaku_clang_flags:
            libslist.append("fjlapackexsve")
        elif "-SSL2" in self.fugaku_clang_flags:
            libslist.append("fjlapacksve")
        if "-SCALAPACK" in self.fugaku_clang_flags:
            libslist.append("fjscalapacksve")
        return libslist

    @property
    def search_flags(self):
        return ""

    @property
    def link_flags(self):
        return "{0}".format(" ".join(self.fugaku_clang_flags))

    @property
    def ld_flags(self):
        return "{0}".format(" ".join(self.fugaku_clang_flags))


class FujitsuSsl2(Package):
    """Fujitsu SSL2 (Scientific Subroutine Library II) is Math library
    for Fujitsu compiler.
    Fujitsu SSL2 implementation only for Fujitsu compiler.
    Fujitsu SSL2 provides the function of blas, lapack and scalapack.
    """

    homepage = "https://www.fujitsu.com/us/"
    has_code = False

    variant("parallel", default=True, description="Build with thread-parallel versions")

    provides("blas")
    provides("lapack")
    provides("scalapack")

    requires(
        "%fj",
        "%clang@17:",
        policy="one_of",
        msg="currently only supports Fujitsu or Clang compilers",
    )

    def install(self, spec, prefix):
        raise InstallError(
            "Fujitsu SSL2 is not installable; it is vendor supplied "
            "You need to specify it as an external package in packages.yaml"
        )

    @property
    def blas_libs(self):
        spec = self.spec
        if spec.satisfies("%clang"):
            if "+parallel" in spec:
                return FugakuClangLinkFlags(["-SSL2BLAMP"])
            else:
                return FugakuClangLinkFlags(["-SSL2"])
        libslist = []
        if spec.target == "a64fx":  # Build with SVE support
            if spec.satisfies("+parallel"):  # parallel
                libslist.append("libfjlapackexsve.so")
            else:
                libslist.append("libfjlapacksve.so")
        else:
            if spec.satisfies("+parallel"):  # parallel
                libslist.append("libfjlapackex.so")
            else:
                libslist.append("libfjlapack.so")

        if spec.satisfies("+parallel"):  # parallel
            libslist.extend(["libfjomphk.so", "libfjomp.so"])

        if spec.target == "a64fx":  # Build with SVE support
            if spec.satisfies("+parallel"):  # parallel
                libslist.append("libssl2mtexsve.a")
            libslist.append("libssl2mtsve.a")
        else:
            if spec.satisfies("+parallel"):  # parallel
                libslist.append("libssl2mtex.a")
            libslist.append("libssl2mt.a")

        libslist.append("libfj90i.so")

        if spec.target == "a64fx":  # Build with SVE support
            libslist.append("libfj90fmt_sve.a")
        else:
            libslist.append("libfj90fmt.a")

        libslist.extend(["libfj90f.so", "libfjsrcinfo.so", "libfj90rt.so"])

        libspath = find(self.prefix.lib64, libslist, recursive=False)
        libs = LibraryList(libspath)

        return libs

    @property
    def lapack_libs(self):
        return self.blas_libs

    @property
    def scalapack_libs(self):
        spec = self.spec
        if self.spec.satisfies("%clang"):
            if "+parallel" in spec:
                return FugakuClangLinkFlags(["-SSL2BLAMP", "-SCALAPACK"])
            else:
                return FugakuClangLinkFlags(["-SSL2", "-SCALAPACK"])
        libslist = []
        if spec.target == "a64fx":  # Build with SVE support
            libslist.append("libfjscalapacksve.so")
            if spec.satisfies("+parallel"):  # parallel
                libslist.append("libfjlapackexsve.so")
            else:
                libslist.append("libfjlapacksve.so")
            libslist.append("libscalapacksve.a")

        else:
            libslist.append("libfjscalapack.so")
            if spec.satisfies("+parallel"):  # parallel
                libslist.append("libfjlapackex.so")
            else:
                libslist.append("libfjlapack.so")
            libslist.append("libscalapack.a")

        libslist.extend(["libmpi_usempi_ignore_tkr.so", "libmpi_mpifh.so"])

        if spec.satisfies("+parallel"):  # parallel
            libslist.extend(["libfjomphk.so", "libfjomp.so"])

        if spec.target == "a64fx":  # Build with SVE support
            if spec.satisfies("+parallel"):  # parallel
                libslist.append("libssl2mtexsve.a")
            libslist.append("libssl2mtsve.a")
        else:
            if spec.satisfies("+parallel"):  # parallel
                libslist.append("libssl2mtex.a")
            libslist.append("libssl2mt.a")

        libslist.append("libfj90i.so")

        if spec.target == "a64fx":  # Build with SVE support
            libslist.append("libfj90fmt_sve.a")
        else:
            libslist.append("libfj90fmt.a")

        libslist.extend(["libfj90f.so", "libfjsrcinfo.so", "libfj90rt.so"])

        libspath = find(self.prefix.lib64, libslist, recursive=False)
        libs = LibraryList(libspath)

        return libs

    def setup_dependent_build_environment(self, env, dependent_spec):
        spec = self.spec
        if spec.satisfies("%clang"):
            if "+parallel" in spec:
                env.append_flags("fcc_ENV", "-SSL2BLAMP")
                env.append_flags("FCC_ENV", "-SSL2BLAMP")
                env.append_flags("frt_ENV", "-SSL2BLAMP")
            else:
                env.append_flags("fcc_ENV", "-SSL2")
                env.append_flags("FCC_ENV", "-SSL2")
                env.append_flags("frt_ENV", "-SSL2")
        path = self.prefix.include
        env.append_flags("fcc_ENV", "-idirafter " + path)
        env.append_flags("FCC_ENV", "-idirafter " + path)

    @property
    def headers(self):
        if self.spec.satisfies("%clang"):
            headers = HeaderList([])
            if "+parallel" in self.spec:
                headers.add_macro("-SSL2BLAMP")
            else:
                headers.add_macro("-SSL2")
            return headers
        else:
            path = join_path(self.spec.prefix, "clang-comp")
            headers = find_headers("cssl", path, recursive=True)
            return headers
