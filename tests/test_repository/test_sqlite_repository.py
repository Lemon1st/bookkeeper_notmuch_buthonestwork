from bookkeeper.repository.sqlite_repository import SQLiteRepository
from dataclasses import dataclass
import pytest


@dataclass(slots=True)
class Custom:
    comment: str = 'Generic_Comment'
    name: str = 'Generic_Name'
    one: int = 1
    test: str = ''
    pk: int | None = None


@pytest.fixture
def repository():
    return SQLiteRepository('testing_repository.db', Custom)


def test_crud(repository):
    repository.delete_all()
    obj1 = Custom('Test1', pk=1)
    pk1 = repository.add(obj1)
    obj2 = Custom('Test2', pk=2)
    pk2 = repository.add(obj2)
    assert obj1 == repository.get(pk1)
    assert obj2 == repository.get(pk2)
    assert obj1 != repository.get(pk2)
    assert obj2 != repository.get(pk1)
    obj_buff = obj1
    obj2.pk = obj1.pk
    repository.update(obj2)
    assert repository.get(pk1) != obj_buff
    assert repository.get(pk1) == obj2
    repository.delete(pk2)
    assert repository.get(pk2) is None
