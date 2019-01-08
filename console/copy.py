def download_through_client(client, remote_path, local_file_path):
    """
    This routeine is used to upload via SSH.
    :param remote_path:
    :param local_file_path:
    :return:
    """
    sftp = client.open_sftp()
    sftp.get(remote_path, local_file_path)
    sftp.close()