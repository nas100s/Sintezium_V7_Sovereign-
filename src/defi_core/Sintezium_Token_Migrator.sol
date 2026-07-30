// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IERC20 {
    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);
    function transfer(address recipient, uint256 amount) external returns (bool);
}

contract Sintezium_Token_Migrator {
    address public legacySNZ = 0x2E32CCE1b65a4bd0f5375bEa97CAb87596e62e92;
    address public premiumSNZ = 0xAfF9205ebD024ADc92fDe128ba29080266057A0A;
    address public owner = 0x6B84F86583F3272F43c3C69CBAC2aEf5F82881cC;

    function migrate(uint256 amount) external {
        require(IERC20(legacySNZ).transferFrom(msg.sender, address(this), amount), "Transfer failed");
        require(IERC20(premiumSNZ).transfer(msg.sender, amount), "Premium failed");
    }
}
