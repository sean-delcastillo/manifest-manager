from manifest import ModrinthManifest
import requests 


def main():
    request = requests.get(ModrinthManifest.remote_url)

    if request.status_code != 200:
        print(f"Error status: {requests.status_code}")
        return
    
    manifest = ModrinthManifest(request.json())

    print(f"{manifest.name}, {manifest.format_version}, {manifest.version_id}")

    for file in manifest.files:
        print(f"{file.project.title}")

main()