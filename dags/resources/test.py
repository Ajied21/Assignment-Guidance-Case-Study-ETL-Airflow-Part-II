import requests
import xml.etree.ElementTree as ET

# Function untuk mengambil XML dari API
def extract_xml(n):
    response = requests.get(f"https://randomuser.me/api/?format=xml&results={n}")
    root = ET.fromstring(response.content)
    data_xml = ET.tostring(root, encoding='unicode', method='xml')
    return data_xml

# Panggil function extract_xml dengan parameter n (misal 1 untuk satu user)
data_xml = extract_xml(5)

# Parsing XML
root = ET.fromstring(data_xml)

# Mengambil data dan mengganti nama kunci
user_data = {}
user = root.find('.//results')  # Mencari elemen 'results'

if user is not None:  # Memeriksa apakah elemen 'results' ditemukan
    user_data = {
        "id_user": user.find('login/uuid').text if user.find('login/uuid') is not None else None,
        "nama_user": user.find('login/username').text if user.find('login/username') is not None else None,
        "kata_sandi_user": user.find('login/password').text if user.find('login/password') is not None else None,
        "nama": f"{user.find('name/title').text if user.find('name/title') is not None else ''} " \
                 f"{user.find('name/first').text if user.find('name/first') is not None else ''} " \
                 f"{user.find('name/last').text if user.find('name/last') is not None else ''}".strip(),
        "jenis_kelamin": user.find('gender').text if user.find('gender') is not None else None,
        "umur": user.find('dob/age').text if user.find('dob/age') is not None else None,
        "nomor_jalan": user.find('location/street/number').text if user.find('location/street/number') is not None else None,
        "jalan": user.find('location/street/name').text if user.find('location/street/name') is not None else None,
        "kecamatan": user.find('location/state').text if user.find('location/state') is not None else None,
        "kota": user.find('location/city').text if user.find('location/city') is not None else None,
        "negara": user.find('location/country').text if user.find('location/country') is not None else None,
        "kode_pos": user.find('location/postcode').text if user.find('location/postcode') is not None else None,
        "email": user.find('email').text if user.find('email') is not None else None,
        "nomor_handphone": user.find('phone').text if user.find('phone') is not None else None,
        "nomor_telepon": user.find('cell').text if user.find('cell') is not None else None,
        "url_photo": user.find('picture/large').text if user.find('picture/large') is not None else None
    }

    # Membuat elemen root
    root_element = ET.Element("user")

    # Menambahkan data ke elemen XML
    for key, value in user_data.items():
        ET.SubElement(root_element, key).text = str(value)  # Konversi ke string jika None

    # Mengubah ke string XML
    xml_string = ET.tostring(root_element, encoding='unicode')

    # Menampilkan string XML
    print(xml_string)

else:
    print("Elemen 'results' tidak ditemukan dalam XML.")
