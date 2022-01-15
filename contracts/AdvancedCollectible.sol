pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract AdvancedCollectible is ERC721, VRFConsumerBase{

    bytes32 public keyHash;
    uint256 public fee;

    mapping(bytes32 => address) public requestIdToOwner;
    mapping(uint256 => Breed) public tokenIdtoBreed;
    uint256 public tokenCounter;
    enum Breed{PUG, SHIBA_INU, ST_BERNARD}

    event BreedAssigned(uint256 indexed tokenId, Breed breed);
    event requestedIdToSender(bytes32 indexed requestId, address sender);


    constructor(address _vrfToken, address _linkToken, bytes32 _keyHash, uint256 _fee) public 
    ERC721("Doggie", "Dog")
    VRFConsumerBase(_vrfToken, _linkToken) {
        tokenCounter = 0;
        keyHash = _keyHash;
        fee = _fee;
    }

    function createCollectible() public {
        bytes32 requestId = requestRandomness(keyHash, fee);
        requestIdToOwner[requestId] = msg.sender;
        // Whenever a mapping is updated, always emit an event
        
        emit requestedIdToSender(requestId, msg.sender);

    }

    function fulfillRandomness(bytes32 requestId, uint256 randomness) internal override {
        Breed breed = Breed(randomness % 3);
        uint256 tokenId = tokenCounter;
        tokenIdtoBreed[tokenId] = breed;
        
        emit BreedAssigned(tokenId, breed);

        address owner = requestIdToOwner[requestId];
        
        _safeMint(owner, tokenId);

        tokenCounter ++;
        
    }

    function setTokenUri(uint256 tokenId, string memory uri) public{
        // This should only be set by the owner of the token represented by the token URI
        require(_isApprovedOrOwner(_msgSender(), tokenId), "Can only be set by the owner");

        _setTokenURI(tokenId, uri);
    }

}