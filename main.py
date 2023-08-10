from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Password@123#@!",
    database="TriotdTech_task_DB"
)

triod_table = (
    "\n"
    "CREATE TABLE IF NOT EXISTS triod_table ("
    "id INT PRIMARY KEY AUTO_INCREMENT,"
    "ProductName VARCHAR(255),"
    "Price VARCHAR(255),"
    "OldPrice VARCHAR(255),"
    "Catagories VARCHAR(255),"
    "IsActive BOOL,"
    "Descriptions VARCHAR(255)"
    ");\n"
    "\n"
)

if conn.is_connected():
    cursor = conn.cursor()
    cursor.execute(triod_table)
    print("mysql is connected Succesfully")
else:
    print("not connected")


@app.route('/api/AddProducts', methods=['POST'])
def addProducts():
    try:
        productName = request.form["productName"]
        price = request.form.get("price")
        oldPrice = request.form.get("oldPrice")
        catagories = request.form.get("catagories")
        isActive_str = request.form.get('isActive')
        isActive = True if isActive_str.lower() == True else False
        descriptions = request.form.get("descriptions")

        cursor = conn.cursor()
        sql = ('INSERT INTO triod_table (ProductName, Price, OldPrice, Catagories, IsActive, Descriptions) '
               'VALUES (%s, %s, %s, %s, %s, %s)')
        val = (productName, price, oldPrice, catagories, isActive, descriptions)
        cursor.execute(sql, val)
        conn.commit()
        cursor.close()

        return jsonify({"message": "Product Added Successfully!"}), 200
    except Exception as e:
        return jsonify({"message": "Error occurred: " + str(e)}), 500
@app.route("/api/getAllProducts",methods=['GET'])
def get_all_products():
    try:
        sql ="select * from  triod_table"
        cursor.execute(sql,)
        result= cursor.fetchall()
        if not result:
            return jsonify({"message":"no products found"})
        else:
            response_list=[]
            for r in result:
                id=r[0]
                productName=r[1]
                price=r[2]
                oldPrice=r[3]
                catagories=r[4]
                isActive=r[5]
                description=r[6]
                response={
                    "id":id,
                    "productName":productName,
                    "price":price,
                    "oldPrice":oldPrice,
                    "catagories":catagories,
                    "isActive":isActive,
                    "description":description
                }
                response_list.append(response)
            return  jsonify(response_list)
    except Exception as e:
        return jsonify({"message": "Error occurred: " + str(e)}), 500
@app.route('/api/updateAllProducts',methods=['POST'])
def update_all_products():
    try:
        selectedId=request.args.get("id")
        productName=request.form.get("productName")
        price=request.form.get('price')
        oldPrice=request.form.get('oldPrice')
        catagories=request.form.get('catagories')
        isActive=request.form.get("isActive")
        description=request.form.get("description")

        cursor=conn.cursor()
        sql='update triod_table set ProductName=%s, Price=%s,OldPrice=%s,Catagories=%s,IsActive=%s,Descriptions=%s WHERE id=%s'
        val=(productName,price,oldPrice,catagories,isActive,description,selectedId)
        cursor.execute(sql,val)
        conn.commit()
        cursor.close()
        return jsonify({"message": "Product Updated Successfully!"}), 200
    except Exception as e:
        return jsonify({"message": "Error occurred: " + str(e)}), 500

@app.route('/api/deleteSelectedProducts',methods=['POST'])
def delete_selected_Products():
    try:
        selectedId=request.args.get('id')
        cursor = conn.cursor()
        sql='DELETE FROM triod_table WHERE id = %s'
        val=(selectedId,)
        cursor.execute(sql,val)
        conn.commit()
        cursor.close()

        return jsonify({"message": "Product Deleted Successfully!"}), 200
    except Exception as e:
        return jsonify({"message": "Error occurred: " + str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)