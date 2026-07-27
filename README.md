# 💱 Public Currency Exchange

A comprehensive single-file Python library for currency conversion and exchange rate management. Simple to use, yet powerful enough for production applications.

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/Code%20Style-PEP8-black.svg)](https://www.python.org/dev/peps/pep-0008/)

## 🚀 Features

- **20+ Major Currencies**: Support for USD, EUR, GBP, JPY, CAD, AUD, and more
- **Real-time Conversion**: Convert between any supported currency pairs
- **Multiple Conversions**: Convert to multiple currencies simultaneously
- **Currency Formatting**: Proper formatting with currency symbols and locale support
- **Exchange Rate Management**: Update and manage exchange rates
- **Comparison Tools**: Compare values across multiple currencies
- **Best Rate Finder**: Find the best exchange rate among options
- **Import/Export**: Save and load exchange rates from JSON files
- **Error Handling**: Comprehensive error handling with custom exceptions
- **Zero Dependencies**: Pure Python implementation, no external dependencies

## 📦 Installation

### Option 1: Docker (Recommended for Development)

Use Docker for a complete development environment:

```bash
# Clone the repository
git clone https://github.com/magikboy/Currency-Exchange.git
cd Currency-Exchange

# Iniciar el contenedor
docker-compose up -d

# Luego entrar
docker-compose exec currency-exchange-dev bash
```

### Option 2: Direct Installation

Simply download the `currency_exchange.py` file and import it into your project:

```bash
# Clone the repository
git clone https://github.com/magikboy/Currency-Exchange.git
cd Currency-Exchange

# Or download just the library file
wget https://raw.githubusercontent.com/magikboy/Currency-Exchange/main/currency_exchange.py
```

## 🔧 Quick Start

### Basic Usage

```python
from currency_exchange import convert_currency, format_currency

# Quick conversion
euros = convert_currency(100, "USD", "EUR")
print(f"100 USD = {euros} EUR")  # 100 USD = 85.0 EUR

# Format with currency symbol
formatted = format_currency(euros, "EUR")
print(formatted)  # €85.00
```

### Advanced Usage

```python
from currency_exchange import CurrencyExchange

# Create exchange instance
exchange = CurrencyExchange()

# Convert to multiple currencies
conversions = exchange.convert_multiple(1000, "USD", ["EUR", "GBP", "JPY", "CAD"])
for currency, amount in conversions.items():
    print(f"{currency}: {exchange.format_currency(amount, currency)}")

# Find best exchange rate
best = exchange.find_best_exchange(100, "USD", ["EUR", "GBP", "CAD", "AUD"])
print(f"Best rate: {best['formatted']} at {best['rate']:.4f}")

# Compare currencies
comparison = exchange.compare_currencies(500, "USD", ["EUR", "GBP", "JPY"])
for currency, data in comparison.items():
    print(f"{currency}: {data['formatted']} (Rate: {data['rate']:.4f})")
```

## 💰 Supported Currencies

| Code | Currency | Symbol |
|------|----------|--------|
| USD | US Dollar | $ |
| EUR | Euro | € |
| GBP | British Pound Sterling | £ |
| JPY | Japanese Yen | ¥ |
| CAD | Canadian Dollar | C$ |
| AUD | Australian Dollar | A$ |
| CHF | Swiss Franc | CHF |
| CNY | Chinese Yuan | ¥ |
| INR | Indian Rupee | ₹ |
| BRL | Brazilian Real | R$ |
| MXN | Mexican Peso | $ |
| KRW | South Korean Won | ₩ |
| SGD | Singapore Dollar | S$ |
| HKD | Hong Kong Dollar | HK$ |
| NOK | Norwegian Krone | kr |
| SEK | Swedish Krona | kr |
| DKK | Danish Krone | kr |
| PLN | Polish Zloty | zł |
| CZK | Czech Koruna | Kč |
| HUF | Hungarian Forint | Ft |

## 📚 API Reference

### Core Functions

#### `convert_currency(amount, from_currency, to_currency)`
Convert an amount between two currencies.

```python
result = convert_currency(100, "USD", "EUR")  # Returns: 85.0
```

#### `get_exchange_rate(from_currency, to_currency)`
Get the exchange rate between two currencies.

```python
rate = get_exchange_rate("USD", "EUR")  # Returns: 0.85
```

#### `format_currency(amount, currency_code)`
Format an amount with proper currency symbol.

```python
formatted = format_currency(1234.56, "EUR")  # Returns: "€1,234.56"
```

### CurrencyExchange Class Methods

#### `convert(amount, from_currency, to_currency)`
Convert between currencies with full error handling.

#### `convert_multiple(amount, from_currency, to_currencies)`
Convert to multiple target currencies at once.

#### `compare_currencies(amount, base_currency, currencies)`
Compare value across multiple currencies with detailed information.

#### `find_best_exchange(amount, from_currency, to_currencies)`
Find the currency that gives the best exchange rate.

#### `update_exchange_rate(currency_code, rate)`
Update the exchange rate for a specific currency.

#### `export_rates(file_path)` / `import_rates(file_path)`
Save/load exchange rates to/from JSON files.

## 🛠️ Examples

### Currency Conversion Dashboard

```python
from currency_exchange import CurrencyExchange

def currency_dashboard(amount, base_currency):
    exchange = CurrencyExchange()
    
    print(f"\n💱 Currency Dashboard for {exchange.format_currency(amount, base_currency)}")
    print("=" * 50)
    
    # Major currencies
    major_currencies = ["EUR", "GBP", "JPY", "CAD", "AUD"]
    conversions = exchange.convert_multiple(amount, base_currency, major_currencies)
    
    print("\n🌍 Major Currencies:")
    for currency, converted_amount in conversions.items():
        formatted = exchange.format_currency(converted_amount, currency)
        rate = exchange.get_exchange_rate(base_currency, currency)
        print(f"  {currency}: {formatted:>12} (Rate: {rate:.4f})")
    
    # Best exchange
    best = exchange.find_best_exchange(amount, base_currency, major_currencies)
    print(f"\n🏆 Best Exchange: {best['formatted']} ({best['currency']})")

# Run dashboard
currency_dashboard(1000, "USD")
```

### Exchange Rate Monitor

```python
from currency_exchange import CurrencyExchange
import json
from datetime import datetime

def save_daily_rates():
    exchange = CurrencyExchange()
    
    # Get all current rates
    rates = exchange.get_all_rates()
    
    # Save with timestamp
    data = {
        "date": datetime.now().isoformat(),
        "rates": rates,
        "base_currency": exchange.base_currency
    }
    
    filename = f"rates_{datetime.now().strftime('%Y%m%d')}.json"
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"📊 Rates saved to {filename}")

save_daily_rates()
```

## 🧪 Testing

Run the built-in demo to test all functionality:

```bash
python currency_exchange.py
```

This will demonstrate:
- Basic currency conversion
- Multiple currency conversions
- Currency comparison
- Best exchange rate finding
- Supported currencies list
- Quick function usage

## 🤝 Contributing

Contributions are welcome! Here are some ways you can contribute:

1. **Add More Currencies**: Extend support for additional currencies
2. **Real-time Rates**: Integrate with live exchange rate APIs
3. **Historical Data**: Add support for historical exchange rates
4. **Performance**: Optimize conversion algorithms
5. **Documentation**: Improve documentation and examples

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔮 Roadmap

- [ ] Integration with live exchange rate APIs (Alpha Vantage, Fixer.io)
- [ ] Historical exchange rate data support
- [ ] Cryptocurrency support
- [ ] Rate change notifications
- [ ] Web API wrapper
- [ ] CLI tool for terminal usage
- [ ] Rate prediction algorithms
- [ ] Multi-language support

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/public-currency-exchange/issues) page
2. Create a new issue with detailed information
3. Include code examples and error messages

## 🙏 Acknowledgments

- Exchange rates are sample rates for demonstration purposes
- In production, integrate with a reliable exchange rate API
- Currency symbols and names follow ISO 4217 standards

---

**Made with ❤️ for the global developer community**

*Happy currency converting! 💱*