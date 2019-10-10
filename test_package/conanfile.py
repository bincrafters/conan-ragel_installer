from conans import ConanFile, tools

class TestPackage(ConanFile):
    settings = "os", "compiler", "build_type", "arch"

    def build(self):
        pass

    def test(self):
        self.run('ragel --version', run_environment=True)
