import logging

# FORMAT = "%(asctime)s %(clientip)-15s %(user)-8s %(message)s"
# logging.basicConfig(format=FORMAT)
# d = {"clientip": "192.168.0.1", "user": "fbloggs"}
# logger = logging.getLogger("tcpserver")


def get_logger(module_name: str) -> logging.Logger:
    """_summary_

    Args:
        module_name: _description_

    Returns:
        _description_
    """
    return logging.getLogger(module_name)
