import json
import falcon

import io
import os
import uuid
import mimetypes
import msgpack


class Resource(object):

    #_CHUNK_SIZE_BYTES = 4096

    def __init__(self, image_store):
        #self._storage_path = storage_path
        self._image_store = image_store


    def on_get(self,req,resp):
        doc = {
            'images':[
                {
                    'href':'/images/pycharm.jpeg'
                }
            ]
        }

        resp.data = msgpack.packb(doc, use_bin_type=True)
        resp.content_type = falcon.MEDIA_MSGPACK
        resp.status = falcon.HTTP_200

    def on_post(self, req,resp):
        name = self._image_store.save(req.stream, req.content_type)
        resp.status = falcon.HTTP_201
        resp.location = '/images/' + name

class ImageStore(object):

    _CHUNK_SIZE_BYTES = 4096

    def __init__(self,storage_path, uuidgen=uuid.uuid4,fopen=io.open):
        self._storage_path = storage_path
        self._uuidgen = uuidgen
        self._fopen = fopen


    def save (self, image_stream, image_content_type):
        ext = mimetypes.guess_extension((image_content_type))
        name = '{uuid}{ext}'.format(uuid=self._uuidgen(),ext=ext)
        image_path = os.path.join(self._storage_path, name)

        with self._fopen(image_path,'wb') as image_file:
            while True:
                chunk = image_stream.read(self._CHUNK_SIZE_BYTES)
                if not chunk:
                    break

                image_file.write(chunk)

        return name
