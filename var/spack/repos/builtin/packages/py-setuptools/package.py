# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySetuptools(PythonPackage):
    """A Python utility that aids in the process of downloading, building,
       upgrading, installing, and uninstalling Python packages."""

    homepage = "https://github.com/pypa/setuptools"
    url      = "https://pypi.io/packages/source/s/setuptools/setuptools-49.2.0.zip"

    import_modules = [
        'setuptools', 'pkg_resources', 'setuptools._vendor',
        'setuptools.command', 'setuptools.extern',
        'setuptools._vendor.packaging', 'pkg_resources._vendor',
        'pkg_resources.extern', 'pkg_resources._vendor.packaging',
        'easy_install'
    ]

    version('50.3.2', sha256='ed0519d27a243843b05d82a5e9d01b0b083d9934eaa3d02779a23da18077bd3c')
    version('50.1.0', sha256='4a7708dafd2d360ce5e2ac7577374da9fb65fc867bc4cdaf461f9f834dfa6ac3')
    version('49.6.0', sha256='46bd862894ed22c2edff033c758c2dc026324788d758e96788e8f7c11f4e9707')
    version('49.2.0', sha256='afe9e81fee0270d3f60d52608549cc8ec4c46dada8c95640c1a00160f577acf2')
    version('46.1.3', sha256='795e0475ba6cd7fa082b1ee6e90d552209995627a2a227a47c6ea93282f4bfb1')
    version('44.1.0', sha256='794a96b0c1dc6f182c36b72ab70d7e90f1d59f7a132e6919bb37b4fd4d424aca')
    version('41.4.0', sha256='7eae782ccf36b790c21bde7d86a4f303a441cd77036b25c559a602cf5186ce4d')
    version('41.0.1', sha256='a222d126f5471598053c9a77f4b5d4f26eaa1f150ad6e01dcf1a42e185d05613')
    version('41.0.0', sha256='79d30254b6fe7a8e672e43cd85f13a9f3f2a50080bc81d851143e2219ef0dcb1')
    version('40.8.0', sha256='6e4eec90337e849ade7103723b9a99631c1f0d19990d6e8412dc42f5ae8b304d')
    version('40.4.3', sha256='acbc5740dd63f243f46c2b4b8e2c7fd92259c2ddb55a4115b16418a2ed371b15')
    version('40.2.0', sha256='47881d54ede4da9c15273bac65f9340f8929d4f0213193fa7894be384f2dcfa6')
    version('39.2.0', sha256='f7cddbb5f5c640311eb00eab6e849f7701fa70bf6a183fc8a2c33dd1d1672fb2')
    version('39.0.1', sha256='bec7badf0f60e7fc8153fac47836edc41b74e5d541d7692e614e635720d6a7c7')
    version('35.0.2', sha256='1e55496ca8058db68ae12ac29a985d1ee2c2483a5901f7692fb68fa2f9a250fd')
    version('34.4.1', sha256='704cc0c9fe6c97edd3c6370d165c5a754dfde318b671058523ed3226d944ea1b')
    version('34.2.0', sha256='7b551f5070f9414d48c08dda58bcb879c8d9276199283a99dc8e1362e2f378a2')
    version('25.2.0', sha256='b2757ddac2c41173140b111e246d200768f6dd314110e1e40661d0ecf9b4d6a6')
    version('20.7.0', sha256='505cdf282c5f6e3a056e79f0244b8945f3632257bba8469386c6b9b396400233')
    version('20.6.7', sha256='d20152ee6337323d3b6d95cd733fb719d6b4f3fbc40f61f7a48e5a1bb96478b2')
    version('19.2',   sha256='f90ed8eb70b14b0594ba74e9de4ffca040c0ec8ee505cbf3570499467859f71a')
    version('18.1',   sha256='ad52a9d5b3a6f39c2a1c2deb96cc4f6aff29d6511bdea2994322c40b60c9c36a')
    version('16.0',   sha256='aa86255dee2c4a0056509750008007667c29306b7a6c13801468515b2c672845')
    version('11.3.1', sha256='bd25f17de4ecf00116a9f7368b614a54ca1612d7945d2eafe5d97bc08c138bc5')

    depends_on('python@3.5:', type=('build', 'run'), when='@45.0.0:')
    depends_on('python@2.6:2.8,3.5:', type=('build', 'run'), when='@44.0.0:44.99.99')
    depends_on('python@2.6:2.8,3.4:', type=('build', 'run'), when='@:43.99.99')

    # Previously, setuptools vendored all of its dependencies to allow
    # easy bootstrapping. As of version 34.0.0, this is no longer done
    # and the dependencies need to be installed externally. As of version
    # 36.0.0, setuptools now vendors its dependencies again. See
    # https://github.com/pypa/setuptools/issues/980 for the reason they
    # reverted back to vendoring again.
    depends_on('py-packaging@16.8:', when='@34:35', type=('build', 'run'))
    depends_on('py-six@1.6.0:',      when='@34:35', type=('build', 'run'))
    depends_on('py-appdirs@1.4.0:',  when='@34:35', type=('build', 'run'))

    def url_for_version(self, version):
        url = 'https://pypi.io/packages/source/s/setuptools/setuptools-{0}'
        url = url.format(version)

        if version > Version('32.1.2'):
            url += '.zip'
        else:
            url += '.tar.gz'

        return url

    def build_test(self):
        # Unit tests require pytest, creating a circular dependency
        pass
