# -*- coding: utf-8 -*-
import datetime
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.utils.cache import add_never_cache_headers



def _get_datatable_response(
    datarows, count, sEcho, format_type="sync", status=200, errors=None, **kwargs
):
    """
    Returns json response formatted data to datatables
    """
    data = _get_return_dict(datarows, count, sEcho, format_type, errors)
    if kwargs:
        data.update(kwargs)
    return_json = json.dumps(data, cls=DjangoJSONEncoder)
    response = HttpResponse(return_json, content_type="application/json", status=status)
    add_never_cache_headers(response)
    return response


def _get_return_dict(datarows, count, sEcho, format_type, errors):
    return {
        "sEcho": sEcho,
        "iTotalRecords": count,
        "iTotalDisplayRecords": count,
        "aaData": [_format_row(row, format_type) for row in datarows],
        "errors": errors,
    }


def _format_row(row, format_type="sync"):
    """
    Formats datatables columns
    """
    entity_id = row.get("entity_id", "")
    entity_key = row.get("entity_key")
    entity_name = row.get("entity_name")
    last_modified = row.get("last_modified")
    last_modifier = row.get("last_modifier")
    status = row.get("status")
    jira_list = row.get("jira_list", "")

    if format_type == "sync_history":
        sync_timestamp = row.get("sync_timestamp")
        entity_type = row.get("entity_type")
        return {
            "0": {"entity_id": entity_id, "value": entity_key},
            "1": entity_type,
            "2": {"entity_id": entity_id, "value": entity_name},
            "3": sync_timestamp,
            "4": last_modified,
            "5": jira_list,
            "DT_RowId": "row_" + entity_id,
        }
    elif format_type == "sync":
        entity_type_descr = row.get("type_description")
        return {
            "0": entity_id,
            "1": {"entity_id": entity_id, "value": entity_key},
            "2": entity_type_descr,
            "3": {"entity_id": entity_id, "value": entity_name},
            "4": last_modified,
            "5": last_modifier,
            "6": "<span id='status_{}'>{}</span>".format(entity_id, status),
            "7": {
                "entity_id": entity_id,
                "status": status,
            },
            "8": jira_list,
            "DT_RowId": "row_" + (entity_id or ""),
        }


def format_date(val):
    if not val:
        return ""
    if not isinstance(val, datetime.datetime):
        val = datetime.datetime.strptime(val, "%Y-%m-%d")
    if val.year < 1900:
        return "1900-01-01"
    return val.strftime("%Y-%m-%d")