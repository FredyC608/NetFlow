from setuptools import setup, Extension
import pybind11

cpp_args = ['-std=c++11']

ext_modules = [
    Extension(
        'netflow_crypto',
        ['cpp_src/crypto_module.cpp'],
        include_dirs=[pybind11.get_include()],
        language='c++',
        extra_compile_args=cpp_args,
    ),
]

setup(
    name='netflow_crypto',
    version='0.1.0',
    author='NetFlow Team',
    description='C++ Extension for Encryption',
    ext_modules=ext_modules,
)