from spack import *

class Ncurses(Package):
    """The ncurses (new curses) library is a free software emulation of curses
       in System V Release 4.0, and more. It uses terminfo format, supports pads and
       color and multiple highlights and forms characters and function-key mapping,
       and has all the other SYSV-curses enhancements over BSD curses.
    """

    homepage = "http://invisible-island.net/ncurses/ncurses.html"

    version('5.9', '8cb9c412e5f2d96bc6f459aa8c6282a1',
            url='http://ftp.gnu.org/pub/gnu/ncurses/ncurses-5.9.tar.gz')
    version('6.0', 'ee13d052e1ead260d7c28071f46eefb1',
            url='http://ftp.gnu.org/pub/gnu/ncurses/ncurses-6.0.tar.gz')

    patch('patch_gcc_5.txt', when='%gcc@5.0:')

    def install(self, spec, prefix):
        opts = [
            "--prefix=%s" % prefix,
            "--with-shared",
            "--with-cxx-shared",
            "--enable-widec",
            "--enable-overwrite",
            "--disable-lib-suffixes",
            "--without-ada"]
        configure(*opts)
        make()
        make("install")
