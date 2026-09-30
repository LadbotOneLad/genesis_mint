// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";

contract SovereignLiquidityVault is Ownable {
    event LiquidityIngested(address indexed sender, uint256 amount, uint256 timestamp);
    event LiquidityDispatched(address indexed recipient, uint256 amount, string purpose);

    constructor() Ownable(msg.sender) {}

    // Allow the vault to ingest native chain liquidity autonomously
    receive() external payable {
        emit LiquidityIngested(msg.sender, msg.value, block.timestamp);
    }

    // Autonomous execution: route liquidity to internal operational nodes or contracts
    function dispatchLiquidity(address payable recipient, uint256 amount, string memory purpose) public onlyOwner {
        require(address(this).balance >= amount, "Insufficient vault liquidity for dispatch");
        (bool success, ) = recipient.call{value: amount}("");
        require(success, "Liquidity transfer failed");
        
        emit LiquidityDispatched(recipient, amount, purpose);
    }

    // Check current autonomous reserves
    function getVaultBalance() public view returns (uint256) {
        return address(this).balance;
    }
}
