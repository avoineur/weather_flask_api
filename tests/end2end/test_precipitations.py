def test_get_precipitations_Le_Havre(client):
    response = client.get("http://test/precipitations?lat=49.49437&lng=0.107929")
    assert response.status_code == 200
