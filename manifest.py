from typing import Optional, cast
import requests
import json
from modrinth_api import (
    ModrinthProject,
    ModrinthVersionFile,
    get_version_files_from_hashes,
    get_projects,
)


class ModrinthFile:
    """Corresponds to an individual object in a manifest's files list.

    Args:
        file_json (dict): The json-encoded content that corresponds to a
        manifest file.
    """

    def __init__(self, file_json: dict):
        self._dict: dict = file_json
        self.path: str = file_json["path"]
        self.slug: str = self.path.split("/")[-1]
        self.downloads: str = file_json["downloads"]
        self.hashes: dict[str, str] = file_json["hashes"]
        self.version_file: Optional[ModrinthVersionFile] = None
        self.project: Optional[ModrinthProject] = None

    def __str__(self) -> str:
        return self._dict.__str__()


class ModrinthManifest:
    """Corresponds to a whole manifest file.

    Args:
        manifest_json (dict): The json-encoded content that corresponds to a
        manifest.
    """

    remote_url: str = (
        "https://raw.githubusercontent.com/sean-delcastillo/modpack-manifest/main/modrinth.index.json"
    )
    local_path: str = ""

    def __init__(self, manifest_json: dict):
        self._dict: dict = manifest_json
        self.name: str = manifest_json["name"]
        self.format_version: str = manifest_json["formatVersion"]
        self.version_id: str = manifest_json["versionId"]

        files: dict[str, ModrinthFile] = {}
        manifest_files: list[dict] = manifest_json["files"]
        for file_json in manifest_files:
            files.update({file_json["hashes"]["sha1"]: ModrinthFile(file_json)})

        self.files = files

        version_files: dict[str, ModrinthVersionFile] = get_version_files_from_hashes(
            list(files.keys())
        )

        projects: dict[str, ModrinthProject] = get_projects(
            [
                cast(str, file.project_id)
                for file in cast(list[ModrinthVersionFile], version_files.values())
            ]
        )

        for version_file in version_files.values():
            for file in version_file.files:
                file_id: str = file["hashes"]["sha1"]
                if file_id in files:
                    matching_file: ModrinthFile = files[file_id]
                    matching_file.version_file = version_file
                    matching_project: ModrinthProject = projects[
                        cast(str, version_file.project_id)
                    ]
                    matching_file.project = matching_project

        self.files = dict(
            sorted(
                files.items(),
                key=lambda file_element_item: cast(
                    ModrinthProject, cast(ModrinthFile, file_element_item[1]).project
                ).title.lower(),
            )
        )


def read_remote(url: str) -> dict:
    request = requests.get(url)
    request.raise_for_status()
    return request.json()
