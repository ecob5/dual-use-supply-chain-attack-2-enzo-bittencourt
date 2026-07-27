"""
Currency Exchange Library

A comprehensive single-file Python library for currency conversion and exchange rate management.
Provides functions for converting between different currencies, managing exchange rates,
and formatting currency values.

Author: Currency Exchange Library
Version: 1.0.0
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
import json


class CurrencyExchangeError(Exception):
    """Custom exception for currency exchange operations."""
    pass


class CurrencyExchange:
    """
    A comprehensive currency exchange class that handles currency conversions,
    exchange rate management, and currency formatting.
    """
    
    def __init__(self):
        """Initialize the currency exchange with default exchange rates."""
        # Base currency is USD
        self.base_currency = "USD"
        
        # Sample exchange rates (USD as base currency)
        # In a real application, these would be fetched from an API
        self._exchange_rates = {
            "USD": 1.0,      # US Dollar (base)
            "EUR": 0.85,     # Euro
            "GBP": 0.73,     # British Pound
            "JPY": 110.0,    # Japanese Yen
            "CAD": 1.25,     # Canadian Dollar
            "AUD": 1.35,     # Australian Dollar
            "CHF": 0.92,     # Swiss Franc
            "CNY": 6.45,     # Chinese Yuan
            "INR": 74.5,     # Indian Rupee
            "BRL": 5.2,      # Brazilian Real
            "MXN": 20.1,     # Mexican Peso
            "KRW": 1180.0,   # South Korean Won
            "SGD": 1.35,     # Singapore Dollar
            "HKD": 7.8,      # Hong Kong Dollar
            "NOK": 8.6,      # Norwegian Krone
            "SEK": 8.9,      # Swedish Krona
            "DKK": 6.3,      # Danish Krone
            "PLN": 3.9,      # Polish Zloty
            "CZK": 21.5,     # Czech Koruna
            "HUF": 295.0,    # Hungarian Forint
        }
        
        # Currency symbols for formatting
        self._currency_symbols = {
            "USD": "$",
            "EUR": "€",
            "GBP": "£",
            "JPY": "¥",
            "CAD": "C$",
            "AUD": "A$",
            "CHF": "CHF",
            "CNY": "¥",
            "INR": "₹",
            "BRL": "R$",
            "MXN": "$",
            "KRW": "₩",
            "SGD": "S$",
            "HKD": "HK$",
            "NOK": "kr",
            "SEK": "kr",
            "DKK": "kr",
            "PLN": "zł",
            "CZK": "Kč",
            "HUF": "Ft",
        }
        
        # Currency names for reference
        self._currency_names = {
            "USD": "US Dollar",
            "EUR": "Euro",
            "GBP": "British Pound Sterling",
            "JPY": "Japanese Yen",
            "CAD": "Canadian Dollar",
            "AUD": "Australian Dollar",
            "CHF": "Swiss Franc",
            "CNY": "Chinese Yuan",
            "INR": "Indian Rupee",
            "BRL": "Brazilian Real",
            "MXN": "Mexican Peso",
            "KRW": "South Korean Won",
            "SGD": "Singapore Dollar",
            "HKD": "Hong Kong Dollar",
            "NOK": "Norwegian Krone",
            "SEK": "Swedish Krona",
            "DKK": "Danish Krone",
            "PLN": "Polish Zloty",
            "CZK": "Czech Koruna",
            "HUF": "Hungarian Forint",
        }
        
        self._last_updated = datetime.now()
    
    def get_supported_currencies(self) -> List[str]:
        """
        Get a list of all supported currency codes.
        
        Returns:
            List[str]: List of supported currency codes
        """
        return list(self._exchange_rates.keys())
    
    def get_currency_name(self, currency_code: str) -> str:
        """
        Get the full name of a currency from its code.
        
        Args:
            currency_code (str): The currency code (e.g., 'USD')
            
        Returns:
            str: The full currency name
            
        Raises:
            CurrencyExchangeError: If currency code is not supported
        """
        currency_code = currency_code.upper()
        if currency_code not in self._currency_names:
            raise CurrencyExchangeError(f"Currency '{currency_code}' is not supported")
        return self._currency_names[currency_code]
    
    def get_currency_symbol(self, currency_code: str) -> str:
        """
        Get the symbol for a currency.
        
        Args:
            currency_code (str): The currency code (e.g., 'USD')
            
        Returns:
            str: The currency symbol
            
        Raises:
            CurrencyExchangeError: If currency code is not supported
        """
        currency_code = currency_code.upper()
        if currency_code not in self._currency_symbols:
            raise CurrencyExchangeError(f"Currency '{currency_code}' is not supported")
        return self._currency_symbols[currency_code]
    
    def is_valid_currency(self, currency_code: str) -> bool:
        """
        Check if a currency code is valid and supported.
        
        Args:
            currency_code (str): The currency code to validate
            
        Returns:
            bool: True if currency is supported, False otherwise
        """
        return currency_code.upper() in self._exchange_rates
    
    def get_exchange_rate(self, from_currency: str, to_currency: str) -> float:
        """
        Get the exchange rate between two currencies.
        
        Args:
            from_currency (str): Source currency code
            to_currency (str): Target currency code
            
        Returns:
            float: Exchange rate from source to target currency
            
        Raises:
            CurrencyExchangeError: If either currency is not supported
        """
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()
        
        if not self.is_valid_currency(from_currency):
            raise CurrencyExchangeError(f"Currency '{from_currency}' is not supported")
        if not self.is_valid_currency(to_currency):
            raise CurrencyExchangeError(f"Currency '{to_currency}' is not supported")
        
        if from_currency == to_currency:
            return 1.0
        
        # Convert through base currency (USD)
        from_rate = self._exchange_rates[from_currency]
        to_rate = self._exchange_rates[to_currency]
        
        return to_rate / from_rate
    
    def convert(self, amount: Union[int, float], from_currency: str, to_currency: str) -> float:
        """
        Convert an amount from one currency to another.
        
        Args:
            amount (Union[int, float]): Amount to convert
            from_currency (str): Source currency code
            to_currency (str): Target currency code
            
        Returns:
            float: Converted amount
            
        Raises:
            CurrencyExchangeError: If either currency is not supported or amount is invalid
        """
        if not isinstance(amount, (int, float)) or amount < 0:
            raise CurrencyExchangeError("Amount must be a non-negative number")
        
        exchange_rate = self.get_exchange_rate(from_currency, to_currency)
        return round(amount * exchange_rate, 2)
    
    def convert_multiple(self, amount: Union[int, float], from_currency: str, 
                        to_currencies: List[str]) -> Dict[str, float]:
        """
        Convert an amount to multiple target currencies.
        
        Args:
            amount (Union[int, float]): Amount to convert
            from_currency (str): Source currency code
            to_currencies (List[str]): List of target currency codes
            
        Returns:
            Dict[str, float]: Dictionary mapping currency codes to converted amounts
            
        Raises:
            CurrencyExchangeError: If any currency is not supported or amount is invalid
        """
        results = {}
        for to_currency in to_currencies:
            results[to_currency.upper()] = self.convert(amount, from_currency, to_currency)
        return results
    
    def format_currency(self, amount: Union[int, float], currency_code: str, 
                       include_symbol: bool = True, decimal_places: int = 2) -> str:
        """
        Format an amount with currency symbol and proper formatting.
        
        Args:
            amount (Union[int, float]): Amount to format
            currency_code (str): Currency code
            include_symbol (bool): Whether to include currency symbol
            decimal_places (int): Number of decimal places
            
        Returns:
            str: Formatted currency string
            
        Raises:
            CurrencyExchangeError: If currency is not supported
        """
        currency_code = currency_code.upper()
        if not self.is_valid_currency(currency_code):
            raise CurrencyExchangeError(f"Currency '{currency_code}' is not supported")
        
        formatted_amount = f"{amount:,.{decimal_places}f}"
        
        if include_symbol:
            symbol = self.get_currency_symbol(currency_code)
            return f"{symbol}{formatted_amount}"
        else:
            return f"{formatted_amount} {currency_code}"
    
    def update_exchange_rate(self, currency_code: str, rate: float) -> None:
        """
        Update the exchange rate for a specific currency.
        
        Args:
            currency_code (str): Currency code to update
            rate (float): New exchange rate (relative to base currency)
            
        Raises:
            CurrencyExchangeError: If currency is not supported or rate is invalid
        """
        currency_code = currency_code.upper()
        if not self.is_valid_currency(currency_code):
            raise CurrencyExchangeError(f"Currency '{currency_code}' is not supported")
        if not isinstance(rate, (int, float)) or rate <= 0:
            raise CurrencyExchangeError("Exchange rate must be a positive number")
        
        self._exchange_rates[currency_code] = float(rate)
        self._last_updated = datetime.now()
    
    def update_multiple_rates(self, rates: Dict[str, float]) -> None:
        """
        Update multiple exchange rates at once.
        
        Args:
            rates (Dict[str, float]): Dictionary mapping currency codes to rates
            
        Raises:
            CurrencyExchangeError: If any currency is not supported or rate is invalid
        """
        for currency_code, rate in rates.items():
            self.update_exchange_rate(currency_code, rate)
    
    def get_all_rates(self) -> Dict[str, float]:
        """
        Get all current exchange rates.
        
        Returns:
            Dict[str, float]: Dictionary of all exchange rates
        """
        return self._exchange_rates.copy()
    
    def get_last_updated(self) -> datetime:
        """
        Get the timestamp of when exchange rates were last updated.
        
        Returns:
            datetime: Last update timestamp
        """
        return self._last_updated
    
    def compare_currencies(self, amount: Union[int, float], base_currency: str, 
                          currencies: List[str]) -> Dict[str, Dict[str, Union[float, str]]]:
        """
        Compare the value of an amount across multiple currencies.
        
        Args:
            amount (Union[int, float]): Amount to compare
            base_currency (str): Base currency for the amount
            currencies (List[str]): List of currencies to compare against
            
        Returns:
            Dict[str, Dict[str, Union[float, str]]]: Comparison results with amounts and formatted strings
        """
        results = {}
        conversions = self.convert_multiple(amount, base_currency, currencies)
        
        for currency, converted_amount in conversions.items():
            results[currency] = {
                'amount': converted_amount,
                'formatted': self.format_currency(converted_amount, currency),
                'rate': self.get_exchange_rate(base_currency, currency)
            }
        
        return results
    
    def find_best_exchange(self, amount: Union[int, float], from_currency: str, 
                          to_currencies: List[str]) -> Dict[str, Union[str, float]]:
        """
        Find the best exchange rate among multiple target currencies.
        
        Args:
            amount (Union[int, float]): Amount to convert
            from_currency (str): Source currency
            to_currencies (List[str]): Target currencies to compare
            
        Returns:
            Dict[str, Union[str, float]]: Best exchange option with currency, amount, and rate
        """
        conversions = self.convert_multiple(amount, from_currency, to_currencies)
        
        best_currency = max(conversions.keys(), key=lambda x: conversions[x])
        best_amount = conversions[best_currency]
        best_rate = self.get_exchange_rate(from_currency, best_currency)
        
        return {
            'currency': best_currency,
            'amount': best_amount,
            'formatted': self.format_currency(best_amount, best_currency),
            'rate': best_rate
        }
    
    def export_rates(self, file_path: str) -> None:
        """
        Export current exchange rates to a JSON file.
        
        Args:
            file_path (str): Path to save the JSON file
        """
        data = {
            'base_currency': self.base_currency,
            'exchange_rates': self._exchange_rates,
            'last_updated': self._last_updated.isoformat(),
            'currency_symbols': self._currency_symbols,
            'currency_names': self._currency_names
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def import_rates(self, file_path: str) -> None:
        """
        Import exchange rates from a JSON file.
        
        Args:
            file_path (str): Path to the JSON file
            
        Raises:
            CurrencyExchangeError: If file cannot be read or format is invalid
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'exchange_rates' in data:
                self._exchange_rates.update(data['exchange_rates'])
            if 'base_currency' in data:
                self.base_currency = data['base_currency']
            if 'last_updated' in data:
                self._last_updated = datetime.fromisoformat(data['last_updated'])
            else:
                self._last_updated = datetime.now()
                
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            raise CurrencyExchangeError(f"Failed to import rates: {str(e)}")


# Convenience functions for quick access
_default_exchange = CurrencyExchange()

def convert_currency(amount: Union[int, float], from_currency: str, to_currency: str) -> float:
    """
    Quick currency conversion function using default exchange rates.
    
    Args:
        amount (Union[int, float]): Amount to convert
        from_currency (str): Source currency code
        to_currency (str): Target currency code
        
    Returns:
        float: Converted amount
    """
    return _default_exchange.convert(amount, from_currency, to_currency)

def get_exchange_rate(from_currency: str, to_currency: str) -> float:
    """
    Quick function to get exchange rate between two currencies.
    
    Args:
        from_currency (str): Source currency code
        to_currency (str): Target currency code
        
    Returns:
        float: Exchange rate
    """
    return _default_exchange.get_exchange_rate(from_currency, to_currency)

def format_currency(amount: Union[int, float], currency_code: str) -> str:
    """
    Quick function to format currency with symbol.
    
    Args:
        amount (Union[int, float]): Amount to format
        currency_code (str): Currency code
        
    Returns:
        str: Formatted currency string
    """
    return _default_exchange.format_currency(amount, currency_code)

def get_supported_currencies() -> List[str]:
    """
    Get list of supported currency codes.
    
    Returns:
        List[str]: List of supported currency codes
    """
    return _default_exchange.get_supported_currencies()


if __name__ == "__main__":
    # Example usage and demonstration
    print("Currency Exchange Library Demo")
    print("=" * 40)
    
    # Create exchange instance
    exchange = CurrencyExchange()
    
    # Basic conversion
    print("\n1. Basic Currency Conversion:")
    usd_amount = 100
    eur_amount = exchange.convert(usd_amount, "USD", "EUR")
    print(f"${usd_amount} USD = {exchange.format_currency(eur_amount, 'EUR')}")
    
    # Multiple conversions
    print("\n2. Multiple Currency Conversions:")
    conversions = exchange.convert_multiple(100, "USD", ["EUR", "GBP", "JPY", "CAD"])
    for currency, amount in conversions.items():
        print(f"  {exchange.format_currency(amount, currency)}")
    
    # Currency comparison
    print("\n3. Currency Comparison:")
    comparison = exchange.compare_currencies(1000, "USD", ["EUR", "GBP", "JPY"])
    for currency, data in comparison.items():
        print(f"  {currency}: {data['formatted']} (Rate: {data['rate']:.4f})")
    
    # Find best exchange
    print("\n4. Best Exchange Rate:")
    best = exchange.find_best_exchange(100, "USD", ["EUR", "GBP", "CAD", "AUD"])
    print(f"  Best option: {best['formatted']} at rate {best['rate']:.4f}")
    
    # Supported currencies
    print("\n5. Supported Currencies:")
    currencies = exchange.get_supported_currencies()
    print(f"  Total: {len(currencies)} currencies")
    print(f"  Sample: {', '.join(currencies[:10])}")
    
    # Quick functions
    print("\n6. Quick Functions:")
    print(f"  Quick convert: {convert_currency(50, 'USD', 'EUR'):.2f} EUR")
    print(f"  Quick format: {format_currency(1234.56, 'GBP')}")
    print(f"  Exchange rate USD->JPY: {get_exchange_rate('USD', 'JPY')}")