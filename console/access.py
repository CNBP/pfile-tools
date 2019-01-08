import paramiko


def getSSHClient(destination_ip: str, destination_login: str, destination_password: str) -> paramiko.SSHClient:
    """
    Instantiate, setup and return a straight forward proxy SSH client
    :param destination_ip:
    :param destination_login:
    :param destination_password:
    :return: a connected client.
    """
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(destination_ip, 22, username=destination_login, password=destination_password)
    return client


