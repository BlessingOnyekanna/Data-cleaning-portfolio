"""
Generate messy e-commerce dataset for data cleaning demonstration.
This script creates intentional data quality issues for portfolio purposes.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_messy_dataset(num_rows=250):
    """Generate e-commerce dataset with intentional data quality issues."""
    
    # Product data with intentional inconsistencies
    products = {
        'Electronics': [
            ('iPhone 13', 'iphone 13', 'IPHONE 13', 'iPhone13', 'Iphone 13'),
            ('Samsung Galaxy', 'samsung galaxy', 'SAMSUNG GALAXY', 'SamsungGalaxy'),
            ('MacBook Pro', 'macbook pro', 'MacBook  Pro', 'Macbook Pro'),
            ('AirPods', 'airpods', 'Air Pods', 'AIRPODS')
        ],
        'Clothing': [
            ("Men's T-Shirt", "mens tshirt", "MEN'S T-SHIRT", "Mens T-shirt"),
            ('Jeans', 'jeans', 'JEANS', 'Jean'),
            ('Running Shoes', 'running shoes', 'RUNNING SHOES', 'RunningShoes')
        ],
        'Home & Garden': [
            ('Coffee Maker', 'coffee maker', 'COFFEE MAKER', 'CoffeeMaker'),
            ('Vacuum Cleaner', 'vacuum cleaner', 'VacuumCleaner', 'Vaccuum Cleaner'),  # typo
        ],
        'Books': [
            ('Python Programming', 'python programming', 'PYTHON PROGRAMMING'),
            ('Data Science Handbook', 'data science handbook', 'DataScience Handbook')
        ]
    }
    
    # Status variations
    statuses = {
        'pending': ['Pending', 'pending', 'PENDING', 'Pnding', 'P'],
        'shipped': ['Shipped', 'shipped', 'SHIPPED', 'Shippd', 'Ship'],
        'delivered': ['Delivered', 'delivered', 'DELIVERED', 'Deliverd', 'Complete'],
        'cancelled': ['Cancelled', 'cancelled', 'CANCELLED', 'Canceled', 'CNCLLD']
    }
    
    first_names = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Emily', 'Robert', 'Lisa', 
                   'William', 'Maria', 'James', 'Jennifer', 'Richard', 'Linda', 'Thomas',
                   'Christopher', 'Jessica', 'Daniel', 'Michelle', 'Matthew']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 
                  'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Wilson', 'Anderson',
                  'Taylor', 'Thomas', 'Moore', 'Jackson', 'Martin', 'Lee']
    
    data = []
    
    for i in range(num_rows):
        # 15% chance of true duplicate (exact same order with minor variations)
        if i > 20 and random.random() < 0.15:
            duplicate_idx = random.randint(max(0, i-50), i-1)
            row = data[duplicate_idx].copy()
            # Add slight variation to make it realistic duplicate
            if random.random() < 0.5:
                row['customer_name'] = row['customer_name'].strip()  # Remove whitespace
            if random.random() < 0.3:
                row['email'] = row['email'].upper() if isinstance(row['email'], str) else row['email']
        else:
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            
            # Customer name variations (whitespace, case issues)
            name_formats = [
                f"{first_name} {last_name}",  # Normal
                f"  {first_name}  {last_name}  ",  # Extra spaces
                f"{first_name.upper()} {last_name.upper()}",  # All caps
                f"{first_name.lower()} {last_name.lower()}",  # All lowercase
                f"{first_name}\t{last_name}",  # Tab
            ]
            customer_name = random.choice(name_formats) if random.random() < 0.4 else f"{first_name} {last_name}"
            
            # Order ID variations
            order_id_formats = [
                f"ORD{1000 + i}",
                f"#{1000 + i}",
                f"ORD-{1000 + i}",
                f"{1000 + i}",
                f"order{1000 + i}",
            ]
            order_id = random.choice(order_id_formats)
            
            # Email issues
            if random.random() < 0.15:  # 15% missing
                email = np.nan
            elif random.random() < 0.12:  # 12% invalid
                invalid_emails = [
                    f"{first_name.lower()}.{last_name.lower()}",  # No @
                    f"{first_name.lower()}@",  # Incomplete
                    f"@{last_name.lower()}.com",  # No username
                    f"{first_name.lower()} {last_name.lower()}@email.com",  # Space
                    "invalidemail",
                ]
                email = random.choice(invalid_emails)
            else:
                email_base = f"{first_name.lower()}.{last_name.lower()}@example.com"
                # Mix case randomly
                if random.random() < 0.3:
                    email = email_base.upper() if random.random() < 0.5 else f"  {email_base}  "
                else:
                    email = email_base
            
            # Phone variations
            if random.random() < 0.20:  # 20% missing
                phone = np.nan
            else:
                area = random.randint(200, 999)
                prefix = random.randint(200, 999)
                line = random.randint(1000, 9999)
                phone_formats = [
                    f"({area})-{prefix}-{line}",
                    f"{area}-{prefix}-{line}",
                    f"{area}{prefix}{line}",
                    f"({area}) {prefix}-{line}",
                    f"+1-{area}-{prefix}-{line}",
                    f"{area}.{prefix}.{line}",
                ]
                phone = random.choice(phone_formats)
            
            # Date with multiple formats and some invalid
            if random.random() < 0.05:  # 5% future dates (invalid)
                order_date = (datetime.now() + timedelta(days=random.randint(1, 100))).strftime("%m/%d/%Y")
            elif random.random() < 0.03:  # 3% missing
                order_date = np.nan
            else:
                base_date = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 400))
                date_formats = [
                    base_date.strftime("%m/%d/%Y"),  # MM/DD/YYYY
                    base_date.strftime("%d-%m-%Y"),  # DD-MM-YYYY
                    base_date.strftime("%Y-%m-%d"),  # YYYY-MM-DD
                    base_date.strftime("%b %d, %Y"),  # Jan 15, 2024
                    base_date.strftime("%d %B %Y"),  # 15 January 2024
                ]
                order_date = random.choice(date_formats)
            
            # Product selection
            category = random.choice(list(products.keys()))
            product_variations = random.choice(products[category])
            product_name = random.choice(product_variations)
            
            # Category variations
            if random.random() < 0.3:
                category_variations = [category, category.upper(), category.lower(), 
                                      category[:4], category.replace('&', 'and')]
                category = random.choice(category_variations)
            
            # Quantity with issues
            if random.random() < 0.05:  # 5% negative (invalid)
                quantity = -random.randint(1, 5)
            elif random.random() < 0.05:  # 5% zero (questionable)
                quantity = 0
            elif random.random() < 0.08:  # 8% as string
                quantity = str(random.randint(1, 10))
            else:
                quantity = random.randint(1, 10)
            
            # Price with formatting issues
            base_price = round(random.uniform(9.99, 599.99), 2)
            if random.random() < 0.25:  # 25% with $ symbol
                price = f"${base_price}"
            elif random.random() < 0.15:  # 15% with comma
                price = f"${base_price:,.2f}"
            elif random.random() < 0.10:  # 10% as string without $
                price = str(base_price)
            elif random.random() < 0.05:  # 5% missing
                price = np.nan
            else:
                price = base_price
            
            # Status
            status_category = random.choice(list(statuses.keys()))
            status = random.choice(statuses[status_category])
            
            row = {
                'order_id': order_id,
                'customer_name': customer_name,
                'email': email,
                'phone': phone,
                'order_date': order_date,
                'product_name': product_name,
                'category': category,
                'quantity': quantity,
                'price': price,
                'status': status,
            }
        
        data.append(row)
    
    return pd.DataFrame(data)


if __name__ == "__main__":
    # Generate dataset
    print("🔄 Generating messy e-commerce dataset...")
    df = generate_messy_dataset(250)
    
    # Create output directory if it doesn't exist
    os.makedirs('data/raw', exist_ok=True)
    
    # Save to data/raw folder
    output_path = 'data/raw/ecommerce_orders_messy.csv'
    df.to_csv(output_path, index=False)
    
    print(f"\n✅ Dataset saved to: {output_path}")
    print(f"   Total rows: {len(df)}")
    
    # Display summary statistics
    print("\n=== DATA QUALITY ISSUES SUMMARY ===")
    print(f"1. Missing emails: {df['email'].isna().sum()}")
    print(f"2. Missing phones: {df['phone'].isna().sum()}")
    print(f"3. Missing prices: {df['price'].isna().sum()}")
    print(f"4. Missing dates: {df['order_date'].isna().sum()}")
    print(f"5. Duplicate rows: {df.duplicated().sum()}")
    print(f"6. Unique product name variations: {df['product_name'].nunique()}")
    print(f"7. Unique category variations: {df['category'].nunique()}")
    print(f"8. Unique status variations: {df['status'].nunique()}")
    
    print("\n📊 Sample of messy data:")
    print(df.head(10).to_string())