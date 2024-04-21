# Challenge Summary

Abuse rounding down to make votes underflow to a huge value when calling `delegate()`.

# Challenge Details

In the spirit of decentralization, GreyHats is now a DAO! 

Vote with your GREY tokens to decide how our funds are spent.

# Author

MiloTruck

# Hints

1. Are the unchecked blocks safe? Could the calculations overflow or underflow?
2. Focus on how vote calculation rounds down.

# Flag

`grey{rounding_is_dangerous_752aa6bb8b6a9f61}`

# Learning Objectives

Learn the nuances when rounding down/up in calculations.