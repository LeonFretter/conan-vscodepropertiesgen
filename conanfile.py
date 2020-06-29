from conans.model import Generator
from conans.paths import BUILD_INFO
from conans import ConanFile
from os import path
from collections import OrderedDict
import pprint

import json

class VSCodeProperties(Generator):
    @property
    def filename(self):
        file_path = self.getPropFilePath()
        print("\nfile_path from filename: ", file_path)
        return file_path

    @property
    def content(self):
        file_path = self.getPropFilePath()

        if not path.isfile(file_path):
            raise Exception("Please create a basic .vscode/c_cpp_properties.json first")
        else:
            config_file = open(file_path)
            json_config = json.load(config_file)

            include_paths = json_config["configurations"][0]["includePath"]
            dependency_include_paths = self.deps_build_info.include_paths

            if type(include_paths) == str:
                include_paths = list(include_paths)

            if type(dependency_include_paths) == str:
                dependency_include_paths = list(dependency_include_paths)

            dependency_include_paths.append("/usr/include")

            for dependency in dependency_include_paths:
                if dependency not in include_paths:
                    include_paths.append(dependency)

            json_config["configurations"][0]["includePath"] = include_paths

            return json.dumps(json_config, indent=4)

    def getPropFilePath(self) -> str:
        project_dir =  path.dirname(self.output_path)
        path_to_file = path.join(project_dir, ".vscode/c_cpp_properties.json")

        return path_to_file


class VSCodePropGen(ConanFile):
    name = "code_cpp_props"
    version = "0.1"
    description = "Simple visual studio code C/C++ extension property generator"
    url = "https://github.com/mkovalchik/conan-vscodepropertiesgen"
    license = "MIT"

    def build(self):
        pass
    
    def package_info(self):
        self.cpp_info.includedirs = []
        self.cpp_info.libdirs = []
        self.cpp_info.bindirs = []
