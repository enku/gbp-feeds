"""noxfile for ci/cd testing"""

# pylint: disable=missing-docstring
import nox

PYTHON_VERSIONS = (
    "3.12",
    "3.13",
    # "3.14",  # python-dispatch does not (yet) work with this
)


@nox.session(python=PYTHON_VERSIONS)
def tests(session: nox.Session) -> None:
    dev_dependencies = nox.project.load_toml("pyproject.toml")["dependency-groups"][
        "dev"
    ]
    session.install(".", *dev_dependencies)

    session.run("coverage", "run", "-m", "tests")
    session.run("coverage", "report")
