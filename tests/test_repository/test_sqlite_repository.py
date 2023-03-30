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


def test_get_all(repository):
    data_size = 5
    repository.delete_all()
    objects = [Custom(pk=i + 1) for i in range(data_size)]
    for o in objects:
        repository.add(o)
    data = repository.get_all()
    for i in range(data_size):
        assert data[i] == objects[i]


def test_get_all_where(repository):
    data_size = 5
    repository.delete_all()
    objects = []
    for i in range(data_size):
        o = Custom(pk=i + 1)
        o.name = str(i)
        o.test = 'testing'
        repository.add(o)
        objects.append(o)
    assert repository.get_all({'name': '0'})[0] == objects[0]
    data = repository.get_all({'testing': 'testing'})
    for i in range(data_size):
        assert data[i] == objects[i]


def test_cant_update(repository):
    obj = Custom()
    print(obj)
    with pytest.raises(TypeError):
        repository.update(obj)


def test_cannot_delete_nonexistent_file(repository):
    with pytest.raises(KeyError):
        repository.delete(100)
