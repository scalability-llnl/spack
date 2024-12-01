# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Cctools(AutotoolsPackage):
    """The Cooperative Computing Tools (cctools) enable large scale
    distributed computations to harness hundreds to thousands of
    machines from clusters, clouds, and grids.
    """

    homepage = "https://cctools.readthedocs.io"
    url = "https://ccl.cse.nd.edu/software/files/cctools-7.4.2-source.tar.gz"
    maintainers("dthain", "btovar")

    version("7.4.2", sha256="7c8c86f09bcb9ad23ab44e52dfb5bf3a4e4a1ad84ef51e500a9c8c2371770f4b")
    version("7.2.10", sha256="4a604329896ae5e0fad7451a3814f531ff2f00a41c96e971ac08276208aa1650")
    version("7.2.4", sha256="36d36465a14b503a27c4739ebe0e11e00970ef6abb07c0365a46670753dddbd0")
    version("7.2.3", sha256="c9d32f9e9d4886ef88b79cc7c898c26e8369a004132080697b8523560cb8765b")
    version("7.2.2", sha256="3eee05826954792e3ef974fefe3b8e436f09cd368b195287639b67f5acfa050f")
    version("7.2.1", sha256="8f847fef9bca1ebd23a93d74fc093807d2c3e584111c087cf25e070e130eb820")
    version("7.1.7", sha256="63cbfabe52591d41a1b27040bf27700d2a11b2f30cb2e25132e0016fb1aade03")
    version("7.1.5", sha256="c01415fd47a1d9626b6c556e0dc0a6b0d3cd67224fa060cabd44ff78eede1d8a")
    version("7.1.3", sha256="b937878ab429dda31bc692e5d9ffb402b9eb44bb674c07a934bb769cee4165ba")
    version("7.1.2", sha256="ca871e9fe245d047d4c701271cf2b868e6e3a170e8834c1887157ed855985131")
    version("7.1.0", sha256="84748245db10ff26c0c0a7b9fd3ec20fbbb849dd4aadc5e8531fd1671abe7a81")
    version("7.0.18", sha256="5b6f3c87ae68dd247534a5c073eb68cb1a60176a7f04d82699fbc05e649a91c2")
    version("6.1.1", sha256="97f073350c970d6157f80891b3bf6d4f3eedb5f031fea386dc33e22f22b8af9d")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("openssl")
    depends_on("perl+shared", type=("build", "run"))
    depends_on("python", type=("build", "run"))
    depends_on("readline")
    depends_on("gettext")  # Corrects python linking of -lintl flag.
    depends_on("swig")
    # depends_on('xrootd')
    depends_on("zlib-api")
    patch("arm.patch", when="target=aarch64:")
    patch("cctools_7.0.18.python.patch", when="@7.0.18")
    patch("cctools_6.1.1.python.patch", when="@6.1.1")

    # Generally SYS_foo is defined to __NR_foo (sys/syscall.h) which
    # is then defined to a syscall number (asm/unistd_64.h).  Certain
    # CentOS systems have SYS_memfd_create defined to
    # __NR_memfd_create but are missing the second definition.
    # This is a belt and suspenders solution to the problem.
    def patch(self):
        before = "#if defined(__linux__) && defined(SYS_memfd_create)"
        after = "#if defined(__linux__) && defined(SYS_memfd_create) && defined(__NR_memfd_create)"
        f = "dttools/src/memfdexe.c"
        kwargs = {"ignore_absent": False, "backup": True, "string": True}
        filter_file(before, after, f, **kwargs)
        if self.spec.satisfies("%fj"):
            makefiles = ["chirp/src/Makefile", "grow/src/Makefile"]
            for m in makefiles:
                filter_file("-fstack-protector-all", "", m)

        # Remove two troublesome test cases:

        # TR_parrot_dir.sh fails b/c of variations in how Linux kernels
        # deal with open() on directories.
        os.unlink("parrot/test/TR_parrot_dir.sh")

        # TR_parrot_execve.sh fails b/c of the complexities of moving
        # a python interpreter around.
        os.unlink("parrot/test/TR_parrot_execve.sh")

    def configure_args(self):
        args = []

        # make sure we do not pick a python outside spack:
        if self.spec.satisfies("@6.1.1"):
            args.extend(
                ["--with-python3-path", self.spec["python"].prefix, "--with-python-path", "no"]
            )
        else:
            # versions 7 and above, where --with-python-path recognized the
            # python version:
            args.extend(
                ["--with-python-path", self.spec["python"].prefix, "--with-python2-path", "no"]
            )

        # disable these bits
        for p in ["mysql", "xrootd"]:
            args.append("--with-{0}-path=no".format(p))

        # point these bits at the Spack installations
        for p in ["openssl", "perl", "readline", "swig"]:
            args.append("--with-{0}-path={1}".format(p, self.spec[p].prefix))

        args.append("--with-zlib-path={0}".format(self.spec["zlib-api"].prefix))

        return args
