// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Permit.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Votes.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/metatx/ERC2771Context.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

/**
 * @title ILegacySintezium
 * @dev Interface for the original Sintezium contract (0x2E32...).
 */
interface ILegacySintezium {
    function balanceOf(address account) external view returns (uint256);
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
}

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
 * @title Sintezium_V7_Absolute_Final
 * @dev The absolute realization of Element 119 with On-chain Lineage, Migration Portal, and Chislobog Time Cycles.
 */
contract Sintezium_V7_Absolute_Final is ERC20, ERC20Permit, ERC20Votes, AccessControl, ERC2771Context, ReentrancyGuard, SinteziumPRM_V7 {
    
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    bytes32 public constant CHISLOBOG_ROLE = keccak256("CHISLOBOG_ROLE");

    // --- Lineage & Migration ---
    address public constant LEGACY_VERSION = 0x2E32CCE1b65a4bd0f5375bEa97CAb87596e62e92;
    address public constant BURN_ADDRESS = 0x000000000000000000000000000000000000dEaD;
    
    // --- System Constants ---
    uint256 public constant Z = 119;
    uint256 public constant RESONANCE_MATRIX = 333;
    uint256 public stabilityIndex = 100;

    // --- Chislobog Cycles (Time/Elements) ---
    uint256 public currentSvarogCycle;
    uint256 public lastCycleUpdate;
    uint256 public constant CYCLE_PERIOD = 25920; // Slavic Great Year approximation (seconds for simulation or blocks)

    mapping(address => mapping(address => bool)) public atomicBonds;
    
    event MetabolismPulse(uint256 metabolism, bool isContracted);
    event LegacyMigrated(address indexed user, uint256 amount);
    event AtomicBondCreated(address indexed from, address indexed to);
    event SvarogCycleShifted(uint256 indexed cycle, uint256 timestamp);

    constructor(address forwarder) 
        ERC20("Sintezium Sovereign Final", "Snz") 
        ERC20Permit("Sintezium Sovereign Final") 
        ERC2771Context(forwarder) 
    {
        _grantRole(DEFAULT_ADMIN_ROLE, _msgSender());
        _grantRole(ADMIN_ROLE, _msgSender());
        _grantRole(MINTER_ROLE, _msgSender());
        _grantRole(CHISLOBOG_ROLE, _msgSender());

        lastCycleUpdate = block.timestamp;

        // Initial awakening supply
        _mint(_msgSender(), 119888 * 10**decimals());
    }

    // --- Chislobog Governance ---

    function executeSvarogCycle() external onlyRole(CHISLOBOG_ROLE) {
        currentSvarogCycle++;
        lastCycleUpdate = block.timestamp;
        
        // Cycle shifts affect stability periodically
        stabilityIndex = 100 + (currentSvarogCycle % 119);
        
        emit SvarogCycleShifted(currentSvarogCycle, block.timestamp);
    }

    // --- Migration Portal ---

    function migrateLegacy(uint256 amount) external nonReentrant {
        require(amount > 0, "Migration: Zero amount");
        
        bool success = ILegacySintezium(LEGACY_VERSION).transferFrom(_msgSender(), BURN_ADDRESS, amount);
        require(success, "Migration: Legacy transfer failed. Check allowance.");

        _mint(_msgSender(), amount);

        emit LegacyMigrated(_msgSender(), amount);
    }

    // --- Core Metabolism Logic ---

    function calculateMetabolism() public view returns (uint256 metabolism, bool isContracted) {
        uint256 gasPrice = tx.gasprice / 1 gwei;
        uint256 timeBonus = (block.timestamp - lastCycleUpdate) / 3600; // Hourly bonus
        
        uint256 logFactor = gasPrice > 50 ? (gasPrice > 100 ? 4 : 3) : 1;
        metabolism = (Z * (stabilityIndex + timeBonus)) / (logFactor + 1);
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
                _addOrbital(keccak256(abi.encodePacked(from, to, block.timestamp, currentSvarogCycle)));
            }
            
            emit MetabolismPulse(m, contracted);
        }
        super._update(from, to, value);
    }

    // --- Admin Operations ---

    function adjustStability(uint256 newIndex) external onlyRole(ADMIN_ROLE) {
        stabilityIndex = newIndex;
    }

    function extractEnergy() external onlyRole(ADMIN_ROLE) nonReentrant {
        uint256 ethBalance = address(this).balance;
        if (ethBalance > 0) payable(_msgSender()).transfer(ethBalance);
        uint256 snzBalance = balanceOf(address(this));
        if (snzBalance > 0) _transfer(address(this), _msgSender(), snzBalance);
    }

    // --- Standard Overrides ---

    function _msgSender() internal view override(Context, ERC2771Context) returns (address) {
        return ERC2771Context._msgSender();
    }

    function _msgData() internal view override(Context, ERC2771Context) returns (bytes calldata) {
        return ERC2771Context._msgData();
    }

    function _contextSuffixLength() internal view override(Context, ERC2771Context) returns (uint256) {
        return ERC2771Context._contextSuffixLength();
    }

    function nonces(address owner) public view override(ERC20Permit, Nonces) returns (uint256) {
        return super.nonces(owner);
    }

    receive() external payable {}
}
