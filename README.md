# CP-ABE-LWE-Based-Smart-Contract
Privacy-Preserving E-Health Record Management Using Blockchain-Based Post-Quantum Access Control https://ieeexplore.ieee.org/document/10794736 doi:10.1109/UNet62310.2024.10794736 

# CP-ABE-LWE-Based-Smart-Contract

**Project Title:** Privacy-Preserving E-Health Record Management Using Blockchain-Based Post-Quantum Access Control  
**DOI:** [10.1109/UNet62310.2024.10794736](https://ieeexplore.ieee.org/document/10794736)

This project implements a smart contract for a Ciphertext-Policy Attribute-Based Encryption (CP-ABE) scheme based on Learning With Errors (LWE), designed for secure e-health record management on a blockchain. It utilizes post-quantum cryptographic principles for access control.

## Prerequisites

Before testing the project, ensure the following software is installed:

1.  **Node.js:** Version 18.12.0 (LTS) is required. Download and install it from the official release page: [https://nodejs.org/en/blog/release/v18.12.0](https://nodejs.org/en/blog/release/v18.12.0).
2.  **npm:** Update npm to the latest version using `npm install -g npm`.
3.  **node-gyp:** Install `node-gyp` globally using `npm install -g node-gyp`.
4.  **Ganache:** A personal Ethereum blockchain for development and testing. Download it from: [https://archive.trufflesuite.com/ganache/](https://archive.trufflesuite.com/ganache/).
5.  **Truffle Suite:** The project is built and tested using the Truffle framework. Install Truffle globally using `npm install -g truffle`.
6.  **Python Packages (for `AccessControl.py`):** Install the required Python packages:
    ```bash
    pip install flask numpy sympy requests json-tricks flask_restful web3
    ```

## Smart Contract Testing and Deployment

Follow these steps to compile, deploy, and test the smart contracts:

1.  **Compilation:** Navigate to the project's root directory (`CP-ABE-LWE-Based-Smart-Contract-main\CP-ABE-LWE-Based-Smart-Contract-main`) and compile the smart contracts using Truffle:
    ```bash
    truffle compile
    ```
2.  **Deployment:**
    *   Launch Ganache.
    *   Configure your Truffle project (typically in `truffle-config.js`) to connect to your local Ganache network (usually `localhost:7545`).
    *   Deploy the compiled contracts to the Ganache blockchain:
        ```bash
        truffle deploy
        ```
3.  **Testing:** Execute the Truffle tests to verify the smart contract functionality:
    ```bash
    truffle test
    ```

## Flask API Script (`AccessControl.py`)

Remember to update the contract address in AccessControl.py with your contract's address.

1.  **Execution:** Run the script using Python from the command line:
    ```bash
    python AccessControl.py
    ```
    *(Note: Use `py` if it's aliased for Python on your system, as in the original text).*
2.  **Access:** Once running, the API will be accessible at `http://127.0.0.1:5000`.
```
