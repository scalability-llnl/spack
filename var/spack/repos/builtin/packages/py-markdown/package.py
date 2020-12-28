# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMarkdown(PythonPackage):
    """This is a Python implementation of John Gruber's Markdown. It is
    almost completely compliant with the reference implementation, though
    there are a few very minor differences. See John's Syntax
    Documentation for the syntax rules.
    """

    homepage = "https://pythonhosted.org/Markdown/"
    url      = "https://pypi.io/packages/source/m/markdown/Markdown-2.6.11.tar.gz"

    version('3.1.1', sha256='2e50876bcdd74517e7b71f3e7a76102050edec255b3983403f1a63e7c8a41e7a')
    version('2.6.11', sha256='a856869c7ff079ad84a3e19cd87a64998350c2b94e9e08e44270faef33400f81')
    version('2.6.7', sha256='daebf24846efa7ff269cfde8c41a48bb2303920c7b2c7c5e04fa82e6282d05c0')
    version('2.6.6', sha256='9a292bb40d6d29abac8024887bcfc1159d7a32dc1d6f1f6e8d6d8e293666c504')
    version('2.6.5', sha256='8d94cf6273606f76753fcb1324623792b3738c7612c2b180c85cc5e88642e560')
    version('2.6.4', sha256='e436eee7aaf2a230ca3315034dd39e8a0fc27036708acaa3dd70625ec62a94ce')
    version('2.6.3', sha256='ad75fc03c45492eba3bc63645e1e6465f65523a05fff0abf36910f810465a9af')
    version('2.6.2', sha256='ee17d0d7dc091e645dd48302a2e21301cc68f188505c2069d8635f94554170bf')
    version('2.6.1', sha256='b5879b87e8e5c125c92ab8c8f3babce78ad4e840446eed73c5b6e2984648d2b1')
    version('2.6', sha256='e1c8a489bb7c7154bc5a8c14f0fd1fc356ee36c8b9988f9fd8febff22dd435da')
    version('2.5.2', sha256='284e97e56db9ada03ede9c0ed2870ca6590ce7869f3119104d53510debf1533d')
    version('2.5.1', sha256='8f81ed12c18608a502828acb7d318f362c42f4eca97d01e93cadfc52c1e40b73')
    version('2.5', sha256='6ba74a1e7141c9603750d80711b639a7577bffb785708e6260090239ee5bc76d')

    depends_on('python@2.7:2.8,3.2:3.4', when='@:2.6.7')
    depends_on('python@2.7:2.8,3.2:3.6', when='@2.6.8:2.6.11')
    depends_on('python@2.7:2.8,3.3.5:', when='@3.1.1:')

    depends_on('py-setuptools', type='build', when='@2.6.11:')
