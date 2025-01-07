# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import re

import llnl.util.tty as tty

import spack.compiler
from spack.package import *


@IntelOneApiPackage.update_description
class Intel(IntelPackage):
    """Intel Compilers. This package has been replaced by
    intel-oneapi-compilers.

    """

    homepage = "https://software.intel.com/en-us/intel-parallel-studio-xe"

    # Robert Cohn
    maintainers("rscohn2")

    depends_on("patchelf", type="build")

    # Same as in ../intel-parallel-studio/package.py, Composer Edition,
    # but the version numbering in Spack differs.
    version(
        "20.0.4",
        sha256="ac1efeff608a8c3a416e6dfe20364061e8abf62d35fbaacdffe3fc9676fc1aa3",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/17117/parallel_studio_xe_2020_update4_composer_edition.tgz",
        deprecated=True,
    )
    version(
        "20.0.2",
        sha256="42af16e9a91226978bb401d9f17b628bc279aa8cb104d4a38ba0808234a79bdd",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/16759/parallel_studio_xe_2020_update2_composer_edition.tgz",
        deprecated=True,
    )
    version(
        "20.0.1",
        sha256="26c7e7da87b8a83adfd408b2a354d872be97736abed837364c1bf10f4469b01e",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/16530/parallel_studio_xe_2020_update1_composer_edition.tgz",
        deprecated=True,
    )
    version(
        "20.0.0",
        sha256="9168045466139b8e280f50f0606b9930ffc720bbc60bc76f5576829ac15757ae",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/16229/parallel_studio_xe_2020_composer_edition.tgz",
        deprecated=True,
    )
    version(
        "19.1.2",
        sha256="42af16e9a91226978bb401d9f17b628bc279aa8cb104d4a38ba0808234a79bdd",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/16759/parallel_studio_xe_2020_update2_composer_edition.tgz",
        deprecated=True,
    )
    version(
        "19.1.1",
        sha256="26c7e7da87b8a83adfd408b2a354d872be97736abed837364c1bf10f4469b01e",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/16530/parallel_studio_xe_2020_update1_composer_edition.tgz",
        deprecated=True,
    )
    version(
        "19.1.0",
        sha256="9168045466139b8e280f50f0606b9930ffc720bbc60bc76f5576829ac15757ae",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/16229/parallel_studio_xe_2020_composer_edition.tgz",
        deprecated=True,
    )
    version(
        "19.0.5",
        sha256="e8c8e4b9b46826a02c49325c370c79f896858611bf33ddb7fb204614838ad56c",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/15813/parallel_studio_xe_2019_update5_composer_edition.tgz",
        deprecated=True,
    )
    version(
        "19.0.4",
        sha256="1915993445323e1e78d6de73702a88fa3df2036109cde03d74ee38fef9f1abf2",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/15537/parallel_studio_xe_2019_update4_composer_edition.tgz",
        deprecated=True,
    )
    version(
        "19.0.3",
        sha256="15373ac6df2a84e6dd9fa0eac8b5f07ab00cdbb67f494161fd0d4df7a71aff8e",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/15272/parallel_studio_xe_2019_update3_composer_edition.tgz",
        deprecated=True,
    )
    version(
        "19.0.1",
        sha256="db000cb2ebf411f6e91719db68a0c68b8d3f7d38ad7f2049ea5b2f1b5f006c25",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/14832/parallel_studio_xe_2019_update1_composer_edition.tgz",
        deprecated=True,
    )
    version(
        "19.0.0",
        sha256="e1a29463038b063e01f694e2817c0fcf1a8e824e24f15a26ce85f20afa3f963a",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/13581/parallel_studio_xe_2019_composer_edition.tgz",
        deprecated=True,
    )

    # Version 18.0.5 comes with parallel studio 2018 update 4. See:
    # https://software.intel.com/en-us/articles/intel-compiler-and-composer-update-version-numbers-to-compiler-version-number-mapping
    version(
        "18.0.5",
        sha256="94aca8f091dff9535b02f022a37aef150b36925c8ef069335621496f8e4db267",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/13722/parallel_studio_xe_2018_update4_composer_edition.tgz",
        deprecated=True,
    )
    version(
        "18.0.3",
        sha256="f21f7759709a3d3e3390a8325fa89ac79b1fce8890c292e73b2ba3ec576ebd2b",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/13002/parallel_studio_xe_2018_update3_composer_edition.tgz",
        deprecated=True,
    )
    version(
        "18.0.2",
        sha256="02d2a9fb10d9810f85dd77700215c4348d2e4475e814e4f086eb1442462667ff",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/12722/parallel_studio_xe_2018_update2_composer_edition.tgz",
        deprecated=True,
    )
    version(
        "18.0.1",
        sha256="db9aa417da185a03a63330c9d76ee8e88496ae6b771584d19003a29eedc7cab5",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/12381/parallel_studio_xe_2018_update1_composer_edition.tgz",
        deprecated=True,
    )
    version(
        "18.0.0",
        sha256="ecad64360fdaff2548a0ea250a396faf680077c5a83c3c3ce2c55f4f4270b904",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/12067/parallel_studio_xe_2018_composer_edition.tgz",
        deprecated=True,
    )
    #
    version(
        "17.0.7",
        sha256="661e33b68e47bf335694d2255f5883955234e9085c8349783a5794eed2a937ad",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/12860/parallel_studio_xe_2017_update7_composer_edition.tgz",
        deprecated=True,
    )
    version(
        "17.0.6",
        sha256="771f50746fe130ea472394c42e25d2c7edae049ad809d2050945ef637becf65f",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/12538/parallel_studio_xe_2017_update6_composer_edition.tgz",
        deprecated=True,
    )
    version(
        "17.0.5",
        sha256="ede4ea9351fcf263103588ae0f130b4c2a79395529cdb698b0d6e866c4871f78",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/12144/parallel_studio_xe_2017_update5_composer_edition.tgz",
        deprecated=True,
    )
    version(
        "17.0.4",
        sha256="4304766f80206a27709be61641c16782fccf2b3fcf7285782cce921ddc9b10ff",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/11541/parallel_studio_xe_2017_update4_composer_edition.tgz",
        deprecated=True,
    )
    version(
        "17.0.3",
        sha256="3648578d7bba993ebb1da37c173979bfcfb47f26e7f4e17f257e78dea8fd96ab",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/11464/parallel_studio_xe_2017_update3_composer_edition.tgz",
        deprecated=True,
    )
    version(
        "17.0.2",
        sha256="abd26ab2a703e73ab93326984837818601c391782a6bce52da8b2a246798ad40",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/11302/parallel_studio_xe_2017_update2_composer_edition.tgz",
        deprecated=True,
    )
    version(
        "17.0.1",
        sha256="bc592abee829ba6e00a4f60961b486b80c15987ff1579d6560186407c84add6f",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/10978/parallel_studio_xe_2017_update1_composer_edition.tgz",
        deprecated=True,
    )
    version(
        "17.0.0",
        sha256="d218db66a5bb57569bea00821ac95d4647eda7422bf8a178d1586b0fb314935a",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/9656/parallel_studio_xe_2017_composer_edition.tgz",
        deprecated=True,
    )
    #
    version(
        "16.0.4",
        sha256="17606c52cab6f5114223a2425923c8dd69f1858f5a3bdf280e0edea49ebd430d",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/9785/parallel_studio_xe_2016_composer_edition_update4.tgz",
        deprecated=True,
    )
    version(
        "16.0.3",
        sha256="fcec90ba97533e4705077e0701813b5a3bcc197b010b03e96f83191a35c26acf",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/9063/parallel_studio_xe_2016_composer_edition_update3.tgz",
        deprecated=True,
    )
    version(
        "16.0.2",
        sha256="6309ef8be1abba7737d3c1e17af64ca2620672b2da57afe2c3c643235f65b4c7",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/8680/parallel_studio_xe_2016_composer_edition_update2.tgz",
        deprecated=True,
    )
    #
    # Grandfathered release; different directory structure.
    version(
        "15.0.6",
        sha256="b1e09833469ca76a2834cd0a5bb5fea11ec9986da85abf4c6eed42cd96ec24cb",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/8432/l_compxe_2015.6.233.tgz",
        deprecated=True,
    )
    version(
        "15.0.1",
        sha256="8a438fe20103e27bfda132955616d0c886aa6cfdd86dcd9764af5d937a8799d9",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/4933/l_compxe_2015.1.133.tgz",
        deprecated=True,
    )

    variant("rpath", default=True, description="Add rpath to .cfg files")

    auto_dispatch_options = IntelPackage.auto_dispatch_options
    variant(
        "auto_dispatch",
        values=any_combination_of(*auto_dispatch_options),
        description="Enable generation of multiple auto-dispatch code paths",
    )

    # MacOS does not support some of the auto dispatch settings
    conflicts("auto_dispatch=SSE2", "platform=darwin", msg="SSE2 is not supported on MacOS")
    conflicts(
        "auto_dispatch=SSE3",
        "platform=darwin target=x86_64:",
        msg="SSE3 is not supported on MacOS x86_64",
    )

    executables = ["^icc$", "^icpc$", "^ifort$"]

    @classmethod
    def determine_version(cls, exe):
        version_regex = re.compile(r"\((?:IFORT|ICC)\) ([^ ]+)")
        try:
            output = spack.compiler.get_compiler_version_output(exe, "--version")
            match = version_regex.search(output)
            if match:
                return match.group(1)
        except ProcessError:
            pass
        except Exception as e:
            tty.debug(str(e))

        return None

    @classmethod
    def determine_variants(cls, exes, version_str):
        compilers = {}
        for exe in exes:
            if "icc" in exe:
                compilers["c"] = exe
            if "icpc" in exe:
                compilers["cxx"] = exe
            if "ifort" in exe:
                compilers["fortran"] = exe
        return "", {"compilers": compilers}

    @property
    def cc(self):
        msg = "cannot retrieve C compiler [spec is not concrete]"
        assert self.spec.concrete, msg
        if self.spec.external:
            return self.spec.extra_attributes["compilers"].get("c", None)
        return str(self.spec.prefix.bin.intel64.icc)

    @property
    def cxx(self):
        msg = "cannot retrieve C++ compiler [spec is not concrete]"
        assert self.spec.concrete, msg
        if self.spec.external:
            return self.spec.extra_attributes["compilers"].get("cxx", None)
        return str(self.spec.prefix.bin.intel64.icpc)

    @property
    def fortran(self):
        msg = "cannot retrieve Fortran compiler [spec is not concrete]"
        assert self.spec.concrete, msg
        if self.spec.external:
            return self.spec.extra_attributes["compilers"].get("fortran", None)
        return str(self.spec.prefix.bin.intel64.ifort)

    # Since the current package is a subset of 'intel-parallel-studio',
    # all remaining Spack actions are handled in the package class.
