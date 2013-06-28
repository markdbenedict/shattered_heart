from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension('c_delaunay', ['c_delaunay.pyx'])]

setup(
    name = 'Delaunay Cython module',
    cmdclass = {'build_ext':build_ext},
    ext_modules = ext_modules   
)