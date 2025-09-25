"""
yang ubah nama creator semoga mandul 7 turunan.

pakai dengan bijak, jika ada eror silahkan hubungi t.me/rafanstr
"""


from flask import Flask, request
import requests
import time
import hashlib
from collections import OrderedDict
import json

app = Flask(__name__)

ORDERKUOTA_URL = "https://app.orderkuota.com/api/v2/qris/mutasi/{}"


@app.route("/mutasi", methods=["POST"])
def mutasi():
    username = request.json.get("username")
    token = request.json.get("token")   

    if not username or not token:
        response_data = OrderedDict([
            ("status", "failed"),
            ("message", "username dan token wajib diisi"),
            ("creator", "t.me/RafanSTR")
        ])
        return app.response_class(
            response=json.dumps(response_data, ensure_ascii=False, indent=4),
            status=400,
            mimetype="application/json; charset=utf-8"
        )

    try:
        merchant_id = token.split(":")[0]
    except Exception:
        response_data = OrderedDict([
            ("status", "failed"),
            ("message", "token tidak valid"),
            ("creator", "t.me/RafanSTR")
        ])
        return app.response_class(
            response=json.dumps(response_data, ensure_ascii=False, indent=4),
            status=400,
            mimetype="application/json; charset=utf-8"
        )

    url = ORDERKUOTA_URL.format(merchant_id)
    timestamp = str(int(time.time() * 1000))

    signature = hashlib.sha256((token + timestamp).encode()).hexdigest()

    headers = {
        "signature": signature,
        "timestamp": timestamp,
        "content-type": "application/x-www-form-urlencoded",
        "user-agent": "okhttp/4.12.0"
    }

    data = {
        "auth_username": username,
        "auth_token": token,
        "requests[qris_history][page]": 1,
        "requests[0]": "account"
    }

    try:
        resp = requests.post(url, headers=headers, data=data, timeout=15)
        res_json = resp.json()
    except Exception as e:
        response_data = OrderedDict([
            ("status", "failed"),
            ("message", f"gagal request: {str(e)}"),
            ("creator", "t.me/RafanSTR")
        ])
        return app.response_class(
            response=json.dumps(response_data, ensure_ascii=False, indent=4),
            status=500,
            mimetype="application/json; charset=utf-8"
        )

    if not res_json.get("success"):
        response_data = OrderedDict([
            ("status", "failed"),
            ("message", "gagal ambil data"),
            ("creator", "t.me/RafanSTR")
        ])
        return app.response_class(
            response=json.dumps(response_data, ensure_ascii=False, indent=4),
            status=400,
            mimetype="application/json; charset=utf-8"
        )

    hasil = []
    for trx in res_json.get("qris_history", {}).get("results", []):
        amount = 0
        if trx["status"] == "OUT":
            amount = int(trx["debet"].replace(".", "")) if trx.get("debet") else 0
        else:
            amount = int(trx["kredit"].replace(".", "")) if trx.get("kredit") else 0

        hasil.append({
            "date": trx["tanggal"].replace("/", "-") + ":00",
            "amount": amount,
            "type": "DB" if trx["status"] == "OUT" else "CR",
            "qris": trx["brand"]["name"],
            "brand_name": trx["brand"]["name"],
            "issuer_reff": "id" + str(trx["id"]),
            "buyer_reff": trx["keterangan"],
            "balance": int(trx["saldo_akhir"].replace(".", "")) if trx.get("saldo_akhir") else 0
        })

    response_data = OrderedDict([
        ("status", "success"),
        ("data", hasil),
        ("creator", "t.me/RafanSTR")
    ])

    return app.response_class(
        response=json.dumps(response_data, ensure_ascii=False, indent=4),  
        status=200,
        mimetype="application/json; charset=utf-8"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
