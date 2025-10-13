# Import the 'connection' class from the OpenStack SDK
# This class provides a high-level interface to interact with OpenStack services (e.g., compute, network, identity)
from openstack import connection

# Define a function that creates and returns an authenticated OpenStack connection object
def create_connection():
    # Return a new OpenStack connection using the provided authentication parameters
    # These credentials must match what’s configured on your OpenStack environment
    return connection.Connection(
        # The URL of the OpenStack Identity (Keystone) service
        # This is where authentication requests are sent
        auth_url='insert url here',

        # The name of the OpenStack project (tenant) to authenticate into
        project_name='admin',

        # The username used to log in to the OpenStack environment
        username='admin',

        # The corresponding password for the username above
        password='insert password here',

        # The domain name of the user (commonly "Default" in DevStack)
        user_domain_name='Default',

        # The domain name of the project (commonly "Default" in DevStack)
        project_domain_name='Default'
    )
