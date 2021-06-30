import pytest

@pytest.mark.django_db
def test_get_task_delete_view_page(client):
    """ Populates the database with data from 
        task/fixtures/dumpdata.json. """

    response = client.get('/delete/3/')

    assert response.status_code == 200
    assert response.content.count(b'Do you want to delete the post') == 1
    assert response.content.count(b'Task Name 3') == 1

@pytest.mark.django_db
def test_get_task_delete_view_page_with_non_existent_object(client):
    """ Populates the database with data from 
        task/fixtures/dumpdata.json. """

    response = client.get('/delete/99/')

    assert response.status_code == 404    

@pytest.mark.django_db
def test_post_task_delete_view_page(client):
    """ Populates the database with data from 
        task/fixtures/dumpdata.json. """

    response = client.post('/delete/3/', follow=True)

    assert response.status_code == 200
    assert response.content.count(b'Success!') == 1
    assert response.content.count(b'Task deleted successfully!') == 1

    response = client.get('/detail/3/')
    assert response.status_code == 404

