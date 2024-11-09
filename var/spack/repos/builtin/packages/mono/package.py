# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mono(AutotoolsPackage):
    """Mono is a software platform designed to allow developers to easily
    create cross platform applications. It is an open source
    implementation of Microsoft's .NET Framework based on the ECMA
    standards for C# and the Common Language Runtime.
    """

    homepage = "https://www.mono-project.com/"
    url = "https://download.mono-project.com/sources/mono/mono-5.0.1.1.tar.bz2"
    maintainers("grospelliergilles")

    # /usr/share/.mono/keypairs needs to exist or be able to be
    # created, e.g. https://github.com/gentoo/dotnet/issues/6
    variant(
        "patch-folder-path",
        default=False,
        description="Point SpecialFolder.CommonApplicationData folder "
        "into Spack installation instead of /usr/share",
    )

    depends_on("cmake", type=("build"))
    depends_on("iconv")
    depends_on("perl", type=("build"))
    depends_on("python", type=("build"))

    license("MIT")

    version(
        "6.12.0.122",
        sha256="29c277660fc5e7513107aee1cbf8c5057c9370a4cdfeda2fc781be6986d89d23",
        url="https://download.mono-project.com/sources/mono/mono-6.12.0.122.tar.xz",
    )
    version(
        "6.8.0.123",
        sha256="e2e42d36e19f083fc0d82f6c02f7db80611d69767112af353df2f279744a2ac5",
        url="https://download.mono-project.com/sources/mono/mono-6.8.0.123.tar.xz",
    )
    version(
        "6.8.0.105",
        sha256="578799c44c3c86a9eb5daf6dec6c60a24341940fd376371956d4a46cf8612178",
        url="https://download.mono-project.com/sources/mono/mono-6.8.0.105.tar.xz",
    )
    version(
        "5.18.0.240", sha256="143e80eb00519ff496742e78ee07403a3c3629437f3a498eee539de8108da895"
    )
    version(
        "5.16.0.220", sha256="f420867232b426c062fa182256a66b29efa92992c119847359cdd1ab75af8de3"
    )
    version(
        "5.14.0.177", sha256="d4f5fa2e8188d66fbc8054f4145711e45c1faa6d070e63600efab93d1d189498"
    )
    version(
        "5.12.0.309", sha256="7c4738c91187bfcea7b40f9e7a4bf3a0e4f54fdc0f4472612f84803e8bed368f"
    )
    version("5.10.1.57", sha256="76cbd8545db6adc5a1738c343d957a7015c95e1439c461ea4f2bd56bd6337ab4")
    version("5.4.1.7", sha256="543d9ec2ccebad9bb8425b22e10271f13d9512487c0e1578eeccdb1b8dc6a055")
    version("5.4.0.167", sha256="c2afe51b0fb074936a8e7eaee805c352f37cbf1093bb41c5345078f77d913ce0")
    version("5.0.1.1", sha256="48d6ae71d593cd01bf0f499de569359d45856cda325575e1bacb5fabaa7e9718")
    version("4.8.0.524", sha256="ca02614cfc9fe65e310631cd611d7b07d1ff205ce193006d4be0f9919c26bdcf")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    def patch(self):
        if "+patch-folder-path" in self.spec:
            before = 'return "/usr/share";'
            after = 'return "{0}";'.format(self.prefix.share)
            f = "mcs/class/corlib/System/Environment.cs"
            kwargs = {"ignore_absent": False, "backup": True, "string": True}
            filter_file(before, after, f, **kwargs)

    def configure_args(self):
        args = []
        if self.spec["iconv"].name == "libiconv":
            args.append(f"--with-libiconv-prefix={self.spec['iconv'].prefix}")
        else:
            args.append("--without-libiconv-prefix")
        return args
