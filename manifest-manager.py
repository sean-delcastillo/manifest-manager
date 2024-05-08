import requests
import json
from time import sleep
from sys import platform

remote_manifest_resource_path = "https://raw.githubusercontent.com/sean-delcastillo/modpack-manifest/main/manifest.json"
local_manifest_path = "./manifest.json"


def main():
    manifest_request = requests.get(remote_manifest_resource_path)

    if manifest_request.status_code != 200:
        print(f"Cannot download remote manifest: Status {manifest_request.status_code}")

    remote_manifest = manifest_request.json()

    with open(local_manifest_path, "r") as local_manifest_file:
        local_manifest = json.loads(local_manifest_file.read())
        
    if remote_manifest["version"] == local_manifest["version"]:
        print(f"Your modpack is already up-to-date. Version {remote_manifest['version']}")
        wait_for_key()
        return

      
    print(f"Your modpack is not up-to-date. Your version {local_manifest['version']} != latest version {remote_manifest['version']}")
    sleep(1)
    
    print("Downloading remote manifest...")
    sleep(1)
   
    print("Applying updates to local modpack...")

    with open(local_manifest_path, "w") as local_manifest_file:
        json.dump(remote_manifest, local_manifest_file, indent=4)

    sleep(2)
    
    print("Done! Please re-zip this folder and import it back into Curseforge.")

    wait_for_key()


def wait_for_key():
    input("Press Enter to continue.")


if __name__ == "__main__":
    main()