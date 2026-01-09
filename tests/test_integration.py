def test_create_weather_api(client, mocker):

    fake_api_response = {
        "main": {"temp": 35, "humidity": 60},
        "weather": [{"main": "Sunny"}],
        "wind": {"speed": "5.0"}
    }

    # Mock external API call
    mocker.patch(
        "app.external.fetch_weather",
        return_value=fake_api_response
    )

    response = client.post("/weather", json={"city": "Chennai"})

    assert response.status_code == 201

    data = response.json()
    assert data["city"] == "Chennai"
    assert data["temperature"] == 35
    assert data["weather"] == "Sunny"
