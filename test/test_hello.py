from nano_gpodder_server.hello import hello


def test_hello():
    assert hello() == "hello!"
