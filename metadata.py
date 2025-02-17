TABLE_COLUMN_MAP = {
    "customer": {
        "age": "customer_age",
        "name": "customer_name",
        "id": "customer_id",
        "email": "customer_email"
    },
    "policy": {
        "status": "policy_status",  # ✅ Corrected mapping
        "type": "policy_type",
        "id": "policy_id",
        "start date": "policy_start_date",
        "end date": "policy_end_date",
        "premium": "premium_amount"
    },
    "claims": {
        "id": "claim_id",
        "amount": "claim_amount",
        "status": "claim_status",  # ✅ Only for claims
        "date": "claim_date"
    },
    "payments": {
        "id": "payment_id",
        "amount": "payment_amount",
        "date": "payment_date"
    }
}