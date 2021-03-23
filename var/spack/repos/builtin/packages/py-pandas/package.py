# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyPandas(PythonPackage):
    """pandas is a fast, powerful, flexible and easy to use open source
    data analysis and manipulation tool, built on top of the Python
    programming language."""

    homepage = "https://pandas.pydata.org/"
    pypi = "pandas/pandas-1.2.0.tar.gz"

    maintainers = ['adamjstewart']
    import_modules = [
        'pandas', 'pandas.compat', 'pandas.compat.numpy', 'pandas.core',
        'pandas.core.reshape', 'pandas.core.tools', 'pandas.core.util',
        'pandas.core.array_algos', 'pandas.core.dtypes', 'pandas.core.groupby',
        'pandas.core.internals', 'pandas.core.computation',
        'pandas.core.window', 'pandas.core.arrays',
        'pandas.core.arrays.sparse', 'pandas.core.ops', 'pandas.core.sparse',
        'pandas.core.indexes', 'pandas.util', 'pandas.io', 'pandas.io.formats',
        'pandas.io.excel', 'pandas.io.json', 'pandas.io.sas',
        'pandas.io.clipboard', 'pandas.tseries', 'pandas._libs',
        'pandas._libs.window', 'pandas._libs.tslibs', 'pandas.plotting',
        'pandas.arrays', 'pandas.api', 'pandas.api.indexers',
        'pandas.api.types', 'pandas.api.extensions', 'pandas.errors',
        'pandas._config'
    ]

    version('1.2.3',  sha256='df6f10b85aef7a5bb25259ad651ad1cc1d6bb09000595cab47e718cbac250b1d')
    version('1.2.2',  sha256='14ed84b463e9b84c8ff9308a79b04bf591ae3122a376ee0f62c68a1bd917a773')
    version('1.2.1',  sha256='5527c5475d955c0bc9689c56865aaa2a7b13c504d6c44f0aadbf57b565af5ebd')
    version('1.2.0',  sha256='e03386615b970b8b41da6a68afe717626741bb2431cec993640685614c0680e4')
    version('1.1.5',  sha256='f10fc41ee3c75a474d3bdf68d396f10782d013d7f67db99c0efbfd0acb99701b')
    version('1.1.4',  sha256='a979d0404b135c63954dea79e6246c45dd45371a88631cdbb4877d844e6de3b6')
    version('1.1.3',  sha256='babbeda2f83b0686c9ad38d93b10516e68cdcd5771007eb80a763e98aaf44613')
    version('1.1.2',  sha256='b64ffd87a2cfd31b40acd4b92cb72ea9a52a48165aec4c140e78fd69c45d1444')
    version('1.1.1',  sha256='53328284a7bb046e2e885fd1b8c078bd896d7fc4575b915d4936f54984a2ba67')
    version('1.1.0',  sha256='b39508562ad0bb3f384b0db24da7d68a2608b9ddc85b1d931ccaaa92d5e45273')
    version('1.0.5',  sha256='69c5d920a0b2a9838e677f78f4dde506b95ea8e4d30da25859db6469ded84fa8')
    version('1.0.4',  sha256='b35d625282baa7b51e82e52622c300a1ca9f786711b2af7cbe64f1e6831f4126')
    version('1.0.3',  sha256='32f42e322fb903d0e189a4c10b75ba70d90958cc4f66a1781ed027f1a1d14586')
    version('1.0.2',  sha256='76334ba36aa42f93b6b47b79cbc32187d3a178a4ab1c3a478c8f4198bcd93a73')
    version('1.0.1',  sha256='3c07765308f091d81b6735d4f2242bb43c332cc3461cae60543df6b10967fe27')
    version('1.0.0',  sha256='3ea6cc86931f57f18b1240572216f09922d91b19ab8a01cf24734394a3db3bec')
    version('0.25.3', sha256='52da74df8a9c9a103af0a72c9d5fdc8e0183a90884278db7f386b5692a2220a4')
    version('0.25.2', sha256='ca91a19d1f0a280874a24dca44aadce42da7f3a7edb7e9ab7c7baad8febee2be')
    version('0.25.1', sha256='cb2e197b7b0687becb026b84d3c242482f20cbb29a9981e43604eb67576da9f6')
    version('0.25.0', sha256='914341ad2d5b1ea522798efa4016430b66107d05781dbfe7cf05eba8f37df995')
    version('0.24.2', sha256='4f919f409c433577a501e023943e582c57355d50a724c589e78bc1d551a535a2')
    version('0.24.1', sha256='435821cb2501eabbcee7e83614bd710940dc0cf28b5afbc4bdb816c31cec71af')
    version('0.23.4', sha256='5b24ca47acf69222e82530e89111dd9d14f9b970ab2cd3a1c2c78f0c4fbba4f4')
    version('0.21.1', sha256='c5f5cba88bf0659554c41c909e1f78139f6fce8fa9315a29a23692b38ff9788a')
    version('0.20.0', sha256='54f7a2bb2a7832c0446ad51d779806f07ec4ea2bb7c9aea4b83669fa97e778c4')
    version('0.19.2', sha256='6f0f4f598c2b16746803c8bafef7c721c57e4844da752d36240c0acf97658014')
    version('0.19.0', sha256='4697606cdf023c6b7fcb74e48aaf25cf282a1a00e339d2d274cf1b663748805b')
    version('0.18.0', sha256='c975710ce8154b50f39a46aa3ea88d95b680191d1d9d4b5dd91eae7215e01814')
    version('0.16.1', sha256='570d243f8cb068bf780461b9225d2e7bef7c90aa10d43cf908fe541fc92df8b6')
    version('0.16.0', sha256='4013de6f8796ca9d2871218861823bd9878a8dfacd26e08ccf9afdd01bbad9f1')

    # Required dependencies
    # https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html#dependencies
    depends_on('python@3.7.1:', type=('build', 'run'), when='@1.2:')
    depends_on('python@3.6.1:', type=('build', 'run'), when='@1:')
    depends_on('python@3.5.3:', type=('build', 'run'), when='@0.25:')
    # https://pandas.pydata.org/docs/whatsnew/v1.0.0.html#build-changes
    depends_on('py-cython@0.29.13:2', type='build', when='@1:')
    depends_on('py-cython@0.29.16:2', type='build', when='@1.1:')
    depends_on('py-cython@0.29.21:2', type='build', when='@1.1.3:')
    depends_on('py-setuptools@24.2.0:', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-numpy@1.13.3:', type=('build', 'run'), when='@0.25:')
    depends_on('py-numpy@1.15.4:', type=('build', 'run'), when='@1.1:')
    depends_on('py-numpy@1.16.5:', type=('build', 'run'), when='@1.2:')
    depends_on('py-python-dateutil', type=('build', 'run'))
    depends_on('py-python-dateutil@2.6.1:', type=('build', 'run'), when='@0.25:')
    depends_on('py-python-dateutil@2.7.3:', type=('build', 'run'), when='@1.1:')
    depends_on('py-pytz@2017.2:', type=('build', 'run'))
    depends_on('py-pytz@2017.3:', type=('build', 'run'), when='@1.2:')

    # Recommended dependencies
    # https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html#recommended-dependencies
    depends_on('py-numexpr', type=('build', 'run'))
    depends_on('py-numexpr@2.6.2:', type=('build', 'run'), when='@0.25:')
    depends_on('py-numexpr@2.6.8:', type=('build', 'run'), when='@1.2:')
    depends_on('py-bottleneck', type=('build', 'run'))
    depends_on('py-bottleneck@1.2.1:', type=('build', 'run'), when='@0.25:')

    # Optional dependencies
    # https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html#optional-dependencies
