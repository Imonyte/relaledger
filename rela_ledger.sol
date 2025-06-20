// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract RELALedger {
    struct Loop {
        string loopId;
        string label;
        uint256 modulus;
        int256 semanticCurrent;
        string parentId;
        uint256 timestamp;
    }

    mapping(string => Loop) public loops;

    event LoopValidated(
        string loopId,
        string label,
        uint256 modulus,
        int256 semanticCurrent,
        string parentId,
        uint256 timestamp
    );

    function submitLoop(
        string memory loopId,
        string memory label,
        uint256 modulus,
        int256 semanticCurrent,
        string memory parentId
    ) public {
        loops[loopId] = Loop(
            loopId,
            label,
            modulus,
            semanticCurrent,
            parentId,
            block.timestamp
        );
        emit LoopValidated(loopId, label, modulus, semanticCurrent, parentId, block.timestamp);
    }

    function getLoop(string memory loopId) public view returns (
        string memory,
        string memory,
        uint256,
        int256,
        string memory,
        uint256
    ) {
        Loop memory l = loops[loopId];
        return (l.loopId, l.label, l.modulus, l.semanticCurrent, l.parentId, l.timestamp);
    }
}
