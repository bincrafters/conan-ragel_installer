# -*- coding: utf-8 -*-

from conans import ConanFile, tools, AutoToolsBuildEnvironment, CMake
import os


class RagelConan(ConanFile):
    name = "ragel_installer"
    version = "6.10"
    description = "Ragel compiles executable finite state machines from regular languages"
    homepage = "http://www.colm.net/open-source/ragel"
    settings = ("os_build", "arch_build", "compiler")
    url = "https://github.com/bincrafters/conan-ragel_installer"
    license = "GPL-2.0"
    topics = ("conan", "ragel", "installer", "FSM", "regex", "fsm-compiler")
    author = "Bincrafters <bincrafters@gmail.com>"
    exports = "LICENSE.md"
    exports_sources = ["CMakeLists.txt", "config.h", "0001-unistd.patch"]
    generators = "cmake"
    _autotools = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def source(self):
        sha256 = "5f156edb65d20b856d638dd9ee2dfb43285914d9aa2b6ec779dac0270cd56c3f"
        source_url = 'http://www.colm.net/files/ragel/ragel-{0}.tar.gz'.format(self.version)
        tools.get(source_url, sha256=sha256)
        extracted_dir = "ragel-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_autotools(self):
        if not self._autotools:
            self._autotools = AutoToolsBuildEnvironment(self)
            self._autotools.configure(configure_dir=self._source_subfolder)
        return self._autotools

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure()
        return cmake

    def build(self):
        if self.settings.os_build == "Windows":
            tools.patch(self._source_subfolder, "0001-unistd.patch")
            cmake = self._configure_cmake()
            cmake.build()
        else:
            autotools = self._configure_autotools()
            autotools.make()

    def package(self):
        self.copy(pattern="COPYING", dst="licenses", src=self._source_subfolder)
        self.copy(pattern="CREDITS", dst="licenses", src=self._source_subfolder)
        if self.settings.os_build == "Windows":
            cmake = self._configure_cmake()
            cmake.install()
        else:
            autotools = self._configure_autotools()
            autotools.install()

    def package_info(self):
        self.env_info.RAGEL_ROOT = self.package_folder
        self.env_info.path.append(os.path.join(self.package_folder, 'bin'))

    def package_id(self):
        del self.info.settings.compiler
