// SPDX-License-Identifier: CC-BY-NC-SA-4.0
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/extensions/ERC4626.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract SinteziumVault4626 is ERC4626 {
    // В качестве базового актива выступает Legacy SNZ (0x2E32...)
    constructor(IERC20 _asset) ERC4626(_asset) ERC20("Staked Sintezium Yield", "sSNZ") {}

    // Хранилище принимает выкупленные с рынка токены SNZ и генерирует доходность
    function totalAssets() public view virtual override returns (uint256) {
        return super.totalAssets();
    }
}
