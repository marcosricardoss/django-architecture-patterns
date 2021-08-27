import pytest


@pytest.mark.django_db
def test_show_task_detail_view(client):
    """Populates the database with data from
    task/fixtures/dumpdata.json."""

    response = client.get("/detail/3/")

    # finished task
    assert response.status_code == 200
    assert response.content.count(b"Task Name 3") == 1
    assert response.content.count(b"tag-1") == 1
    assert response.content.count(b"tag-2") == 1
    assert response.content.count(b"tag-3") == 1

    # opened task
    response = client.get("/detail/10/")
    assert response.status_code == 200

    # overdue
    response = client.get("/detail/11/")
    assert response.status_code == 200
