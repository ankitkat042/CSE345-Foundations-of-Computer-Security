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

//https://stackoverflow.com/questions/67317392/how-to-transfer-a-nft-from-one-account-to-another-using-erc721
  function transferNFT(address seller, address buyer, uint256 tokenID) external {
    require(msg.sender == seller || 
    msg.sender == this.getApproved(tokenID) || 
    this.isApprovedForAll(seller, msg.sender), "msg not owned by seller");
    
    this.safeTransferFrom(seller, buyer, tokenID);
  }

// https://docs.secondstate.io/oasis-network-ethereum-runtime/tutorial-mint-and-transfer-your-own-erc-721-nft-tokens
// https://forum.moralis.io/t/why-doesnt-safetransferfrom-from-to-tokenid-work-with-my-erc721-tokens-on-the-testnets-opensea-io/9820/3
  function tradeNFT(address address1, address address2, uint256 tokenID1, uint256 tokenID2) external {

      require(this.ownerOf(tokenID1) == address1, "nft1 not owned by address1");
      require(this.ownerOf(tokenID2) == address2, "nft2 not owned bt address2");

      require(this.getApproved(tokenID1) == address2 || this.isApprovedForAll(address1, address2), "address1 not approved");
      require(this.getApproved(tokenID2) == address1 || this.isApprovedForAll(address2, address1), "address2 not approved");

 
      this.safeTransferFrom(address1, address2, tokenID1, "");
      this.safeTransferFrom(address2, address1, tokenID2, "");
  }  

}
