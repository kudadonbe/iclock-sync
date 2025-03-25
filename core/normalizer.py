from core.utils import generate_doc_id

def normalize_sdk_log(log):
    doc_id = generate_doc_id(log.user_id, log.timestamp)

    return {
        "doc_id": doc_id,
        "staffId": str(log.user_id),
        "timestamp": log.timestamp,
        "status": int(log.status),
        "workCode": int(log.punch)
    }
