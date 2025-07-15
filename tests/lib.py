"""tests library"""

# pylint: disable=missing-docstring

import random
from typing import Iterable

from faker import Faker
from faker.providers import BaseProvider
from gbp_testkit import fixtures as testkit
from gbp_testkit.factories import ArtifactFactory
from gentoo_build_publisher.build_publisher import BuildPublisher
from gentoo_build_publisher.types import Build
from unittest_fixtures import Fixtures, fixture

fake = Faker()


class Provider(BaseProvider):
    def version(self) -> str:
        return f"{random.randint(0,9)}.{random.randint(0,9)}.{random.randint(0,9)}"

    def cpv(self) -> str:
        return f"{fake.word()}-{fake.word()}/{fake.word()}-{self.version()}"


fake.add_provider(Provider)


@fixture(testkit.environ, testkit.publisher)
def pulled_builds(
    fixtures: Fixtures,
    machines: Iterable[str] = ("babette", "polaris"),
    num_builds: int = 3,
    packages_per_build: int = 3,
) -> list[str]:
    publisher: BuildPublisher = fixtures.publisher
    jenkins = publisher.jenkins
    builder: ArtifactFactory = jenkins.artifact_builder

    for i, machine in enumerate(machines):
        for j in range(num_builds):
            build = Build(machine, str(i + j))
            for _ in range(packages_per_build):
                builder.build(build, fake.cpv())
            publisher.pull(build)

    return publisher.repo.build_records.list_machines()
