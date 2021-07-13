def test_add_cronjob_view(admin_client):
    response = admin_client.get("/crontab_manager/add", follow=True)
    assert response.status_code == 200
    assert response.content.count(b"Success!") == 1
    assert (
        response.content.count(
            b"All cronjobs were removed from execution successfully!"
        )
        == 1
    )
    assert response.content.count(b"Reload") == 1
    assert response.content.count(b"Remove All") == 1


def test_add_cronjob_admin_view(admin_client):
    response = admin_client.get("/crontab_manager/add-admin/", follow=True)
    assert response.status_code == 200
    assert (
        response.content.count(
            b"All cronjobs were removed from execution successfully!"
        )
        == 1
    )


def test_access_add_all_cronjobs_view_without_being_logged_as_admin_user(client):
    response = client.get("/crontab_manager/add-admin/")
    assert response.status_code == 302
