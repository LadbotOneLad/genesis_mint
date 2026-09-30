// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Strings.sol";

contract FullyOnChainSovereign is ERC721, Ownable {
    using Strings for uint256;
    uint256 private _nextTokenId;

    mapping(uint256 => string) private _namespaces;

    constructor() ERC721("Fully On-Chain Sovereign Root", "FOCR") Ownable(msg.sender) {}

    function mintSovereignNode(address recipient, string memory namespace) public onlyOwner returns (uint256) {
        uint256 tokenId = _nextTokenId++;
        _safeMint(recipient, tokenId);
        _namespaces[tokenId] = namespace;
        return tokenId;
    }

    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        require_token_exists(tokenId);
        string memory ns = _namespaces[tokenId];
        
        // Constructing fully on-chain JSON metadata payload
        return string(
            abi.encodePacked(
                'data:application/json;utf8,{"name": "Sovereign Node #', tokenId.stringUtils(), 
                '", "description": "Absolute on-chain sovereign infrastructure handle", "attributes": [{"trait_type": "Namespace", "value": "', ns, '"}]}'
            )
        );
    }

    function require_token_exists(uint256 tokenId) internal view {
        address owner = ownerOf(tokenId);
        require(owner != address(0), "URI query for nonexistent token");
    }
}
