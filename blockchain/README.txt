# CSE 469: Blockchain Chain of Custody

The project we will be doing is based on the Chain of Custody form. This is a form which is a critical element to a forensic investigation as it provides a record/history of the evidence from the time it is found until the case is close. 

This record shows integrity in the evidence and will help identify clearly responsible parties in any interaction with the chain.

## Chain Of Custody

The chain of custody keeps track of:

- **Where** the evidence was stored
- **Who** had access to the evidence and **when**
- **What** actions were done to the evidence

## Requirements For Block-chain

The block-chain we will be implementing must have the following commands

```
bchoc add -c case_id -i item_id [-i item_id ...]
bchoc checkout -i item_id
bchoc checkin -i item_id
bchoc log [-r] [-n num_entries] [-c case_id] [-i item_id]
bchoc remove -i item_id -y reason [-o owner]
bchoc init
bchoc verify
```

Details for more in-depth overview of what is supposed to happen can be found [here](https://sites.google.com/view/jjbaek/group-project). 

Blocks will look like below

0x00 =========================

> Previous SHA-1 Hash of the previous
>
> or parent block (20 Bytes + 4 Alignment bytes)

0x18 =========================

> Time stamp:
>
> ​	Unix time : 1549766702 (for the date 02/10/2019 @ 2:45am (UTC))

0x20 =========================

> Case ID - UUID Stored as int

0x30 =========================

> Evidince item ID 4 byte int

0x34 =========================

> State: INITIAL (first block only), CHECKEDIN, CHECKEDOUT, DISPOSED, DESTROYED, or RELEASED + one  padding byte

0x40 =========================

> Data Length represented with 4 byte integer

0x44 =========================

> Free form data text with byte length specified

=============================
