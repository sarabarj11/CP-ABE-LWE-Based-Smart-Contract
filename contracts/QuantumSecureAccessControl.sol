// SPDX-License-Identifier: MIT
pragma solidity ^0.8.11;

contract QuantumSecureAccessControl {
    address public owner;
	
    constructor() {
        owner = msg.sender;
    }

    struct User {
	    mapping(string => string) encryptedAttributes;
    }

    struct Service {
        string publicKey;
		string name;
    }
	mapping(address => User) private users;
    mapping(address => Service) public services;
    
	event PublicKeyGenerated(address indexed service, string serviceName, string publicKey);
    event UserGenerated(address indexed user, string encryptedAttributes);
    event GrantedAccess(address indexed user, string serviceName, string encryptedAttributes);
	event RevokedAccess(address indexed user, string serviceName);
    
	modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can perform this action");
        _;
    }
	
    function setPublicKey(address service, string memory serviceName, string memory pubKey) public payable {
        require(bytes(pubKey).length > 0, "Public key cannot be empty");
        require(bytes(serviceName).length > 0, "Service name cannot be empty");
        require(service == msg.sender, "Only the service can perform this action");
		Service storage serviceRecord = services[service];
        serviceRecord.publicKey = pubKey;
		serviceRecord.name = serviceName;
        emit PublicKeyGenerated(service, serviceName, pubKey);
    }
	
	function getPublicKey(address service) public view returns (string memory) {
		return  services[service].publicKey;
	}
	
	function setUserAttributes(address userAddress, string memory serviceName, string memory encryptedAttributes) public payable {
		require(bytes(serviceName).length > 0, "Service name cannot be empty");
		require(bytes(encryptedAttributes).length > 0, "Attributes must not be empty");
		require(userAddress == msg.sender, "Only the user can perform this action");
		User storage userRecord = users[msg.sender];
		userRecord.encryptedAttributes[serviceName] = encryptedAttributes;
		emit UserGenerated(userAddress, encryptedAttributes);
	}

    function grantAccess(address userAddress, string memory serviceName, string memory encryptedAttributes) public payable {
        require(bytes(serviceName).length > 0, "Service name cannot be empty");
        require(bytes(encryptedAttributes).length > 0, "Data cannot be empty");
		require(userAddress == msg.sender, "Only the user can perform this action");
        User storage userRecord = users[userAddress];
        userRecord.encryptedAttributes[serviceName] = encryptedAttributes;
        emit GrantedAccess(userAddress, serviceName, encryptedAttributes);
    }

    function hasAccess(address userAddress, string memory serviceName) public view returns (string memory) {
        return users[userAddress].encryptedAttributes[serviceName];
    }
	
	function revokeAccess(address userAddress, string memory serviceName) public {
		require(bytes(serviceName).length > 0, "Service name cannot be empty");
		require(userAddress == msg.sender, "Only the user can perform this action");
        User storage userRecord = users[userAddress];
		userRecord.encryptedAttributes[serviceName] = "";
        emit RevokedAccess(userAddress, serviceName);
    }
}
