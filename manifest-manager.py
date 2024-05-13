from manifest import Manifest


def main():
    remote = Manifest.get_remote_manifest()
    local = Manifest.get_local_manifest()
    
    if Manifest.is_manifest_versions_equal(remote, local):
        print(f"Your modpack is already up-to-date. Version {remote.version}")
        wait_for_key()
        return
      
    print(f"Your modpack is not up-to-date. Your version {local.version} != latest version {remote.version}")

    Manifest.overwrite_local_manifest(remote.manifest)    

    wait_for_key()


def wait_for_key(label = ""):
    if label != "":
        input(f"{label}. Press Enter to continue.")
    else:
        input("Press Enter to continue.")


if __name__ == "__main__":
    main()