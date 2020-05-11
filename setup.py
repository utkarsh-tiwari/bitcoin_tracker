from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    required = f.read()

setup(
    name='json_to_excel',
    version='0.1',
    description='A sample Python project',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Utkarsh_Tiwari',
    author_email='utkarshtiwari1504@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    py_modules=["json_to_excel"],
    python_requires='>=3.5',
    install_requires=required,
    # entry_points={
    #     'console_scripts': [
    #         'sample=sample:main',
    #     ],
    # },
)