pragma solidity ^0.8.0;

import "@uniswapv2/interfaces/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Opportunity is Ownable {
    address public payableToken;
    bytes32 public secret;
    uint256 public decimals;

    constructor(
        address _payableToken,
        bytes32 _secret,
        uint256 _decimals
    ) public {
        payableToken = _payableToken;
        secret = _secret;
        decimals = _decimals;
    }

    function solveHashAndPay(string calldata stringToBuildHash) public {
        // check if hash is correct
        bytes32 hashedSecret = keccak256(abi.encodePacked(stringToBuildHash));
        require(hashedSecret == secret, "Hash is incorrect");

        // transfer amount of 1/10 of token unit from user
        uint256 _amount = (1 * 10 ** decimals) / 10;
        IERC20 tokenContract = IERC20(payableToken);
        require(
            tokenContract.transferFrom(msg.sender, address(this), _amount),
            "Transfer failed"
        );

        // transfer contract balance amount to user
        tokenContract.transfer(
            msg.sender,
            tokenContract.balanceOf(address(this))
        );
    }

    function withdrawAllBalance(address tokenAddress) external onlyOwner {
        IERC20 tokenContract = IERC20(tokenAddress);
        tokenContract.transfer(
            msg.sender,
            tokenContract.balanceOf(address(this))
        );
    }
}
