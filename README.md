# Manifest Manager

![Image Showing The TUI Interface In Two States: One Where The Manifests Match, and The Other Where They Do Not Match](images/manifest_manager_readme_image.png "Manage Modrinth Manifests The Easy Way!")

A TUI (Terminal User Interface) utility to manage a Modrinth manifest file (.mrpack).

## Usage

### Run the TUI

By invoking the main script

```
python manifest-manager.py
```

You will need to supply two manifests: the remote and the local. The remote manifest accepts a web URL that returns a JSON that matches the mrpack `modrinth.index.json` manifest file format. The local manifest accepts a local path towards a mrpack file.
