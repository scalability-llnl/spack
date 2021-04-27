# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class FujitsuSsl2(Package):
    """Fujitsu SSL2 (Scientific Subroutine Library II) is Math library
    for Fujitsu compiler.
    Fujitsu SSL2 implementation only for Fujitsu compiler.
    Fujitsu SSL2 provides the function of blas, lapack and scalapack.
    """

    homepage = "https://www.fujitsu.com/us/"
    has_code = False

    variant("parallel", default=True, description="Build with thread-parallel versions")

    conflicts("%arm")
    conflicts("%cce")
    conflicts("%apple-clang")
    conflicts("%clang")
    conflicts("%gcc")
    conflicts("%intel")
    conflicts("%nag")
    conflicts("%pgi")
    conflicts("%xl")
    conflicts("%xl_r")

    provides("blas")
    provides("lapack")
    provides("scalapack")

    def install(self, spec, prefix):
        raise InstallError(
            "Fujitsu SSL2 is not installable; it is vendor supplied \
             You need to specify it as an external package in packages.yaml"
        )

    @property
    def blas_libs(self):
        spec = self.spec
        libslist = []
        if spec.target == "a64fx":  # Build with SVE support
            if "+parallel" in spec:  # parallel
                libslist.append("libfjlapackexsve.so")
            else:
                libslist.append("libfjlapacksve.so")
        else:
            if "+parallel" in spec:  # parallel
                libslist.append("libfjlapackex.so")
            else:
                libslist.append("libfjlapack.so")

        if "+parallel" in spec:  # parallel
            libslist.extend(["libfjomphk.so", "libfjomp.so"])

        if spec.target == "a64fx":  # Build with SVE support
            if "+parallel" in spec:  # parallel
                libslist.append("libssl2mtexsve.a")
            libslist.append("libssl2mtsve.a")
        else:
            if "+parallel" in spec:  # parallel
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
        libslist = []
        if spec.target == "a64fx":  # Build with SVE support
            libslist.append("libfjscalapacksve.so")
            if "+parallel" in spec:  # parallel
                libslist.append("libfjlapackexsve.so")
            else:
                libslist.append("libfjlapacksve.so")
            libslist.append("libscalapacksve.a")

        else:
            libslist.append("libfjscalapack.so")
            if "+parallel" in spec:  # parallel
                libslist.append("libfjlapackex.so")
            else:
                libslist.append("libfjlapack.so")
            libslist.append("libscalapack.a")

        libslist.extend(
            ["libmpi_usempi_ignore_tkr.so", "libmpi_mpifh.so"]
        )

        if "+parallel" in spec:  # parallel
            libslist.extend(["libfjomphk.so", "libfjomp.so"])

        if spec.target == "a64fx":  # Build with SVE support
            if "+parallel" in spec:  # parallel
                libslist.append("libssl2mtexsve.a")
            libslist.append("libssl2mtsve.a")
        else:
            if "+parallel" in spec:  # parallel
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
        path = self.prefix.include
        env.append_flags(
            "fcc_ENV", "-idirafter " + path
        )
        env.append_flags(
            "FCC_ENV", "-idirafter " + path
        )

    @property
    def headers(self):
        path = join_path(
            self.spec.prefix, "clang-comp"
        )
        headers = find_headers('cssl', path, recursive=True)
        return headers
