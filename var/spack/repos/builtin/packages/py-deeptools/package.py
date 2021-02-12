# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDeeptools(PythonPackage):
    """deepTools addresses the challenge of handling the large amounts of data
       that are now routinely generated from DNA sequencing centers."""

    homepage = "https://pypi.org/project/deepTools/"
    url      = "https://files.pythonhosted.org/packages/f6/f3/789edda975fcca4736fab2007d82cab2e86739901c88bb0528db5c338d1f/deepTools-3.5.0.tar.gz"

    version('3.5.0', sha256='1a14a29e60be13eac11bd204dab9aef73cd72fe56a94c587333f21087584c0d8')
    version('3.4.3', url="https://files.pythonhosted.org/packages/51/72/c6b2fdf1ab026ff827e7b8dce72643046ae8744499eb209844aa2cbd3d75/deepTools-3.4.3.tar.gz", sha256='abdf0853f8944341547e0958f7df881573e9fb948d450b9232ce15ada395efab')
    version('3.4.2', url="https://files.pythonhosted.org/packages/45/34/9964dfaf1dd0977bbb4b0459ce35de87cd1a15f7614773f68434e147dde5/deepTools-3.4.2.tar.gz", sha256='fcda9557504e675f7ff68e13e977815063e779089e806fe5b3ce62c605dfe70c')
    version('3.4.1', url="https://files.pythonhosted.org/packages/65/bc/f0cc8e7793c8d1d7a30850e70a9700e4704a1df159264f8d57eae3ecac2c/deepTools-3.4.1.tar.gz", sha256='fa2512be2728af67aa51ab3df29b4cafc511e8b1d0d2a22d44e0c313e64bfc17')
    version('3.4.0', url="https://files.pythonhosted.org/packages/9c/7a/c839acf4cb493a92c3efe1f69f322d0c3cf6356c208006a094a1001285b2/deepTools-3.4.0.tar.gz", sha256='a5c8aec3b0333c56b42d0561256693b6d5c4456e8cf4bbaafec0999be79b9d49')
    version('3.3.2', url="https://files.pythonhosted.org/packages/80/7a/7f87b1acbdde421cafe91e4a3ce7edca20390f5a72a2e39cf02d40648737/deepTools-3.3.2.tar.gz", sha256='c3cb0549e1a5fc1f708a8f60b4ca79461eccf57d62318cb1521aa28a1e2eecfe')
    version('3.3.1', url="https://files.pythonhosted.org/packages/82/8e/d9d4b66b2ce1bd48f1db43357c8eb019ae3e8bb1bb7a9e82667db981e1df/deepTools-3.3.1.tar.gz", sha256='514240f97e58bcfbf8c8b69ae9071d26569b491f089e1c1c46ba4866d335e322')
    version('3.3.0', url="https://files.pythonhosted.org/packages/3d/16/3e1757b61db790c86d1d9cf189a80946785ee69a60648647e1a44bfe504f/deepTools-3.3.0.tar.gz", sha256='a9a6d2aff919f45e869acfb477e977db627da84f8136e4b4af0a5100057e6bc3')
    version('3.2.1', url="https://files.pythonhosted.org/packages/cb/31/bfd1dd80e048075269d083230a635d1285ad2229cf22af14fb104e764cce/deepTools-3.2.1.tar.gz", sha256='ccbabb46d6c17c927e96fadc43d8d4770efeaf40b9bcba3b94915a211007378e')
    version('3.2.0', url="https://files.pythonhosted.org/packages/24/c8/ab6daedf122fa31e51193646bd9f811be2cc3b18b7738de8a4cd4e2c26f3/deepTools-3.2.0.tar.gz", sha256='2748136fb809c69376e6b383ce5a00ba3e7310e2668a82c5550d4c9bb47fe868')
    version('3.1.3', url="https://files.pythonhosted.org/packages/43/0b/0ff8d6440feba7fa4e7911ab0d13bab4ce5c72c9be2ffa6633f417a7cfef/deepTools-3.1.3.tar.gz", sha256='bfbaf077d5206871f237fa4a8fd0da8ecf0d22f4e868fc6eeb215fd14574f3fb')
    version('3.1.2', url="https://files.pythonhosted.org/packages/54/7b/a0248f8a65468f399e7956fc79761f55ff785d86775466db0d16e7af163f/deepTools-3.1.2.tar.gz", sha256='fc8b17f0a791b5ba6a3d6bcb32ec0731614da2397d38218217ec3d3cd6ee6129')
    version('3.1.1', url="https://files.pythonhosted.org/packages/ff/27/93ac9d14907605d724f98a49a9ece4c7f659c48dd15631cf0448acc8f0e0/deepTools-3.1.1.tar.gz", sha256='272ff20c573f4f5a0355b66b946cf64d122ddfe8b19c5f42902083d9151ee73b')
    version('3.1.0', url="https://files.pythonhosted.org/packages/7b/87/d3fd45754dc54aca526c2a34f185091e994f94a0c89d005bd499ba502adb/deepTools-3.1.0.tar.gz", sha256='cba820f4e8525ef3ea1e1a7b7b5c621ac1b27627882a2d0c9aa502ca2cb9a405')
    version('3.0.2', url="https://files.pythonhosted.org/packages/21/63/095615a9338c824dcc1496a302d04267c674175f0081e1ee2f897f33539f/deepTools-3.0.2.tar.gz", sha256='3f350d95fe30aa264691303d3aaaab4a16a6811ebdfe2f3fde4644abb0c3cfb3')
    version('3.0.1', url="https://files.pythonhosted.org/packages/77/78/82c94aafd83d844fa33d43c5e8c6be2e48222603280332ff16accd9711de/deepTools-3.0.1.tar.gz", sha256='10225daf7fdfd9d6e825c8dc802cb5475a0b0f7e533cde3b4a1fcc8be717e193')
    version('3.0.0', url="https://files.pythonhosted.org/packages/5c/f3/e50326fb2f185cbf89946348e6afceee04535c390225d44a88471263fff0/deepTools-3.0.0.tar.gz", sha256='a25767be0565c132153c15f4f6c7099a966df02ca14d9d068d2adb174685bec9')
    version('2.5.7', url="https://files.pythonhosted.org/packages/15/7d/fba2f2a9927a638a9e85a6e688f64c525537706148564066713e0a47fe2e/deepTools-2.5.7.tar.gz", sha256='e35f723ca58b0cd7575a9f966f1972193e4010ff57e68a498fdf480d31314550')

    depends_on('python@2.7:',                   type=('build', 'run'))
    depends_on('py-setuptools',                 type='build')
    depends_on('py-numpy@1.9.0:',               type=('build', 'run'))
    depends_on('py-scipy@0.17.0:',              type=('build', 'run'))
    depends_on('py-matplotlib@3.1.0:',          type=('build', 'run'))
    depends_on('py-pysam@0.14.0:',              type=('build', 'run'))
    depends_on('py-numpydoc@0.5:',              type=('build', 'run'))
    depends_on('py-pybigwig@0.2.1:',            type=('build', 'run'))
    depends_on('py-py2bit@0.2.0:',              type=('build', 'run'))
    depends_on('py-plotly@2.0.0:',              type=('build', 'run'))
    depends_on('py-deeptoolsintervals@0.1.8:',  type=('build', 'run'))