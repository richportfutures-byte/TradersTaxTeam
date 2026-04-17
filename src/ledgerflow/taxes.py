from dataclasses import dataclass


@dataclass
class TaxEstimate:
    est_tax: float
    est_after_tax_profit: float
    set_aside_target: float


def estimate_taxes(profit_after_costs: float, effective_tax_rate: float = 0.40, set_aside_buffer: float = 0.05) -> TaxEstimate:
    taxable_base = max(0.0, float(profit_after_costs))
    est_tax = taxable_base * float(effective_tax_rate)
    set_aside_target = est_tax * (1.0 + float(set_aside_buffer))
    est_after_tax_profit = profit_after_costs - est_tax
    return TaxEstimate(est_tax=est_tax, est_after_tax_profit=est_after_tax_profit, set_aside_target=set_aside_target)


def quarterly_estimates(quarterly_profits: dict[str, float], effective_tax_rate: float = 0.40, set_aside_buffer: float = 0.05) -> dict[str, TaxEstimate]:
    return {
        q: estimate_taxes(v, effective_tax_rate, set_aside_buffer)
        for q, v in quarterly_profits.items()
    }
