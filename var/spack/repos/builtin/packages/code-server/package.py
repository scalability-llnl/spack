# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class CodeServer(Package):
    """code-server is VS Code running on a remote server,
    accessible through the browser."""

    homepage = "https://coder.com/docs/code-server/latest"
    url = "https://github.com/coder/code-server/releases/download/v4.4.0/code-server-4.4.0-linux-amd64.tar.gz"

    version("4.12.0", sha256="d50ee947c4144a6ff2656e664ecbb3f70b75168b8a6e8c3eef47787f3c240c26")
    version("4.11.0", sha256="4eb233054941ec298caec6fc84dfba0a72c1bc5fadc0fe4896b10f3f4a291d51")
    version("4.10.1", sha256="f34ce611a9c058982a5e9d200fdf009788e3a564e970b053f4145574bce21b09")
    version("4.4.0", sha256="e3dd265acb18c2230c72d19bbce619ac5c1bd800ebb26e5e169c4d613069500d")
    version("4.3.0", sha256="42c71e98de85270b164b023ef8eb0692cf7700c03081ba5a44eaca014a92eb57")
    version("4.2.0", sha256="98be5bc43ac604c49ae11da259e318b581757a59a25edeee5cf55317ca589ec6")
    version("4.1.0", sha256="f720b20d1f615b78f3a1be9b1614f3d99ed722b8da3047a4143dbe5835e52ce3")
    version("4.0.2", sha256="68c11afa3288707a6880920013d8bac7404cd590eb4f63cac92979d0b0bf4fd1")
    version("4.0.1", sha256="5fe6d26e9d19e685946f0f392d9c822e5303a800cac3ac54a6a2c26104d239fd")
    version("3.12.0", sha256="d3ca41a55e36d73d80300702af2687e25d440cff6b613bb58a2c88d9b8a0a38f")
    version("3.11.1", sha256="d34b0b79582196d59d44ac971aabb7f15cb05d837318b94f62470dc8475665e9")
    version("3.11.0", sha256="dddb97f044ed615a4b8a526328fca6ad703b9c671a28a6090d84668a18755589")
    version("3.10.2", sha256="47154a6b9e61a0313ba499dd5d948613a17841c2f580612f9721c31964622bf5")
    version("3.10.1", sha256="18175624df78976488dbcc2a26f2582a71cef5ca0a419e691b1b70da0b27c7ef")
    version("3.10.0", sha256="5dfce848747f3dd5074cba435cca6730ac99d6d3aa3f50e0a9bf222ad12d3e97")
    version("3.9.3", sha256="eba42eaf868c2144795b1ac54929e3b252ae35403bf8553b3412a5ac4f365a41")
    version("3.9.2", sha256="5dbda5ac598223006f72bcb700b133a752aabe4468ed8105806d1d69b5364408")
    version("3.9.1", sha256="f2648a4387c5a5be8666fb82a7b8a58274c45b91942251ab337e202e078ae8a5")
    version("3.9.0", sha256="229b0fb95d78a7f7ff0dd55bc151a7521fcd699af50151faf67f6c7ce51110f4")
    version("3.8.1", sha256="130cf94e3921d0e2adfa33e875bf1aa81fd28548aac94fd31fbc589baa68d45f")
    version("3.8.0", sha256="70b069f26b30c38cca5fa07b5f25db4d15976de80af3a644b9105d1b5e23e7d5")
    version("3.7.4", sha256="01ca0e48df44df70cdf702644b013102024a5b30edf6c1fbb2e10b0310056382")
    version("3.7.3", sha256="7a90f3171c9bc6f65266066e35cc34d48a032910c136ea21116d28f3d7214547")
    version("3.7.2", sha256="c3054f214392b1b2eb4c77c57cb950ac5d733d349a426975e8bf32028e65a226")
    version("3.7.1", sha256="bebd9e0c46e0fd4b4f295fd91fc2db135a694614db972095e9842bf7969f4cee")
    version("3.7.0", sha256="5f8df8ed3924e8e594674d73fb50b00a06efa529f96a0495a5ee8c39c68f3ce1")
    version("3.6.2", sha256="fd4ac7d61f3e1b2a5034f1706e409c77fad299adef0ede204828d8ecfe317e45")
    version("3.6.1", sha256="bbe4ef9585e093b3521deb34a0820d2136172271862d6396df21c2e9a26c6374")
    version("3.6.0", sha256="d1ae4f7263741e0551358d3ed77dad587b33b352d827623d4df25e98f9e21019")
    version("3.5.0", sha256="90c19c84611becac4af1fb0bd5324ab30f9200769fa7914cd10ccb6b88c657bb")
    version("3.4.1", sha256="afdb89f4dc7201c03cb35d4f8dc1ccb6060bd0da324a6789089de264d3406817")
    version("3.4.0", sha256="918c28696b73b96dc9361977f93e788d5c8884b5d4a088d206f05d5b8bccb738")
    version("3.3.1", sha256="57b9855b20f511e22776ee8a53d1ff30f864498814c4c0b0af3510f71d7a2969")
    version("3.3.0", sha256="6ca5148a447b41753d5151c5a49a8af24122c7b0808609782aec454e66be4f2c")
    version("3.2.0", sha256="a8157e8766d6a0e255c72db25e8677a57adb8d889d653e78750b4d26a6ff7400")
    version("3.1.1", sha256="5dd922d28b2e351c146081849d987fb1e439ee7d53b941434b2eecb2a194da71")
    version("3.1.0", sha256="5ef85c8f280ce781a176a8b77386b333efe892755a5c325a1782e4eac6016e59")
    version("3.0.2", sha256="04367cfeb23991f3dc3f1ef8e3dfe5e9d683bb50c9e1fa69e3c21757facfd7ee")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    def url_for_version(self, version):
        if version <= Version("3.2.0"):
            return "https://github.com/coder/code-server/releases/download/{0}/code-server-{0}-linux-x86_64.tar.gz".format(
                version
            )
        else:
            return "https://github.com/coder/code-server/releases/download/v{0}/code-server-{0}-linux-amd64.tar.gz".format(
                version
            )

    def install(self, spec, prefix):
        install_tree(".", prefix)

        if spec.version <= Version("3.1.1"):
            mkdir(prefix.bin)
            symlink("{0}/code-server".format(prefix), prefix.bin)
