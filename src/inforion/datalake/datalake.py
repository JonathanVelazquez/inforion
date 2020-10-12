import requests
import aiohttp
from inforion.ionapi.model import inforlogin

async def get_v1_payloads_list(session, filter=None,  sort=None, page=None, records=None, retries=3):
    """
    List data object properties using a filter.
    """
    url = inforlogin.base_url() + "/IONSERVICES/datalakeapi/v1/payloads/list"
    headers = inforlogin.header()
    payload = {}

    if filter is not None:
        payload["filter"] = filter

    if sort is not None:
        payload["sort"] = sort

    if page is not None:
        payload["page"] = page

    if records is not None:
        payload["records"] = records

    async with session.get(url, headers=headers, params=payload) as resp:
        if resp.status == 401 and retries > 0:
            inforlogin.check_and_reconnect()
            return await get_v1_payloads_list(session, filter, sort, page, records, retries - 1)
        return await resp.json()


async def get_v1_payloads_stream_by_id(dl_id, session, retries=3):
    """
    Retrieve payload based on id from datalake.
    """
    url = inforlogin.base_url() + "/IONSERVICES/datalakeapi/v1/payloads/streambyid"
    headers = inforlogin.header()
    payload = {"datalakeId": dl_id}
    async with session.get(url, headers=headers, params=payload) as resp:
        if resp.status == 401 and retries > 0:
            inforlogin.check_and_reconnect()
            return await get_v1_payloads_stream_by_id(dl_id, session, retries - 1)
        return await resp.text()


def delete_v1_purge_id(ids):
    """
    Deletes Data Objects based on the given Data Object identifiers.
    """
    url = inforlogin.base_url() + "/IONSERVICES/datalakeapi/v1/purge/ids"
    headers = inforlogin.header()
    payload = {"id": ids}
    res = requests.delete(url, headers=headers, params=payload)
    return res


def delete_v1_purge_filter(purge_filter):
    """
    Deletes Data Objects based on the given Filter.
    """
    url = inforlogin.base_url() + "/IONSERVICES/datalakeapi/v1/purge/filter"
    headers = inforlogin.header()
    payload = {"filter": purge_filter}
    res = requests.delete(url, headers=headers, params=payload)
    return res


async def get_v1_payloads_splitquery(filter, session, sort=None, retries=3):
    """
    Split a demanding filter (producing more than 10K results) into several smaller filters producing the same result (up to 9500 results per one filter).
    """
    url = inforlogin.base_url() + "/IONSERVICES/datalakeapi/v1/payloads/splitquery"
    headers = inforlogin.header()
    payload = {"filter": filter}

    if sort is not None:
        payload["sort"] = sort

    async with session.get(url, headers=headers, params=payload) as resp:
        if resp.status == 401 and retries > 0:
            inforlogin.check_and_reconnect()
            return await get_v1_payloads_splitquery(filter, session, sort, retries - 1)
        return await resp.json()

async def get_v2_payloads_splitquery(filter, session, sort=None, retries=3):
    """
    Split a demanding filter (producing more than 10K results) into several smaller filters producing the same result (up to 9500 results per one filter).
    """
    url = inforlogin.base_url() + "/IONSERVICES/datalakeapi/v2/payloads/splitquery"
    headers = inforlogin.header()
    payload = {"filter": filter}

    if sort is not None:
        payload["sort"] = sort

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=payload) as resp:
            if resp.status == 401 and retries > 0:
                print("Attempting to re auth")
                inforlogin.check_and_reconnect()
                return await get_v2_payloads_splitquery(filter, session, sort, retries - 1)
            return await resp.json()

