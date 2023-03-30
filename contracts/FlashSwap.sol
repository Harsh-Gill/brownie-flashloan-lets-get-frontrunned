pragma solidity ^0.8.0;

import "@uniswapv2/interfaces/IERC20.sol";
import "@uniswapv2/interfaces/IUniswapV2Pair.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "./Opportunity.sol";

contract FlashSwapPancake is Ownable {
    IUniswapV2Pair internal poolContract;

    event ReceivedLoan(
        address indexed sender,
        uint256 receivedAmount,
        uint256 totalBalance
    );
    event RepaymentFees(address indexed sender, uint256 amount);

    function borrowFlashloan(
        address poolAddress,
        address tokenBorrowAddress,
        bool isBorrow0,
        uint256 amount,
        bytes calldata data
    ) external onlyOwner {
        // choose token to borrow
        uint256 amount0;
        uint256 amount1;

        if (isBorrow0) {
            amount0 = amount;
        } else {
            amount1 = amount;
        }

        // load pool interface for actions
        poolContract = IUniswapV2Pair(poolAddress);

        // borrow flashloan to this address by inculding non zero data argument
        IUniswapV2Pair(poolAddress).swap(amount0, amount1, address(this), data);
    }

    function pancakeCall(
        address _sender,
        uint256 _amount0,
        uint256 _amount1,
        bytes calldata _data
    ) external {
        // decode data
        (
            bool isBorrow0,
            uint256 amount,
            address tokenBorrowAddress,
            address OpportunityAddress,
            string memory secret
        ) = abi.decode(_data, (bool, uint256, address, address, string));

        // check to see if balance of borrowed token has increased
        IERC20 tokenContract = IERC20(tokenBorrowAddress);
        uint256 balance = tokenContract.balanceOf(address(this));
        emit ReceivedLoan(address(this), amount, balance);

        Opportunity opportunityContract = Opportunity(OpportunityAddress);

        // approve the opportunity contract to transfer from this contract
        tokenContract.approve(OpportunityAddress, 100 * 10 ** 18);
        opportunityContract.solveHashAndPay(secret);

        // repay flashloan
        // Calculate the amount to repay at the end
        uint256 fee = ((amount * 3) / 997) + 1;
        uint256 amountToRepay = amount + fee;

        emit RepaymentFees(msg.sender, fee);

        // get balance of contract
        uint256 balance0 = tokenContract.balanceOf(address(this));
        require(balance0 >= amountToRepay, "Not enough balance");

        tokenContract.transfer(msg.sender, amount + fee);
    }

    function withdrawAllBalance(address tokenAddress) external onlyOwner {
        IERC20 tokenContract = IERC20(tokenAddress);
        tokenContract.transfer(
            msg.sender,
            tokenContract.balanceOf(address(this))
        );
    }
}
