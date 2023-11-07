import setuptools

setuptools.setup(
    name="g2pk3",
    version="1.0",
    license='MIT',
    author="kdr",
    author_email="kdrhacker1234@gmail.com",
    description="",
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kdrkdrkdr/g2pk3",
    packages=setuptools.find_packages(),
    package_data={'': ['*.txt', '*.csv']},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        'unidecode',
        'jamo',
        'cmake',
        'jaconv',
        'pyopenjtalk',
        'g2p_en',
    ],
    py_modules = ['g2pk3']
)
