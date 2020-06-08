from urlshort import create_app

# We are passing client to simulate that user is accessing web browser.
def test_shorten(client):

    # Let we visit home page
    response = client.get('/')

    # Let check if there is any String 'Shorten' on the home page(hint: it is the submit button to get short url)
    assert b'Shorten' in response.data

# Here the test file must start with test_......

# Go to terminal and run command=> pytest

# output

# test_main.py .                                [100%]

# ================= 1 passed in 0.09s =================