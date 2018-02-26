from distutils.core import setup

setup(
    name='CloeePy',
    version='0.0.1-dev',
    packages=['cloeepy',],
    package_data = {
        '.': ['*.md'],
        'cloeepy': ['data/*.yml'],
    },
    include_package_data=True,    # include everything in source control
    license='MIT',
    description="Light weight framework for non-HTTP systems.",
    install_requires=[
          "pyaml==17.12.1",
          "python-json-logger==0.1.8",
          "PyYAML==3.12",
     ],
     url = "https://github.com/cloeeai/CloeePy",
     author = "Scott Crespo",
     author_email = "sccrespo@gmail.com",
     keywords = "mini framework yaml cloee",
     python_requires='~=3.3',
)
