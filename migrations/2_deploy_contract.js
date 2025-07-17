
//var QuantumSecureAccessControl = artifacts.require("QuantumSecureAccessControl");
//module.exports = function(deployer) {
	//deployer.deploy(HelloWorld);
	//};
const QuantumSecureAccessControl = artifacts.require("QuantumSecureAccessControl");

module.exports = function (deployer) {
  deployer.deploy(QuantumSecureAccessControl);
};
//const QuantumSecureAccessControl = artifacts.require("QuantumSecureAccessControl");
//const usingProvable = artifacts.require("usingProvable");

//module.exports = async function (deployer) {
  // Deploy the usingProvable library (provableAPI)
  //await deployer.deploy(usingProvable);

  // Link the usingProvable library to CPABEContract
  //await deployer.link(usingProvable, QuantumSecureAccessControl);

  // Deploy QuantumSecureAccessControl
  //await deployer.deploy(QuantumSecureAccessControl);
//};

//module.exports = function(deployer) {
  //deployer.deploy(QuantumSecureAccessControl)
    //.then(async instance => {
      // Additional deployment and setup steps can be added here if needed
      // For example, you can call functions on the deployed contract or perform other actions.
	
		//const instance = await QuantumSecureAccessControl.deployed();
      
	//});
//};


//const QuantumSecureAccessControl = artifacts.require("QuantumSecureAccessControl");

//module.exports = function (deployer) {
  //deployer.deploy(QuantumSecureAccessControl)
    //.then(async () => {
  //    const instance = await QuantumSecureAccessControl.deployed();

      // Additional deployment steps, if required
      // For example, you can configure the contract or set initial values here
//    });
//};


//const QuantumSecureAccessControl = artifacts.require("QuantumSecureAccessControl");
//const UsingProvable = artifacts.require("UsingProvable"); // Assuming the correct contract name is "UsingProvable"

//module.exports = async function (deployer) {
  // Deploy the UsingProvable library (provableAPI)
  //await deployer.deploy(UsingProvable);

  // Link the UsingProvable library to QuantumSecureAccessControl
  //await deployer.link(UsingProvable, QuantumSecureAccessControl);

  // Deploy QuantumSecureAccessControl
  //await deployer.deploy(QuantumSecureAccessControl);
//};

