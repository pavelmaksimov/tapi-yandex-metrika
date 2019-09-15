# coding: utf-8

STATS_RESOURCE_MAPPING = {
    "stats": {
        "resource": "stat/v1/data",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/api_v1/intro-docpage/",
        "params": [
            "direct_client_logins=<string,_string,...>",
            "ids=<int,int,...>",
            "metrics=<string>",
            "accuracy=<string>",
            "callback=<string>",
            "date1=<string>",
            "date2=<string>",
            "dimensions=<string>",
            "filters=<string>",
            "include_undefined=<boolean>",
            "lang=<string>",
            "limit=<integer>",
            "offset=<integer>",
            "preset=<string>",
            "pretty=<boolean>",
            "proposed_accuracy=<boolean>",
            "sort=<string>",
            "timezone=<string>",
        ]
    },
}

LOGSAPI_RESOURCE_MAPPING = {
    "allinfo": {
        "resource": "management/v1/counter/{counterId}/logrequests",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/logs/queries/getlogrequests-docpage/",
        "params": None
    },
    "info": {
        "resource": "management/v1/counter/{counterId}/logrequest/{requestId}",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/logs/queries/getlogrequest-docpage/",
        "params": None
    },
    "download": {
        "resource": "management/v1/counter/{counterId}/logrequest/{requestId}/part/{partNumber}/download",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/logs/queries/download-docpage/",
        "params": None
    },
    "clean": {
        "resource": "management/v1/counter/{counterId}/logrequest/{requestId}/clean",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/logs/queries/clean-docpage/",
        "params": None
    },
    "cancel": {
        "resource": "management/v1/counter/{counterId}/logrequest/{requestId}/cancel",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/logs/queries/cancel-docpage/",
        "params": None
    },
    "create": {
        "resource": "management/v1/counter/{counterId}/logrequests",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/logs/queries/createlogrequest-docpage/",
        "params": ["date1", "date2", "fields", "source"],
    },
    "evaluate": {
        "resource": "management/v1/counter/{counterId}/logrequests/evaluate",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/logs/queries/evaluate-docpage/",
        "params": ["date1", "date2", "fields", "source"],
    },
}

MANAGEMENT_RESOURCE_MAPPING = {
    "counters": {
        "resource": "management/v1/counters",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/management/counters/counters-docpage/",
        "params": """[callback=<string>]
 & [favorite=<boolean>]
 & [field=<string>]
 & [label_id=<integer>]
 & [offset=<int>]
 & [per_page=<int>]
 & [permission=<string>]
 & [reverse=<boolean>]
 & [search_string=<string>]
 & [sort=<counters_sort>]
 & [status=<counter_status>]
 & [type=<counter_type>]""",
        "methods": ["GET", "POST"]
    },
    "counter": {
        "resource": "management/v1/counter/{counterId}",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/management/counters/counter-docpage/",
        "params": """[callback=<string>] & [field=<string>]""",
        "methods": ["GET", "DELETE", "PUT"],
    },
    "counter_undelete": {
        "resource": "management/v1/counter/{counterId}/undelete",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/management/counters/undeletecounter-docpage/",
        "params": """""",
        "methods": ["POST"]
    },
    "goals": {
        "resource": "management/v1/counter/{counterId}/goals",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/management/goals/goals-docpage/",
        "params": """[callback=<string>] & [useDeleted=<boolean>]""",
        "methods": ["GET", "POST"]
    },
    "goal": {
        "resource": "management/v1/counter/{counterId}/goal/{goalId}",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/management/goals/goal-docpage/",
        "params": """[callback=<string>]""",
        "methods": ["GET", "DELETE", "PUT"]
    },
    "accounts": {
        "resource": "management/v1/accounts",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/management/accounts/accounts-docpage/",
        "params": """[callback=<string>] & [user_login=<string>]""",
        "methods": ["GET", "DELETE", "PUT"]
    },
    "clients": {
        "resource": "management/v1/clients",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/management/direct_clients/getclients-docpage/",
        "params": """counters=<list>""",
        "methods": ["GET", ]
    },
    "filters": {
        "resource": "management/v1/counter/{counterId}/filters",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/management/filters/filters-docpage/",
        "params": """[callback=<string>]""",
        "methods": ["GET", "POST"]
    },
    "filter": {
        "resource": "management/v1/counter/{counterId}/filter/{filterId}",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/management/filters/filter-docpage/",
        "params": """[callback=<string>]""",
        "methods": ["GET", "DELETE", "PUT"]
    },
    "operations": {
        "resource": "management/v1/counter/{counterId}/operations",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/management/operations/operations-docpage/",
        "params": """[callback=<string>]""",
        "methods": ["GET", "POST"]
    },
    "operation": {
        "resource": "management/v1/counter/{counterId}/operation/{operationId}",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/management/operations/operation-docpage/",
        "params": """[callback=<string>]""",
        "methods": ["GET", "DELETE", "PUT"]
    },
    "grants": {
        "resource": "management/v1/counter/{counterId}/grants",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/management/grants/grants-docpage/",
        "params": """[callback=<string>]""",
        "methods": ["GET", "POST"]
    },
    "grant": {
        "resource": "management/v1/counter/{counterId}/grant",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/management/grants/grant-docpage/",
        "params": """user_login=<string>""",
        "methods": ["GET", "PUT", "DELETE"]
    },
    "public_grant": {
        "resource": "management/v1/counter/{counterId}/public_grant",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/management/public-grants/addgrant-docpage/",
        "params": """""",
        "methods": ["POST", "DELETE"]
    },
    "delegates": {
        "resource": "management/v1/delegates",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/management/delegates/delegates-docpage/",
        "params": """[callback=<string>]""",
        "methods": ["GET", "POST"]
    },
    "delegate": {
        "resource": "management/v1/delegate",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/management/delegates/deletedelegate-docpage/",
        "params": """user_login=<string>""",
        "methods": ["DELETE"]
    },
    "labels": {
        "resource": "management/v1/labels",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/management/labels/getlabels-docpage/",
        "params": None,
        "methods": ["GET", "POST"]
    },
    "label": {
        "resource": "management/v1/label/{labelId}",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/management/labels/getlabel-docpage/",
        "params": None,
        "methods": ["GET", "DELETE", "PUT"]
    },
    "set_counter_label": {
        "resource": "management/v1/counter/{counterId}/label/{labelId}",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/management/links/setcounterlabel-docpage/",
        "params": None,
        "methods": ["POST", "DELETE"]
    },
    "segments": {
        "resource": "management/v1/counter/{counterId}/apisegment/segments",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/management/segments/getsegmentsforcounter-docpage/",
        "params": None,
        "methods": ["GET", "POST"]
    },
    "segment": {
        "resource": "management/v1/counter/{counterId}/apisegment/segment/{segmentId}",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/management/segments/getsegment-docpage/",
        "params": None,
        "methods": ["GET", "DELETE", "PUT"]
    },
    "user_params_uploadings": {
        "resource": "management/v1/counter/{counterId}/user_params/uploadings",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/management/userparams/findall-docpage/",
        "params": None,
        "methods": ["GET"]
    },
    "user_params_uploading": {
        "resource": "management/v1/counter/{counterId}/user_params/uploading/{uploadingId}",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/management/userparams/findbyid-docpage/",
        "params": None,
        "methods": ["GET", "PUT"]
    },
    "user_params_upload": {
        "resource": "management/v1/counter/{counterId}/user_params/uploadings/upload",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/management/userparams/upload-docpage/",
        "params": """action=<user_params_uploading_action>""",
        "methods": ["POST"]
    },
    "user_params_uploading_confirm": {
        "resource": "management/v1/counter/{counterId}/user_params/uploading/{uploadingId}/confirm",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/management/userparams/confirm-docpage/",
        "params": None,
        "methods": ["POST"]
    },
    "chart_annotations": {
        "resource": "management/v1/counter/{counterId}/chart_annotations",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/management/chart_annotation/findall-docpage/",
        "params": None,
        "methods": ["GET", "POST"]
    },
    "chart_annotation": {
        "resource": "management/v1/counter/{counterId}/chart_annotation/{id}",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/management/chart_annotation/get-docpage/",
        "params": None,
        "methods": ["GET", "DELETE", "PUT"]
    },
    "yclid_conversions_uploadings": {
        "resource": "management/v1/counter/{counterId}/yclid_conversions/uploadings",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/management/yclid-conversion/findall-docpage/",
        "params": """[limit=<integer>] & [offset=<integer>""",
        "methods": ["GET"]
    },
    "yclid_conversions_uploading": {
        "resource": "management/v1/counter/{counterId}/yclid_conversions/uploading/{id}",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/management/yclid-conversion/findbyid-docpage/",
        "params": None,
        "methods": ["GET"]
    },
    "yclid_conversions_upload": {
        "resource": "management/v1/counter/{counterId}/yclid_conversions/upload",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/management/yclid-conversion/upload-docpage/",
        "params": """[comment=<string>]""",
        "methods": ["GET"]
    },
    "offline_conversions_uploadings": {
        "resource": "management/v1/counter/{counterId}/offline_conversions/uploadings",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/management/offline_conversion/findall-docpage/",
        "params": None,
        "methods": ["GET"]
    },
    "offline_conversions_calls_uploadings": {
        "resource": "management/v1/counter/{counterId}/offline_conversions/calls_uploadings",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/management/offline_conversion/findallcalluploadings-docpage/",
        "params": None,
        "methods": ["GET"]
    },
    "offline_conversions_uploading": {
        "resource": "management/v1/counter/{counterId}/offline_conversions/uploading/{id}",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/management/offline_conversion/findbyid-docpage/",
        "params": None,
        "methods": ["GET"]
    },
    "offline_conversions_calls_uploading": {
        "resource": "management/v1/counter/{counterId}/offline_conversions/calls_uploading/{id}",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/management/offline_conversion/findcalluploadingbyid-docpage/",
        "params": None,
        "methods": ["GET"]
    },
    "offline_conversions_upload": {
        "resource": "management/v1/counter/{counterId}/offline_conversions/upload",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/management/offline_conversion/upload-docpage/",
        "params": """client_id_type=<offline_conversion_uploading_client_id_type> & [comment=<string>]""",
        "methods": ["POST"]
    },
    "offline_conversions_upload_calls": {
        "resource": "management/v1/counter/{counterId}/offline_conversions/upload_calls",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/management/offline_conversion/uploadcalls-docpage/",
        "params": """client_id_type=<offline_conversion_uploading_client_id_type>
 & [comment=<string>]
 & [new_goal_name=<string>]""",
        "methods": ["POST"]
    },
    "offline_conversions_extended_threshold": {
        "resource": "management/v1/counter/{counterId}/offline_conversions/extended_threshold",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/management/offline_conversion/enableextendedthreshold-docpage/",
        "params": None,
        "methods": ["POST", "DELETE"]
    },
    "offline_conversions_calls_extended_threshold": {
        "resource": "management/v1/counter/{counterId}/offline_conversions/calls_extended_threshold",
        "docs": "https://yandex.ru/dev/metrika/doc/api2/management/offline_conversion/enablecallsextendedthreshold-docpage/",
        "params": None,
        "methods": ["POST", "DELETE"]
    },
}
