
const QuantumSecureAccessControl = artifacts.require("QuantumSecureAccessControl");

module.exports = function (deployer) {
  deployer.deploy(QuantumSecureAccessControl);
};
