import setuptools

def readme():
    with open('README.md') as f:
        README = f.read()
    return README
    
    
setuptools.setup(
     name='codeit',  
     version='0.0.1',
     author="Pete Moore",
     author_email="1petemoore@gmail.com",
     description="Aid code writing by using inline watch functions to colorize and visualize data.",
     long_description_content_type="text/markdown",
     long_description=readme(),
     url="https://github.com/pete312/codeit",
     data_files=[('', ['LICENSE.txt'])],
     include_package_data=False,
     packages=setuptools.find_packages(),
     license="MIT",
     classifiers=[
         "License :: OSI Approved :: MIT License",
         "Programming Language :: Python :: 3",
         "Programming Language :: Python :: 3.6",
         "Operating System :: OS Independent",
     ],
     install_requires=[ 'tabulate==0.8.2',
                        'natsort==7.0.1',
                       ]
)
