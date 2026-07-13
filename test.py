import mysql.connector

try:
    conn = mysql.connector.connect(
        host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
        port=4000,
        user="4D81iepo59Yk2PB.root",
        password="rF0II96dmPcS8eb3",
        database="ai_customer_support",
        ssl_ca="C:/Users/admin/Downloads/isrgrootx1.pem",  # apni .pem file ka path
        ssl_verify_cert=True
    )

    print("✅ Connected Successfully")

except Exception as e:
    print(e)