// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract SovereignDomain is ERC721, Ownable {
    uint256 private _nextTokenId;
    
    // Mapping from token ID to domain name string (e.g., "ghostnet.tg")
    mapping(uint256 => string) private _domainNames;
    
    // Mapping from domain name hash to existence check
    mapping(string => bool) public domainExists;

    constructor() ERC721("Sovereign Network Domain", "SND") Ownable(msg.sender) {}

    function registerDomain(address recipient, string memory domainName) public onlyOwner returns (uint256) {
        require(!domainExists[domainName], "Domain already registered");
        
        uint256 tokenId = _nextTokenId++;
        _safeMint(recipient, tokenId);
        
        _domainNames[tokenId] = domainName;
        domainExists[domainName] = true;
        
        return tokenId;
    }

    function getDomainName(uint256 tokenId) public view returns (string memory) {
        require_owner_exists(tokenId);
        return _domainNames[tokenId];
    }

    function require_owner_exists(uint256 tokenId) internal view {
        // Built-in ownership check via OpenZeppelin base contract
        address owner = ownerOf(tokenId);
        require(owner != address(0), "Domain query for nonexistent token");
    }
}
