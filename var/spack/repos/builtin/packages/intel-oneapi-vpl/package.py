# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


@IntelOneApiPackage.update_description
class IntelOneapiVpl(IntelOneApiLibraryPackage):
    """The Intel oneAPI Video Processing Library (oneVPL) is the successor
    to Intel Media SDK. This library takes you from abstractions for
    integrated graphics to using oneVPL to unlock media features on a
    much broader range of accelerators.  oneVPL provides a single,
    video-focused API for encoding, decoding, and video processing
    that works across a wide range of accelerators. The library is
    perfect for applications spanning broadcasting, streaming, video
    on demand (VOD), in-cloud gaming, and remote desktop solutions.

    """

    maintainers("rscohn2")

    homepage = (
        "https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/onevpl.html"
    )

    version(
        "2023.1.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/e2f5aca0-c787-4e1d-a233-92a6b3c0c3f2/l_oneVPL_p_2023.1.0.43488_offline.sh",
        sha256="8cc6aa0464dc962def9f96e1f766b6d21745391398626121feeca132f34261be",
        expand=False,
    )
    version(
        "2023.0.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/19134/l_oneVPL_p_2023.0.0.25332_offline.sh",
        sha256="69e42fc7f412271c92395412a693bd158ef6df1472b3e0e783a63fddfc44c5af",
        expand=False,
    )
    version(
        "2022.2.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18903/l_oneVPL_p_2022.2.0.8703_offline.sh",
        sha256="cb8af222d194ebb4b1dafe12e0b70cbbdee204f9fcfe9eafb46b287ee33b3797",
        expand=False,
    )
    version(
        "2022.1.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18750/l_oneVPL_p_2022.1.0.154_offline.sh",
        sha256="486cca918c9772a43f62da77e07cdf54dabb92ecebf494eb8c89c4492ab43447",
        expand=False,
    )
    version(
        "2022.0.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18375/l_oneVPL_p_2022.0.0.58_offline.sh",
        sha256="600b8566e1aa523b97291bed6b08f69a04bc7c4c75c035942a64a38f45a1a7f0",
        expand=False,
    )
    version(
        "2021.6.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18190/l_oneVPL_p_2021.6.0.458_offline.sh",
        sha256="40c50008be3f03d17cc8c0c34324593c1d419ee4c45af5543aa5a2d5fb11071f",
        expand=False,
    )
    version(
        "2021.2.2",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/17733/l_oneVPL_p_2021.2.2.212_offline.sh",
        sha256="21106ba5cde22f3e31fd55280fbccf263508fa054030f12d5dff4a5379ef3bb7",
        expand=False,
    )
    version(
        "2021.1.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/17418/l_oneVPL_p_2021.1.1.66_offline.sh",
        sha256="0fec42545b30b7bb2e4e33deb12ab27a02900f5703153d9601673a8ce43082ed",
        expand=False,
    )

    # VPL no longer releases as part of oneapi, so there will never be
    # a 2024 release
    @property
    def v2_layout_versions(self):
        return "@2024:"

    @property
    def component_dir(self):
        return "vpl"
