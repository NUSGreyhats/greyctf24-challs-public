# Challenge Summary

Incorrect calldata size check in `initialize()` can be bypassed by specifying ETH address as 19 zero bytes.

# Challenge Details

Introducing NFT-based escrows - you can deposit assets and trade escrows by selling your ownership NFT!

However, I accidentally renounced ownership for my own escrow. Can you help me recover the funds?

# Author

MiloTruck

# Hints

1. Find out how the clones-with-immutable-args library implements immutable variables when functions are called.

# Flag

`grey{cwia_bytes_overlap_5a392abcfa2d040a}`

