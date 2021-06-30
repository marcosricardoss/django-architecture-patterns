import pytest

@pytest.mark.django_db
def test_get_task_list_view_page(client):
    """ Populates the database with data from 
        task/fixtures/dumpdata.json. """

    response = client.get('/')
    
    assert response.status_code == 200    
    assert response.content.count(b'Task Name 1') == 1
    assert response.content.count(b'Task Name 2') == 1
    assert response.content.count(b'Task Name 3') == 1
    assert (b'tag-1') in response.content    
    assert (b'tag-2') in response.content    
    assert (b'tag-3') in response.content    

@pytest.mark.django_db
def test_get_task_list_view_page(client):
    """ Populates the database with data from 
        task/fixtures/dumpdata.json. """

    response = client.get('/?page=2')    
    assert response.status_code == 200            