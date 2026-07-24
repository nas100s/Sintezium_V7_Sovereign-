// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Permit.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Votes.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/metatx/ERC2771Context.sol";

/**
 * @title SinteziumPRM_V7
 * @dev Periodic Resource Management V7 with enhanced shell logic.
 */
abstract contract SinteziumPRM_V7 {
    enum ShellType { Core, Yield, Discovery, Expansion, Sovereign }
    struct Shell {
        uint256 id;
        uint256 capacity;
        uint256 filled;
        bool isClosed;
        ShellType shellType;
    }

    uint256 public currentZ;
    uint256 public activeShellId;
    mapping(uint256 => Shell) public shells;
    mapping(uint256 => mapping(uint256 => bytes32)) public orbitals;

    event OrbitalAdded(uint256 indexed shellId, uint256 indexed orbitalId, bytes32 dataAnchor);
    event ShellClosed(uint256 indexed shellId, uint256 complexityZ);
    event NewShellCreated(uint256 indexed shellId, uint256 capacity);

    constructor() {
        _createNewShell(2);
    }

    function _addOrbital(bytes32 dataAnchor) internal {
        Shell storage shell = shells[activeShellId];
        if (shell.isClosed) {
            _createNewShell(shell.capacity + 10);
            shell = shells[activeShellId];
        }
        
        orbitals[activeShellId][shell.filled] = dataAnchor;
        shell.filled++;
        currentZ++;

        emit OrbitalAdded(activeShellId, shell.filled - 1, dataAnchor);

        if (shell.filled >= shell.capacity) {
            _closeActiveShell();
        }
    }

    function _closeActiveShell() internal {
        Shell storage shell = shells[activeShellId];
        shell.isClosed = true;
        emit ShellClosed(activeShellId, currentZ);
    }

    function _createNewShell(uint256 capacity) internal {
        activeShellId++;
        Shell storage shell = shells[activeShellId];
        shell.id = activeShellId;
        shell.capacity = capacity;
        
        if (activeShellId == 1) shell.shellType = ShellType.Core;
        else if (activeShellId == 2) shell.shellType = ShellType.Yield;
        else if (activeShellId == 3) shell.shellType = ShellType.Discovery;
        else if (activeShellId == 7) shell.shellType = ShellType.Sovereign;
        else shell.shellType = ShellType.Expansion;

        emit NewShellCreated(activeShellId, capacity);
    }
}

/**
 * @title Sintezium_Sovereign_V7
 * @dev The absolute realization of Element 119 with Governance and Meta-transaction support.
 */
contract Sintezium_Sovereign_V7 is ERC20, ERC20Permit, ERC20Votes, AccessControl, ERC2771Context, SinteziumPRM_V7 {
    
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");

    uint256 public constant Z = 119;
    uint256 public constant RESONANCE_MATRIX = 333;
    uint256 public stabilityIndex = 100;

    mapping(address => mapping(address => bool)) public atomicBonds;
    
    event MetabolismUpdate(uint256 metabolism, bool isContracted);
    event AtomicBondCreated(address indexed from, address indexed to);
    event EnergyExtracted(uint256 ethAmount, uint256 snzAmount);

    constructor(address forwarder) 
        ERC20("Sintezium", "Snz") 
        ERC20Permit("Sintezium") 
        ERC2771Context(forwarder) 
    {
        _grantRole(DEFAULT_ADMIN_ROLE, _msgSender());
        _grantRole(ADMIN_ROLE, _msgSender());
        _grantRole(MINTER_ROLE, _msgSender());

        _mint(_msgSender(), 333888 * 10**decimals());
    }

    // --- Core Logic ---

    function calculateMetabolism() public view returns (uint256 metabolism, bool isContracted) {
        uint256 gasPrice = tx.gasprice / 1 gwei;
        uint256 logFactor = 1;
        if (gasPrice > 150) logFactor = 5;
        else if (gasPrice > 100) logFactor = 4;
        else if (gasPrice > 50) logFactor = 3;
        else if (gasPrice > 20) logFactor = 2;

        metabolism = (Z * stabilityIndex) / (logFactor + 1);
        isContracted = (gasPrice > 50);
    }

    function _update(address from, address to, uint256 value) internal override(ERC20, ERC20Votes) {
        if (from != address(0) && to != address(0)) {
            (uint256 m, bool contracted) = calculateMetabolism();
            
            if (contracted) {
                uint256 tax = value / 100;
                super._update(from, address(this), tax);
                value -= tax;
            }
            
            if (!atomicBonds[from][to]) {
                atomicBonds[from][to] = true;
                emit AtomicBondCreated(from, to);
                _addOrbital(keccak256(abi.encodePacked(from, to, block.timestamp)));
            }
        }
        super._update(from, to, value);
    }

    // --- Admin Functions ---

    function setStability(uint256 newIndex) external onlyRole(ADMIN_ROLE) {
        stabilityIndex = newIndex;
    }

    function mint(address to, uint256 amount) external onlyRole(MINTER_ROLE) {
        _mint(to, amount);
    }

    /**
     * @dev Emergency extraction of retained tax/energy (ETH and Snz).
     */
    function extractEnergy() external onlyRole(ADMIN_ROLE) {
        uint256 ethBalance = address(this).balance;
        if (ethBalance > 0) {
            payable(_msgSender()).transfer(ethBalance);
        }
        uint256 snzBalance = balanceOf(address(this));
        if (snzBalance > 0) {
            _transfer(address(this), _msgSender(), snzBalance);
        }
        emit EnergyExtracted(ethBalance, snzBalance);
    }

    // --- Overrides ---

    function _msgSender() internal view override(Context, ERC2771Context) returns (address) {
        return ERC2771Context._msgSender();
    }

    function _msgData() internal view override(Context, ERC2771Context) returns (bytes calldata) {
        return ERC2771Context._msgData();
    }

    function nonces(address owner) public view override(ERC20Permit, Nonces) returns (uint256) {
        return super.nonces(owner);
    }

    receive() external payable {}
}
