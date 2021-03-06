"""Development automation
"""
import os

import nox

nox.options.sessions = ["lint", "test"]
nox.options.reuse_existing_virtualenvs = True


@nox.session(python="3.8")
def lint(session):
    session.install("pre-commit")

    if session.posargs:
        args = session.posargs
    elif "CI" in os.environ:
        args = ["--show-diff-on-failure"]
    else:
        args = []

    session.run("pre-commit", "run", "--all-files", *args)


@nox.session(python=["2.7", "3.5", "3.6", "3.7", "3.8", "pypy2", "pypy3"])
def test(session):
    session.install(".[test]")

    htmlcov_output = os.path.join(session.virtualenv.location, "htmlcov")

    session.run(
        "pytest",
        "--cov=installer",
        "--cov-fail-under=100",
        "--cov-report=term-missing",
        "--cov-report=html:{}".format(htmlcov_output),
        "--cov-context=test",
        "-n",
        "auto",
        *session.posargs
    )


@nox.session(python="3.8")
def getlaunchers(session):
    session.install("httpx")
    session.run("python", "tools/getlaunchers.py")
