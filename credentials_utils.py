def read_credentials(cred_path):
    username = password = None
    with open(cred_path, 'r') as f:
        for line in f:
            if line.startswith('username='):
                username = line.strip().split('=', 1)[1]
            elif line.startswith('password='):
                password = line.strip().split('=', 1)[1]
    if not username or not password:
        raise ValueError('Username or password not found in credentials.txt')
    return username, password
