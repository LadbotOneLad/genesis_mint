import os
from web3 import Web3
import solcx

solcx.install_solc("0.8.20")

# 1. Recursive Merkle Root Calculation for 259 Star Nodes
print("[*] Computing 259-Star Recursive Merkle Root State Proof...")
stars = [f"star_node_id_{i}_sovereign_vector" for i in range(1, 260)]

def hash_leaf(data: str) -> bytes:
    return Web3.solidity_keccak(["string"], [data])

def build_recursive_merkle_tree(leaves):
    layer = leaves
    tree = [layer]
    while len(layer) > 1:
        next_layer = []
        for i in range(0, len(layer), 2):
            left = layer[i]
            right = layer[i+1] if i + 1 < len(layer) else left
            parent = Web3.solidity_keccak(["bytes32", "bytes32"], [left, right])
            next_layer.append(parent)
        tree.append(next_layer)
        layer = next_layer
    return tree

leaves = [hash_leaf(s) for s in stars]
tree = build_recursive_merkle_tree(leaves)
merkle_root = tree[-1][0]
print(f"[+] Merkle Root Anchor Secured: {merkle_root.hex()}")

# 2. Solidity Monolith Code
SOLIDITY_SOURCE = '''
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "https://raw.githubusercontent.com/OpenZeppelin/openzeppelin-contracts/v5.0.0/contracts/token/ERC721/ERC721.sol";
import "https://raw.githubusercontent.com/OpenZeppelin/openzeppelin-contracts/v5.0.0/contracts/access/Ownable.sol";
import "https://raw.githubusercontent.com/OpenZeppelin/openzeppelin-contracts/v5.0.0/contracts/utils/cryptography/MerkleProof.sol";
import "https://raw.githubusercontent.com/OpenZeppelin/openzeppelin-contracts/v5.0.0/contracts/utils/Pausable.sol";
import "https://raw.githubusercontent.com/OpenZeppelin/openzeppelin-contracts/v5.0.0/contracts/utils/ReentrancyGuard.sol";

error DomainAlreadyClaimed(string domain);
error InvalidMerkleProof();
error DomainDoesNotExist(uint256 tokenId);
error InsufficientClaimFee();
error NotTokenOwner();
error DomainNotForSale();
error InsufficientPayment();
error TransferFailed();

contract SovereignWealthDomainRegistry is ERC721, Ownable, Pausable, ReentrancyGuard {
    uint256 private _nextTokenId;
    bytes32 public immutable merkleRoot;
    uint256 public constant CLAIM_FEE = 0.005 ether;

    mapping(uint256 => string) private _tokenNames;
    mapping(string => bool) public domainClaimed;

    mapping(uint256 => uint256) public domainPrices;
    mapping(uint256 => address) public domainSellers;

    event DomainClaimed(address indexed claimant, uint256 indexed tokenId, string domainName);
    event DomainListed(uint256 indexed tokenId, uint256 price);
    event DomainUnlisted(uint256 indexed tokenId);
    event DomainSold(uint256 indexed tokenId, address indexed buyer, address indexed seller, uint256 price);

    constructor(bytes32 _merkleRoot) ERC721("Sovereign Wealth Domain", "SWD") Ownable(msg.sender) {
        merkleRoot = _merkleRoot;
    }

    function pause() external onlyOwner { _pause(); }
    function unpause() external onlyOwner { _unpause(); }

    function claimGenesisDomain(string memory domainName, bytes32[] calldata merkleProof) external payable whenNotPaused nonReentrant {
        if (msg.value < CLAIM_FEE) revert InsufficientClaimFee();
        if (domainClaimed[domainName]) revert DomainAlreadyClaimed(domainName);
        
        bytes32 leaf = keccak256(abi.encodePacked(domainName));
        if (!MerkleProof.verify(merkleProof, merkleRoot, leaf)) revert InvalidMerkleProof();

        domainClaimed[domainName] = true;
        uint256 tokenId = _nextTokenId++;
        _tokenNames[tokenId] = domainName;
        _safeMint(msg.sender, tokenId);

        (bool success, ) = payable(owner()).call{value: msg.value}("");
        if (!success) revert TransferFailed();

        emit DomainClaimed(msg.sender, tokenId, domainName);
    }

    function listDomain(uint256 tokenId, uint256 price) external nonReentrant {
        if (ownerOf(tokenId) != msg.sender) revert NotTokenOwner();
        domainPrices[tokenId] = price;
        domainSellers[tokenId] = msg.sender;
        emit DomainListed(tokenId, price);
    }

    function unlistDomain(uint256 tokenId) external {
        if (ownerOf(tokenId) != msg.sender) revert NotTokenOwner();
        domainPrices[tokenId] = 0;
        domainSellers[tokenId] = address(0);
        emit DomainUnlisted(tokenId);
    }

    function buyDomain(uint256 tokenId) external payable nonReentrant {
        uint256 price = domainPrices[tokenId];
        address seller = domainSellers[tokenId];
        
        if (price == 0) revert DomainNotForSale();
        if (msg.value < price) revert InsufficientPayment();

        domainPrices[tokenId] = 0;
        domainSellers[tokenId] = address(0);

        _safeTransfer(seller, msg.sender, tokenId, "");

        (bool success, ) = payable(seller).call{value: price}("");
        if (!success) revert TransferFailed();

        if (msg.value > price) {
            (bool refundSuccess, ) = payable(msg.sender).call{value: msg.value - price}("");
            if (!refundSuccess) revert TransferFailed();
        }

        emit DomainSold(tokenId, msg.sender, seller, price);
    }

    function getDomainName(uint256 tokenId) external view returns (string memory) {
        if (_ownerOf(tokenId) == address(0)) revert DomainDoesNotExist(tokenId);
        return _tokenNames[tokenId];
    }
}
'''

print("[+] Compiling Solidity Monolith via py-solc-x...")
compiled = solcx.compile_source(
    SOLIDITY_SOURCE,
    output_values=["abi", "bin"],
    solc_version="0.8.20",
    allow_paths="."
)
print("[+] Compilation successful. Ready to broadcast payload.")
