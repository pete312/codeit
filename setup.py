import setuptools


setuptools.setup(
     name='codeit',  
     version='0.1.a1',
     author="Pete Moore",
     description="code writing by using print decorators.",
     #long_description=long_description,
     url="",
     #data_files=[('', ['LICENSE.txt'])],
     data_files=( [None] ),
     include_package_data=False,
     packages=setuptools.find_packages(),
     classifiers=[
         "License :: OSI Approved :: MIT License",
         "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
     ],
     install_requires=[ 'tabulate==0.8.2',
                        'natsort==7.0.1',
                       ]
)
