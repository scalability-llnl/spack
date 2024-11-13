# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xqilla(AutotoolsPackage, SourceforgePackage):
    """XQilla is an XQuery and XPath 2 library and command line utility
    written in C++, implemented on top of the Xerces-C library."""

    homepage = "https://xqilla.sourceforge.net/HomePage"
    sourceforge_mirror_path = "xqilla/XQilla-2.3.3.tar.gz"

    license("Apache-2.0")

    version("2.3.3", sha256="8f76b9b4f966f315acc2a8e104e426d8a76ba4ea3441b0ecfdd1e39195674fd6")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("debug", default=False, description="Build a debugging version.")
    variant("shared", default=True, description="Build shared libraries.")

    # see https://sourceforge.net/p/xqilla/bugs/48/
    patch(
        "https://src.fedoraproject.org/rpms/xqilla/raw/1f2f53305f429aa3db2ab078d9613fbc367b402d/f/0004-xerces-3.2.0-casts.patch",
        sha256="78997e098f041bf41def6fab436ea406b2dceaa15ae3ec8a8d2aa7ed356a0bb9",
        when="@:2.3.3",
    )
    patch(
        "https://src.fedoraproject.org/rpms/xqilla/raw/1f2f53305f429aa3db2ab078d9613fbc367b402d/f/0005-xqilla-gcc11.patch",
        sha256="52e5f03012fe9ae5b0f90d04eff042fb2082aa8f366a47d9e6be0d452de87b73",
        when="%gcc@11:",
    )

    depends_on("xerces-c")

    def configure_args(self):
        args = ["--with-xerces={0}".format(self.spec["xerces-c"].prefix)]

        if "+shared" in self.spec:
            args.extend(["--enable-shared=yes", "--enable-static=no"])
        else:
            args.extend(["--enable-shared=no", "--enable-static=yes", "--with-pic"])

        if "+debug" in self.spec:
            args.append("--enable-debug")

        return args
