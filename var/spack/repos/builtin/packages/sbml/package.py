# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sbml(CMakePackage):
    """Library for the Systems Biology Markup Language"""

    homepage = "https://sbml.org"
    maintainers("rblake-llnl")

    license("LGPL-2.1-or-later")

    version("5.18.0", sha256="6c01be2306ec0c9656b59cb082eb7b90176c39506dd0f912b02e08298a553360")
    version("5.17.0", sha256="189216e1472777e4464b791c506b79267d07a5454cb23ac991452711f8e0ed3a")
    version("5.16.0", sha256="c6855481434dd2a667fef73e1ff2feade509aa2f3a76d4d06e29022975ce1496")
    version("5.15.0", sha256="c779c2a8a97c5480fe044028099d928a327261fb68cf08657ec8d4f3b3fc0a21")
    version("5.13.0", sha256="e58430edb1b454d7414bcf1be0549bf6860a6d19d73232eb58211559485c2c05")
    version("5.12.0", sha256="c637494b19269947fc90ebe479b624d36f80d1cb5569e45cd76ddde81dd28ae4")
    version("5.11.4", sha256="6429188b689b331b0b8f2c8b55b3f2339196ccd4c93191648fa767e1d02152a3")
    version("5.11.0", sha256="b21931ca7461494915c617b30d4a9f2cafe831d6ce74989b3e5874e6e3c3f72b")
    version("5.10.2", sha256="83f32a143cf657672b1050f5f79d3591c418fc59570d180fb1f39b103f4e5286")
    version("5.10.0", sha256="2cd8b37018ce8b1df869c8c182803addbce6d451512ae25a7f527b49981f0966")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    def url_for_version(self, version):
        url = "https://downloads.sourceforge.net/project/sbml/libsbml/{0}/stable/libSBML-{1}-core-plus-packages-src.tar.gz".format(
            version, version
        )
        return url

    variant("python", default=False, description="Build with python support")
    depends_on("python", when="+python")

    variant("perl", default=False, description="Build with perl support")
    depends_on("perl", when="+perl")

    variant("ruby", default=False, description="Build with ruby support")
    depends_on("ruby", when="+ruby")

    variant("r", default=False, description="Build with R support")
    depends_on("r", when="+r")

    variant("octave", default=False, description="Build with octave support")
    depends_on("octave", when="+octave")

    variant("matlab", default=False, description="Build with matlab support")
    depends_on("matlab", when="+matlab")

    variant("java", default=False, description="Build with java support")
    depends_on("java", when="+java")

    variant("mono", default=False, description="Build with mono support")
    depends_on("mono", when="+mono")

    variant("cpp", default=False, description="All c++ includes should be under a namespace")

    depends_on("swig@2:", type="build")
    depends_on("cmake", type="build")
    depends_on("zlib-api")
    depends_on("bzip2")
    depends_on("libxml2")

    def cmake_args(self):
        spec = self.spec
        args = [
            "-DENABLE_COMP:BOOL=ON",
            "-DENABLE_FBC:BOOL=ON",
            "-DENABLE_GROUPS:BOOL=ON",
            "-DENABLE_LAYOUT:BOOL=ON",
            "-DENABLE_QUAL:BOOL=ON",
            "-DENABLE_RENDER:BOOL=ON",
            "-DWITH_BZIP2:BOOL=ON",
            "-DWITH_CHECK:BOOL=OFF",
            "-DWITH_DOXYGEN:BOOL=OFF",
            "-DWITH_EXAMPLES:BOOL=OFF",
            "-DWITH_EXPAT:BOOL=OFF",
            "-DWITH_LIBXML:BOOL=ON",
            "-DWITH_SWIG:BOOL=ON",
            "-DWITH_WALL:BOOL=ON",
            "-DWITH_XERCES:BOOL=OFF",
            "-DWITH_ZLIB:BOOL=ON",
        ]
        args.append(self.define_from_variant("WITH_CPP_NAMESPACE", "cpp"))
        if "+python" in spec:
            args.extend(
                ["-DWITH_PYTHON:BOOL=ON", "-DWITH_PYTHON_INCLUDE:PATH=%s" % spec["python"].prefix]
            )
        else:
            args.append("-DWITH_PYTHON:BOOL=OFF")

        args.append(self.define_from_variant("WITH_CSHARP", "mono"))

        if "+java" in spec:
            args.extend(
                [
                    "-DWITH_JAVA:BOOL=ON",
                    "-DJDK_PATH:STRING=%s" % spec["java"].prefix,
                    "-DJAVA_INCLUDE_PATH:STRING=%s" % spec["java"].prefix,
                ]
            )
        else:
            args.append("-DWITH_JAVA:BOOL=OFF")

        if "+matlab" in spec:
            args.extend(
                [
                    "-DWITH_MATLAB:BOOL=ON",
                    "-DMATLAB_ROOT_PATH:PATH=%s" % spec["matlab"].prefix,
                    "-DWITH_MATLAB_MEX:BOOL=ON",
                ]
            )
        else:
            args.append("-DWITH_MATLAB:BOOL=OFF")

        args.append(self.define_from_variant("WITH_OCTAVE", "octave"))
        args.append(self.define_from_variant("WITH_PERL", "perl"))
        args.append(self.define_from_variant("WITH_R", "r"))
        args.append(self.define_from_variant("WITH_RUBY", "ruby"))

        return args
