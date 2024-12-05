# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class NfsGanesha(CMakePackage):
    """NFS-Ganesha is an NFSv3,v4,v4.1 fileserver that runs in user mode
    on most UNIX/Linux systems. It also supports the 9p.2000L protocol."""

    homepage = "https://github.com/nfs-ganesha/nfs-ganesha/wiki"
    url = "https://github.com/nfs-ganesha/nfs-ganesha/archive/V3.2.tar.gz"

    version("3.2", sha256="1e3635f0eb0bc32868ea7d923d061d0f6b1bd03b45da34356c7c53d4c0ebafbd")
    version("3.1", sha256="c4cf78929f39b8af44b05e813783b2c39e348b485043c6290c4bca705bb5015f")
    version("3.0.3", sha256="fcc0361b9a2752be7eb4e990230765e17de373452ac24514be22c81a5447a460")
    version("3.0", sha256="136c5642ff21ec6e8a4e77c037f6218a39b2eeba77798b13556f1abbb0923ccd")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("bison", type="build")
    depends_on("flex", type="build")
    depends_on("py-stsci-distutils", type="build")
    depends_on("userspace-rcu")
    depends_on("ntirpc")
    depends_on("krb5")

    root_cmakelists_dir = "src"

    def setup_build_environment(self, env):
        env.prepend_path("CPATH", self.spec["ntirpc"].prefix.include.ntirpc)
