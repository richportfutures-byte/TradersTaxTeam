# Trading Tax Model (Planning Only)

## Purpose
Describe the conceptual planning model used by LedgerFlow MVP.

## Core decomposition
1. Gross trading P&L
2. Less direct trade costs
3. Equals net trading P&L
4. Less overhead expenses (business-use allocated)
5. Equals profit after costs
6. Apply planning tax rate and reserve buffer
7. Produce estimated tax and set-aside targets

## Important distinctions
- direct trade costs come from broker data
- overhead expenses are separate user-entered costs
- asset purchases may be planning-tagged but not automatically filed
- Trader Tax Status relevance is contextual, not adjudicated by the app

## Planning settings
- effective_tax_rate
- set_aside_buffer

## Caution
This model is useful for disciplined reserves, not authoritative tax determination.
