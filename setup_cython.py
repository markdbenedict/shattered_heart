from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension('c_voronoi', ['c_voronoi.pyx'])]

setup(
    name = 'Voronoi noise Cython module',
    cmdclass = {'build_ext':build_ext},
    ext_modules = ext_modules   
)