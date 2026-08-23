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


def test_families_units_and_error_contracts():
    with app.test_client() as client:
        assert client.get('/').status_code == 200
        assert client.get('/api/families').get_json()['families']['Length']
        assert client.get('/api/units/Length').status_code == 200
        assert client.get('/api/units/Unknown').status_code == 404
        assert client.post('/api/convert', json={'value': 1, 'from_unit': 'meter', 'to_unit': 'not-a-unit'}).status_code == 400
        assert client.post('/api/convert', json={}).status_code == 400
        assert client.post('/api/expressions', json={'expression': '10 meter', 'target': 'centimeter'}).get_json()['result'] == 1000
        assert client.post('/api/expressions', json={}).status_code == 400
        assert client.post('/api/expressions', json={'expression': 'not a quantity'}).status_code == 400


def test_v1_contract_temperature_modes_and_help():
    with app.test_client() as client:
        assert client.get('/help').status_code == 200
        assert 'Length' in client.get('/api/v1/units/families').get_json()['families']
        assert client.get('/api/v1/units/units?family=pressure').status_code == 200
        absolute = client.post('/api/v1/units/convert', json={
            'value': 25, 'from': 'degC', 'to': 'kelvin', 'mode': 'absolute'
        })
        interval = client.post('/api/v1/units/convert', json={
            'value': 25, 'from': 'degC', 'to': 'kelvin', 'mode': 'interval'
        })
        mismatch = client.post('/api/v1/units/convert', json={
            'value': 1, 'from': 'meter', 'to': 'second'
        })
    assert absolute.get_json()['result'] == 298.15
    assert interval.get_json()['result'] == 25
    assert mismatch.status_code == 400
    assert mismatch.get_json()['error_code'] == 'DIMENSION_MISMATCH'
    assert absolute.headers['X-Content-Type-Options'] == 'nosniff'
