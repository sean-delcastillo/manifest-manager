"""Provides bindings for Modrinth's REST API.

This module contains functions that can be invoked to make common API requests.

Usage:
    from modrinth_api import ModrinthProject, get_project

    project: ModrinthProject = get_project("project_id")
"""

import logging
from typing import TypeAlias, cast
import requests

_user_agent = "sean-delcastillo/manifest-manager"
_default_header = {"user-agent": _user_agent}
_api_url = "https://api.modrinth.com/v2"


class ModrinthProject:
    """Projects are what Modrinth is centered around, be it mods, modpacks,
    resource packs, etc.
    Args:
        project_json (dict): The json-encoded content that corresponds to a
        project.
    """

    def __init__(self, project_json: dict) -> None:
        self._dict: dict = project_json
        self.title: str = project_json["title"]
        self.description: str = project_json["description"]
        self.id: str = project_json["id"]

    def __str__(self) -> str:
        return self._dict.__str__()


class ModrinthVersionFile:
    """Versions can contain multiple files.

    Args:
        version_file_json (dict): The json-encoded content that corresponds to
        a version file.
    """

    def __init__(self, version_file_json: dict) -> None:
        self._dict: dict = version_file_json
        self.name: str = version_file_json["name"]
        self.version_number: str = version_file_json["version_number"]
        self.id: str = version_file_json["id"]
        self.project_id: str = version_file_json["project_id"]
        self.files: list[dict] = version_file_json["files"]

    def __str__(self) -> str:
        return self._dict.__str__()


def _make_get_request(
    route: str, path_parameters: str = "", query_parameters: dict = {}, data: str = ""
) -> dict:
    q_params: str = ""
    for key in query_parameters.keys():
        q_params = f"{q_params}?{key}={query_parameters.get(key)}"
    logging.debug(f"{_api_url}/{route}/{path_parameters}{q_params}")

    request_url: str = f"{_api_url}/{route}"
    if path_parameters != "":
        request_url = request_url + f"/{path_parameters}"

    request: requests.Response = requests.get(
        url=request_url, headers=_default_header, params=query_parameters, data=data
    )
    request.raise_for_status()

    return request.json()


def _make_get_request_without_percent_encoding(
    route: str, path_parameters: str = "", query_parameters: dict = {}, data: str = ""
) -> list[dict]:
    request_url: str = f"{_api_url}/{route}"
    if path_parameters != "":
        request_url = request_url + f"/{path_parameters}"

    q_params: str = ""
    for key in query_parameters.keys():
        q_params += f"?{str(key)}={str(query_parameters[key])}"
    q_params = q_params.replace("'", '"')

    s = requests.Session()
    req = requests.Request("GET", request_url)
    p = req.prepare()
    assert isinstance(p.url, str)
    p.url += q_params

    response: requests.Response = s.send(p)
    response.raise_for_status()

    return response.json()


def _make_post_request(route: str, body: dict) -> dict:

    request_url: str = f"{_api_url}/{route}"

    request: requests.Response = requests.post(url=request_url, json=body)

    request.raise_for_status()

    return request.json()


def get_project(id: str) -> ModrinthProject:
    """Gets a project object.

    Args:
        id (str): The unique project identifier.

    Returns:
        ModrinthProject: The project object.

    Raises:
        HTTPError: A non-successful HTTP code was returned while attemping
        to get the project.
    """
    return ModrinthProject(_make_get_request(route="project", path_parameters=id))


ModrinthProjectId: TypeAlias = str


def get_projects(ids: list[str]) -> dict[ModrinthProjectId, ModrinthProject]:
    """Gets a list of project objects.

    Args:
        ids (list[str]): A list of unique project identifiers.

    Returns:
        dict[ModrinthProjectId, ModrinthProject]: The projects corresponding
        to the given id list argument identified by the projects' id property.

    Raises:
        HTTPError: A non-successful HTTP code was returned while attemping
        to get projects.
    """
    projects_json: list = _make_get_request_without_percent_encoding(
        route="projects", query_parameters={"ids": str(ids)}
    )

    projects: dict[str, ModrinthProject] = {}
    for project_json in projects_json:
        project = ModrinthProject(project_json)
        projects.update({project.id: project})

    return projects


def get_version_file_from_hash(
    hash: str, algorithm: str = "sha1"
) -> ModrinthVersionFile:
    """Gets a version file from a hash identifier.

    Args:
        hash (str): Either a sha1 or sha512 hash that uniquely identifies
        the version file.
        algorithm (str, optional): The hash format of the hash argument.
        Defaults to "sha1".

    Returns:
        ModrinthVersionFile: A version file object
    """
    return ModrinthVersionFile(
        _make_get_request(
            "version_file",
            path_parameters=hash,
            query_parameters={"algorithm": algorithm},
        )
    )


ModrinthVersionId: TypeAlias = str


def get_version_files_from_hashes(
    hashes: list[str], algorithm: str = "sha1"
) -> dict[ModrinthVersionId, ModrinthVersionFile]:
    """Gets version files from a list of hash identifiers.

    Args:
        hashes (list[str]): Either a sha1 or sha512 hash that uniquely
        identifies a version file.
        algorithm (str, optional): The hash format of the hash argument.
        Defaults to "sha1".

    Returns:
        dict[ModrinthVersionId, ModrinthVersionFile]: The version files
        corresponding to the given list of hashes identified by their unique
        version file ID.
    """

    version_files: dict[str, ModrinthVersionFile] = {}
    request_body = {"hashes": hashes, "algorithm": algorithm}
    version_files_json: dict = _make_post_request("version_files", body=request_body)

    for version_file_json in version_files_json.values():
        version: ModrinthVersionFile = ModrinthVersionFile(version_file_json)
        version_files.update({version.id: version})

    return version_files
