# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Opari2(AutotoolsPackage):
    """OPARI2 is a source-to-source instrumentation tool for OpenMP and hybrid
    codes. It surrounds OpenMP directives and runtime library calls with calls
    to the POMP2 measurement interface. OPARI2 will provide you with a new
    initialization method that allows for multi-directory and parallel builds
    as well as the usage of pre-instrumented libraries. Furthermore, an
    efficient way of tracking parent-child relationships was added.
    Additionally, we extended OPARI2 to support instrumentation of OpenMP 3.0
    tied tasks.
    """

    homepage = "https://www.vi-hps.org/projects/score-p"
    url = "https://perftools.pages.jsc.fz-juelich.de/cicd/opari2/tags/opari2-2.0.8/opari2-2.0.8.tar.gz"

    version("2.0.8", sha256="196e59a2a625e6c795a6124c61e784bad142f9f38df0b4fa4d435ba9b9c19721")
    version("2.0.7", sha256="e302a4cc265eb2a4aa27c16a90eabd9e1e58cb02a191dd1c4d86f9a0df128715")
    version("2.0.6", sha256="55972289ce66080bb48622110c3189a36e88a12917635f049b37685b9d3bbcb0")
    version("2.0.5", sha256="9034dd7596ac2176401090fd5ced45d0ab9a9404444ff767f093ccce68114ef5")
    version("2.0.4", sha256="f69e324792f66780b473daf2b3c81f58ee8188adc72b6fe0dacf43d4c1a0a131")
    version("2.0.3", sha256="7e2efcfbc99152ee6e31454ef4fb747f77165691539d5d2c1df2abc4612de86c")
    version("2.0.1", sha256="f49d74d7533f428a4701cd561eba8a69f60615332e81b66f01ef1c9b7ee54666")
    version("2.0", sha256="0c4e575be05627cd001d692204f10caef37b2f3d1ec825f98cbe1bfa4232b0b7")
    version("1.1.4", sha256="b80c04fe876faaa4ee9a0654486ecbeba516b27fc14a90d20c6384e81060cffe")
    version("1.1.2", sha256="8405c2903730d94c828724b3a5f8889653553fb8567045a6c54ac0816237835d")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    def url_for_version(self, version):
        if version >= Version("2.0.6"):
            url = "https://perftools.pages.jsc.fz-juelich.de/cicd/opari2/tags/opari2-{0}/opari2-{0}.tar.gz"
        else:
            url = "https://www.vi-hps.org/cms/upload/packages/opari2/opari2-{0}.tar.gz"

        return url.format(version)

    def configure_args(self):
        return ["--enable-shared"]
