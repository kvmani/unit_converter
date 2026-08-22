from app import app


def test_health_and_conversion():
    with app.test_client() as client:
        assert client.get('/api/health').get_json()['tool_id'] == 'unit-converter'
        response = client.post('/api/convert', json={'value': 1, 'from_unit': 'meter', 'to_unit': 'centimeter'})
    assert response.status_code == 200
    assert response.get_json()['result'] == 100


def test_expression_conversion():
    with app.test_client() as client:
        response = client.post('/api/expressions', json={'expression': '2 kg * 9.81 m/s^2 to N'})
    assert response.status_code == 200
    assert abs(response.get_json()['result'] - 19.62) < 1e-8
