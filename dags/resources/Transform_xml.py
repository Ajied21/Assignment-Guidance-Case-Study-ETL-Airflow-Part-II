import os
import xml.etree.ElementTree as ET
from .Extract_xml import extract_xml

# Fungsi untuk mengambil data XML
def get_xml(n):
    results = extract_xml(n)
    root = ET.fromstring(results)

    user_data_list = []
    for user in root.findall('.//results'):
        user_data = {
            "id_user": user.find('login/uuid').text if user.find('login/uuid') is not None else None,
            "nama_user": user.find('login/username').text if user.find('login/username') is not None else None,
            "kata_sandi_user": user.find('login/password').text if user.find('login/password') is not None else None,
            "nama": f"{user.find('name/first').text if user.find('name/first') is not None else ''} " \
                    f"{user.find('name/last').text if user.find('name/last') is not None else ''}".strip(),
            "jenis_kelamin": user.find('gender').text if user.find('gender') is not None else None,
            "umur": user.find('dob/age').text if user.find('dob/age') is not None else None,
            "nomor_jalan": user.find('location/street/number').text if user.find('location/street/number') is not None else None,
            "nama_jalan": user.find('location/street/name').text if user.find('location/street/name') is not None else None,
            "kecamatan": user.find('location/state').text if user.find('location/state') is not None else None,
            "kota": user.find('location/city').text if user.find('location/city') is not None else None,
            "negara": user.find('location/country').text if user.find('location/country') is not None else None,
            "kode_pos": user.find('location/postcode').text if user.find('location/postcode') is not None else None,
            "email": user.find('email').text if user.find('email') is not None else None,
            "nomor_handphone": user.find('phone').text if user.find('phone') is not None else None,
            "nomor_telepon": user.find('cell').text if user.find('cell') is not None else None,
            "url_photo": user.find('picture/large').text if user.find('picture/large') is not None else None
        }

        if user_data["id_user"] is not None:
            user_data_list.append(user_data)

    if not user_data_list:
        return '<users></users>'

    root_element = ET.Element("results")
    for user_data in user_data_list:
        user_element = ET.SubElement(root_element, "user")
        for key, value in user_data.items():
            ET.SubElement(user_element, key).text = str(value) if value is not None else ''

    data_xml = ET.tostring(root_element, encoding='unicode')

    return data_xml

def transfrom_to_xml(file_name, n):
    folder_path = './dags/data/xml'
    os.makedirs(folder_path, exist_ok=True)

    # Ambil data XML
    data_xml = get_xml(n)

    # Simpan ke file XML
    file_path = os.path.join(folder_path, f'{file_name}.xml')
    with open(file_path, 'w') as xml_file:
        xml_file.write(data_xml)
    print(f"Data tersimpan ke {file_path}")
    print(f"Data berhasil ke transform:\n{data_xml}")

if __name__ == '__main__':
    
    transfrom_to_xml()