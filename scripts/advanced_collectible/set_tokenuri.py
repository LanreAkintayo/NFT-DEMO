from brownie import AdvancedCollectible
from scripts.helpful_scripts import get_breed, get_account, OPENSEA_FORMAT

dog_metadata_dic = {
    "PUG": "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmdryoExpgEQQQgJPoruwGJyZmz6SqV4FRTX1i73CT3iXn?filename=1-SHIBA_INU.json",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmbBnUjyHHN7Ytq9xDsYF9sucZdDJLRkWz7vnZfrjMXMxs?filename=2-ST_BERNARD.json",
}

def main():
    account = get_account()
    advancedCollectible = AdvancedCollectible[-1]
    number_of_collectibles = advancedCollectible.tokenCounter()
    print(f"You have {number_of_collectibles} collectibles")
    
    print(f"Setting the token URI of the {number_of_collectibles} collectibles")
    for token_id in range(number_of_collectibles):
        breed_number = advancedCollectible.tokenIdtoBreed(token_id)
        # uint256 tokenId, string memory uri
        breed = get_breed(breed_number)
        
        if not advancedCollectible.tokenURI(token_id).startswith("https://"):
            print(f"Setting token URI of {token_id}")
            token_uri = dog_metadata_dic[breed]
            set_token_uri(token_id, advancedCollectible, token_uri)


    
    print(f"Token URI all set!")

def set_token_uri(token_id, nft_contract, token_uri):
    account = get_account()

    tx = nft_contract.setTokenUri(token_id, token_uri, {"from": account})

    tx.wait(1)

    print(f"Awesome, You can view your NFT at {OPENSEA_FORMAT.format(nft_contract.address, token_id)}")
    print("Please wait up to 20 minutes before you hit the refresh metadata button")
