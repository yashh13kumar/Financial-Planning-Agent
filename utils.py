import streamlit as st
import re
from typing import Dict, Any, Union, Optional

def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}
    
    if 'show_formula_explanation' not in st.session_state:
        st.session_state.show_formula_explanation = False
    
    if 'questionnaire_completed' not in st.session_state:
        st.session_state.questionnaire_completed = False
    
    if 'questionnaire_data' not in st.session_state:
        st.session_state.questionnaire_data = {}

def format_currency(amount: Union[int, float], decimals: int = 0) -> str:
    """
    Format a number as currency in Indian Rupees with proper formatting.
    
    Args:
        amount: The amount to format
        decimals: Number of decimal places to show
        
    Returns:
        Formatted currency string in rupees
        
    Example:
        >>> format_currency(1234567.89)
        '₹12,34,568'
        >>> format_currency(1234567.89, 2)
        '₹12,34,567.89'
    """
    if amount is None:
        return "₹0"
    
    try:
        # Indian numbering system formatting
        if decimals == 0:
            formatted = f"{amount:,.0f}"
        else:
            formatted = f"{amount:,.{decimals}f}"
        
        # Convert to Indian numbering system (lakhs and crores)
        if amount >= 10000000:  # 1 crore
            formatted = f"{amount/10000000:.1f} Cr"
        elif amount >= 100000:  # 1 lakh
            formatted = f"{amount/100000:.1f} L"
        else:
            formatted = f"{amount:,.0f}"
        
        return f"₹{formatted}"
    except (ValueError, TypeError):
        return "₹0"

def format_percentage(rate: float, decimals: int = 1) -> str:
    """
    Format a decimal rate as a percentage.
    
    Args:
        rate: The rate as a decimal (e.g., 0.07 for 7%)
        decimals: Number of decimal places to show
        
    Returns:
        Formatted percentage string
        
    Example:
        >>> format_percentage(0.075)
        '7.5%'
    """
    if rate is None:
        return "0.0%"
    
    try:
        return f"{rate * 100:.{decimals}f}%"
    except (ValueError, TypeError):
        return "0.0%"

def validate_financial_input(value: Any, field_name: str, min_value: Optional[float] = None, 
                           max_value: Optional[float] = None) -> tuple[bool, str]:
    """
    Validate financial input values with appropriate constraints.
    
    Args:
        value: The value to validate
        field_name: Name of the field for error messages
        min_value: Minimum allowed value
        max_value: Maximum allowed value
        
    Returns:
        Tuple of (is_valid: bool, error_message: str)
        
    Example:
        >>> validate_financial_input(25, "age", 18, 100)
        (True, "")
        >>> validate_financial_input(-5, "savings", 0)
        (False, "Savings cannot be negative")
    """
    if value is None:
        return False, f"{field_name} is required"
    
    try:
        numeric_value = float(value)
    except (ValueError, TypeError):
        return False, f"{field_name} must be a valid number"
    
    if min_value is not None and numeric_value < min_value:
        return False, f"{field_name} cannot be less than {format_currency(min_value) if 'income' in field_name.lower() or 'savings' in field_name.lower() else min_value}"
    
    if max_value is not None and numeric_value > max_value:
        return False, f"{field_name} cannot be greater than {format_currency(max_value) if 'income' in field_name.lower() or 'savings' in field_name.lower() else max_value}"
    
    return True, ""

def parse_financial_amount(text: str) -> Optional[float]:
    """
    Parse financial amounts from text, handling various formats.
    
    Args:
        text: Text containing financial amount
        
    Returns:
        Parsed amount as float, or None if not found
        
    Example:
        >>> parse_financial_amount("$75,000")
        75000.0
        >>> parse_financial_amount("75k")
        75000.0
        >>> parse_financial_amount("not a number")
        None
    """
    if not text:
        return None
    
    # Remove currency symbols and spaces
    cleaned = re.sub(r'[$,\s]', '', str(text))
    
    # Handle 'k' for thousands
    if cleaned.lower().endswith('k'):
        try:
            return float(cleaned[:-1]) * 1000
        except ValueError:
            return None
    
    # Handle 'm' for millions
    if cleaned.lower().endswith('m'):
        try:
            return float(cleaned[:-1]) * 1000000
        except ValueError:
            return None
    
    # Try to parse as regular number
    try:
        return float(cleaned)
    except ValueError:
        return None

def extract_percentage(text: str) -> Optional[float]:
    """
    Extract percentage values from text.
    
    Args:
        text: Text containing percentage
        
    Returns:
        Percentage as decimal (e.g., 0.15 for 15%), or None if not found
        
    Example:
        >>> extract_percentage("15%")
        0.15
        >>> extract_percentage("save 10 percent")
        0.10
    """
    if not text:
        return None
    
    # Look for number followed by % or percent
    percentage_pattern = r'(\d+(?:\.\d+)?)\s*(?:%|percent)'
    match = re.search(percentage_pattern, text.lower())
    
    if match:
        try:
            return float(match.group(1)) / 100
        except ValueError:
            return None
    
    return None

def calculate_years_between_ages(current_age: int, target_age: int) -> int:
    """
    Calculate years between two ages with validation.
    
    Args:
        current_age: Current age
        target_age: Target age
        
    Returns:
        Number of years between ages
        
    Raises:
        ValueError: If ages are invalid
    """
    if current_age < 0 or target_age < 0:
        raise ValueError("Ages cannot be negative")
    
    if current_age > 150 or target_age > 150:
        raise ValueError("Ages seem unrealistic (over 150)")
    
    if target_age < current_age:
        raise ValueError("Target age cannot be less than current age")
    
    return target_age - current_age

def get_risk_tolerance_return(risk_tolerance: str) -> float:
    """
    Get expected annual return rate based on risk tolerance.
    
    Args:
        risk_tolerance: Risk tolerance level ('conservative', 'moderate', 'aggressive')
        
    Returns:
        Expected annual return rate as decimal
        
    Example:
        >>> get_risk_tolerance_return('moderate')
        0.07
    """
    rates = {
        'conservative': 0.05,  # 5% annual return
        'moderate': 0.07,      # 7% annual return
        'aggressive': 0.09     # 9% annual return
    }
    
    return rates.get(risk_tolerance.lower(), 0.07)  # Default to moderate

def create_summary_metrics(user_data: Dict) -> Dict[str, Any]:
    """
    Create summary metrics from user data for display.
    
    Args:
        user_data: Dictionary containing user financial data
        
    Returns:
        Dictionary with calculated summary metrics
    """
    if not user_data:
        return {}
    
    summary = {}
    
    # Basic info
    if 'age' in user_data and 'retirement_age' in user_data:
        summary['years_to_retirement'] = user_data['retirement_age'] - user_data['age']
    
    # Savings rate calculation
    if 'current_income' in user_data and 'monthly_savings' in user_data:
        annual_savings = user_data['monthly_savings'] * 12
        summary['savings_rate'] = annual_savings / user_data['current_income']
    
    # Emergency fund coverage
    if 'current_savings' in user_data and 'monthly_expenses' in user_data:
        summary['emergency_fund_months'] = user_data['current_savings'] / user_data['monthly_expenses']
    
    # Expected return rate
    if 'risk_tolerance' in user_data:
        summary['expected_return'] = get_risk_tolerance_return(user_data['risk_tolerance'])
    
    return summary

def format_time_period(years: float) -> str:
    """
    Format a time period in years to a human-readable string.
    
    Args:
        years: Number of years (can be fractional)
        
    Returns:
        Formatted time period string
        
    Example:
        >>> format_time_period(15.5)
        '15 years, 6 months'
        >>> format_time_period(2.25)
        '2 years, 3 months'
    """
    if years < 0:
        return "Invalid time period"
    
    whole_years = int(years)
    remaining_months = int((years - whole_years) * 12)
    
    if whole_years == 0:
        return f"{remaining_months} months"
    elif remaining_months == 0:
        return f"{whole_years} year{'s' if whole_years != 1 else ''}"
    else:
        return f"{whole_years} year{'s' if whole_years != 1 else ''}, {remaining_months} month{'s' if remaining_months != 1 else ''}"

def generate_error_message(error_type: str, context: str = "") -> str:
    """
    Generate user-friendly error messages for different error types.
    
    Args:
        error_type: Type of error ('validation', 'calculation', 'input', etc.)
        context: Additional context for the error
        
    Returns:
        User-friendly error message
    """
    error_messages = {
        'validation': f"Please check your input: {context}",
        'calculation': f"Unable to perform calculation: {context}",
        'input': f"Invalid input provided: {context}",
        'missing_data': f"Required information missing: {context}",
        'unrealistic': f"The value seems unrealistic: {context}",
        'insufficient_funds': "Insufficient funds for this scenario",
        'negative_value': "Values cannot be negative in this context",
        'api_error': "Unable to connect to financial services. Please try again later."
    }
    
    return error_messages.get(error_type, f"An error occurred: {context}")

def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely divide two numbers, handling division by zero.
    
    Args:
        numerator: The numerator
        denominator: The denominator
        default: Default value to return if division by zero
        
    Returns:
        Result of division or default value
    """
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except (TypeError, ValueError):
        return default

def is_reasonable_financial_value(value: float, field_type: str) -> bool:
    """
    Check if a financial value is within reasonable bounds.
    
    Args:
        value: The value to check
        field_type: Type of financial field ('income', 'savings', 'age', etc.)
        
    Returns:
        True if value is reasonable, False otherwise
    """
    reasonable_ranges = {
        'age': (18, 100),
        'income': (10000, 10000000),  # $10K to $10M annually
        'savings': (0, 100000000),    # $0 to $100M
        'retirement_age': (50, 85),
        'return_rate': (-0.5, 0.3),   # -50% to 30%
        'inflation_rate': (0, 0.15),  # 0% to 15%
        'percentage': (0, 1)          # 0% to 100%
    }
    
    if field_type not in reasonable_ranges:
        return True  # If we don't have a range, assume it's reasonable
    
    min_val, max_val = reasonable_ranges[field_type]
    return min_val <= value <= max_val
