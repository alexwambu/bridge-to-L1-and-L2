
---


```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract BridgeL1 {
    address public admin;
    event Burn(address indexed from, uint256 amount);

    constructor() {
        admin = msg.sender;
    }

    function burn(uint256 amount) external {
        emit Burn(msg.sender, amount);
    }
}
