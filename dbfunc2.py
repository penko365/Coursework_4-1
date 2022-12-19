import psycopg2

def connectToDB(authDict):
  try:
    connection = psycopg2.connect(dbname=authDict['dbname'],
                                  user=authDict['user'],
                                  password=authDict['password'],
                                  host=authDict['host'],
                                  port=authDict['port'])
    connection.autocommit = True
    return connection
  except:
    # connection.close()
    return -1

def check_atc_chemical_substance(authDict, atc_code):
  # if type(atc_code) != str or len(atc_code) != 7:
  #   return 77
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()

  toex = "SELECT id FROM atc_chemical_substance WHERE atc_code='{}';".format(atc_code.upper())
  cursor.execute(toex)
  res = cursor.fetchall()
  if res != []:
    conn.close()
    return 1
  else:
    conn.close()
    return 0

def check_atc_chemical_subgr(authDict, atc_code):
  if type(atc_code) != str or len(atc_code) != 5:
    return 75
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()

  toex = "SELECT id FROM atc_chemical_subgr WHERE atc_code='{}';".format(atc_code.upper())
  cursor.execute(toex)
  res = cursor.fetchall()
  if res != []:
    conn.close()
    return 1
  else:
    conn.close()
    return 0

def check_atc_pharmacological_subgr(authDict, atc_code):
  if type(atc_code) != str or len(atc_code) != 4:
    return 74
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()

  toex = "SELECT id FROM atc_pharmacological_subgr WHERE atc_code='{}';".format(atc_code.upper())
  cursor.execute(toex)
  res = cursor.fetchall()
  if res != []:
    conn.close()
    return 1
  else:
    conn.close()
    return 0

def check_atc_therapeutic_subgr(authDict, atc_code):
  if type(atc_code) != str or len(atc_code) != 3:
    return 73
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()

  toex = "SELECT id FROM atc_therapeutic_subgr WHERE atc_code='{}';".format(atc_code.upper())
  cursor.execute(toex)
  res = cursor.fetchall()
  if res != []:
    conn.close()
    return 1
  else:
    conn.close()
    return 0

def check_atc_anatomical_gr(authDict, atc_code):
  if type(atc_code) != str or len(atc_code) != 1:
    return 71
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()

  toex = "SELECT id FROM atc_anatomical_gr WHERE atc_code='{}';".format(atc_code.upper())
  cursor.execute(toex)
  res = cursor.fetchall()
  if res != []:
    conn.close()
    return 1
  else:
    conn.close()
    return 0

def check_drugs(authDict, drug_name=None, drug_atc=None, manufacturer_id=None, supplier_id=None, drug_id=None):
  # if type(name) != str or len(name) > 200:
  #   return 401
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()
  i_list = []
  toex = []
  i_string = ""
  if drug_id and drug_id!='':
    i_list.append("drugs.id={}".format(drug_id))
    toex = ["SELECT * from drugs ",
            "WHERE id={};".format(drug_id)]

  else:
    if drug_name and drug_name!='':
      i_list.append("drugs.name='{}' ".format(drug_name.upper()))
    if drug_atc and drug_atc!='':
      i_list.append("atc_chemical_substance.atc_code='{}' ".format(drug_atc.upper()))
    if manufacturer_id and manufacturer_id != '':
      i_list.append("drug_manufacturer.manufacturer_id={} ".format(str(manufacturer_id)))
    if supplier_id and supplier_id != '':
      i_list.append("drug_supplier.supplier_id={} ".format(str(supplier_id)))

    if i_list != []:
      i_string = " WHERE " + "AND ".join(i_list)
      toex = ["SELECT drugs.id, atc_chemical_substance.atc_code, drug_manufacturer.manufacturer_id, drug_supplier.supplier_id ",
                "FROM ((drugs INNER JOIN atc_chemical_substance ",
                  "ON drugs.atc_chemical_substance_id=atc_chemical_substance.id) ",
                "INNER JOIN drug_manufacturer ",
                  "ON drugs.id=drug_manufacturer.drug_id) ",
                "INNER JOIN drug_supplier ",
                  "ON drugs.id=drug_supplier.drug_id"
                "{};".format(i_string)]
  toex = "".join(toex)
  # print(toex)
  cursor.execute(toex)
  res = cursor.fetchall()
  # print("\n")
  # print(res)
  if res != []:
    conn.close()
    return 1
  else:
    conn.close()
    return 0

def check_medic_ranks(authDict, name):
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()
  toex = "SELECT id FROM medic_ranks WHERE name='{}';".format(name.upper())
  cursor.execute(toex)
  res = cursor.fetchall()
  if res != []:
    conn.close()
    return 1
  else:
    conn.close()
    return 0

def check_suppliers(authDict, name, country):
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()
  toex = "SELECT id FROM suppliers WHERE name='{}' AND country='{}';".format(name.upper(), country.upper())
  cursor.execute(toex)
  res = cursor.fetchall()
  if res != []:
    conn.close()
    return 1
  else:
    conn.close()
    return 0

def check_manufacturers(authDict, name, country):
  if type(name) != str or len(name) > 200:
    return 701
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()
  toex = "SELECT id FROM manufacturers WHERE name='{}' AND country='{}';".format(name.upper(), country.upper())
  cursor.execute(toex)
  res = cursor.fetchall()
  if res != []:
    conn.close()
    return 1
  else:
    conn.close()
    return 0

def check_drugs_prohibited(authDict, drug_id=None, medic_rank_id=None, prohibition_id=None):
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()
  i_list = []
  if prohibition_id and prohibition_id!='':
    i_list.append("id={}".format(prohibition_id))
  else:
    if drug_id and drug_id!='':
      i_list.append("drug_id={} ".format(drug_id))
    if medic_rank_id and medic_rank_id!='':
      i_list.append("medic_rank_id={} ".format(medic_rank_id))
  if i_list != []:
    i_string = " WHERE " + "AND ".join(i_list)
  toex = ["SELECT * FROM drugs_prohibited",
          "{};".format(i_string)]
  toex = "".join(toex)
  cursor.execute(toex)
  res = cursor.fetchall()
  if res != []:
    conn.close()
    return 1
  else:
    conn.close()
    return 0

# def doTests1():
#   inpt = 'A08AA11'
#   out = check_atc_chemical_substance(authDict, inpt)
#   print(out)

#   inpt = 'A08AA'
#   out = check_atc_chemical_subgr(authDict, inpt)
#   print(out)

#   inpt = 'A08A'
#   out = check_atc_pharmacological_subgr(authDict, inpt)
#   print(out)

#   inpt = 'A08'
#   out = check_atc_therapeutic_subgr(authDict, inpt)
#   print(out)

#   inpt = 'A'
#   out = check_atc_anatomical_gr(authDict, inpt)
#   print(out)

def insert_atc_chemical_substance(authDict, atc_code, name):
  if type(atc_code) != str or type(name) != str or len(atc_code) != 7:
    return 77
  lvl1Code = atc_code[0]
  lvl2Code = atc_code[0:3]
  lvl3Code = atc_code[0:4]
  lvl4Code = atc_code[0:5]
  if check_atc_anatomical_gr(authDict, lvl1Code) == 0:
    return -101
  if check_atc_therapeutic_subgr(authDict, lvl2Code) == 0:
    return -102
  if check_atc_pharmacological_subgr(authDict, lvl3Code) == 0:
    return -103
  if check_atc_chemical_subgr(authDict, lvl4Code) == 0:
    return -104
  if check_atc_chemical_substance(authDict, atc_code) == 1:
    return 105
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()
  toex = ["INSERT INTO atc_chemical_substance (atc_code, name, atc_chemical_subgr_id) ",
          "values ('{}', '{}', (SELECT id FROM atc_chemical_subgr ".format(atc_code.upper(), name.lower()),
                                "WHERE atc_code='{}'".format(lvl4Code.upper()),
                                ")",
                  ");"]
  toex = "".join(toex)
  try:
    cursor.execute(toex)
  except Exception as error:
    print(error)
    conn.close()
    return 0
  conn.close()
  return 1

def insert_atc_chemical_subgr(authDict, atc_code, name):
  if type(atc_code) != str or type(name) != str or len(atc_code) != 5:
    return 75
  lvl1Code = atc_code[0]
  lvl2Code = atc_code[0:3]
  lvl3Code = atc_code[0:4]
  lvl4Code = atc_code[0:5]
  if check_atc_anatomical_gr(authDict, lvl1Code) == 0:
    return -101
  if check_atc_therapeutic_subgr(authDict, lvl2Code) == 0:
    return -102
  if check_atc_pharmacological_subgr(authDict, lvl3Code) == 0:
    return -103
  if check_atc_chemical_subgr(authDict, lvl4Code) == 1:
    return 104
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()
  toex = ["INSERT INTO atc_chemical_subgr (atc_code, name, atc_pharmacological_subgr_id) ",
          "values ('{}', '{}', (SELECT id FROM atc_pharmacological_subgr ".format(atc_code.upper(), name.lower()),
                                "WHERE atc_code='{}'".format(lvl3Code.upper()),
                                ")",
                  ");"]
  toex = "".join(toex)
  try:
    cursor.execute(toex)
  except Exception as error:
    print(error)
    conn.close()
    return 0
  conn.close()
  return 1

def insert_atc_pharmacological_subgr(authDict, atc_code, name):
  if type(atc_code) != str or type(name) != str or len(atc_code) != 4:
    return 74
  lvl1Code = atc_code[0]
  lvl2Code = atc_code[0:3]
  lvl3Code = atc_code[0:4]
  if check_atc_anatomical_gr(authDict, lvl1Code) == 0:
    return -101
  if check_atc_therapeutic_subgr(authDict, lvl2Code) == 0:
    return -102
  if check_atc_pharmacological_subgr(authDict, lvl3Code) == 1:
    return 103
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()
  toex = ["INSERT INTO atc_pharmacological_subgr (atc_code, name, atc_therapeutic_subgr_id) ",
          "values ('{}', '{}', (SELECT id FROM atc_therapeutic_subgr ".format(atc_code.upper(), name.lower()),
                                "WHERE atc_code='{}'".format(lvl2Code.upper()),
                                ")",
                  ");"]
  toex = "".join(toex)
  try:
    cursor.execute(toex)
  except Exception as error:
    print(error)
    conn.close()
    return 0
  conn.close()
  return 1

def insert_atc_therapeutic_subgr(authDict, atc_code, name):
  if type(atc_code) != str or type(name) != str or len(atc_code) != 3:
    return 73
  lvl1Code = atc_code[0]
  lvl2Code = atc_code[0:3]
  if check_atc_anatomical_gr(authDict, lvl1Code) == 0:
    return -101
  if check_atc_therapeutic_subgr(authDict, lvl2Code) == 1:
    return 102
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()
  toex = ["INSERT INTO atc_therapeutic_subgr (atc_code, name, atc_anatomical_gr_id) ",
          "values ('{}', '{}', (SELECT id FROM atc_anatomical_gr ".format(atc_code.upper(), name.upper()),
                                "WHERE atc_code='{}'".format(lvl1Code.upper()),
                                ")",
                  ");"]
  toex = "".join(toex)
  try:
    cursor.execute(toex)
  except Exception as error:
    print(error)
    conn.close()
    return 0
  conn.close()
  return 1

def insert_atc_anatomical_gr(authDict, atc_code, name):
  if type(atc_code) != str or type(name) != str or len(atc_code) != 1:
    return 71
  lvl1Code = atc_code[0]
  if check_atc_anatomical_gr(authDict, lvl1Code) == 1:
    return 101
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()
  toex = ["INSERT INTO atc_anatomical_gr (atc_code, name) ",
          "values ('{}', '{}');".format(atc_code.upper(), name.upper())
          ]
  toex = "".join(toex)
  try:
    cursor.execute(toex)
  except Exception as error:
    print(error)
    conn.close()
    return 0
  conn.close()
  return 1

def insert_drugs(authDict, name, atc_code, quantity, description):
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()
  toex = ["INSERT INTO drugs (name, quantity, description, atc_chemical_substance_id) ",
          "values ('{}', {}, '{}', (SELECT id FROM atc_chemical_substance ".format(name.upper(), quantity, description),
                                "WHERE atc_code='{}'".format(atc_code.upper()),
                                ")",
                  ");"]
  toex = "".join(toex)
  try:
    cursor.execute(toex)
    conn.close()
    return 1
  except Exception as error:
    print(error)
    conn.close()
    return 0

def insert_medic_ranks(authDict, name):
  # if type(name) != str or len(name) > 200:
  #   return 501
  # if check_madic_ranks(authDict, name) == 1:
  #   return 510
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()
  toex = ["INSERT INTO medic_ranks (name) ",
          "values ('{}');".format(name.upper())
          ]
  toex = "".join(toex)
  try:
    cursor.execute(toex)
  except Exception as error:
    print(error)
    conn.close()
    return 0
  conn.close()
  return 1

def insert_suppliers(authDict, name, country, contact_info):
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()
  toex = ["INSERT INTO suppliers (name, country, contact_info) ",
          "values ('{}', '{}', '{}');".format(name.upper(), country.upper(), contact_info.upper())]
  toex = "".join(toex)
  try:
    cursor.execute(toex)
  except Exception as error:
    print(error)
    conn.close()
    return 0
  conn.close()
  return 1

def insert_manufacturers(authDict, name, country, contact_info):
  # if type(name) != str or len(name) > 200:
  #   return 701
  # if type(country) != str or len(country) > 50:
  #   return 702
  # if type(contact_info) != str or len(contact_info) > 200:
  #   return 703
  # if check_manufacturers(authDict, name,) == 1:
  #   return 710
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()
  toex = ["INSERT INTO manufacturers (name, country, contact_info) ",
          "values ('{}', '{}', '{}');".format(name.upper(), country.upper(), contact_info.upper())]
  toex = "".join(toex)
  try:
    cursor.execute(toex)
  except Exception as error:
    print(error)
    conn.close()
    return 0
  conn.close()
  return 1

def insert_drug_manufacturer(authDict, drug_id, manufacturer_id):
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()
  toex = ["INSERT INTO drug_manufacturer (drug_id, manufacturer_id) ",
          "values ('{}', '{}');".format(str(drug_id), str(manufacturer_id))]
  toex = "".join(toex)
  try:
    cursor.execute(toex)
  except Exception as error:
    print(error)
    conn.close()
    return 0
  conn.close()
  return 1

def insert_issued_to_medic(authDict, drug_id, medic_rank_id, quantity, timestamp, medic_fname, medic_lname, medic_pname):
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()
  toex = ["INSERT INTO issued_to_medic (drug_id, medic_rank_id, quantity, date, medic_fname, medic_lname, medic_pname) ",
          "values ('{}', ".format(str(drug_id)),
                  "'{}', ".format(str(medic_rank_id)),
                  "'{}', ".format(str(quantity)),
                  "'{}', ".format(str(timestamp)),
                  "'{}', ".format(str(medic_fname)),
                  "'{}', ".format(str(medic_lname)),
                  "'{}');".format(str(medic_pname))]
  toex = "".join(toex)
  try:
    cursor.execute(toex)
  except Exception as error:
    print(error)
    conn.close()
    return 0
  conn.close()
  return 1

def insert_drug_supplier(authDict, drug_id, supplier_id):
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()
  toex = ["INSERT INTO drug_supplier (drug_id, supplier_id) ",
          "values ('{}', '{}');".format(str(drug_id), str(supplier_id))]
  toex = "".join(toex)
  try:
    cursor.execute(toex)
  except Exception as error:
    print(error)
    conn.close()
    return 0
  conn.close()
  return 1

def insert_drugs_prohibited(authDict, drug_id, medic_rank_id):
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()
  toex = ["INSERT INTO drugs_prohibited (drug_id, medic_rank_id) ",
          "values ('{}', {});".format(str(drug_id), str(medic_rank_id))]
  toex = "".join(toex)
  try:
    cursor.execute(toex)
  except Exception as error:
    print(error)
    conn.close()
    return 0
  conn.close()
  return 1

# def doTests2():
#   out = insert_atc_anatomical_gr(authDict, 'Z', 'TEST ANATOMICAL GR')
#   # print(out)
#   out = insert_atc_therapeutic_subgr(authDict, 'Z00', 'TEST THERAPEUTIC SUBGR')
#   # print(out)
#   out = insert_atc_pharmacological_subgr(authDict, 'Z00Z', 'TEST PHARM SUBGR')
#   # print(out)
#   out = insert_atc_chemical_subgr(authDict, 'Z00ZZ', 'TEST CHEM SUBGR')
#   # print(out)
#   out = insert_atc_chemical_substance(authDict, 'Z00ZZ00', 'TEST CHEM SUBSTANCE')
#   # print(out)
  
def delete_atc_chemical_substance(authDict, atc_code):
  if type(atc_code) != str or len(atc_code) != 7:
    return 77
  if check_atc_chemical_substance(authDict, atc_code) == 0:
    return -107
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()
  toex = ["DELETE FROM atc_chemical_substance ",
          "WHERE atc_code='{}';".format(atc_code.upper())]
  toex = "".join(toex)
  try:
    cursor.execute(toex)
  except Exception as error:
    print(error)
    conn.close()
    return 0
  conn.close()
  return 1

def delete_atc_chemical_subgr(authDict, atc_code):
  if type(atc_code) != str or len(atc_code) != 5:
    return 75
  if check_atc_chemical_subgr(authDict, atc_code) == 0:
    return -105
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()
  toex = ["SELECT * FROM atc_chemical_substance ",
          "WHERE atc_chemical_subgr_id=(",
            "SELECT id FROM atc_chemical_subgr ",
              "WHERE atc_code='{}'".format(atc_code.upper()),
          ");"]
  toex = "".join(toex)
  cursor.execute(toex)
  res = cursor.fetchone()
  if res != None:
    conn.close()
    return 207
  toex = ["DELETE FROM atc_chemical_subgr ",
          "WHERE atc_code='{}';".format(atc_code.upper())]
  toex = "".join(toex)
  try:
    cursor.execute(toex)
  except Exception as error:
    print(error)
    conn.close()
    return 0
  conn.close()
  return 1

def delete_atc_pharmacological_subgr(authDict, atc_code):
  if type(atc_code) != str or len(atc_code) != 4:
    return 74
  if check_atc_pharmacological_subgr(authDict, atc_code) == 0:
    return -104
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()
  toex = ["SELECT * FROM atc_chemical_subgr ",
          "WHERE atc_pharmacological_subgr_id=(",
            "SELECT id FROM atc_pharmacological_subgr ",
              "WHERE atc_code='{}'".format(atc_code.upper()),
          ");"]
  toex = "".join(toex)
  cursor.execute(toex)
  res = cursor.fetchone()
  if res != None:
    conn.close()
    return 205
  toex = ["DELETE FROM atc_pharmacological_subgr ",
          "WHERE atc_code='{}';".format(atc_code.upper())]
  toex = "".join(toex)
  try:
    cursor.execute(toex)
  except Exception as error:
    print(error)
    conn.close()
    return 0
  conn.close()
  return 1

def delete_atc_therapeutic_subgr(authDict, atc_code):
  if type(atc_code) != str or len(atc_code) != 3:
    return 73
  if check_atc_therapeutic_subgr(authDict, atc_code) == 0:
    return -103
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()
  toex = ["SELECT * FROM atc_pharmacological_subgr ",
          "WHERE atc_therapeutic_subgr_id=(",
            "SELECT id FROM atc_therapeutic_subgr ",
              "WHERE atc_code='{}'".format(atc_code.upper()),
          ");"]
  toex = "".join(toex)
  cursor.execute(toex)
  res = cursor.fetchone()
  if res != None:
    conn.close()
    return 204
  toex = ["DELETE FROM atc_therapeutic_subgr ",
          "WHERE atc_code='{}';".format(atc_code.upper())]
  toex = "".join(toex)
  try:
    cursor.execute(toex)
  except Exception as error:
    print(error)
    conn.close()
    return 0
  conn.close()
  return 1

def delete_atc_anatomical_gr(authDict, atc_code):
  if type(atc_code) != str or len(atc_code) != 1:
    return 71
  if check_atc_anatomical_gr(authDict, atc_code) == 0:
    return -101
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()
  toex = ["SELECT * FROM atc_therapeutic_subgr ",
          "WHERE atc_anatomical_gr_id=(",
            "SELECT id FROM atc_anatomical_gr ",
              "WHERE atc_code='{}'".format(atc_code.upper()),
          ");"]
  toex = "".join(toex)
  cursor.execute(toex)
  res = cursor.fetchone()
  if res != None:
    conn.close()
    return 203
  toex = ["DELETE FROM atc_anatomical_gr ",
          "WHERE atc_code='{}';".format(atc_code.upper())]
  toex = "".join(toex)
  try:
    cursor.execute(toex)
  except Exception as error:
    print(error)
    conn.close()
    return 0
  conn.close()
  return 1

def delete_drugs(authDict, name):
  if type(name) != str or len(name) > 200:
    return 401
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()
  toex = "DELETE FROM drugs WHERE name='{}';".format(name.upper())
  try:
    cursor.execute(toex)
  except Exception as error:
    print(error)
    conn.close()
    return 0
  conn.close()
  return 1

def delete_drugs_prohibited(authDict, prohibition_id):
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()
  toex = "DELETE FROM drugs_prohibited WHERE id={};".format(prohibition_id)
  try:
    cursor.execute(toex)
  except Exception as error:
    print(error)
    conn.close()
    return 0
  conn.close()
  return 1

# def doTests3():
#   out = insert_atc_anatomical_gr(authDict, 'Z', 'TEST ANATOMICAL SUBGR')
#   print(out)
#   input('PRESS ENTER')
#   out = delete_atc_anatomical_gr(authDict, 'Z')
#   print(out)

def get_all_drugs(authDict):
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()
  toex = ["SELECT drugs.id, drugs.name, atc_chemical_substance.atc_code, quantity ",
          "FROM drugs INNER JOIN atc_chemical_substance ",
          "ON drugs.atc_chemical_substance_id=atc_chemical_substance.id;"]
  toex = "".join(toex)
  cursor.execute(toex)
  res = cursor.fetchall()
  if res != None:
    conn.close()
    return res
  else:
    conn.close()
    return 0

def get_all_manufacturers(authDict):
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()
  toex = "SELECT * FROM manufacturers;"
  cursor.execute(toex)
  res = cursor.fetchall()
  if res != None:
    conn.close()
    return res
  else:
    conn.close()
    return 0

def get_all_suppliers(authDict):
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()
  toex = "SELECT * FROM suppliers;"
  cursor.execute(toex)
  res = cursor.fetchall()
  if res != None:
    conn.close()
    return res
  else:
    conn.close()
    return 0

def get_all_medic_ranks(authDict):
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()
  toex = "SELECT * FROM medic_ranks;"
  cursor.execute(toex)
  res = cursor.fetchall()
  if res != None:
    conn.close()
    return res
  else:
    conn.close()
    return 0

def get_drug(authDict, name=None, atc=None, drug_id=None, descr=None):
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()
  i_list = []
  if drug_id and drug_id != '':
    i_list.append("drugs.id={} ".format(str(drug_id)))
  if name and name != '':
    i_list.append("drugs.name='{}' ".format(name.upper()))
  if atc and atc !='':
    i_list.append("atc_chemical_substance.atc_code='{}' ".format(atc.upper()))
  if descr and descr != '':
    i_list.append("drugs.description='{}' ".format(descr))
  i_string = "AND ".join(i_list)
  toex = ["SELECT drugs.id, drugs.name, atc_chemical_substance.atc_code, drugs.quantity, drugs.description ",
            "FROM drugs INNER JOIN atc_chemical_substance ",
            "ON drugs.atc_chemical_substance_id=atc_chemical_substance.id ",
            "WHERE {};".format(i_string)]
  toex = "".join(toex)
  cursor.execute(toex)
  res = cursor.fetchall()
  if res != []:
    conn.close()
    return res
  else:
    conn.close()
    return 0

def get_manufacturer(authDict, manufacturer_id):
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()
  toex = ["SELECT * ",
          "FROM manufacturers ",
          "WHERE id={};".format(manufacturer_id)]
  toex = "".join(toex)
  cursor.execute(toex)
  res = cursor.fetchall()
  if res != []:
    conn.close()
    return res
  else:
    conn.close()
    return 0

def get_supplier(authDict, supplier_id):
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()
  toex = ["SELECT * ",
          "FROM suppliers ",
          "WHERE id={};".format(supplier_id)]
  toex = "".join(toex)
  cursor.execute(toex)
  res = cursor.fetchall()
  if res != []:
    conn.close()
    return res
  else:
    conn.close()
    return 0

def find_drugs(authDict, drug_name, drug_atc):
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()
  i_list = []
  if drug_name and drug_name!='':
    i_list.append("drugs.name LIKE '%{}%' ".format(drug_name.upper()))
  if drug_atc and drug_atc!='':
    i_list.append("atc_chemical_substance.atc_code LIKE '%{}%' ".format(drug_atc.upper()))
  i_string = ""
  if i_list != []:
    i_string = " WHERE " + "AND ".join(i_list)
  toex = ["SELECT drugs.id, drugs.name, atc_chemical_substance.atc_code, drugs.quantity ",
          "FROM drugs INNER JOIN atc_chemical_substance ",
          "ON drugs.atc_chemical_substance_id=atc_chemical_substance.id ",
          "{};".format(i_string)]
  toex = "".join(toex)
  cursor.execute(toex)
  res = cursor.fetchall()
  if res != []:
    conn.close()
    return res
  else:
    conn.close()
    return 0

def find_issued_to_medic(authDict, drug_name=None, fname=None, lname=None, pname=None, from_date=None, to_date=None):
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()
  i_list = []
  if drug_name and drug_name!='':
    i_list.append("drugs.name LIKE '%{}%' ".format(drug_name.upper()))
  if fname and fname!='':
    i_list.append("issued_to_medic.medic_fname LIKE '%{}%' ".format(fname))
  if lname and lname!='':
    i_list.append("issued_to_medic.medic_lname LIKE '%{}%' ".format(lname))
  if pname and pname!='':
    i_list.append("issued_to_medic.medic_pname LIKE '%{}%' ".format(pname))
  if from_date and from_date!='' and not to_date:
    i_list.append("issued_to_medic.date=>'{}'".format(from_date))
  if to_date and to_date!='' and not from_date:
    i_list.append("issued_to_medic.date=<'{}'".format(to_date))
  if from_date and from_date!='' and to_date and to_date!='':
    i_list.append("issued_to_medic.date>='{}' AND issued_to_medic.date<='{}'".format(from_date, to_date))
  i_string = ""
  if i_list != []:
    i_string = " WHERE " + "AND ".join(i_list)
  toex = ["SELECT issued_to_medic.date, drugs.name, issued_to_medic.quantity, ",
                  "issued_to_medic.medic_fname, issued_to_medic.medic_lname, ",
                  "issued_to_medic.medic_pname, medic_ranks.name ",
          "FROM (drugs INNER JOIN issued_to_medic ",
                "ON drugs.id=issued_to_medic.drug_id) ",
                "INNER JOIN medic_ranks ",
                      "ON issued_to_medic.medic_rank_id=medic_ranks.id",
          "{};".format(i_string)]
  toex = "".join(toex)
  cursor.execute(toex)
  res = cursor.fetchall()
  # print(toex)
  if res != []:
    conn.close()
    return res
  else:
    conn.close()
    return 0

def find_drugs_prohibited(authDict, drug_name=None, medic_rank_id=None):
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()
  i_list = []
  if drug_name and drug_name!='':
    i_list.append("drugs.name LIKE '%{}%' ".format(drug_name.upper()))
  if medic_rank_id and medic_rank_id!='':
    i_list.append("medic_ranks.id={} ".format(medic_rank_id))
  i_string = ""
  if i_list != []:
    i_string = " WHERE " + "AND ".join(i_list)
  toex = ["SELECT drugs_prohibited.id, drugs.name, medic_ranks.name ",
          "FROM (drugs INNER JOIN drugs_prohibited ",
                "ON drugs.id=drugs_prohibited.drug_id) ",
                "INNER JOIN medic_ranks ",
                      "ON drugs_prohibited.medic_rank_id=medic_ranks.id",
          "{};".format(i_string)]
  toex = "".join(toex)
  cursor.execute(toex)
  res = cursor.fetchall()
  # print(toex)
  if res != []:
    conn.close()
    return res
  else:
    conn.close()
    return 0

def find_manufacturers(authDict, manufacturer_name=None, manufacturer_country=None, manufacturer_id=None):
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()
  i_list = []
  if manufacturer_id and manufacturer_id!='':
    i_list.append("id={} ".format(manufacturer_id))
  if manufacturer_name and manufacturer_name!='':
    i_list.append("name LIKE '%{}%' ".format(manufacturer_name.upper()))
  if manufacturer_country and manufacturer_country!='':
    i_list.append("country LIKE '%{}%' ".format(manufacturer_country.upper()))
  
  i_string = ""
  if i_list != []:
    i_string = " WHERE " + "AND ".join(i_list)
  toex = ["SELECT id, name, country ",
          "FROM manufacturers ",
          "{};".format(i_string)]
  toex = "".join(toex)
  cursor.execute(toex)
  res = cursor.fetchall()
  # print(toex)
  if res != []:
    conn.close()
    return res
  else:
    conn.close()
    return 0

def find_suppliers(authDict, supplier_name=None, supplier_country=None, supplier_id=None):
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()
  i_list = []
  if supplier_id and supplier_id!='':
    i_list.append("id={} ".format(supplier_id))
  if supplier_name and supplier_name!='':
    i_list.append("name LIKE '%{}%' ".format(supplier_name.upper()))
  if supplier_country and supplier_country!='':
    i_list.append("country LIKE '%{}%' ".format(supplier_country.upper()))
  
  i_string = ""
  if i_list != []:
    i_string = " WHERE " + "AND ".join(i_list)
  toex = ["SELECT id, name, country ",
          "FROM suppliers ",
          "{};".format(i_string)]
  toex = "".join(toex)
  cursor.execute(toex)
  res = cursor.fetchall()
  # print(toex)
  if res != []:
    conn.close()
    return res
  else:
    conn.close()
    return 0

def find_delivery_log(authDict, drug_name=None, manufacturer_name=None, manufacturer_country=None, supplier_name=None, supplier_country=None):
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()
  i_list = []
  if drug_name and drug_name!='':
    i_list.append("drugs.name LIKE '%{}%' ".format(drug_name.upper()))
  if supplier_name and supplier_name!='':
    i_list.append("suppliers.name LIKE '%{}%' ".format(supplier_name.upper()))
  if supplier_country and supplier_country!='':
    i_list.append("suppliers.country LIKE '%{}%' ".format(supplier_country.upper()))
  if manufacturer_name and manufacturer_name!='':
    i_list.append("manufacturers.name LIKE '%{}%' ".format(manufacturer_name.upper()))
  if manufacturer_country and manufacturer_country!='':
    i_list.append("manufacturers.country LIKE '%{}%' ".format(manufacturer_country.upper()))

  i_string = ""
  if i_list != []:
    i_string = " WHERE " + "AND ".join(i_list)
  toex = ["SELECT drugs.id, drugs.name, ",
          "manufacturers.id, manufacturers.name, manufacturers.country, ",
          "suppliers.id, suppliers.name, suppliers.country ",
          "FROM (((suppliers INNER JOIN drug_supplier ",
            "ON suppliers.id=drug_supplier.supplier_id) INNER JOIN drugs ",
              "ON drug_supplier.drug_id=drugs.id) INNER JOIN drug_manufacturer ",
                "ON drugs.id=drug_manufacturer.drug_id) INNER JOIN manufacturers ",
                  "ON drug_manufacturer.manufacturer_id=manufacturers.id ",
          "{};".format(i_string)]
  toex = "".join(toex)
  cursor.execute(toex)
  res = cursor.fetchall()
  # print(toex)
  if res != []:
    conn.close()
    # print(res)
    return res
  else:
    conn.close()
    return 0

def update_drugs(authDict, drug_id, name=None, atc_code=None, quantity=None, description=None):
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()
  i_string = ""
  i_list = []
  if name and name!='':
    i_list.append("name='{}'".format(name.upper()))
  if quantity and quantity!='':
    i_list.append("quantity={}".format(str(quantity)))
  if description and description!='':
    i_list.append("description='{}'".format(description))
  if atc_code and atc_code!='':
    i_list.append("atc_chemical_substance_id=(SELECT id FROM atc_chemical_substance WHERE atc_code='{}')".format(atc_code.upper()))
  i_string = ", ".join(i_list)

  toex = ["UPDATE drugs ",
          "SET {} ".format(i_string),
          "WHERE id={};".format(str(drug_id))]
  toex = "".join(toex)
  try:
    cursor.execute(toex)
    conn.close()
    return 1
  except Exception as error:
    print(error)
    conn.close()
    return 0

def update_manufacturers(authDict, id, name=None, country=None, contact_info=None):
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()
  i_string = ""
  i_list = []
  if name and name!='':
    i_list.append("name='{}'".format(name.upper()))
  if country and country!='':
    i_list.append("country='{}'".format(country.upper()))
  if contact_info and contact_info!='':
    i_list.append("contact_info='{}'".format(contact_info))
  i_string = ", ".join(i_list)

  toex = ["UPDATE manufacturers ",
          "SET {} ".format(i_string),
          "WHERE id={};".format(id)]
  toex = "".join(toex)
  try:
    cursor.execute(toex)
    conn.close()
    return 1
  except Exception as error:
    print(error)
    conn.close()
    return 0

def update_suppliers(authDict, id, name=None, country=None, contact_info=None):
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()
  i_string = ""
  i_list = []
  if name and name!='':
    i_list.append("name='{}'".format(name.upper()))
  if country and country!='':
    i_list.append("country='{}'".format(country.upper()))
  if contact_info and contact_info!='':
    i_list.append("contact_info='{}'".format(contact_info))
  i_string = ", ".join(i_list)

  toex = ["UPDATE suppliers ",
          "SET {} ".format(i_string),
          "WHERE id={};".format(id)]
  toex = "".join(toex)
  try:
    cursor.execute(toex)
    conn.close()
    return 1
  except Exception as error:
    print(error)
    conn.close()
    return 0

def writeoff_drugs(authDict, drug_id, quantity):
  conn = connectToDB(authDict)
  if conn == -1:
    return -1
  cursor = conn.cursor()
  toex = ["UPDATE drugs ",
          "SET quantity=quantity-{} ".format(str(quantity)),
          "WHERE id={};".format(str(drug_id))]
  toex = "".join(toex)
  try:
    cursor.execute(toex)
    conn.close()
    return 1
  except Exception as error:
    print(error)
    conn.close()
    return 0


# res = find_issued_to_medic()
# print(type(str(res[0][0])))
# update_drugs('15', 'test drug 99', 'z00zz00', '99', 'Zhizha.')
# print(check_drugs('test drug', 'z00zz00', '1', '1'))
# print(check_drugs_prohibited(2, 2))
# doTests2()
# print(get_drug('TEST DRUG 1', 'z00zz00'))
# print(find_drugs('est'))