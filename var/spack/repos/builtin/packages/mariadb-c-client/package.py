# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class MariadbCClient(CMakePackage):
    """MariaDB turns data into structured information in a wide array of
    applications, ranging from banking to websites. It is an enhanced,
    drop-in replacement for MySQL. MariaDB is used because it is fast,
    scalable and robust, with a rich ecosystem of storage engines,
    plugins and many other tools make it very versatile for a wide
    variety of use cases. This package comprises only the standalone 'C
    Connector', which enables connections to MariaDB and MySQL servers.
    """

    homepage = "https://mariadb.org/about/"

    url = "https://downloads.mariadb.com/Connectors/c/connector-c-3.0.3/mariadb-connector-c-3.0.3-src.tar.gz"
    list_url = "https://downloads.mariadb.com/Connectors/c/"
    list_depth = 1

    license("LGPL-2.1-or-later")

    version("3.3.8", sha256="f9f076b4aa9fb22cc94b24f82c80f9ef063805ecd6533a2eb5d5060cf93833e8")
    version("3.3.7", sha256="975a9a862fed80f84e0206373f7ef05537aada5b65d99b71b36ab892b44240bf")
    version("3.3.5", sha256="ca72eb26f6db2befa77e48ff966f71bcd3cb44b33bd8bbb810b65e6d011c1e5c")
    version("3.3.4", sha256="486e5fdf976a8e7fadf583ae912128655e013ac575fa79b2d1af0fb8827a78ed")
    version("3.3.2", sha256="7e0722e07d30bb906fac9fe10fb582cde1e148e05a83d9ca7b6fcc884b68fbce")
    version("3.2.7", sha256="9d7196248e6697c09c73e173fe9b282045f55ec9d7ae743c1ebad08b9ea56dda")
    version("3.2.6", sha256="9c22fff9d18db7ebdcb63979882fb6b68d2036cf2eb62f043eac922cd36bdb91")
    version("3.1.18", sha256="b01ecacf7531c2f36d90708845488e66462bf63627c58cb5986bd1c0833e4d9c")
    version("3.1.13", sha256="0271a5edfd64b13bca5937267474e4747d832ec62e169fc2589d2ead63746875")
    version("3.1.9", sha256="108d99bf2add434dcb3bd9526ba1d89a2b9a943b62dcd9d0a41fcbef8ffbf2c7")
    version("3.1.6", sha256="d266bb67df83c088c4fb05392713d2504c67be620894cedaf758a9561c116720")
    version("3.1.5", sha256="a9de5fedd1a7805c86e23be49b9ceb79a86b090ad560d51495d7ba5952a9d9d5")
    version("3.1.4", sha256="7a1a72fee00e4c28060f96c3efbbf38aabcbbab17903e82fce85a85002565316")
    version("3.0.10", sha256="bd9aa1f137ead3dc68ed3165adc53541712076d08949800b6ccebd33da6d0ae8")
    version("3.0.9", sha256="7277c0caba6f50b1d07e1d682baf0b962a63e2e6af9e00e09b8dcf36a7858641")
    version("3.0.8", sha256="2ca368fd79e87e80497a5c9fd18922d8316af8584d87cecb35bd5897cb1efd05")
    version("3.0.7", sha256="f63883c9360675d111646fba5c97feb0d08e0def5873dd189d78bafbb75fa004")
    version("3.0.6", sha256="2b2d18dc969dc385f7f740e4db112300e11bc626c9ba9aa05c284704095b9e48")
    version("3.0.5", sha256="940017f13a13846153eb9d36290824c4615c8a8be4142b6bbaeb698609f02667")
    version("3.0.4", sha256="6eff680cd429fdb32940f6ea4755a997dda1bb00f142f439071f752fd0b200cf")
    version("3.0.3", sha256="210f0ee3414b235d3db8e98e9e5a0a98381ecf771e67ca4a688036368984eeea")
    version("3.0.2", sha256="518d14b8d77838370767d73f9bf1674f46232e1a2a34d4195bd38f52a3033758")
    version("2.3.7", sha256="94f9582da738809ae1d9f1813185165ec7c8caf9195bdd04e511f6bdcb883f8e")
    version("2.3.6", sha256="6b271d25dddda15f1c2328eee64f646a2e8b116ea21b04ece24b5a70712c3e96")
    version("2.3.5", sha256="2f3bf4c326d74284debf7099f30cf3615f7978d1ec22b8c1083676688a76746f")
    version("2.3.4", sha256="8beb0513da8a24ed2cb47836564c8b57045c3b36f933362f74b3676567c13abc")
    version("2.3.3", sha256="82a5710134e7654b9cad58964d6a25ed91b3dc1804ff51e8be2def0032914089")
    version("2.3.2", sha256="4063c8655dc37608d4eade981e25b76f67f5d36e8426dc7f20d59e48ebba628a")
    version("2.3.1", sha256="6ab7e1477ae1484939675a3b499f98148980a0bd340d15d22df00a5c6656c633")
    version("2.3.0", sha256="37faae901ca77bd48d2c6286f2e19e8c1abe7cac6fb1b128bd556617f4335c8a")
    version("2.2.3", sha256="cd01ce2c418382f90fd0b21c3c756b89643880efe3447507bf740569b9d08eed")
    version("2.2.2", sha256="93f56ad9f08bbaf0da8ef03bc96f7093c426ae40dede60575d485e1b99e6406b")
    version("2.2.1", sha256="c30ba19be03a6ac8688ef7620aed0eabdf34ca9ee886c017c56b013b5f8ee06a")
    version("2.2.0", sha256="3825b068d38bc19d6ad1eaecdd74bcd49d6ddd9d00559fb150e4e851a55bbbd4")
    version("2.1.0", sha256="568050b89463af7610d458669fd9eee06dcc9405689aca8a526ac8c013b59167")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    provides("mariadb-client")
    provides("mysql-client")

    depends_on("cmake@2.6:", type="build")
    depends_on("curl")
    depends_on("pcre")
    depends_on("openssl")
    depends_on("zlib-api")
    depends_on("krb5")

    # patch needed for cmake-3.20
    patch(
        "https://github.com/mariadb-corporation/mariadb-connector-c/commit/242cab8c.patch?full_index=1",
        sha256="760fd19cd8d4d756a0799ed9110cfd2898237e43835fefe3668079c5b87fc36d",
        when="@:3.1.12",
    )

    def url_for_version(self, version):
        url = "https://downloads.mariadb.com/Connectors/c/connector-c-{0}/mariadb-connector-c-{1}-src.tar.gz"
        return url.format(version.up_to(3), version)

    def cmake_args(self):
        args = ["-DWITH_EXTERNAL_ZLIB=ON", "-DWITH_MYSQLCOMPAT=ON"]
        return args

    @property
    def libs(self):
        return find_libraries(["libmariadb"], root=self.prefix, recursive=True, shared=True)
