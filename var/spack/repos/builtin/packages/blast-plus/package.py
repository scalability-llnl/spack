# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class BlastPlus(AutotoolsPackage):
    """Basic Local Alignment Search Tool."""

    homepage = "https://blast.ncbi.nlm.nih.gov/"
    url = "https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.13.0/ncbi-blast-2.13.0+-src.tar.gz"

    maintainers("weijianwen")

    version("2.16.0", sha256="17c93cf009721023e5aecf5753f9c6a255d157561638b91b3ad7276fd6950c2b")
    version("2.15.0", sha256="6918c370524c8d44e028bf491e8f245a895e07c66c77b261ce3b38d6058216e0")
    version("2.14.1", sha256="712c2dbdf0fb13cc1c2d4f4ef5dd1ce4b06c3b57e96dfea8f23e6e99f5b1650e")
    version("2.13.0", sha256="89553714d133daf28c477f83d333794b3c62e4148408c072a1b4620e5ec4feb2")
    version("2.12.0", sha256="fda3c9c9d488cad6c1880a98a236d842bcf3610e3e702af61f7a48cf0a714b88")
    version("2.11.0", sha256="d88e1858ae7ce553545a795a2120e657a799a6d334f2a07ef0330cc3e74e1954")
    version("2.9.0", sha256="a390cc2d7a09422759fc178db84de9def822cbe485916bbb2ec0d215dacdc257")
    version("2.8.1", sha256="e03dd1a30e37cb8a859d3788a452c5d70ee1f9102d1ee0f93b2fbd145925118f")
    version("2.7.1", sha256="10a78d3007413a6d4c983d2acbf03ef84b622b82bd9a59c6bd9fbdde9d0298ca")
    version("2.6.0", sha256="0510e1d607d0fb4389eca50d434d5a0be787423b6850b3a4f315abc2ef19c996")
    version("2.2.30", sha256="26f72d51c81b9497f33b7274109565c36692572faef4d72377f79b7e59910e40")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # homebrew sez: Fixed upstream in future version > 2.6
    # But this bug sez that it will be fixed in 2.6
    #    https://github.com/Homebrew/homebrew-science/pull/4740
    # The 2.6.0 src still matches the "before" bit of the patch
    # so it's probably still "needed".
    # On the other hand, the `find` command is broken and there
    # aren't any .svn dirs in the tree, so I've updated their patch
    # to just comment out the block.
    patch("blast-make-fix2.5.0.diff", when="@2.5.0:2.6.0")

    # See https://github.com/Homebrew/homebrew-science/issues/2337#issuecomment-170011511
    @when("@:2.2.31")
    def patch(self):
        filter_file(
            "2.95* | 2.96* | 3.* | 4.* )",
            "2.95* | 2.96* | 3.* | 4.* | 5.* )",
            "c++/src/build-system/configure",
            string=True,
        )

    # No...
    # depends_on :mysql => :optional

    depends_on("cpio", type="build")

    variant("static", default=False, description="Build with static linkage")
    variant("jpeg", default=True, description="Build with jpeg support")
    variant("png", default=True, description="Build with png support")
    variant("freetype", default=True, description="Build with freetype support")
    # variant('hdf5', default=True,
    #        description='Build with hdf5 support')
    variant("gnutls", default=True, description="Build with gnutls support")
    variant("openssl", default=True, description="Build with openssl support")
    variant("zlib", default=True, description="Build with zlib support")
    variant("bzip2", default=True, description="Build with bzip2 support")
    variant("lzo", default=True, description="Build with lzo support")
    variant("pcre", default=True, description="Build with pcre support")
    variant("perl", default=True, description="Build with perl support")
    variant("python", default=True, description="Build with python support")

    depends_on("jpeg", when="+jpeg")
    depends_on("libpng", when="+png")
    depends_on("freetype", when="+freetype")
    # depends_on('hdf5', when='+hdf5')
    depends_on("gnutls", when="+gnutls")
    depends_on("openssl", when="+openssl")
    depends_on("zlib-api", when="+zlib")
    depends_on("bzip2", when="+bzip2")
    depends_on("lzo", when="+lzo")
    depends_on("pcre", when="+pcre")

    depends_on("python", when="+python")
    depends_on("perl", when="+perl")

    depends_on("lmdb", when="@2.7.1:")

    configure_directory = "c++"

    def configure_args(self):
        spec = self.spec

        config_args = ["--with-bin-release", "--without-debug", "--with-mt", "--without-boost"]

        if spec.target.family != "aarch64":
            config_args.append("--with-64")
        if spec.satisfies("+static"):
            config_args.append("--with-static")
            # FIXME
            # args << "--with-static-exe" unless OS.linux?
            # args << "--with-dll" if build.with? "dll"
        else:
            config_args.extend(["--with-dll", "--without-static", "--without-static-exe"])

        if spec.satisfies("+jpeg"):
            config_args.append("--with-jpeg={0}".format(self.spec["jpeg"].prefix))
        else:
            config_args.append("--without-jpeg")

        if spec.satisfies("+png"):
            config_args.append("--with-png={0}".format(self.spec["libpng"].prefix))
        else:
            config_args.append("--without-png")

        if spec.satisfies("+freetype"):
            config_args.append("--with-freetype={0}".format(self.spec["freetype"].prefix))
        else:
            config_args.append("--without-freetype")

        config_args.append("--without-hdf5")
        # if '+hdf5' in spec:
        #     # FIXME
        #     config_args.append(
        #         '--with-hdf5={0}'.format(self.spec['hdf5'].prefix)
        #     )
        # else:
        #     config_args.append('--without-hdf5')

        if spec.satisfies("+zlib"):
            config_args.append("--with-z={0}".format(self.spec["zlib-api"].prefix))
        else:
            config_args.append("--without-z")

        if spec.satisfies("+bzip2"):
            config_args.append("--with-bz2={0}".format(self.spec["bzip2"].prefix))
        else:
            config_args.append("--without-bz2")

        if spec.satisfies("+lzo"):
            config_args.append("--with-lzo={0}".format(self.spec["lzo"].prefix))
        else:
            config_args.append("--without-lzo")

        if spec.satisfies("+gnutls"):
            config_args.append("--with-gnutls={0}".format(self.spec["gnutls"].prefix))
        else:
            config_args.append("--without-gnutls")

        if spec.satisfies("+openssl"):
            config_args.append("--with-openssl={0}".format(self.spec["openssl"].prefix))
        else:
            config_args.append("--without-openssl")

        if spec.satisfies("+pcre"):
            config_args.append("--with-pcre={0}".format(self.spec["pcre"].prefix))
        else:
            config_args.append("--without-pcre")

        if spec.satisfies("+python"):
            config_args.append("--with-python={0}".format(self.spec["python"].home))
        else:
            config_args.append("--without-python")

        if spec.satisfies("+perl"):
            config_args.append("--with-perl={0}".format(self.spec["perl"].prefix))
        else:
            config_args.append("--without-python")

        return config_args
