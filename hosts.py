import sys

def update_hosts(ip, domain, hosts_file="/etc/hosts"):
    try:
        # Read the current contents of the hosts file
        with open(hosts_file, 'r') as file:
            lines = file.readlines()
        
        # Check if the domain exists and process accordingly
        domain_exists = False
        updated = False
        
        for index, line in enumerate(lines):
            # Skip comment or empty lines
            if line.strip().startswith("#") or not line.strip():
                continue
            
            # Parse each line into IP and domains
            parts = line.split()
            if len(parts) >= 2 and domain in parts[1:]:
                domain_exists = True
                if parts[0] == ip:
                    print(f"The domain '{domain}' with IP '{ip}' already exists.")
                    return
                else:
                    # Update IP for the domain
                    lines[index] = f"{ip} {domain}\n"
                    updated = True
                    break
        
        # Add the new entry if the domain does not exist
        if not domain_exists:
            lines.append(f"{ip} {domain}\n")
            updated = True
        
        # Write changes back to the hosts file if updates were made
        if updated:
            with open(hosts_file, 'w') as file:
                file.writelines(lines)
            print(f"The hosts file has been updated: {ip} {domain}")
        else:
            print("No changes were made to the hosts file.")
    
    except PermissionError:
        print("Permission denied. Please run the script with sudo.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python update_hosts.py <IP> <DOMAIN>")
        sys.exit(1)
    
    ip = sys.argv[1]
    domain = sys.argv[2]
    update_hosts(ip, domain)
