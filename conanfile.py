#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools, AutoToolsBuildEnvironment
import os


class RagelConan(ConanFile):
    name = "ragel_installer"
    version = "6.10"
    description = "Ragel compiles executable finite state machines from regular languages"
    homepage = "http://www.colm.net/open-source/ragel"
    settings = {"os_build": ["Windows", "Linux", "Macos"],
                "arch_build": ["x86", "x86_64"],
                "compiler": None}
    url = "https://github.com/bincrafters/conan-ragel_installer"
    license = "GPL-2.0"
    topics = ("conan", "ragel", "installer", "FSM", "regex", "fsm-compiler")
    author = "Bincrafters <bincrafters@gmail.com>"
    build_policy = "missing"
    _autotools = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def build_requirements(self):
        if self.settings.os_build == "Windows":
            self.build_requires("msys2_installer/latest@bincrafters/stable")

    def source(self):
        sha256 = "5f156edb65d20b856d638dd9ee2dfb43285914d9aa2b6ec779dac0270cd56c3f"
        source_url = 'http://www.colm.net/files/ragel/ragel-{0}.tar.gz'.format(self.version)
        tools.get(source_url, sha256=sha256)
        extracted_dir = "ragel-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_autotools(self):
        if not self._autotools:
            if self.settings.os_build == "Windows":
                self._autotools = self._configure_autotools_windows()
            else:
                self._autotools = self._configure_autotools_unix()
        return self._autotools

    def _configure_autotools_unix(self):
        autotools = AutoToolsBuildEnvironment(self)
        autotools.configure(configure_dir=self._source_subfolder)
        return autotools

    def _configure_autotools_windows(self):
        if "VisualStudioVersion" in os.environ:
            del os.environ["VisualStudioVersion"]

        compiler_cxx = compiler_cc = '$PWD/ragel-%s/compile cl -nologo' % self.version

        autotools = AutoToolsBuildEnvironment(self, win_bash=tools.os_info.is_windows)

        with tools.chdir(self._source_subfolder):
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
            autotools.configure(configure_dir=self._source_subfolder, args=configure_args)
        return autotools

    def build(self):
        autotools = self._configure_autotools()
        autotools.make()

    def package(self):
        self.copy(pattern="COPYING", dst="licenses", src=self._source_subfolder)
        self.copy(pattern="CREDITS", dst="licenses", src=self._source_subfolder)
        autotools = self._configure_autotools()
        autotools.install()

    def package_info(self):
        self.env_info.RAGEL_ROOT = self.package_folder
        self.env_info.path.append(os.path.join(self.package_folder, 'bin'))

    def package_id(self):
        del self.info.settings.compiler
