#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools, AutoToolsBuildEnvironment
import os


class RagelConan(ConanFile):
    name = "ragel_installer"
    version = "6.10"
    description = "Ragel compiles executable finite state machines from regular languages. " \
                  "Ragel targets C, C++ and ASM. "
    homepage = "http://www.colm.net/open-source/ragel"

    settings = {"os_build": ["Windows", "Linux", "Macos"],
                "arch_build": ["x86", "x86_64"], "compiler": None}

    url = "https://github.com/bincrafters/conan-ragel_installer"
    license = "https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html"
    author = "Bincrafters <bincrafters@gmail.com>"
    source_url = 'http://www.colm.net/files/ragel/ragel-{0}.tar.gz'.format(version)
    build_policy = "missing"
    autotools = None

    def build_requirements(self):
        if self.settings.os_build == "Windows":
            self.build_requires("msys2_installer/latest@bincrafters/stable")

    def source(self):
        filename = "ragel-%s.tar.gz" % self.version
        tools.download(self.source_url, filename)
        tools.untargz(filename)
        os.unlink(filename)

    def configure_autotools(self):
        if not self.autotools:
            self.autotools = AutoToolsBuildEnvironment(self)
            self.autotools.configure(configure_dir="ragel-%s" % self.version)
        return self.autotools

    def unix_build(self):
        autotools = self.configure_autotools()
        autotools.make()

    def windows_build(self):
        # this overrides pre-configured environments (such as Appveyor's)
        if "VisualStudioVersion" in os.environ:
            del os.environ["VisualStudioVersion"]

        compiler_cxx = compiler_cc = '$PWD/ragel-%s/compile cl -nologo' % self.version

        self.autotools = AutoToolsBuildEnvironment(self, win_bash=True)

        with tools.chdir("{0}-{1}".format('ragel', self.version)):
            tools.run_in_windows_bash(self, 'pacman -S automake-wrapper autoconf --noconfirm --needed')

            makefile_am = os.path.join('ragel', 'Makefile.am').replace('\\', '/')
            self.output.info("Patching: %s" % makefile_am)
            tools.replace_in_file(makefile_am,
                                  'INCLUDES = -I$(top_srcdir)/aapl',
                                  'AM_CPPFLAGS = -I$(top_srcdir)/aapl')

            main_cpp = os.path.join('ragel', 'main.cpp').replace('\\', '/')
            self.output.info("Patching: %s" % main_cpp)
            tools.replace_in_file(main_cpp,
                                  '#include <unistd.h>',
                                  '')

            tools.run_in_windows_bash(self, 'aclocal')
            tools.run_in_windows_bash(self, 'autoheader')
            tools.run_in_windows_bash(self, 'automake --foreign --add-missing --force-missing')
            tools.run_in_windows_bash(self, 'autoconf')

        with tools.vcvars(self.settings):
            compiler_options = '-D_CRT_SECURE_NO_WARNINGS -D_CRT_SECURE_NO_DEPRECATE ' \
                               '-D_CRT_NONSTDC_NO_WARNINGS -WL -W2 -WX- -Gy -DNDEBUG ' \
                               '-diagnostics:classic -DWIN32 -D_WINDOWS -O2 -Ob2 '

            compiler_options += '-wd4577 -wd5026 -wd5027 -wd4710 -wd4711 -wd4626 -wd4250 -wd4365 ' \
                                '-wd4625 -wd4774 -wd4530 -wd4100 -wd4706 -wd4512 -wd4800 -wd4702 ' \
                                '-wd4819 -wd4355 -wd4091 -wd4267 -wd4365 -wd4625 -wd4774 -wd4820'

            linker_options = '/MACHINE:X{0}'.format('86' if self.settings.arch_build == 'x86' else '64')
            runtime = '-%s' % str(self.settings.compiler.runtime)

            prefix = tools.unix_path(os.path.abspath(self.package_folder), tools.MSYS2)

            flags = '{compiler_options} {runtime} -I{prefix}/include'.format(compiler_options=compiler_options,
                                                                             runtime=runtime,
                                                                             prefix=prefix)
            ldflags = '-L{prefix}/lib {linker_options}'.format(linker_options=linker_options,
                                                               prefix=prefix)
            configure_args = ['CC={compiler_cc}'.format(compiler_cc=compiler_cc),
                              'CXX={compiler_cxx}'.format(compiler_cxx=compiler_cxx),
                              'CFLAGS={flags}'.format(flags=flags),
                              'CXXFLAGS={flags}'.format(flags=flags),
                              'CPPFLAGS={flags}'.format(flags=flags),
                              'LDFLAGS={ldflags}'.format(ldflags=ldflags),
                              'LD=link',
                              'NM=dumpbin -symbols',
                              'STRIP=:',
                              'RANLIB=:']
            self.autotools.configure(configure_dir="ragel-%s" % self.version, args=configure_args)
            self.autotools.make()

    def build(self):
        if self.settings.os_build != "Windows":
            self.unix_build()
        else:
            self.windows_build()

    def package(self):
        build_src_dir = "{0}-{1}".format('ragel', self.version)

        self.copy(pattern="COPYING", dst="licenses", src=build_src_dir)
        self.copy(pattern="CREDITS", dst="licenses", src=build_src_dir)
        autotools = self.configure_autotools()
        autotools.make(args=["install"])

    def package_info(self):
        self.env_info.RAGEL_ROOT = self.package_folder
        self.env_info.path.append(os.path.join(self.package_folder, 'bin'))

    def package_id(self):
        self.info.settings.compiler = 'Any'
