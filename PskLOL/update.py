from ._updatedb import fetch_data


def update(institution: int):
    fetch_data(institution)
