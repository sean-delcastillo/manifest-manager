import requests
import json

class Manifest:
    remote_manifest_path = "https://raw.githubusercontent.com/sean-delcastillo/modpack-manifest/main/manifest.json"
    local_manifest_path = "./manifest.json"

    def __init__(self, version, projects, manifest):
        self.version = version
        self.projects = projects
        self.manifest = manifest

    def difference_with(self, otherModpack):
        differences = []    

        for project_id in self.projects:
            if project_id not in otherModpack.projects:
                differences.append(project_id)

        return differences

    @staticmethod
    def get_projects(manifest):
        project_ids = []

        for entry in manifest["files"]:
            project_ids.append(entry["projectID"])

        return project_ids
    
    @staticmethod
    def get_remote_manifest():
        manifest_request = requests.get(Manifest.remote_manifest_path)

        if manifest_request.status_code != 200:
            raise RemoteManifestNotAvailableError

        manifest = manifest_request.json()

        return Manifest(version=manifest["version"], projects=Manifest.get_projects(manifest), manifest=manifest)
    
    @staticmethod
    def get_local_manifest():
        with open(Manifest.local_manifest_path, "r") as local_manifest_file:
            manifest = json.loads(local_manifest_file.read())

        return Manifest(version=manifest["version"], projects=Manifest.get_projects(manifest), manifest=manifest)

    @staticmethod
    def is_manifest_versions_equal(manifest_1, manifest_2):
        if manifest_1.version != manifest_2.version:
            return False
        return True

    @staticmethod
    def overwrite_local_manifest(with_manifest):
            with open(Manifest.local_manifest_path, "w") as local_manifest_file:
                json.dump(with_manifest, local_manifest_file, indent=4)


class RemoteManifestNotAvailableError(Exception):
    def __init__(self, status_code, message="Cannot get remote manifest. Status Code: "):
        self.status_code = status_code
        self.message = message + self.status_code
        super().__init__(self.message)