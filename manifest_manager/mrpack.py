import pathlib
from typing import Optional
import zipfile
import tempfile
import shutil
import json


class MrPack:
    def __init__(self, path: pathlib.Path | str) -> None:
        self.path: pathlib.Path = (
            path if isinstance(path, pathlib.Path) else pathlib.Path(path)
        )

    def _get_extracted_files(self) -> dict[zipfile.ZipInfo, str]:
        extracted_files: dict[zipfile.ZipInfo, str] = {}

        with zipfile.ZipFile(self.path, "r") as manifest_archive:
            with tempfile.TemporaryDirectory() as tmpdirname:
                for member_info in manifest_archive.infolist():
                    file_content = manifest_archive.extract(member_info, tmpdirname)
                    extracted_files.update({member_info: file_content})

                return extracted_files

    def copy_manifest(
        self, src_manifest: dict, new_pack_dest: Optional[pathlib.Path | str] = None
    ):
        """Copies a manifest dictionary into MrPack's manifest file, replacing the existing manifest file. If given a
        new pack destination instead creates a new .mrpack archive.

        Args:
            src_manifest (dict): A new manifest dictionary to write into file.
            new_pack_dest (Optional[pathlib.Path  |  str], optional): New pack destination. Defaults to None.
        """
        if new_pack_dest is None:
            new_pack_dest = self.path
        else:
            new_pack_dest = (
                new_pack_dest
                if isinstance(new_pack_dest, pathlib.Path)
                else pathlib.Path(new_pack_dest)
            )

        with tempfile.TemporaryDirectory() as tmpdirname:
            tmp_archive = pathlib.Path(tmpdirname).joinpath("tmparchive")
            with zipfile.ZipFile(tmp_archive, "x") as archive:
                for zip_info, file_content in self._get_extracted_files().items():
                    if zip_info.filename.startswith("overrides/"):
                        archive.writestr(zip_info, file_content)

                archive.writestr(
                    "modrinth.index.json", json.dumps(src_manifest, indent=4)
                )

            shutil.copy2(
                tmp_archive,
                new_pack_dest,
            )
