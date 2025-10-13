# Import the time module to allow us to pause execution 
import time

# Import a custom function create_connection from utils.connection module
# creates and returns an OpenStack connection object
from utils.connection import create_connection

# Import a custom function choose_host_hint from the scheduler module
# pick a host or placement hint for VM scheduling
from scheduler import choose_host_hint


# Define a function that creates a virtual machine (VM) on OpenStack
def create_vm(conn, name, image, flavor, network, scheduler_hints=None, az=None):
    # Define a dictionary with the basic attributes required to create a VM
    server_attrs = {
        'name': name,                     # Name of the VM
        'image_id': image,                # ID of the image to boot the VM from
        'flavor_id': flavor,              # ID of the flavor to use
        'networks': [{"uuid": network}],  # Network ID to attach the VM to
    }

    # If a scheduler hint is provided include it in the server attributes
    if scheduler_hints:
        server_attrs['scheduler_hints'] = scheduler_hints

    # If an availability zone is provided include it in the server attributes
    if az:
        server_attrs['availability_zone'] = az

    # Print a message indicating that VM creation is starting
    print(f"Creating VM: {name}")

    # Use the OpenStack SDK to send a request to create the VM with the given attributes
    server = conn.compute.create_server(**server_attrs)

    # Wait for the VM creation to complete and reach the ACTIVE state
    server = conn.compute.wait_for_server(server)

    # Print a success message once the VM is active
    print(f"✅ VM {name} is ACTIVE (ID: {server.id})")

    # Return the server object (useful for further actions)
    return server


# Define a function to list all currently running VMs
def list_vms(conn):
    # Print a header for the list
    print("\nCurrent VMs:")

    # Loop through all the servers retrieved from the compute service
    for srv in conn.compute.servers():
        # Print each VM’s name and status (e.g., ACTIVE, SHUTOFF)
        print(f"  - {srv.name} ({srv.status})")


# Define a function to delete a VM by its ID
def delete_vm(conn, server_id):
    # Use the OpenStack SDK to send a delete request for the given server
    conn.compute.delete_server(server_id)

    # Print a message confirming deletion
    print(f"🗑️ Deleted VM {server_id}")


# Define the main function where everything is orchestrated
def main():
    # Establish an OpenStack connection by calling the helper function
    conn = create_connection()

    # Define the resource IDs to use when creating VMs
    IMAGE = "4ec51d9b-d81a-42cb-9b88-542890bad699"   # The image UUID or name
    FLAVOR = "m1.tiny"                               # The flavor name or ID
    NETWORK = "eef99664-e954-49e9-a64f-168914fccf2c" # The network UUID
    AVAIL_ZONE = "nova"                              # Availability zone to deploy in

    # Launch multiple VMs with scheduling logic
    for i in range(2):  # Loop runs twice: i = 0 and i = 1
        # Construct a VM name with an incrementing number
        name = f"vm-auto-{i+1}"

        # Get a scheduling hint from the scheduler module 
        hint = choose_host_hint()

        # Create the VM using the provided parameters and hint
        vm = create_vm(conn, name, IMAGE, FLAVOR, NETWORK, scheduler_hints=hint, az=AVAIL_ZONE)

    # After creating the VMs list all current VMs to verify
    list_vms(conn)

    # Wait for 30 seconds before cleaning up (gives time to observe VMs)
    time.sleep(30)

    # Print a header indicating cleanup is starting
    print("\nCleaning up VMs...")

    # Loop through all servers again and delete them one by one
    for srv in conn.compute.servers():
        delete_vm(conn, srv.id)


if __name__ == "__main__":
    main()
