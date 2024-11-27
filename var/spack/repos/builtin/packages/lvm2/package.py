# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Lvm2(AutotoolsPackage, SourcewarePackage):
    """LVM2 is the userspace toolset that provides logical volume
    management facilities on linux.

    To use it you need 3 things: device-mapper in your kernel, the userspace
    device-mapper support library (libdevmapper) and the userspace LVM2 tools
    (dmsetup). These userspace components, and associated header files, are
    provided by this package.

    See http://sources.redhat.com/dm/ for additional information
    about the device-mapper kernel and userspace components.
    """

    homepage = "https://www.sourceware.org/lvm2"
    sourceware_mirror_path = "lvm2/LVM2.2.03.14.tgz"

    license("GPL-2.0-or-later AND LGPL-2.1-or-later AND BSD-2-Clause")

    version("2.03.14", sha256="4a63bc8a084a8ae3c7bc5e6530cac264139d218575c64416c8b99e3fe039a05c")
    version("2.03.05", sha256="ca52815c999b20c6d25e3192f142f081b93d01f07b9d787e99664b169dba2700")
    version("2.03.04", sha256="f151f36fc0039997d2d9369b607b9262568b1a268afe19fd1535807355402142")
    version("2.03.03", sha256="cedefa63ec5ae1b62fedbfddfc30706c095be0fc7c6aaed6fd1c50bc8c840dde")
    version("2.03.02", sha256="550ba750239fd75b7e52c9877565cabffef506bbf6d7f6f17b9700dee56c720f")
    version("2.03.01", sha256="424e58b074195ec08e0315fa1aff2550590998c33aea5c43bdceb8c1d135530b")
    version("2.03.00", sha256="405992bf76960e60c7219d84d5f1e22edc34422a1ea812e21b2ac3c813d0da4e")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    def url_for_version(self, version):
        url = "https://sourceware.org/pub/lvm2/releases/LVM2.{0}.tgz"
        return url.format(version)

    variant("pkgconfig", default=True, description="install pkgconfig support")

    depends_on("libaio")
    depends_on("pkgconfig", type="build", when="+pkgconfig")

    conflicts("platform=darwin", msg="lvm2 depends on libaio which does not support Darwin")

    def configure_args(self):
        return [
            "--with-confdir={0}".format(self.prefix.etc),
            "--with-default-system-dir={0}".format(self.prefix.etc.lvm),
        ] + self.enable_or_disable("pkgconfig")
