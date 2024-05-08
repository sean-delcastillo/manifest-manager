import requests;

manifest_resource_path = "https://raw.githubusercontent.com/sean-delcastillo/modpack-manifest/main/manifest.json"


def main():
    manifest_resource = requests.get(manifest_resource_path)

if __name__ == "__main__":
    main()