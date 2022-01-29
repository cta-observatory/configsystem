from setuptools import setup


extras_require = {
    "astropy": ["astropy"],
    "tests": ["pytest", "pytest-cov"],
}

extras_require["all"] = list({
    dep for extra in extras_require.values()
    for dep in extra
})

setup(
    extras_require=extras_require,
)
