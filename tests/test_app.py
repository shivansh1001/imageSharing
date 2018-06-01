from typing import Dict, List

import falcon
from falcon import testing
import msgpack
import pytest
from look.app import api
from unittest.mock import mock_open,call

def test_posted_image_gets_saved(client, monkeypatch):
    mock_file_open = mock_open()
    monkeypatch.setattr('io.open', mock_file_open)

    fake_uuid = '123e4567-e89b-12d3-a456-426655440000'
    monkeypatch.setattr('uuid.uuid4',lambda :fake_uuid)

    fake_image_bytes = b'fake-image-bytes'
    response = client.simulate_post(
        '/images',
        body = fake_image_bytes,
        headers={'content-type':'image/png'}
    )

    assert response.status == falcon.HTTP_CREATED
    assert call().write(fake_image_bytes) in mock_file_open.mock_calls
    assert response.headers['location'] == '/images/{}.png'.format(fake_uuid)

@pytest.fixture()
def client():
    return testing.TestClient(api)


def test_list_images(client):
    doc = {
        'images': [
            {
                'href': '/images/pycharm.jpeg'
            }
        ]
    }

    response = client.simulate_get('/images')
    result_doc = msgpack.unpackb(response.content, encoding='utf-8')

    assert result_doc == doc
    assert response.status == falcon.HTTP_OK