# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Xsd(MakefilePackage):
    """CodeSynthesis XSD is an open-source, cross-platform W3C XML Schema
    to C++ data binding compiler. It support in-memory and event-driven XML
    processing models and is available for a wide range of C++ compilers
    and platforms."""

    homepage = "https://www.codesynthesis.com"
    url = "https://www.codesynthesis.com/download/xsd/4.0/xsd-4.0.0+dep.tar.bz2"

    version("4.0.0", sha256="eca52a9c8f52cdbe2ae4e364e4a909503493a0d51ea388fc6c9734565a859817")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("xerces-c")
    depends_on("libtool", type="build")

    patch(
        "https://git.codesynthesis.com/cgit/libxsd-frontend/libxsd-frontend/patch/?id=5029f8665190879285787a9dcdaf5f997cadd2e2",
        sha256="d57e0aed8784d2b947983209b6513c81ac593c9936c3d7b809b4cd60d4c28607",
        working_dir="libxsd-frontend",
    )

    def install(self, spec, prefix):
        make("install", "install_prefix=" + prefix)

    def setup_build_environment(self, env):
        xercesc_lib_flags = self.spec["xerces-c"].libs.search_flags
        env.append_flags("LDFLAGS", xercesc_lib_flags)

    def url_for_version(self, version):
        url = "https://www.codesynthesis.com/download/xsd/{0}/xsd-{1}+dep.tar.bz2"
        return url.format(version.up_to(2), version)
