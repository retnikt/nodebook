def test_openapi_json(client):
    response = client.get("/api/openapi.json")
    assert response.status_code == 200
    assert response.json()


def test_redoc_html(client):
    # this should probably be tested with puppeteer
    response = client.get("/api/")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert response.text
