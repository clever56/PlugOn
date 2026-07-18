#!/usr/bin/env python3
"""
Bug Bounty Dorks - Automated Google Search Script
Discovery tool for finding bug bounty programs using Google Dorks

Usage:
    python dork_search.py                    # Basic run
    python dork_search.py --limit 10         # Search 10 dorks
    python dork_search.py --output results.csv  # Save to file
    python dork_search.py --delay 5          # 5 second delay between searches
"""

import argparse
import time
import csv
from datetime import datetime
from pathlib import Path

def load_dorks(filepath="dorks.txt"):
    """
    Load dorks from file.
    
    Args:
        filepath: Path to dorks.txt file
        
    Returns:
        List of dork queries
    """
    if not Path(filepath).exists():
        print(f"Error: {filepath} not found!")
        return []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        dorks = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    return dorks

def generate_google_url(dork):
    """
    Generate a Google search URL for a dork.
    
    Args:
        dork: The search query
        
    Returns:
        URL string for Google search
    """
    # URL encode the dork
    from urllib.parse import quote
    encoded = quote(dork)
    return f"https://www.google.com/search?q={encoded}"

def print_header():
    """
    Print welcome header.
    """
    print("\n" + "="*60)
    print("  BUG BOUNTY DORKS - Search Generator")
    print("  Automated Google Search Query Generator")
    print("="*60)
    print()

def print_dork_info(index, total, dork):
    """
    Print information about current dork.
    
    Args:
        index: Current dork number
        total: Total dorks
        dork: The dork query
    """
    print(f"\n[{index}/{total}] Dork Query:")
    print(f"    Query: {dork}")
    print(f"    Google URL: {generate_google_url(dork)}")

def save_to_csv(dorks, output_file):
    """
    Save dorks to CSV file with Google search URLs.
    
    Args:
        dorks: List of dork queries
        output_file: Output CSV filename
    """
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Index', 'Dork Query', 'Google Search URL', 'Generated Date'])
        
        for i, dork in enumerate(dorks, 1):
            url = generate_google_url(dork)
            timestamp = datetime.now().isoformat()
            writer.writerow([i, dork, url, timestamp])
    
    print(f"✓ Results saved to {output_file}")
    print(f"  Total dorks: {len(dorks)}")

def main():
    """
    Main function.
    """
    parser = argparse.ArgumentParser(
        description='Bug Bounty Dorks - Google Search Query Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python dork_search.py                    # Show all dorks
  python dork_search.py --limit 10         # Show first 10 dorks
  python dork_search.py --output results.csv  # Export to CSV
  python dork_search.py --limit 5 --output findings.csv
        '''
    )
    
    parser.add_argument(
        '-l', '--limit',
        type=int,
        default=None,
        help='Limit number of dorks to process (default: all)'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output CSV file (if specified, results are saved to file)'
    )
    parser.add_argument(
        '-d', '--delay',
        type=int,
        default=0,
        help='Delay between dorks in seconds (default: 0)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show verbose output'
    )
    parser.add_argument(
        '-f', '--file',
        type=str,
        default='dorks.txt',
        help='Path to dorks.txt file (default: dorks.txt)'
    )
    
    args = parser.parse_args()
    
    # Print header
    print_header()
    
    # Load dorks
    print("📂 Loading dorks from file...")
    dorks = load_dorks(args.file)
    
    if not dorks:
        print("❌ No dorks found!")
        return
    
    print(f"✓ Loaded {len(dorks)} dorks")
    
    # Apply limit
    if args.limit:
        dorks = dorks[:args.limit]
        print(f"✓ Limited to first {len(dorks)} dorks")
    
    # Process dorks
    print(f"\n🔍 Generating Google search URLs...\n")
    
    for i, dork in enumerate(dorks, 1):
        if args.verbose:
            print_dork_info(i, len(dorks), dork)
        else:
            print(f"[{i}/{len(dorks)}] {dork[:60]}..." if len(dork) > 60 else f"[{i}/{len(dorks)}] {dork}")
        
        if args.delay and i < len(dorks):
            time.sleep(args.delay)
    
    # Save to output file if specified
    if args.output:
        print(f"\n💾 Saving results...")
        save_to_csv(dorks, args.output)
    
    # Print summary
    print(f"\n" + "="*60)
    print(f"  ✓ Processing Complete")
    print(f"  Total dorks processed: {len(dorks)}")
    if args.output:
        print(f"  Output file: {args.output}")
    print(f"="*60)
    
    # Instructions
    print(f"\n📚 Next Steps:")
    print(f"  1. Open generated URLs in your browser")
    print(f"  2. Review Google search results")
    print(f"  3. Visit promising company websites")
    print(f"  4. Look for security/bug-bounty pages")
    print(f"  5. Document findings in a spreadsheet")
    print(f"\n⚠️  Remember:")
    print(f"  • Only test programs you have permission to test")
    print(f"  • Follow responsible disclosure guidelines")
    print(f"  • Review each program's rules before testing")
    print(f"\n")

if __name__ == "__main__":
    main()
