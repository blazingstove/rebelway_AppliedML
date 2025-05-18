import os
import inspect
from library_manager.utils import *

database_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
database_testpath = os.path.join(database_dir, 'test_library_database.json')

def test_save_json()->None:
    if os.path.exists(database_testpath):
        os.remove(database_testpath)
    save_json(database_testpath, data={'test':''})
    assert os.path.exists(database_testpath)

def test_load_json()->None:
    data = load_json(database_testpath)
    assert 'test' in data

def test_get_unique_id()->None:
    idA = get_unique_id()
    idB = get_unique_id()
    assert idA != idB