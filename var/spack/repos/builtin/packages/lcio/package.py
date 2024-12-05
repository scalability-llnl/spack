# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Lcio(CMakePackage):
    """HEP Library for Linear Collider Input/Output"""

    homepage = "http://lcio.desy.de"
    git = "https://github.com/iLCSoft/LCIO.git"
    url = "https://github.com/iLCSoft/LCIO/archive/v02-13-03.tar.gz"

    tags = ["hep"]

    maintainers("gaede", "vvolkl", "jmcarcell")

    license("BSD-3-Clause")

    version("master", branch="master")
    version("2.22.2", sha256="e5ad9690af85160ef52dd407fc0995451b4293f3aee415a8ea8a950de63d87a1")
    version("2.22.1", sha256="4bc3d2c83af7b1c65d6736dd14ee82f41af7ce9bfc7cfe779c5f47417e8dc326")
    version("2.22", sha256="95676977a0427f5ecc857e8504b13f332c2c2e5769dc00f6beecff3c73dab395")
    version("2.21", sha256="a9f0a9922ab2ef17c6f1b8f7187bfc341f27567745a43c0480c103b617dfcea6")
    version("2.20.2", sha256="b37cee344c28ccddc590e5317721b375ef19f4392ae067bc86583107acaf2374")
    version("2.20.1", sha256="125f657297de12b40694cb0dddec1d1ce3379058492f2a6a2a6f992ee51604d6")
    version("2.20", sha256="5ef92c9ef04ce468ffb48be0ec6010377a400b064e352cb50f9f4c9599e7e990")
    version("2.19", sha256="2d6b37094d8d556ab0ba0efa632f10d8b851f533ca5c767e436397df18cb57c7")
    version("2.18", sha256="e722df7f4a6adcc2459ea1c6488a2a6e40bb04f7ee99536fdc60b51e6c80f565")
    version("2.17.1", sha256="e7e4e4399a53680dfb8cc497e7f59633a96361f8f9435d1b044a90fd3ad97ab7")
    version("2.17", sha256="a81e07790443f0e2d9abb18bc3b5f2929edbc8d8e4f307f931679eaa39bb044a")
    version("2.16.1", sha256="992a649f864785e62fe12d7a638b2696c91f9535881de33f22b3cceabcdcdbaf")
    version("2.16", sha256="aff7707750d821f31cbae3d7529fd8e22457f48d759e834ec01aa9389b5dbf1a")
    version("2.15.4", sha256="720c8130762d445df44d2c245da01c0a1ca807d7ed62362cebf7b3a99f9a37d7")
    version("2.15.3", sha256="a00f9e1e8fc98151e88e603bbfca8088ded21ae3daca5c91869628a19af0cefb")
    version("2.15.2", sha256="9886c6f5c275c1c51bde978e4f5514bb4ea9588239f1d3ee95a76ef4b686e69d")
    version("2.15.1", sha256="32921feb162408357d00a81cdd489c374b3ed8ab6f442d798b22835de7243d32")
    version("2.15", sha256="27ea161a36ca93bf6b11381b63e90d100d3aeda3a00377bebcf2972c436aa3a7")
    version("2.14.2", sha256="e64f4bf932edf6d6cdaf0162e5104f8fbf3e5fd9737c7a080c48859009621919")
    version("2.14.1", sha256="ef670b10b6a01649fd4f3afcf38cbbee4cd83133612f922977260a6fea2bf30f")
    version("2.14", sha256="85a7da4873b3501887d371cb8d993cb9f373323b190a8d523ad91b900a5f1284")
    version("2.13.3", sha256="35aaa7989be33574a7c44ea7e6d7780ab26ef8bd4aa29d495f3831a3cd269304")
    version("2.13.2", sha256="9f153ba13e56ee16795378f9192678d40df1faca51d00aaa8fb80547bfecb8d8")
    version("2.13.1", sha256="aa572e2ba38c0cadd6a92fa933c3ed97e21d016c7982578d3f293901169f4ec0")

    depends_on("cxx", type="build")  # generated

    variant(
        "cxxstd",
        default="17",
        values=(
            "11",
            "14",
            "17",
            "20",
            # c++17 became minimum with 2.18
            conditional("17", "20", when="@2.18:"),
        ),
        multi=False,
        description="Use the specified C++ standard when building.",
    )
    variant("jar", default=False, description="Turn on to build/install lcio.jar")
    variant("rootdict", default=True, description="Turn on to build/install ROOT dictionary.")
    variant("examples", default=False, description="Turn on to build LCIO examples")

    depends_on("sio@0.0.2:", when="@2.14:")
    depends_on("sio@0.1:", when="@2.16:")
    depends_on("sio@0.2:", when="@2.21:")

    depends_on("root@6.04:", when="+rootdict")
    depends_on("root@6.04: cxxstd=11", when="+rootdict cxxstd=11")
    depends_on("root@6.04: cxxstd=14", when="+rootdict cxxstd=14")
    depends_on("root@6.04: cxxstd=17", when="+rootdict cxxstd=17")
    depends_on("root@6.04: cxxstd=20", when="+rootdict cxxstd=20")
    depends_on("openjdk", when="+jar")
    # build error with +termlib, to be investigated
    depends_on("ncurses~termlib", when="+examples")
    depends_on("delphes", when="+examples")
    depends_on("readline", when="+examples")

    def cmake_args(self):
        args = [
            self.define("CMAKE_CXX_STANDARD", self.spec.variants["cxxstd"].value),
            self.define("BUILD_TESTING", self.run_tests),
            self.define_from_variant("BUILD_LCIO_EXAMPLES", "examples"),
            self.define_from_variant("BUILD_ROOTDICT", "rootdict"),
            self.define_from_variant("INSTALL_JAR", "jar"),
        ]
        return args

    def url_for_version(self, version):
        base_url = self.url.rsplit("/", 1)[0]
        major = str(version[0]).zfill(2)
        minor = str(version[1]).zfill(2)
        # handle the different cases for the patch version:
        # first case, no patch version is given in spack, i.e 0.1
        if len(version) == 2:
            url = base_url + "/v%s-%s.tar.gz" % (major, minor)
        # a patch version is specified in spack, i.e. 0.1.x ...
        elif len(version) == 3:
            patch = str(version[2]).zfill(2)
            # ... but it is zero, and not part of the ilc release url
            if version[2] == 0:
                url = base_url + "/v%s-%s.tar.gz" % (major, minor)
            # ... if it is non-zero, it is part  of the release url
            else:
                url = base_url + "/v%s-%s-%s.tar.gz" % (major, minor, patch)
        else:
            print("Error - Wrong version format provided")
            return
        return url

    def setup_run_environment(self, env):
        env.set("LCIO", self.prefix)
        env.prepend_path("PYTHONPATH", self.prefix.python)
        # needed for the python bindings to find "Exceptions.h"
        env.prepend_path("CPATH", self.prefix)
        env.prepend_path("LD_LIBRARY_PATH", self.spec["lcio"].libs.directories[0])

    @run_after("install")
    def install_source(self):
        # these files are needed for the python bindings and root to
        # find the headers
        if self.spec.version > Version("2.17"):
            # This has been fixed upstream
            return

        install_tree("src/cpp/include/pre-generated/", self.prefix.include + "/pre-generated")
        install("src/cpp/include/IOIMPL/LCEventLazyImpl.h", self.prefix.include + "/IOIMPL/")
        install("src/cpp/include/SIO/SIOHandlerMgr.h", self.prefix.include + "/SIO/")
        install("src/cpp/include/SIO/SIOObjectHandler.h", self.prefix.include + "/SIO/")
