from usfm import USFMParser

def select_parser(version_info):
    if "USFM" in version_info:
        return USFMParser, "USFM"