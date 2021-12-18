from dataclasses import dataclass


@dataclass
class Connection:
    """
    Class for abstracting keys from connection.
    """
    public_api_key: str
    private_api_key: str
