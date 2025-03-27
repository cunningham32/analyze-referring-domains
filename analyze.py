import pandas as pd
import glob
import os
from ipaddress import IPv4Address
from collections import defaultdict

def is_sequential_ip(ip1, ip2):
    """Check if two IPs are sequential in the first three octets"""
    try:
        # Split IPs into octets
        oct1 = list(map(int, ip1.split('.')))
        oct2 = list(map(int, ip2.split('.')))
        
        # Check if first two octets are identical
        if oct1[0] != oct2[0] or oct1[1] != oct2[1]:
            return False
            
        # Check if third octet is sequential
        return abs(oct1[2] - oct2[2]) == 1
    except:
        return False

def analyze_single_report(report_file):
    try:
        # Create processed directory if it doesn't exist
        processed_dir = 'processed'
        if not os.path.exists(processed_dir):
            os.makedirs(processed_dir)

        # Read the report
        df = pd.read_csv(report_file)
        ip_records = []
        
        # Store each record
        for _, row in df.iterrows():
            ip = row['IP Address']
            country = row['Country']
            domain = row['Domain']
            ip_records.append((ip, country, domain))
        
        # Create lists to store results
        identical_results = []
        sequential_results = []
        
        # Group by IP address
        ip_groups = defaultdict(list)
        for record in ip_records:
            ip_groups[record[0]].append(record)
        
        # Find identical IPs (only include groups with multiple domains)
        for ip, records in ip_groups.items():
            if len(records) > 1:  # Only include if multiple domains share the IP
                for ip, country, domain in records:
                    identical_results.append({
                        'IP Address': ip,
                        'Country': country,
                        'Domain': domain,
                        'Group Type': 'Identical'
                    })
        
        # Find sequential IPs
        sorted_ips = sorted(ip_groups.keys(), key=lambda x: IPv4Address(x))
        
        current_group = [sorted_ips[0]]
        for i in range(1, len(sorted_ips)):
            if is_sequential_ip(sorted_ips[i-1], sorted_ips[i]):
                current_group.append(sorted_ips[i])
            else:
                if len(current_group) > 1:  # Only include groups with multiple IPs
                    for ip in current_group:
                        for record in ip_groups[ip]:
                            sequential_results.append({
                                'IP Address': record[0],
                                'Country': record[1],
                                'Domain': record[2],
                                'Group Type': 'Sequential'
                            })
                current_group = [sorted_ips[i]]
        
        # Handle last sequential group
        if len(current_group) > 1:  # Only include groups with multiple IPs
            for ip in current_group:
                for record in ip_groups[ip]:
                    sequential_results.append({
                        'IP Address': record[0],
                        'Country': record[1],
                        'Domain': record[2],
                        'Group Type': 'Sequential'
                    })
        
        # Combine results and save to CSV only if we found any groups
        all_results = identical_results + sequential_results
        if all_results:
            # Generate output filename based on input filename
            base_name = os.path.splitext(os.path.basename(report_file))[0]
            output_file = f'{base_name}_analysis_results.csv'
            
            results_df = pd.DataFrame(all_results)
            results_df.to_csv(output_file, index=False)
            print(f"Results for {report_file} have been saved to {output_file}")
        else:
            print(f"No IP groups found in {report_file}")
        
        # Move original file to processed directory
        processed_file = os.path.join(processed_dir, os.path.basename(report_file))
        os.rename(report_file, processed_file)
        print(f"Original file {report_file} has been moved to {processed_file}")
            
    except Exception as e:
        print(f"Error processing {report_file}: {e}")
        return False
    
    return True

def process_reports():
    # Get all CSV files in the reports directory
    csv_files = glob.glob(os.path.join('reports', '*.csv'))
    
    if not csv_files:
        print("No CSV files found in the reports directory")
        return
    
    for report_file in csv_files:
        print(f"\nProcessing {report_file}...")
        analyze_single_report(report_file)

if __name__ == "__main__":
    process_reports()