import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request


@app.route('/add', methods=['POST'])
def add_emp():
    try:
        _json = request.json
        _firstname = _json['firstname']
        _lastname = _json['lastname']
        _email = _json['email']
        _contactnumber = _json['contactnumber'],
        _address = _json['address']
        if _firstname and _lastname and _email and _contactnumber and _address and request.method == 'POST':
            sql = "INSERT INTO Contact(FirstName, LastName,EmailAddress,ContactNumber,Address,CreatedTS) VALUES(%s," \
                  "%s, %s, %s,%s,CURRENT_DATE()) "
            data = (_firstname, _lastname, _email, _contactnumber, _address)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('Contact added successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/contacts')
def emp():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT ContactID, FirstName,LastName, EmailAddress, ContactNumber, Address FROM Contact")
        contacts = cursor.fetchall()
        response = jsonify(contacts)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/contact/<int:id>')
def getbyid(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT ContactID,FirstName,LastName,EmailAddress,ContactNumber,Address FROM Contact WHERE "
                       "ContactID =%s", id)
        contact = cursor.fetchone()
        respone = jsonify(contact)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/update', methods=['PUT'])
def update_emp():
    try:
        _json = request.json
        _id = _json['id']
        _firstname = _json['firstname']
        _lastname = _json['lastname']
        _email = _json['email']
        _contactnumber = _json['contactnumber'],
        _address = _json['address']
        if _firstname and _lastname and _email and _contactnumber and _address and _id and request.method == 'PUT':
            sql = "UPDATE Contact SET FirstName=%s,LastName=%s, EmailAddress=%s, ContactNumber=%s, Address=%s , " \
                       "ModifiedTS=CURRENT_DATE() WHERE ContactID=%s "
            data = (_firstname, _lastname, _email, _contactnumber, _address, _id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            respone = jsonify('Contact updated successfully!')
            respone.status_code = 200
            return respone
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_contact(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Contact WHERE ContactID =%s", (id,))
        conn.commit()
        respone = jsonify('Contact deleted successfully!')
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone


if __name__ == "__main__":
    app.run(debug=True)

