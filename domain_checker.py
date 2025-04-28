import whois
import time
import sys
from concurrent.futures import ThreadPoolExecutor

# List of creative domain name suggestions (only checking .com)
domain_names = [
    # Professional & Business-Focused
    "InvoiceCanvas", "BillingLaunch", "InvoiceSuite", "PaymentForge", "InvoiceArchitect",
    "BillingMatrix", "InvoiceCatalyst", "ReceiptGenius", "InvoiceEmpire", "BillingOrbit",
    
    # Modern & Tech-Focused
    "InvoicePixel", "BillingByte", "InvoiceCode", "DigitalReceipt", "InvoiceAlgorithm",
    "BillingCloud", "InvoiceMatrix", "CyberBilling", "InvoiceNexus", "TechInvoice",
    
    # Simple & Direct
    "MakeInvoice", "SimpleBiller", "EasyInvoicing", "QuickBills", "JustInvoice",
    "DirectBilling", "PureInvoice", "ClearBilling", "PlainInvoice", "StraightBill",
    
    # Clever Wordplay
    "InvoiceAble", "BillBright", "InvoiceLy", "BillWise", "InvoiceFy",
    "BillBuddy", "InvoiceIQ", "BillGenius", "InvoiceMind", "BillSavvy",
    
    # Financial Terms
    "InvoiceCapital", "BillingAsset", "InvoiceTreasury", "BillingEquity", "InvoiceVenture",
    "BillingFund", "InvoiceProfit", "BillingRevenue", "InvoicePortfolio", "BillingDividend",
    
    # Metaphorical
    "InvoiceRocket", "BillingLaunchpad", "InvoiceJourney", "BillingBridge", "InvoiceCompass",
    "BillingLighthouse", "InvoiceAnchor", "BillingHarbor", "InvoiceVoyage", "BillingPilot",
    
    # Creative Compounds
    "InvoiceStudio", "BillCraft", "InvoiceForge", "BillSmith", "InvoiceWorks",
    "BillFactory", "InvoiceLab", "BillShop", "InvoiceHub", "BillCenter",
    
    # Friendly & Approachable
    "FriendlyInvoice", "HappyBilling", "SmileInvoice", "CheerfulBill", "PleasantInvoice",
    "JoyfulBilling", "DelightfulInvoice", "GladBill", "WarmInvoice", "KindBilling",
    
    # Efficiency-Focused
    "SwiftInvoice", "RapidBilling", "InstantInvoice", "SpeedyBill", "QuickInvoice",
    "FastBilling", "PromptInvoice", "ExpressBill", "FlashInvoice", "TurboInvoice",
    
    # Premium & Luxury
    "EliteInvoice", "PremiumBilling", "LuxuryInvoice", "PrestigeBill", "ExclusiveInvoice",
    "SupremeBilling", "RoyalInvoice", "NobleInvoice", "GrandBilling", "MajesticInvoice",
    
    # Unique & Memorable
    "InvoiceZephyr", "BillingQuest", "InvoiceJewel", "BillingCrystal", "InvoiceWhisper",
    "BillingEcho", "InvoiceSparkle", "BillingCharm", "InvoiceMagic", "BillingWonder",
    
    # Memorable Phrases
    "SendTheBill", "MakeMyInvoice", "BillItNow", "InvoiceMeUp", "GetPaidFast",
    "BillsOnTime", "InvoiceAndGo", "BillWithEase", "InvoiceItRight", "BillsNoHassle"
]

def check_domain(domain_name):
    """Check if a domain is available."""
    domain = f"{domain_name.lower()}.com"
    try:
        domain_info = whois.whois(domain)
        # If the domain doesn't have a registration date or registrar, it might be available
        if domain_info.registrar is None and domain_info.creation_date is None:
            return domain, True
        else:
            return domain, False
    except Exception as e:
        error_str = str(e)
        # If there's an error with "No match for domain", the domain is likely available
        if "No match for domain" in error_str or "No match for" in error_str:
            return domain, True
        # Sleep a bit to avoid rate limiting
        time.sleep(1)
        return domain, f"Error: {error_str}"

def main():
    available_domains = []
    unavailable_domains = []
    error_domains = []
    
    # Select a subset of domain names to avoid rate limiting
    # Check the next 50 domains (skip the first 50 we already checked)
    selected_domains = domain_names[50:100]  
    
    print(f"Checking availability for {len(selected_domains)} .com domains...")
    print("This may take a few minutes. Please wait...")
    
    # Use ThreadPoolExecutor to check domains in parallel
    with ThreadPoolExecutor(max_workers=3) as executor:  # Further reduced workers to avoid rate limiting
        results = list(executor.map(check_domain, selected_domains))
    
    # Process results
    for domain, status in results:
        if status is True:
            available_domains.append(domain)
        elif isinstance(status, str) and status.startswith("Error"):
            error_domains.append((domain, status))
        else:
            unavailable_domains.append(domain)
    
    # Print results
    print("\n=== AVAILABLE DOMAINS ===")
    for domain in available_domains:
        print(f"+ {domain}")
    
    print(f"\n=== UNAVAILABLE DOMAINS ({len(unavailable_domains)}) ===")
    for domain in unavailable_domains[:10]:  # Show only first 10 unavailable
        print(f"X {domain}")
    if len(unavailable_domains) > 10:
        print(f"... and {len(unavailable_domains) - 10} more")
    
    print("\n=== ERRORS ===")
    for domain, error in error_domains:
        print(f"? {domain}: {error}")
    
    print(f"\nSummary: {len(available_domains)} available, {len(unavailable_domains)} unavailable, {len(error_domains)} errors")

if __name__ == "__main__":
    main()
