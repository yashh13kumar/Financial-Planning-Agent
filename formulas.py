import math
from decimal import Decimal, getcontext
from typing import Union, Optional

# Set decimal precision for financial calculations
getcontext().prec = 10

class FinancialFormulas:
    """
    Pure Python implementation of financial formulas for retirement planning.
    All calculations use proven financial mathematics without external libraries.
    """
    
    def __init__(self):
        """Initialize the financial formulas calculator."""
        pass
    
    def future_value(self, present_value: float, rate: float, periods: int) -> float:
        """
        Calculate Future Value using compound interest formula.
        
        Formula: FV = PV × (1 + r)^n
        
        Args:
            present_value: Initial amount (PV)
            rate: Interest rate per period (r)
            periods: Number of periods (n)
            
        Returns:
            Future value of the investment
            
        Example:
            >>> calc = FinancialFormulas()
            >>> calc.future_value(10000, 0.07, 10)
            19671.51
        """
        if present_value < 0:
            raise ValueError("Present value cannot be negative")
        if periods < 0:
            raise ValueError("Number of periods cannot be negative")
        if rate < -1:
            raise ValueError("Interest rate cannot be less than -100%")
        
        return present_value * math.pow(1 + rate, periods)
    
    def present_value(self, future_value: float, rate: float, periods: int) -> float:
        """
        Calculate Present Value (discounting future cash flows).
        
        Formula: PV = FV / (1 + r)^n
        
        Args:
            future_value: Future amount (FV)
            rate: Discount rate per period (r)
            periods: Number of periods (n)
            
        Returns:
            Present value of the future amount
            
        Example:
            >>> calc = FinancialFormulas()
            >>> calc.present_value(20000, 0.07, 10)
            10162.67
        """
        if future_value < 0:
            raise ValueError("Future value cannot be negative")
        if periods < 0:
            raise ValueError("Number of periods cannot be negative")
        if rate < -1:
            raise ValueError("Discount rate cannot be less than -100%")
        
        return future_value / math.pow(1 + rate, periods)
    
    def future_value_annuity(self, payment: float, rate: float, periods: int) -> float:
        """
        Calculate Future Value of an Ordinary Annuity.
        
        Formula: FV = PMT × [(1 + r)^n - 1] / r
        
        Args:
            payment: Regular payment amount (PMT)
            rate: Interest rate per period (r)
            periods: Number of periods (n)
            
        Returns:
            Future value of the annuity
            
        Example:
            >>> calc = FinancialFormulas()
            >>> calc.future_value_annuity(1000, 0.07, 10)
            13816.45
        """
        if payment < 0:
            raise ValueError("Payment cannot be negative")
        if periods < 0:
            raise ValueError("Number of periods cannot be negative")
        if rate < -1:
            raise ValueError("Interest rate cannot be less than -100%")
        
        if rate == 0:
            return payment * periods
        
        return payment * (math.pow(1 + rate, periods) - 1) / rate
    
    def present_value_annuity(self, payment: float, rate: float, periods: int) -> float:
        """
        Calculate Present Value of an Ordinary Annuity.
        
        Formula: PV = PMT × [1 - (1 + r)^(-n)] / r
        
        Args:
            payment: Regular payment amount (PMT)
            rate: Discount rate per period (r)
            periods: Number of periods (n)
            
        Returns:
            Present value of the annuity
            
        Example:
            >>> calc = FinancialFormulas()
            >>> calc.present_value_annuity(1000, 0.07, 10)
            7023.58
        """
        if payment < 0:
            raise ValueError("Payment cannot be negative")
        if periods < 0:
            raise ValueError("Number of periods cannot be negative")
        if rate < -1:
            raise ValueError("Discount rate cannot be less than -100%")
        
        if rate == 0:
            return payment * periods
        
        return payment * (1 - math.pow(1 + rate, -periods)) / rate
    
    def payment_for_future_value(self, future_value: float, rate: float, periods: int) -> float:
        """
        Calculate required payment to reach a future value (sinking fund).
        
        Formula: PMT = FV × r / [(1 + r)^n - 1]
        
        Args:
            future_value: Target future value (FV)
            rate: Interest rate per period (r)
            periods: Number of periods (n)
            
        Returns:
            Required payment amount
            
        Example:
            >>> calc = FinancialFormulas()
            >>> calc.payment_for_future_value(100000, 0.07, 20)
            2439.29
        """
        if future_value < 0:
            raise ValueError("Future value cannot be negative")
        if periods <= 0:
            raise ValueError("Number of periods must be positive")
        if rate < -1:
            raise ValueError("Interest rate cannot be less than -100%")
        
        if rate == 0:
            return future_value / periods
        
        return future_value * rate / (math.pow(1 + rate, periods) - 1)
    
    def payment_for_present_value(self, present_value: float, rate: float, periods: int) -> float:
        """
        Calculate payment amount for a given present value (loan payment).
        
        Formula: PMT = PV × r / [1 - (1 + r)^(-n)]
        
        Args:
            present_value: Loan or present value amount (PV)
            rate: Interest rate per period (r)
            periods: Number of periods (n)
            
        Returns:
            Required payment amount
            
        Example:
            >>> calc = FinancialFormulas()
            >>> calc.payment_for_present_value(100000, 0.05/12, 360)
            536.82
        """
        if present_value < 0:
            raise ValueError("Present value cannot be negative")
        if periods <= 0:
            raise ValueError("Number of periods must be positive")
        if rate < -1:
            raise ValueError("Interest rate cannot be less than -100%")
        
        if rate == 0:
            return present_value / periods
        
        return present_value * rate / (1 - math.pow(1 + rate, -periods))
    
    def retirement_age_calculator(self, current_age: int, current_savings: float, 
                                current_income: float, savings_rate: float, 
                                target_nest_egg: float, expected_return: float) -> int:
        """
        Calculate the age at which retirement is possible given current savings strategy.
        
        Args:
            current_age: Current age
            current_savings: Current savings amount
            current_income: Current annual income
            savings_rate: Percentage of income saved annually (e.g., 0.15 for 15%)
            target_nest_egg: Required nest egg for retirement
            expected_return: Expected annual return rate
            
        Returns:
            Retirement age (rounded up)
            
        Example:
            >>> calc = FinancialFormulas()
            >>> calc.retirement_age_calculator(30, 50000, 100000, 0.15, 1000000, 0.07)
            57
        """
        if current_age < 18 or current_age > 100:
            raise ValueError("Current age must be between 18 and 100")
        if current_savings < 0:
            raise ValueError("Current savings cannot be negative")
        if current_income <= 0:
            raise ValueError("Current income must be positive")
        if savings_rate < 0 or savings_rate > 1:
            raise ValueError("Savings rate must be between 0 and 1")
        if target_nest_egg <= 0:
            raise ValueError("Target nest egg must be positive")
        if expected_return < -1:
            raise ValueError("Expected return cannot be less than -100%")
        
        annual_savings = current_income * savings_rate
        
        # If no annual savings, can only rely on current savings growth
        if annual_savings == 0:
            if current_savings == 0:
                return float('inf')  # Never possible
            years_needed = math.log(target_nest_egg / current_savings) / math.log(1 + expected_return)
        else:
            # Solve for time using financial mathematics
            if expected_return == 0:
                years_needed = (target_nest_egg - current_savings) / annual_savings
            else:
                # Use iterative approach for complex annuity formula
                years_needed = self._solve_for_periods(
                    current_savings, annual_savings, target_nest_egg, expected_return
                )
        
        retirement_age = current_age + math.ceil(years_needed)
        return int(min(retirement_age, 100))  # Cap at age 100
    
    def savings_duration_calculator(self, current_savings: float, withdrawal_rate: float, 
                                  annual_return: float = 0.04) -> float:
        """
        Calculate how long savings will last with regular withdrawals.
        
        Args:
            current_savings: Current savings amount
            withdrawal_rate: Annual withdrawal amount
            annual_return: Expected annual return on remaining balance
            
        Returns:
            Number of years savings will last
            
        Example:
            >>> calc = FinancialFormulas()
            >>> calc.savings_duration_calculator(500000, 40000, 0.04)
            17.67
        """
        if current_savings <= 0:
            raise ValueError("Current savings must be positive")
        if withdrawal_rate <= 0:
            raise ValueError("Withdrawal rate must be positive")
        if annual_return < -1:
            raise ValueError("Annual return cannot be less than -100%")
        
        # If withdrawal rate exceeds growth, calculate finite duration
        if withdrawal_rate <= current_savings * annual_return:
            return float('inf')  # Savings will last indefinitely
        
        # Use present value of annuity formula solved for periods
        if annual_return == 0:
            return current_savings / withdrawal_rate
        
        # Solve: PV = PMT × [1 - (1 + r)^(-n)] / r for n
        ratio = current_savings * annual_return / withdrawal_rate
        if ratio >= 1:
            return float('inf')
        
        return -math.log(1 - ratio) / math.log(1 + annual_return)
    
    def goal_based_savings_calculator(self, target_amount: float, time_horizon: int, 
                                    current_savings: float = 0, 
                                    expected_return: float = 0.07) -> float:
        """
        Calculate required monthly savings to reach a financial goal.
        
        Args:
            target_amount: Target amount to save
            time_horizon: Time horizon in years
            current_savings: Current savings amount
            expected_return: Expected annual return rate
            
        Returns:
            Required monthly savings amount
            
        Example:
            >>> calc = FinancialFormulas()
            >>> calc.goal_based_savings_calculator(100000, 10, 10000, 0.07)
            563.04
        """
        if target_amount <= 0:
            raise ValueError("Target amount must be positive")
        if time_horizon <= 0:
            raise ValueError("Time horizon must be positive")
        if current_savings < 0:
            raise ValueError("Current savings cannot be negative")
        if expected_return < -1:
            raise ValueError("Expected return cannot be less than -100%")
        
        # Future value of current savings
        future_current_savings = self.future_value(current_savings, expected_return, time_horizon)
        
        # Additional amount needed
        additional_needed = target_amount - future_current_savings
        
        if additional_needed <= 0:
            return 0  # Goal already achieved
        
        # Calculate required annual savings
        annual_savings = self.payment_for_future_value(additional_needed, expected_return, time_horizon)
        
        # Convert to monthly
        return annual_savings / 12
    
    def mortgage_vs_invest_analysis(self, mortgage_balance: float, mortgage_rate: float, 
                                  mortgage_years: int, investment_return: float) -> dict:
        """
        Analyze whether to pay down mortgage or invest the extra money.
        
        Args:
            mortgage_balance: Current mortgage balance
            mortgage_rate: Annual mortgage interest rate
            mortgage_years: Remaining years on mortgage
            investment_return: Expected annual investment return
            
        Returns:
            Dictionary with analysis results
            
        Example:
            >>> calc = FinancialFormulas()
            >>> result = calc.mortgage_vs_invest_analysis(200000, 0.03, 15, 0.07)
            >>> result['recommendation']
            'invest'
        """
        if mortgage_balance <= 0:
            raise ValueError("Mortgage balance must be positive")
        if mortgage_rate < 0:
            raise ValueError("Mortgage rate cannot be negative")
        if mortgage_years <= 0:
            raise ValueError("Mortgage years must be positive")
        if investment_return < -1:
            raise ValueError("Investment return cannot be less than -100%")
        
        # Calculate current mortgage payment
        monthly_rate = mortgage_rate / 12
        total_payments = mortgage_years * 12
        monthly_payment = self.payment_for_present_value(mortgage_balance, monthly_rate, total_payments)
        
        # Scenario 1: Pay off mortgage early (extra payment)
        # For simplicity, assume doubling the payment
        extra_payment = monthly_payment
        total_monthly_payment = monthly_payment + extra_payment
        
        # Calculate time to pay off with extra payments
        payoff_months = self._calculate_payoff_time(mortgage_balance, monthly_rate, total_monthly_payment)
        payoff_years = payoff_months / 12
        
        # Interest saved by paying off early
        original_total_interest = (monthly_payment * total_payments) - mortgage_balance
        early_total_payments = total_monthly_payment * payoff_months
        early_total_interest = early_total_payments - mortgage_balance
        interest_saved = original_total_interest - early_total_interest
        
        # Scenario 2: Invest the extra payment
        monthly_investment_return = investment_return / 12
        future_investment_value = self.future_value_annuity(
            extra_payment, monthly_investment_return, int(payoff_months)
        )
        
        # Determine recommendation
        net_benefit = future_investment_value - interest_saved
        recommendation = "invest" if net_benefit > 0 else "pay_mortgage"
        
        return {
            'mortgage_payment': monthly_payment,
            'extra_payment': extra_payment,
            'payoff_years': payoff_years,
            'interest_saved': interest_saved,
            'investment_value': future_investment_value,
            'net_benefit': net_benefit,
            'recommendation': recommendation,
            'analysis': f"{'Investing' if recommendation == 'invest' else 'Paying off mortgage'} "
                       f"is better by ${abs(net_benefit):,.2f}"
        }
    
    def _solve_for_periods(self, present_value: float, payment: float, 
                          future_value: float, rate: float, tolerance: float = 0.01) -> float:
        """
        Solve for number of periods using iterative method.
        Used when analytical solution is complex.
        """
        low, high = 0, 100
        
        for _ in range(1000):  # Max iterations
            mid = (low + high) / 2
            calculated_fv = self.future_value(present_value, rate, int(mid)) + \
                           self.future_value_annuity(payment, rate, int(mid))
            
            if abs(calculated_fv - future_value) < tolerance:
                return mid
            elif calculated_fv < future_value:
                low = mid
            else:
                high = mid
        
        return (low + high) / 2
    
    def _calculate_payoff_time(self, balance: float, monthly_rate: float, 
                              monthly_payment: float) -> float:
        """Calculate time to pay off loan with given monthly payment."""
        if monthly_rate == 0:
            return balance / monthly_payment
        
        return -math.log(1 - (balance * monthly_rate / monthly_payment)) / math.log(1 + monthly_rate)
    
    def calculate_rule_of_72(self, interest_rate: float) -> float:
        """
        Calculate doubling time using Rule of 72.
        
        Args:
            interest_rate: Annual interest rate (as decimal, e.g., 0.07 for 7%)
            
        Returns:
            Approximate years to double investment
        """
        if interest_rate <= 0:
            raise ValueError("Interest rate must be positive")
        
        return 0.72 / interest_rate
    
    def inflation_adjusted_return(self, nominal_return: float, inflation_rate: float) -> float:
        """
        Calculate real return adjusted for inflation.
        
        Formula: Real Return = (1 + nominal) / (1 + inflation) - 1
        
        Args:
            nominal_return: Nominal return rate
            inflation_rate: Inflation rate
            
        Returns:
            Real return rate
        """
        return (1 + nominal_return) / (1 + inflation_rate) - 1
