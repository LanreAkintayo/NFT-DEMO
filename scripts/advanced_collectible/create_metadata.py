from scripts.meta_data_template import metadata_template
from brownie import AdvancedCollectible, network, config
from scripts.helpful_scripts import get_breed
from pathlib import Path
import json
import requests
import os

breed_to_image_uri = {
    "PUG": "https://ipfs.io/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8?filename=pug.png",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmYx6GsYAKnNzZ9A6NvEKV9nf1VaDzJrqDR23Y8YSkebLU?filename=shiba-inu.png",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmUPjADFGEKmfohdTaNcWhp7VGk26h5jXDA7v3VtTnTLcW?filename=st-bernard.png",
}

def main():
    advancedCollectible = AdvancedCollectible[-1]
    number_of_collectibles = advancedCollectible.tokenCounter()
    print(f"We have {number_of_collectibles} collectibles")

    for tokenId in range(number_of_collectibles):
        breed_number = advancedCollectible.tokenIdtoBreed(tokenId)
        breed = get_breed(breed_number)
        # tokenId: 0 breed_number = 0
        # tokenId: 1 breed_number = 2
        metadata_filename = f"./metadata/{network.show_active()}/{tokenId}-{breed}.json"
        if Path(metadata_filename).exists():
            print(f"{metadata_filename} already existed. Delete this to override")

        else:
            print(f"Creating {metadata_filename} ... ")
            collectible_metadata = metadata_template
            collectible_metadata["name"] = breed
            collectible_metadata["description"] = f"An adorable {breed} pup!"

            image_uri = None
            image_path = "./img/" + breed.lower().replace("_", "-") + ".png"

            if os.getenv("UPLOADI_IPFS") == "true":
                image_uri = upload_to_ipfs(image_path)
            
            image_uri = image_uri if image_uri else breed_to_image_uri[breed]

            collectible_metadata["imageURI"] = image_uri

            with open(metadata_filename, "w") as file:
                json.dump(collectible_metadata, file)
            
            if os.getenv("UPLOAD_IPFS") == "true":
                upload_to_ipfs(metadata_filename)


def upload_to_ipfs(file_path):
    with Path(file_path).open("rb") as image:
        image_binary = image.read()

        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        image_hash = response.json()["Hash"]

        filename = file_path.split("/")[-1:][0]

        # https://ipfs.io/ipfs/<imageHash>?filename=<imageName>
        image_uri = f"https://ipfs.io/ipfs/{image_hash}?filename={filename}"

        print(f"Image URI: {image_uri}")
        return image_uri




""" {
  "name": "SHIBA_INU",
  "description": "An adorable SHIBA_INU pup!",
  "imageURI": "https://ipfs.io/ipfs/QmYx6GsYAKnNzZ9A6NvEKV9nf1VaDzJrqDR23Y8YSkebLU?filename=shiba-inu.png",
  "attributes": [{ "trait_type": "cuteness", "value": "100" }]
}
"""