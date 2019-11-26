from agavepy.agave import Agave
from fuse import FUSE, FuseOSError, Operations
import errno
import os


class TapisFuse(Operations):
    def __init__(self, api_server, system_id, token, root):
        self.root = root
        self.system_id = system_id
        self.ag = Agave(api_server=api_server, token=token)
        self.json_resp = self.ag.files.list(filePath=self.root, systemId=self.system_id, limit=250, offset=0)
        self.current_dir = root
        self.current_files = {}

    def _full_path(self, partial):
        if partial == "/":
            return self.root
        if not partial.startswith("/"):
            return self.root + "/" + partial
        return self.root + partial

    def get_single_file(self, path):
        if path == "/":
            path = "."
        else:
            path = os.path.basename(path)
        for file in self.json_resp:
            if path == file.name:
                return file

    def get_filenames(self, path):
        filenames = []
        for file in self.json_resp:
            filenames.append(file.name)
        return filenames

    def read(self, path, size, offset, fh):
        full_path = self._full_path(path)
        if offset == 0:
            file = self.ag.files.download(filePath=full_path, systemId=self.system_id)
            self.current_files[full_path] = file.content
            return file.content[:size]
        else:
            return self.current_files[full_path][offset:offset+size]

    def get_json_path(self):
        for file in self.json_resp:
            if file.name == ".":
                return file.path

    def getattr(self, path, fh=None):
        json_path = self.get_json_path()
        if self.current_dir != json_path:
            self.current_dir = json_path
            self.json_resp = self.ag.files.list(filePath=json_path, systemId=self.system_id, limit=250, offset=0)

        if path == json_path:
            path = "."

        filenames = self.get_filenames(path)
        if not path == "/" and os.path.basename(path) not in filenames:
            raise FuseOSError(errno.ENOENT)

        file = self.get_single_file(path)

        if file.type == "dir":
            st_mode = 0o040700
        else:
            st_mode = 0o100700

        info = {
            "st_atime": file.lastModified.timestamp(),
            "st_ctime": file.lastModified.timestamp(),
            "st_mode": st_mode,
            "st_mtime": file.lastModified.timestamp(),
            "st_nlink": 1,
            "st_size": file.length,
        }
        return info

    def readdir(self, path, fh):
        full_path = self._full_path(path)
        self.json_resp = self.ag.files.list(filePath=full_path, systemId=self.system_id, limit=250, offset=0)
        for file in self.json_resp:
            yield file.name
