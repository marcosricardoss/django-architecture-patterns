import os
import pytest

from selenium.webdriver.common.keys import Keys

APP_URL = os.environ.get("TESTER_APP_URL")


@pytest.mark.django_db
def test_get_task_update_view(client):
    """Populates the database with data from
    task/fixtures/dumpdata.json."""

    response = client.get("/create/")

    assert response.status_code == 200
    assert response.content.count(b"CREATE TASK") == 1
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
def test_post_task_via_form(client, dates):
    data = {
        "title": "Test Task Title",
        "description": "Task description test.",
        "deadline_at": dates["later"].strftime("%Y-%m-%dT%H:%M"),
        "finished_at": dates["tomorrow"].strftime("%Y-%m-%dT%H:%M"),
    }
    response = client.post("/create/", data, follow=True)
    assert response.status_code == 200
    assert response.content.count(b"Success!") == 1
    assert response.content.count(b"Task created successfully!") == 1
    assert response.content.count(b"Test Task Title") == 1
    assert response.content.count(b"Task description test") == 1


@pytest.mark.django_db
def test_post_task_via_form_with_invalid_data(client, dates):
    data = {
        # MISSING: "title": "Test Task Title",
        "description": "Task description test.",
        # MISSING: "deadline_at": dates["later"].strftime('%Y-%m-%dT%H:%M'),
    }
    response = client.post("/create/", data)
    assert response.status_code == 200
    assert response.content.count(b"CREATE TASK") == 1


@pytest.mark.django_db
def test_task_create_view_page_when_do_click_on_save_button(browser):
    browser.get(f"{APP_URL}/create/")

    assert browser.find_element_by_tag_name("h1").text == "CREATE TASK"
    assert browser.find_element_by_name("csrfmiddlewaretoken")

    page_title = browser.find_element_by_tag_name("h1")
    form = browser.find_element_by_tag_name("form")
    csrfmiddlewaretoken = browser.find_element_by_name("csrfmiddlewaretoken")
    title_field = browser.find_element_by_name("title")
    description_field = browser.find_element_by_name("description")
    deadline_at_field = browser.find_element_by_name("deadline_at")
    finished_at = browser.find_element_by_name("finished_at")
    save_bt = browser.find_element_by_id("save_bt")

    assert form
    assert csrfmiddlewaretoken
    # try to save without task title
    save_bt.click()
    assert page_title.text == "CREATE TASK"
    assert (
        title_field.get_attribute("validationMessage")
        == "Please fill out this field."
    )

    # try to save without deadline date
    title_field.send_keys("Task Title")
    description_field.send_keys("Task description.")
    save_bt.click()
    assert (
        browser.find_element_by_name("deadline_at").get_attribute("validationMessage")
        == "Please fill out this field."
    )

    # try to save with invalida deadline date
    deadline_at_field.send_keys("99999999")
    deadline_at_field.send_keys(Keys.ARROW_RIGHT)
    deadline_at_field.send_keys("9999")
    deadline_at_field.send_keys(Keys.ARROW_DOWN)
    save_bt.click()
    assert (
        browser.find_element_by_name("deadline_at").get_attribute("validationMessage")
        == "Please enter a valid value. The field is incomplete or has an invalid date."
    )

    # fill the a valid deadline date
    deadline_at_field.send_keys("10202021")
    deadline_at_field.send_keys(Keys.ARROW_RIGHT)
    deadline_at_field.send_keys("0821")
    deadline_at_field.send_keys(Keys.ARROW_DOWN)

    # try to save with invalid finished date
    finished_at.send_keys("99999999")
    finished_at.send_keys(Keys.ARROW_RIGHT)
    finished_at.send_keys("9999")
    finished_at.send_keys(Keys.ARROW_DOWN)

    save_bt.click()
    assert (
        finished_at.get_attribute("validationMessage")
        == "Please enter a valid value. The field is incomplete or has an invalid date."
    )

    # fill the a valid finished date
    finished_at.send_keys("10202021")
    finished_at.send_keys(Keys.ARROW_RIGHT)
    finished_at.send_keys("2000")
    finished_at.send_keys(Keys.ARROW_DOWN)

    save_bt.click()

    # assert on task list page
    assert browser.find_element_by_tag_name("h1").text == "TASKS"
    assert (
        browser.find_element_by_xpath("/html/body/div[2]/div[1]/div").text
        == "Success!"
    )
    assert (
        browser.find_element_by_xpath("/html/body/div[2]/div[1]/p").text
        == "Task created successfully!"
    )

    browser.save_screenshot(
        "/usr/src/app/media/test_task_create_view_page_when_do_click_on_save_button.png"
    )
