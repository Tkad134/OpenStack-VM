# Import the connection class from the OpenStack SDK
# This class provides a high-level interface to interact with OpenStack services 
from openstack import connection

# Define a function that creates and returns an authenticated OpenStack connection object
def create_connection():
    # Return a new OpenStack connection using the provided authentication parameters
    # Match these credentials to what you have configured on your openstack environment. 
    return connection.Connection(
        # The URL of the OpenStack Identity (Keystone) service
        # This is where authentication requests are sent
        auth_url='insert url here',

        # The name of the OpenStack project to authenticate into
        project_name='admin',

        # The username used to log in to the OpenStack environment
        username='admin',

        # The corresponding password for the username above
        password='insert password here',

        # The domain name of the user 
        user_domain_name='Default',

        # The domain name of the project 
        project_domain_name='Default'
    )
