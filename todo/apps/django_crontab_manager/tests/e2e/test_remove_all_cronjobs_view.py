def test_run_cronjob_view(admin_client):
    response = admin_client.get("/crontab_manager/remove", follow=True)
    assert response.status_code == 200
    assert response.content.count(b"Success!") == 1
    assert response.content.count(b"All cronjobs were removed successfully!") == 1
    assert response.content.count(b"Run All") == 1
    assert response.content.count(b"Remove All") == 1


def test_run_cronjob_admin_view(admin_client):
    response = admin_client.get("/crontab_manager/remove-admin/", follow=True)
    assert response.status_code == 200
    assert response.content.count(b"All cronjobs were removed successfully!") == 1


def test_access_add_all_cronjobs_view_without_being_logged_as_admin_user(client):
    response = client.get("/crontab_manager/remove")
    assert response.status_code == 301
