// SPDX-License-Identifier: MIT
pragma solidity >= 0.4.0 <= 0.9;

contract Auction {
    string public users;
    string public product;
    string public history;
    string public transaction;
   

    function addUsers(string memory u) public {
        users = u;	
    }

    function getUsers() public view returns (string memory) {
        return users;
    }


    function addproduct(string memory ca) public {
        product = ca;
    }

    function getproduct() public view returns (string memory) {
        return product;
    }

    function addhistory(string memory ra) public {
        history = ra;
    }

    function gethistory() public view returns (string memory) {
        return history;
    }

    function addtransaction(string memory ba) public {
        transaction = ba;
    }

    function gettransaction() public view returns (string memory) {
        return transaction;
    }

   

    constructor() public {
    users = "empty";
    product = "empty";
    history = "empty";
    transaction = "empty";
    
    
    }
}