import setuptools

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='mumaxc',
    version='0.1',
    description='Python interface to mumax3 integrated into Jupyter notebook.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://joommf.github.io',
    author='Marijan Beg, Ryan A. Pepper, JL, JM, G, V,  Thomas Kluyver, and Hans Fangohr',
    author_email='jupyteroommf@gmail.com',
    packages=setuptools.find_packages(),
    install_requires=['scipy',
                      'micromagneticmodel',
                      'oommfodt'],
    #package_data={'oommfc.tests': ['test_files/test_oommf.mif',
    #                               'test_files/m0.omf']},
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: BSD License',
                 'Programming Language :: Python :: 3 :: Only',
                 'Operating System :: Unix',
                 'Operating System :: MacOS',
                 'Operating System :: Microsoft :: Windows',
                 'Topic :: Scientific/Engineering :: Physics',
                 'Intended Audience :: Science/Research',
                 'Natural Language :: English']
)
