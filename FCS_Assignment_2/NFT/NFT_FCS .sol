// SPDX-License-Identifier: MIT

pragma solidity 0.8.22;

// code snippet from https://github.com/nibbstack/erc721/tree/master
import "https://github.com/0xcert/ethereum-erc721/src/contracts/tokens/nf-token-metadata.sol";
import "https://github.com/0xcert/ethereum-erc721/src/contracts/ownership/ownable.sol";



contract fcsNFT is 
    NFTokenMetadata, 
    Ownable {
 
  /**
   * @dev Contract constructor. Sets metadata extension `name` and `symbol`.
   */

  constructor() {
    nftName = "fcs_class";
    nftSymbol = "INR";
  }
 

  function metamask(address myaddress, uint256 tokenID, string calldata uri) external onlyOwner {
    super._mint(myaddress, tokenID);
    super._setTokenUri(tokenID, uri);
  }

}
