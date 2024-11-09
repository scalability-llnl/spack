# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.builder
from spack.build_systems import autotools, cmake
from spack.package import *


class Proj(CMakePackage, AutotoolsPackage):
    """PROJ is a generic coordinate transformation software, that transforms
    geospatial coordinates from one coordinate reference system (CRS) to
    another. This includes cartographic projections as well as geodetic
    transformations."""

    homepage = "https://proj.org/"
    url = "https://download.osgeo.org/proj/proj-7.2.1.tar.gz"

    maintainers("adamjstewart")

    # Version 6 removes projects.h, while version 7 removes proj_api.h.
    # Many packages that depend on proj do not yet support the newer API.
    # See https://github.com/OSGeo/PROJ/wiki/proj.h-adoption-status

    license("MIT")

    version("9.4.1", sha256="ffe20170ee2b952207adf8a195e2141eab12cda181e49fdeb54425d98c7171d7")
    version("9.4.0", sha256="3643b19b1622fe6b2e3113bdb623969f5117984b39f173b4e3fb19a8833bd216")
    version("9.3.1", sha256="b0f919cb9e1f42f803a3e616c2b63a78e4d81ecfaed80978d570d3a5e29d10bc")
    version("9.3.0", sha256="91a3695a004ea28db0448a34460bed4cc3b130e5c7d74339ec999efdab0e547d")
    version("9.2.1", sha256="15ebf4afa8744b9e6fccb5d571fc9f338dc3adcf99907d9e62d1af815d4971a1")
    version("9.2.0", sha256="dea816f5aa732ae6b2ee3977b9bdb28b1d848cf56a1aad8faf6708b89f0ed50e")
    version("9.1.1", sha256="003cd4010e52bb5eb8f7de1c143753aa830c8902b6ed01209f294846e40e6d39")
    version("9.1.0", sha256="81b2239b94cad0886222cde4f53cb49d34905aad2a1317244a0c30a553db2315")
    version("9.0.1", sha256="737eaacbe7906d0d6ff43f0d9ebedc5c734cccc9e6b8d7beefdec3ab22d9a6a3")
    version("9.0.0", sha256="0620aa01b812de00b54d6c23e7c5cc843ae2cd129b24fabe411800302172b989")
    version("8.2.1", sha256="76ed3d0c3a348a6693dfae535e5658bbfd47f71cb7ff7eb96d9f12f7e068b1cf")
    version("8.2.0", sha256="de93df9a4aa88d09459ead791f2dbc874b897bf67a5bbb3e4b68de7b1bdef13c")
    version("8.1.1", sha256="82f1345e5fa530c407cb1fc0752e83f8d08d2b98772941bbdc7820241f7fada2")
    version("8.1.0", sha256="22c5cdc5aa0832077b16c95ebeec748a0942811c1c3438c33d43c8d2ead59f48")
    version("8.0.1", sha256="e0463a8068898785ca75dd49a261d3d28b07d0a88f3b657e8e0089e16a0375fa")
    version("8.0.0", sha256="aa5d4b934450149a350aed7e5fbac880e2f7d3fa2f251c26cb64228f96a2109e")
    version("7.2.1", sha256="b384f42e5fb9c6d01fe5fa4d31da2e91329668863a684f97be5d4760dbbf0a14")
    version("7.2.0", sha256="2957798e5fe295ff96a2af1889d0428e486363d210889422f76dd744f7885763")
    version("7.1.0", sha256="876151e2279346f6bdbc63bd59790b48733496a957bccd5e51b640fdd26eaa8d")
    version("7.0.1", sha256="a7026d39c9c80d51565cfc4b33d22631c11e491004e19020b3ff5a0791e1779f")
    version(
        "7.0.0",
        sha256="ee0e14c1bd2f9429b1a28999240304c0342ed739ebaea3d4ff44c585b1097be8",
        deprecated=True,
    )
    version("6.3.2", sha256="cb776a70f40c35579ae4ba04fb4a388c1d1ce025a1df6171350dc19f25b80311")
    version("6.3.1", sha256="6de0112778438dcae30fcc6942dee472ce31399b9e5a2b67e8642529868c86f8")
    version("6.2.0", sha256="b300c0f872f632ad7f8eb60725edbf14f0f8f52db740a3ab23e7b94f1cd22a50")
    version("6.1.0", sha256="676165c54319d2f03da4349cbd7344eb430b225fe867a90191d848dc64788008")
    version("6.0.0", sha256="4510a2c1c8f9056374708a867c51b1192e8d6f9a5198dd320bf6a168e44a3657")
    version("5.2.0", sha256="ef919499ffbc62a4aae2659a55e2b25ff09cccbbe230656ba71c6224056c7e60")
    version("5.1.0", sha256="6b1379a53317d9b5b8c723c1dc7bf2e3a8eb22ceb46b8807a1ce48ef65685bb3")
    version("5.0.1", sha256="a792f78897482ed2c4e2af4e8a1a02e294c64e32b591a635c5294cb9d49fdc8c")
    version("4.9.2", sha256="60bf9ad1ed1c18158e652dfff97865ba6fb2b67f1511bc8dceae4b3c7e657796")
    version("4.9.1", sha256="fca0388f3f8bc5a1a803d2f6ff30017532367992b30cf144f2d39be88f36c319")
    version(
        "4.8.0",
        sha256="2db2dbf0fece8d9880679154e0d6d1ce7c694dd8e08b4d091028093d87a9d1b5",
        deprecated=True,
    )
    version(
        "4.7.0",
        sha256="fc5440002a496532bfaf423c28bdfaf9e26cc96c84ccefcdefde911efbd98986",
        deprecated=True,
    )
    version(
        "4.6.1",
        sha256="76d174edd4fdb4c49c1c0ed8308a469216c01e7177a4510b1b303ef3c5f97b47",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("tiff", default=True, when="@7:", description="Enable TIFF support")
    variant("curl", default=True, when="@7:", description="Enable curl support")
    variant("shared", default=True, description="Enable shared libraries")
    variant("pic", default=False, description="Enable position-independent code (PIC)")

    # https://github.com/OSGeo/PROJ#distribution-files-and-format
    # https://github.com/OSGeo/PROJ-data
    resource(
        name="proj-data",
        url="https://download.osgeo.org/proj/proj-data-1.13.tar.gz",
        sha256="f1e5e42ba15426d01d1970be727af77ac9b88c472215497a5a433d0a16dd105b",
        placement=join_path("share", "proj"),
        when="@7:",
    )

    # https://github.com/OSGeo/PROJ#distribution-files-and-format
    # https://github.com/OSGeo/proj-datumgrid
    resource(
        name="proj-datumgrid",
        url="https://download.osgeo.org/proj/proj-datumgrid-1.8.tar.gz",
        sha256="3ff6618a0acc9f0b9b4f6a62e7ff0f7bf538fb4f74de47ad04da1317408fcc15",
        placement=join_path("share", "proj"),
        when="@:6",
    )

    patch(
        "https://github.com/OSGeo/PROJ/commit/3f38a67a354a3a1e5cca97793b9a43860c380d95.patch?full_index=1",
        sha256="dc620ff1bbcc0ef4130d53a40a8693a1e2e72ebf83bd6289f1139d0f1aad2a40",
        when="@6.2:9.1",
    )

    # https://proj.org/install.html#build-requirements
    with when("build_system=cmake"):
        # https://github.com/OSGeo/PROJ/pull/3374
        patch("proj-8-tiff.patch", when="@8:9.1")
        patch("proj-7-tiff.patch", when="@7")
        # https://github.com/spack/spack/pull/41065
        patch("proj.cmakelists.5.0.patch", when="@5.0")
        patch("proj.cmakelists.5.1.patch", when="@5.1:5.2")

        depends_on("cmake@3.16:", when="@9.4:", type="build")
        depends_on("cmake@3.9:", when="@6:", type="build")
        depends_on("cmake@3.5:", when="@5", type="build")
        depends_on("cmake@2.6:", when="@:4", type="build")

    with when("build_system=autotools"):
        depends_on("pkgconfig@0.9:", when="@6:", type="build")

    depends_on("sqlite@3.11:", when="@6:")
    depends_on("libtiff@4:", when="@7:+tiff")
    depends_on("curl@7.29:", when="@7:+curl")
    depends_on("googletest@1.8:", when="@6:", type="test")

    build_system(
        conditional("autotools", when="@:8"), conditional("cmake", when="@5:"), default="cmake"
    )

    def setup_run_environment(self, env):
        # PROJ_LIB doesn't need to be set. However, it may be set by conda.
        # If an incompatible version of PROJ is found in PROJ_LIB, it can
        # cause the package to fail at run-time. See the following for details:
        # * https://proj.org/usage/environmentvars.html
        # * https://rasterio.readthedocs.io/en/latest/faq.html
        env.set("PROJ_LIB", self.prefix.share.proj)


class BaseBuilder(metaclass=spack.builder.PhaseCallbacksMeta):
    def setup_build_environment(self, env):
        env.set("PROJ_LIB", join_path(self.pkg.stage.source_path, "nad"))

    @run_after("install")
    def install_datum_grids(self):
        install_tree(join_path("share", "proj"), self.prefix.share.proj)


class CMakeBuilder(BaseBuilder, cmake.CMakeBuilder):
    def cmake_args(self):
        shared_arg = "BUILD_SHARED_LIBS" if self.spec.satisfies("@7:") else "BUILD_LIBPROJ_SHARED"
        args = [
            self.define_from_variant("ENABLE_TIFF", "tiff"),
            self.define_from_variant("ENABLE_CURL", "curl"),
            self.define_from_variant(shared_arg, "shared"),
            # projsync needs curl
            self.define_from_variant("BUILD_PROJSYNC", "curl"),
            self.define_from_variant("CMAKE_POSITION_INDEPENDENT_CODE", "pic"),
        ]
        if self.spec.satisfies("@6:") and self.pkg.run_tests:
            args.append(self.define("USE_EXTERNAL_GTEST", True))
        if self.spec.satisfies("@7:"):
            test_flag = "BUILD_TESTING"
        elif self.spec.satisfies("@5.1:"):
            test_flag = "PROJ_TESTS"
        else:
            test_flag = "PROJ4_TESTS"
        args.append(self.define(test_flag, self.pkg.run_tests))
        return args


class AutotoolsBuilder(BaseBuilder, autotools.AutotoolsBuilder):
    def configure_args(self):
        args = []

        if self.spec.satisfies("@6:") and self.pkg.run_tests:
            args.append("--with-external-gtest")

        if self.spec.satisfies("@7:"):
            args.extend(self.enable_or_disable("tiff"))

            if "+curl" in self.spec:
                args.append("--with-curl=" + self.spec["curl"].prefix.bin.join("curl-config"))
            else:
                args.append("--without-curl")

        args.extend(self.enable_or_disable("shared"))
        args.extend(self.with_or_without("pic"))

        if self.spec.satisfies("^libtiff+jpeg~shared"):
            args.append("LDFLAGS=%s" % self.spec["jpeg"].libs.ld_flags)
            args.append("LIBS=%s" % self.spec["jpeg"].libs.link_flags)

        return args
