from app import app

def test_home():
    # Setup: Create a test client
    test_client = app.test_client()

    # Exercise: Perform the request
    response = test_client.get('/')

    # Verify: Check the response
    assert b"Welcome to Jenkins Tutorials" in response.data
    assert response.status_code == 200

    # Teardown: (Optional) Clean up any resources used during the test
    # This is automatically called if you use a `with` statement for the test client
