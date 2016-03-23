from spack import *

class Git(Package):
    """Git is a free and open source distributed version control
       system designed to handle everything from small to very large
       projects with speed and efficiency."""
    homepage = "http://git-scm.com"
    url      = "https://github.com/git/git/archive/v2.7.3.tar.gz"


    version('2.8.0-rc2', '98a5bbeec5b4e8f61f96160aed67dff9')
    # The versions 2.7.x below have some vulnerabilities
    version('2.7.3', '627165fe4453a93cad7899cd7b649784')
    version('2.7.1', 'a3cae4589bd75b82451b813f2b8ed8bc')


    # See here for info on vulnerable Git versions:
    # http://www.theregister.co.uk/2016/03/16/git_server_client_patch_now/
    # All the following are vulnerable
    #version('2.6.3', 'b711be7628a4a2c25f38d859ee81b423')
    #version('2.6.2', 'da293290da69f45a86a311ad3cd43dc8')
    #version('2.6.1', '4c62ee9c5991fe93d99cf2a6b68397fd')
    #version('2.6.0', 'eb76a07148d94802a1745d759716a57e')
    #version('2.5.4', '3eca2390cf1fa698b48e2a233563a76b')
    #version('2.2.1', 'ff41fdb094eed1ec430aed8ee9b9849c')


    # Git compiles with curl support by default on but if your system
    # does not have it you will not be able to clone https repos
    variant("curl", default=True, description="Support curl for https clone")

    # Git compiles with expat support by default on but if your system
    # does not have it you will not be able to push https repos
    variant("expat", default=False, description="Support expat for https push")

    depends_on("autoconf")
    depends_on("curl", when="+curl")
    depends_on("expat", when="+expat")
    depends_on("openssl")
    # depends_on("perl")
    depends_on("pcre")

    depends_on("zlib")

    def install(self, spec, prefix):
        configure_args = [
            "CC=/usr/bin/cc",
            "--prefix=%s" % prefix,
            "--with-libpcre=%s" % spec['pcre'].prefix,
            # "--with-perl=%s" % spec['perl'].prefix,
            "--with-openssl=%s" % spec['openssl'].prefix,
            "--with-zlib=%s" % spec['zlib'].prefix
            ]

        if '+curl' in spec:
            configure_args.append("--with-curl=%s" % spec['curl'].prefix)

        if '+expat' in spec:
            configure_args.append("--with-expat=%s" % spec['expat'].prefix)

        which('autoreconf')('-i')
        configure(*configure_args)
        make()
        make("install")
