"""
E-commerce Data Cleaning Script
Cleans messy order data and generates quality reports.
"""

import pandas as pd
import numpy as np
import re
from datetime import datetime
import os


class DataCleaner:
    """Clean e-commerce order data with comprehensive quality checks."""
    
    def __init__(self, input_path):
        """Initialize cleaner with input file path."""
        self.input_path = input_path
        self.df = None
        self.original_df = None
        self.cleaning_log = []
        
    def load_data(self):
        """Load the messy dataset."""
        print("📂 Loading messy dataset...")
        self.df = pd.read_csv(self.input_path)
        self.original_df = self.df.copy()  # Keep original for comparison
        print(f"   Loaded {len(self.df)} rows, {len(self.df.columns)} columns")
        return self
    
    def log_change(self, step, description, count):
        """Log cleaning actions for the report."""
        self.cleaning_log.append({
            'step': step,
            'description': description,
            'count': count
        })
    
    def remove_duplicates(self):
        """Remove duplicate rows from the dataset."""
        print("\n🔍 Removing duplicates...")
        
        initial_count = len(self.df)
        
        # Remove exact duplicates
        self.df.drop_duplicates(inplace=True)
        
        duplicates_removed = initial_count - len(self.df)
        
        if duplicates_removed > 0:
            print(f"   ✓ Removed {duplicates_removed} duplicate rows")
            self.log_change('remove_duplicates', 'Duplicate rows removed', duplicates_removed)
        else:
            print(f"   ✓ No duplicates found")
        
        return self

    def clean_whitespace(self):
        """Remove extra whitespace from text columns."""
        print("\n✂️ Cleaning whitespace in text fields...")
        
        text_columns = ['customer_name', 'email', 'product_name', 'category', 'status']
        total_cleaned = 0
        
        for col in text_columns:
            if col in self.df.columns:
                # Count how many have whitespace issues
                has_whitespace = self.df[col].astype(str).str.strip() != self.df[col].astype(str)
                count = has_whitespace.sum()
                
                # Strip leading/trailing whitespace and collapse multiple spaces
                self.df[col] = self.df[col].astype(str).str.strip()
                self.df[col] = self.df[col].str.replace(r'\s+', ' ', regex=True)  # Multiple spaces -> single space
                self.df[col] = self.df[col].str.replace('\t', ' ')  # Tabs -> space
                
                if count > 0:
                    print(f"   ✓ Cleaned {count} values in '{col}'")
                    total_cleaned += count
        
        self.log_change('clean_whitespace', 'Whitespace cleaned in text fields', total_cleaned)
        return self

    def standardize_emails(self):
        """Standardize and validate email addresses."""
        print("\n📧 Standardizing email addresses...")
        
        # Convert to lowercase
        self.df['email'] = self.df['email'].str.lower()
        
        # Email validation regex pattern
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        # Find invalid emails
        valid_emails = self.df['email'].str.match(email_pattern, na=False)
        invalid_count = (~valid_emails & self.df['email'].notna()).sum()
        
        # Mark invalid emails as NaN
        self.df.loc[~valid_emails & self.df['email'].notna(), 'email'] = np.nan
        
        if invalid_count > 0:
            print(f"   ✓ Converted emails to lowercase")
            print(f"   ✓ Marked {invalid_count} invalid emails as missing")
            self.log_change('standardize_emails', 'Invalid emails removed', invalid_count)
        else:
            print(f"   ✓ All emails valid and lowercase")
        
        return self

    def clean_phone_numbers(self):
        """Standardize phone numbers to XXX-XXX-XXXX format."""
        print("\n📱 Standardizing phone numbers...")
        
        def format_phone(phone):
            """Extract digits and format as XXX-XXX-XXXX."""
            if pd.isna(phone):
                return np.nan
            
            # Extract only digits
            digits = re.sub(r'\D', '', str(phone))
            
            # Remove leading 1 if present (country code)
            if len(digits) == 11 and digits.startswith('1'):
                digits = digits[1:]
            
            # Must have exactly 10 digits
            if len(digits) == 10:
                return f"{digits[0:3]}-{digits[3:6]}-{digits[6:10]}"
            else:
                return np.nan  # Invalid phone number
        
        # Count non-null before cleaning
        valid_before = self.df['phone'].notna().sum()
        
        # Apply formatting
        self.df['phone'] = self.df['phone'].apply(format_phone)
        
        # Count non-null after cleaning
        valid_after = self.df['phone'].notna().sum()
        invalid_count = valid_before - valid_after
        
        print(f"   ✓ Standardized {valid_after} phone numbers to XXX-XXX-XXXX format")
        if invalid_count > 0:
            print(f"   ✓ Marked {invalid_count} invalid phone numbers as missing")
            self.log_change('clean_phone_numbers', 'Invalid phone numbers removed', invalid_count)
        
        return self

    def standardize_dates(self):
        """Convert all date formats to YYYY-MM-DD."""
        print("\n📅 Standardizing dates...")
        
        def parse_date(date_str):
            """Try multiple date formats and convert to YYYY-MM-DD."""
            if pd.isna(date_str):
                return np.nan
            
            date_str = str(date_str).strip()
            
            # List of possible date formats in the data
            date_formats = [
                '%m/%d/%Y',      # 01/15/2024
                '%d-%m-%Y',      # 15-01-2024
                '%Y-%m-%d',      # 2024-01-15
                '%b %d, %Y',     # Jan 15, 2024
                '%d %B %Y',      # 15 January 2024
            ]
            
            # Try each format
            for fmt in date_formats:
                try:
                    parsed_date = datetime.strptime(date_str, fmt)
                    
                    # Check if date is in the future (invalid for orders)
                    if parsed_date > datetime.now():
                        return np.nan
                    
                    # Return in standard format
                    return parsed_date.strftime('%Y-%m-%d')
                except ValueError:
                    continue
            
            # If no format worked, return NaN
            return np.nan
        
        # Count valid dates before
        valid_before = self.df['order_date'].notna().sum()
        
        # Apply date parsing
        self.df['order_date'] = self.df['order_date'].apply(parse_date)
        
        # Count valid dates after
        valid_after = self.df['order_date'].notna().sum()
        invalid_count = valid_before - valid_after
        
        print(f"   ✓ Standardized {valid_after} dates to YYYY-MM-DD format")
        if invalid_count > 0:
            print(f"   ✓ Marked {invalid_count} invalid/future dates as missing")
            self.log_change('standardize_dates', 'Invalid dates removed', invalid_count)
        
        return self

    def clean_prices(self):
        """Clean price column - remove symbols and convert to float."""
        print("\n💰 Cleaning prices...")
        
        def parse_price(price):
            """Remove currency symbols and convert to float."""
            if pd.isna(price):
                return np.nan
            
            # Convert to string and remove whitespace
            price_str = str(price).strip()
            
            # Remove $ and commas
            price_str = price_str.replace('$', '').replace(',', '')
            
            try:
                price_float = float(price_str)
                
                # Validate: price should be positive
                if price_float <= 0:
                    return np.nan
                
                return round(price_float, 2)
            except ValueError:
                return np.nan
        
        # Count valid prices before
        valid_before = self.df['price'].notna().sum()
        
        # Apply price cleaning
        self.df['price'] = self.df['price'].apply(parse_price)
        
        # Count valid prices after
        valid_after = self.df['price'].notna().sum()
        invalid_count = valid_before - valid_after
        
        print(f"   ✓ Cleaned {valid_after} prices (removed $, commas)")
        if invalid_count > 0:
            print(f"   ✓ Marked {invalid_count} invalid prices as missing")
            self.log_change('clean_prices', 'Invalid prices removed', invalid_count)
        
        return self

    def clean_quantities(self):
        """Clean quantity column - convert to integer and validate."""
        print("\n🔢 Cleaning quantities...")
        
        def parse_quantity(qty):
            """Convert to integer and validate."""
            if pd.isna(qty):
                return np.nan
            
            try:
                qty_int = int(float(str(qty).strip()))
                
                # Validate: quantity should be positive
                if qty_int <= 0:
                    return np.nan
                
                return qty_int
            except (ValueError, TypeError):
                return np.nan
        
        # Count valid quantities before
        valid_before = self.df['quantity'].notna().sum()
        
        # Apply quantity cleaning
        self.df['quantity'] = self.df['quantity'].apply(parse_quantity)
        
        # Count valid quantities after
        valid_after = self.df['quantity'].notna().sum()
        invalid_count = valid_before - valid_after
        
        print(f"   ✓ Cleaned {valid_after} quantities (converted to integers)")
        if invalid_count > 0:
            print(f"   ✓ Marked {invalid_count} invalid quantities (negative/zero) as missing")
            self.log_change('clean_quantities', 'Invalid quantities removed', invalid_count)
        
        return self

    def standardize_categories(self):
        """Standardize category names to consistent values."""
        print("\n📦 Standardizing categories...")
        
        # Define mapping from variations to standard names
        category_mapping = {
            # Electronics variations
            'electronics': 'Electronics',
            'ELECTRONICS': 'Electronics',
            'elec': 'Electronics',
            'Elec': 'Electronics',
            
            # Clothing variations
            'clothing': 'Clothing',
            'CLOTHING': 'Clothing',
            'clot': 'Clothing',
            'Clot': 'Clothing',
            
            # Home & Garden variations
            'home & garden': 'Home & Garden',
            'HOME & GARDEN': 'Home & Garden',
            'home and garden': 'Home & Garden',
            'Home and Garden': 'Home & Garden',
            'home': 'Home & Garden',
            'Home': 'Home & Garden',
            
            # Books variations
            'books': 'Books',
            'BOOKS': 'Books',
            'book': 'Books',
            'Book': 'Books',
        }
        
        # Count unique categories before
        unique_before = self.df['category'].nunique()
        
        # Apply mapping (leave unmapped values as-is, then title case them)
        self.df['category'] = self.df['category'].replace(category_mapping)
        
        # Apply title case to any remaining values
        self.df['category'] = self.df['category'].str.title()
        
        # Count unique categories after
        unique_after = self.df['category'].nunique()
        variations_removed = unique_before - unique_after
        
        print(f"   ✓ Standardized categories from {unique_before} to {unique_after} unique values")
        if variations_removed > 0:
            self.log_change('standardize_categories', 'Category variations consolidated', variations_removed)
        
        return self

    def standardize_status(self):
        """Standardize order status values."""
        print("\n✅ Standardizing order status...")
        
        # Define mapping from variations to standard statuses
        status_mapping = {
            # Pending variations
            'pending': 'Pending',
            'PENDING': 'Pending',
            'pnding': 'Pending',
            'Pnding': 'Pending',
            'p': 'Pending',
            'P': 'Pending',
            
            # Shipped variations
            'shipped': 'Shipped',
            'SHIPPED': 'Shipped',
            'shippd': 'Shipped',
            'Shippd': 'Shipped',
            'ship': 'Shipped',
            'Ship': 'Shipped',
            
            # Delivered variations
            'delivered': 'Delivered',
            'DELIVERED': 'Delivered',
            'deliverd': 'Delivered',
            'Deliverd': 'Delivered',
            'complete': 'Delivered',
            'Complete': 'Delivered',
            'COMPLETE': 'Delivered',
            
            # Cancelled variations
            'cancelled': 'Cancelled',
            'CANCELLED': 'Cancelled',
            'canceled': 'Cancelled',
            'Canceled': 'Cancelled',
            'cnclld': 'Cancelled',
            'CNCLLD': 'Cancelled',
        }
        
        # Count unique statuses before
        unique_before = self.df['status'].nunique()
        
        # Apply mapping
        self.df['status'] = self.df['status'].replace(status_mapping)
        
        # Count unique statuses after
        unique_after = self.df['status'].nunique()
        variations_removed = unique_before - unique_after
        
        print(f"   ✓ Standardized status from {unique_before} to {unique_after} unique values")
        if variations_removed > 0:
            self.log_change('standardize_status', 'Status variations consolidated', variations_removed)
        
        return self

    def run_cleaning_pipeline(self):
        """Execute all cleaning steps in sequence."""
        print("\n" + "="*60)
        print("🚀 STARTING DATA CLEANING PIPELINE")
        print("="*60)
        
        self.load_data()
        self.remove_duplicates()
        self.clean_whitespace()
        self.standardize_emails()
        self.clean_phone_numbers()
        self.standardize_dates()
        self.clean_prices()
        self.clean_quantities()
        self.standardize_categories()
        self.standardize_status()
        
        print("\n" + "="*60)
        print("✅ CLEANING PIPELINE COMPLETE")
        print("="*60)
        
        return self
    
    def save_cleaned_data(self, output_path):
        """Save the cleaned dataset to CSV."""
        print(f"\n💾 Saving cleaned data...")
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save to CSV
        self.df.to_csv(output_path, index=False)
        
        print(f"   ✓ Cleaned data saved to: {output_path}")
        print(f"   ✓ Total rows: {len(self.df)}")
        
        return self
    
    def generate_report(self, report_path):
        """Generate a comprehensive cleaning report."""
        print(f"\n📊 Generating cleaning report...")
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        with open(report_path, 'w') as f:
            f.write("="*70 + "\n")
            f.write("DATA CLEANING REPORT\n")
            f.write("="*70 + "\n\n")
            
            # Overview
            f.write("OVERVIEW\n")
            f.write("-"*70 + "\n")
            f.write(f"Original rows: {len(self.original_df)}\n")
            f.write(f"Cleaned rows: {len(self.df)}\n")
            f.write(f"Rows removed: {len(self.original_df) - len(self.df)}\n")
            f.write(f"Columns: {len(self.df.columns)}\n\n")
            
            # Cleaning steps performed
            f.write("CLEANING ACTIONS PERFORMED\n")
            f.write("-"*70 + "\n")
            for i, log in enumerate(self.cleaning_log, 1):
                f.write(f"{i}. {log['description']}: {log['count']}\n")
            f.write("\n")
            
            # Data quality before vs after
            f.write("DATA QUALITY COMPARISON\n")
            f.write("-"*70 + "\n")
            f.write(f"{'Field':<20} {'Missing Before':<20} {'Missing After':<20}\n")
            f.write("-"*70 + "\n")
            
            for col in self.df.columns:
                missing_before = self.original_df[col].isna().sum()
                missing_after = self.df[col].isna().sum()
                f.write(f"{col:<20} {missing_before:<20} {missing_after:<20}\n")
            
            f.write("\n")
            
            # Final data statistics
            f.write("FINAL CLEANED DATA STATISTICS\n")
            f.write("-"*70 + "\n")
            f.write(f"Total valid orders: {len(self.df)}\n")
            f.write(f"Unique customers: {self.df['customer_name'].nunique()}\n")
            # Handle date range safely
            if self.df['order_date'].notna().any():
                date_min = self.df['order_date'].dropna().min()
                date_max = self.df['order_date'].dropna().max()
                f.write(f"Date range: {date_min} to {date_max}\n")
            else:
                f.write(f"Date range: No valid dates\n")
            # Handle numeric fields safely
            total_revenue = self.df['price'].sum() if self.df['price'].notna().any() else 0
            avg_order = self.df['price'].mean() if self.df['price'].notna().any() else 0
            total_items = self.df['quantity'].sum() if self.df['quantity'].notna().any() else 0

            f.write(f"Total revenue: ${total_revenue:,.2f}\n")
            f.write(f"Average order value: ${avg_order:.2f}\n")
            f.write(f"Total items sold: {int(total_items)}\n\n")
            # Category breakdown
            f.write("CATEGORY BREAKDOWN\n")
            f.write("-"*70 + "\n")
            category_counts = self.df['category'].value_counts()
            for cat, count in category_counts.items():
                percentage = (count / len(self.df)) * 100
                f.write(f"{cat:<20} {count:<10} ({percentage:.1f}%)\n")
            f.write("\n")
            
            # Status breakdown
            f.write("ORDER STATUS BREAKDOWN\n")
            f.write("-"*70 + "\n")
            status_counts = self.df['status'].value_counts()
            for status, count in status_counts.items():
                percentage = (count / len(self.df)) * 100
                f.write(f"{status:<20} {count:<10} ({percentage:.1f}%)\n")
            f.write("\n")
            
            f.write("="*70 + "\n")
            f.write("END OF REPORT\n")
            f.write("="*70 + "\n")
        
        print(f"   ✓ Report saved to: {report_path}")
        
        return self

if __name__ == "__main__":
    # Define paths
    input_file = 'data/raw/ecommerce_orders_messy.csv'
    output_file = 'data/cleaned/ecommerce_orders_cleaned.csv'
    report_file = 'reports/cleaning_report.txt'
    
    # Run the complete pipeline
    cleaner = DataCleaner(input_file)
    cleaner.run_cleaning_pipeline()
    cleaner.save_cleaned_data(output_file)
    cleaner.generate_report(report_file)
    
    # Display summary
    print("\n" + "="*60)
    print("📈 SUMMARY")
    print("="*60)
    print(f"✅ Original dataset: {len(cleaner.original_df)} rows")
    print(f"✅ Cleaned dataset: {len(cleaner.df)} rows")
    print(f"✅ Rows removed: {len(cleaner.original_df) - len(cleaner.df)}")
    print(f"✅ Data quality improved across {len(cleaner.cleaning_log)} steps")
    print("\n📁 Output files created:")
    print(f"   • {output_file}")
    print(f"   • {report_file}")
    print("\n🎉 Data cleaning complete! Check the report for details.")
    print("="*60)