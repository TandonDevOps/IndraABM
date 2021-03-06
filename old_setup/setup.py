from setuptools import setup, find_packages

setup(name='indras_net',
    version='2.0.6',
    description='A framework for agent-based modeling in Python.',
    url='ihttps://github.com/TandonDevOps/IndraABM.git',
    author='Gene Callahan, Nathan Conroy, Denys Fenchenko, Abhinav Sharma',
    author_email='gcallah@mac.com',
    license='GNU',
    zip_safe=False,
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*",
                                 "tests"]),
    install_requires=[
        "networkx",
        "numpy", 'propargs', 'matplotlib'
    ],
    test_suite="",
    entry_points={
        "console_scripts": ['indra = indra.__main__:main']
    },
    classifiers=[
            # How mature is this project? Common values are
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 4 - Beta',

            # Indicate who your project is intended for
            'Intended Audience :: Developers',

            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
    ],
)
