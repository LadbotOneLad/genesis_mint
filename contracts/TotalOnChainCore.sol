// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";

contract TotalOnChainCore is Ownable {
    struct SystemState {
        uint256 timestamp;
        string nodeIdentity;
        bytes32 entropySeal;
        uint256 unifiedVector;
    }

    // Mapping from state version index to immutable on-chain system record
    mapping(uint256 => SystemState) public stateRegistry;
    uint256 public totalStateRecords;

    event StateAnchored(uint256 indexed version, string nodeIdentity, bytes32 entropySeal);

    constructor() Ownable(msg.sender) {}

    function anchorSystemState(
        string memory nodeIdentity, 
        bytes32 entropySeal, 
        uint256 unifiedVector
    ) public onlyOwner {
        uint256 version = totalStateRecords++;
        
        stateRegistry[version] = SystemState({
            timestamp: block.timestamp,
            nodeIdentity: nodeIdentity,
            entropySeal: entropySeal,
            unifiedVector: unifiedVector
        });

        emit StateAnchored(version, nodeIdentity, entropySeal);
    }

    function getStateRecord(uint256 version) public view returns (SystemState memory) {
        require(version < totalStateRecords, "State record does not exist on-chain");
        return stateRegistry[version];
    }
}
