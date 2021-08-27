import pytest


@pytest.mark.django_db
def test_get_task_update_view(client):
    """Populates the database with data from
    task/fixtures/dumpdata.json."""

    response = client.get("/update/3/")

    assert response.status_code == 200
    assert response.content.count(b"UPDATE TASK") == 1
    assert response.content.count(b"tag-1") == 1
    assert response.content.count(b"tag-2") == 1
    assert response.content.count(b"tag-3") == 1
    assert (
        response.content.count(
            b'<input id="save_bt" type="submit" value="Save" class="ui green button">'
        )
        == 1
    )


@pytest.mark.django_db
def test_update_task_via_form(client, dates):
    data = {
        "title": "Task Edited",
        "description": "Task description edited.",
        "deadline_at": dates["later"].strftime("%Y-%m-%dT%H:%M"),
        "finished_at": dates["tomorrow"].strftime("%Y-%m-%dT%H:%M"),
    }
    response = client.post("/update/3/", data, follow=True)
    assert response.status_code == 200
    assert response.content.count(b"Success!") == 1
    assert response.content.count(b"Task updated successfully!") == 1
    assert response.content.count(b"Task Edited") == 1
    assert response.content.count(b"Task description edited.") == 1


@pytest.mark.django_db
def test_update_a_non_existent_task_via_form(client, dates):
    data = {
        "title": "Task Edited",
        "description": "Task description edited.",
        "deadline_at": dates["later"].strftime("%Y-%m-%dT%H:%M"),
        "finished_at": dates["tomorrow"].strftime("%Y-%m-%dT%H:%M"),
    }
    response = client.post("/update/999", data, follow=True)
    assert response.status_code == 404


@pytest.mark.django_db
def test_post_task_via_form_with_invalid_data(client):
    data = {
        "title": "Task title",
        "description": "Task description test.",
        "deadline_at": "9999-99-99T99:99",
        "finished_at": "9999-99-99T99:99",
    }
    response = client.post("/update/3/", data, follow=True)
    assert response.status_code == 200
    # assert response.content.count(b'UPDATE TASK') == 1
    # assert response.content == 1
