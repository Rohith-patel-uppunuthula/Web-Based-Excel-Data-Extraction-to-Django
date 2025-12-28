import requests
import pandas as pd
from bs4 import BeautifulSoup
import openpyxl
from datetime import datetime

def download_nsdl_fii_data(url=None):
    """
    Downloads FII sector-wise investment data from NSDL and saves to Excel
    """
    
    # Default to the latest report URL
    if url is None:
        url = "https://www.fpi.nsdl.co.in/web/StaticReports/Fortnightly_Sector_wise_FII_Investment_Data/FIIInvestSector_Dec152025.html"
    
    print("=" * 70)
    print("NSDL FII Sector-wise Investment Data Downloader")
    print("=" * 70)
    print(f"\nTarget URL: {url}")
    
    # Headers to mimic browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'https://www.fpi.nsdl.co.in/'
    }
    
    try:
        print("\nConnecting to NSDL server...")
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            print("✓ Successfully connected!")
            print(f"✓ Downloaded {len(response.content)} bytes")
            
            # Save the HTML file for reference
            with open("nsdl_page.html", "w", encoding="utf-8") as f:
                f.write(response.text)
            print("✓ Saved HTML to 'nsdl_page.html'")
            
            # Parse tables from HTML
            print("\nExtracting tables from HTML...")
            dfs = pd.read_html(response.text)
            print(f"✓ Found {len(dfs)} table(s)")
            
            # Display information about each table
            print("\nTable Summary:")
            print("-" * 70)
            for idx, df in enumerate(dfs):
                print(f"Table {idx+1}: {len(df)} rows × {len(df.columns)} columns")
                if len(df) > 0:
                    print(f"  First few columns: {list(df.columns[:5])}")
            print("-" * 70)
            
            # Save to Excel with multiple sheets
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"NSDL_FII_Sector_Data_{timestamp}.xlsx"
            
            print(f"\nSaving data to Excel file: {output_file}")
            
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                for idx, df in enumerate(dfs):
                    if len(df) > 0:
                        # Create meaningful sheet names
                        if idx == 0:
                            sheet_name = 'Sector_Investment_Data'
                        else:
                            sheet_name = f'Table_{idx+1}'
                        
                        # Clean the data
                        df = df.copy()
                        
                        # Clean column names (remove newlines, extra spaces)
                        df.columns = [str(col).replace('\n', ' ').strip() for col in df.columns]
                        
                        # Remove completely empty rows
                        df = df.dropna(how='all')
                        
                        # Save to Excel
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
                        print(f"  ✓ Saved '{sheet_name}': {len(df)} rows × {len(df.columns)} columns")
            
            print(f"\n{'='*70}")
            print(f"SUCCESS! Data saved to: {output_file}")
            print(f"{'='*70}")
            
            # Display preview of the main table
            if len(dfs) > 0:
                main_df = dfs[0]
                print("\nPreview of main data (first 10 rows):")
                print("-" * 70)
                pd.set_option('display.max_columns', None)
                pd.set_option('display.width', None)
                pd.set_option('display.max_colwidth', 20)
                print(main_df.head(10))
                print("-" * 70)
                print(f"\nTotal sectors: {len(main_df)}")
            
            return dfs
            
        else:
            print(f"❌ Failed to connect. HTTP Status: {response.status_code}")
            print(f"Response: {response.text[:500]}")
            return None
            
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection Error: {str(e)}")
        print("\nPossible reasons:")
        print("  1. No internet connection")
        print("  2. Website is down")
        print("  3. Firewall/proxy blocking the request")
        print("  4. VPN might be required")
        return None
        
    except requests.exceptions.Timeout:
        print("❌ Request timed out. The server took too long to respond.")
        return None
        
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def list_available_reports():
    """
    Helper function to list other available reports
    You can modify dates to get different reports
    """
    print("\nOther available report URLs (modify date as needed):")
    print("-" * 70)
    
    dates = [
        "Dec152025", "Nov302025", "Nov152025", 
        "Oct312025", "Oct152025"
    ]
    
    base_url = "https://www.fpi.nsdl.co.in/web/StaticReports/Fortnightly_Sector_wise_FII_Investment_Data/FIIInvestSector_{}.html"
    
    for date in dates:
        print(f"  {base_url.format(date)}")

if __name__ == "__main__":
    # Main execution
    print("\n")
    
    # Download the latest report
    url = "https://www.fpi.nsdl.co.in/web/StaticReports/Fortnightly_Sector_wise_FII_Investment_Data/FIIInvestSector_Dec152025.html"
    
    dfs = download_nsdl_fii_data(url)
    
    if dfs:
        print("\n✓ Download completed successfully!")
        
        # Optional: Show available reports
        print("\n")
        list_available_reports()
        
        print("\n" + "="*70)
        print("TIP: To download a different date, modify the URL in the script")
        print("="*70)
    else:
        print("\n❌ Download failed. Please check the error messages above.")
    
    print("\n")