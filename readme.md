# Panduan penggunaan Kurs API

Kurs API adalah sebuah sistem untuk menyimpan data kurs secara berkala pada suatu tanggal dan currency yang unik. Pekerjaan dilakukan dengan menganut Clean Code Principle dan dikerjakan menggunakan Test Driven Development. 
Aplikasi ini live pada heroku di link berikut: 
[https://kurs-api-backend-task.herokuapp.com/](https://kurs-api-backend-task.herokuapp.com/)
Sedangkan, Code repository dapat diakses pada link berikut:
[https://github.com/realr3fo/kurs-api](https://github.com/realr3fo/kurs-api)

Panduan ini terdiri dari beberapa bagian, yakni:

 - Persiapan environment untuk penggunaan
 - Dokumentasi mengenai API yang dibuat
	 - Menyimpan List Kurs Exchange hari ini [GET]
	 - Membuat sebuah data kurs baru [POST]
	 - Mengedit data kurs yang sudah ada [PUT]
	 - Menghapus data kurs yang sudah ada [DELETE]
	 - Mencari data berdasarkan rentang tanggal [GET]
	 - Mencari data berdasarkan rentang tanggal dan mata uang [GET]
---
## Persiapan environment untuk penggunaan kurs API secara lokal

Terdapat beberapa tahap dalam menyiapkan environment agar dapat menggunakan Kurs API secara local.

 1. Memastikan python3 dan pip telah diinstall pada device
 2. Menggunakan virutal environment dengan perintah `virutalenv venv`
 3. Melakukan instalasi requirements dengan perintah `pip3 install -r requirements.txt`
 4. Membuat dua buah database satu untuk menjalankan test dan satu untuk menjalankan program backend dengan perintah `createdb test_db` dan `createdb kurs_api`
 5. Melakukan migrasi dengan menjalankan perintah `python manage.py db init` kemudian dilanjutkan dengan `python manage.py db migrate` dan terakhir `python manage.py upgrade`.
 6. Program kemudian bisa dijalankan dengan menggunakan perintah `flask run` , `python run.py` , ataupun `gunicorn app:app`
 7. Adapun test untuk Kurs API dapat dijalankan dengan perintah `python test_kurs_api.py`
---
## Dokumentasi mengenai API yang dibuat

Kurs API terdiri dari enam buah API yang terdiri dari tiga GET, satu POST, satu PUT, dan satu DELETE Method, Pada bagian ini akan diberikan dokumentasi lengkap dengan penjelasan masing-masing fungsi nya.

###  Menyimpan List Kurs Exchange hari ini `[GET] /api/indexing`

API ini akan melakukan scraping dari url https://www.bca.co.id/id/Individu/Sarana/Kurs-dan-Suku-Bunga/Kurs-dan-Kalkulator
untuk diambil data tentang harga masing-masing mata uang yang tercantum pada website tersebut. Data yang diambil dari hasil
scraping kemudian akan disimpan di dalam database. 

#### Contoh pemanggilan

Berikut adalah contoh pemanggilan endpoint ini.

#### Request
Request yang diperlukan cukup url dari endpoint ini tanpa parameter ataupun data request body.

```GET /api/indexing```

#### Response
Response berupa data hasil scraping dari url di atas, 

```
{
    "data": [
        {
            "bank_notes_beli": "16.250,00",
            "bank_notes_jual": "16.750,00",
            "currency": "USD",
            "date": "Thu, 02 Apr 2020 00:00:00 GMT",
            "date_created": "Thu, 02 Apr 2020 06:14:01 GMT",
            "date_modified": "Thu, 02 Apr 2020 06:14:01 GMT",
            "erate_beli": "16.440,00",
            "erate_jual": "16.590,00",
            "id": 17,
            "tt_counter_beli": "16.275,00",
            "tt_counter_jual": "16.775,00"
        },
        {
            "bank_notes_beli": "11.408,00",
            "bank_notes_jual": "11.767,00",
            "currency": "SGD",
            "date": "Thu, 02 Apr 2020 00:00:00 GMT",
            "date_created": "Thu, 02 Apr 2020 06:14:01 GMT",
            "date_modified": "Thu, 02 Apr 2020 06:14:01 GMT",
            "erate_beli": "11.455,84",
            "erate_jual": "11.573,63",
            "id": 18,
            "tt_counter_beli": "11.343,10",
            "tt_counter_jual": "11.700,10"
        },
        
        ...

        {
            "bank_notes_beli": "429,00",
            "bank_notes_jual": "514,00",
            "currency": "THB",
            "date": "Thu, 02 Apr 2020 00:00:00 GMT",
            "date_created": "Thu, 02 Apr 2020 06:14:02 GMT",
            "date_modified": "Thu, 02 Apr 2020 06:14:02 GMT",
            "erate_beli": "494,93",
            "erate_jual": "504,93",
            "id": 32,
            "tt_counter_beli": "493,00",
            "tt_counter_jual": "508,00"
        }
    ]
}
```

### Membuat sebuah data kurs baru `[POST] /api/kurs`

API ini akan melakukan penyimpanan berdaasarkan objek kurs yang dikirim oleh pengguna, Berdasarkan
input yang diberikan pengguna, objek akan dibuat oleh sistem dan kemudian disimpan ke dalam database.
 
#### Contoh pemanggilan
Berikut adalah contoh pemanggilan endpoint ini.

#### Request
Request yang diperlukan adalah request dengan body sebagai berikiut dalam tipe json.

`[POST] /api/kurs`
```
{
	"currency": "ABF",
	"e_rate": {
		"jual": 1803.55,
		"beli": 177355
	},
	"tt_counter": {
		"jual": 1803.55,
		"beli": 177355
	},
	"bank_notes": {
		"jual": 1803.55,
		"beli": 177355
	},
	"date": "2018-05-16"
}
```

#### Response

Response yang dikembalikan adalah objek hasil dari request user yang telah disimpan ke dalam database oleh sistem.

```
{
    "bank_notes_beli": "177355",
    "bank_notes_jual": "1803.55",
    "currency": "ABF",
    "date": "Wed, 16 May 2018 00:00:00 GMT",
    "date_created": "Thu, 02 Apr 2020 05:01:04 GMT",
    "date_modified": "Thu, 02 Apr 2020 05:01:04 GMT",
    "erate_beli": "177355",
    "erate_jual": "1803.55",
    "id": 52,
    "tt_counter_beli": "177355",
    "tt_counter_jual": "1803.55"
}
```

### Mengedit data kurs yang sudah ada `[PUT] Mengedit data kurs yang sudah ada`
API ini akan melakukan update terhadap data yang sudah ada di dalam database.

#### Contoh pemanggilan
Berikut adalah contoh pemanggilan endpoint ini.

#### Request
request yang diperlukan pada endpoint ini sama dengan request pada POST di atas, yakni  komponen kurs
lengkap.

`[PUT] /api/kurs`
```
{
	"currency": "ABF",
	"e_rate": {
		"jual": 123,
		"beli": 123
	},
	"tt_counter": {
		"jual": 123,
		"beli": 123
	},
	"bank_notes": {
		"jual": 123,
		"beli": 123
	},
	"date": "2018-05-16"
}

```


#### Response
Response yang dikembalikan adalah data hasil perubahana berdasarkan requeest yang dikirimkan.
```
{
    "bank_notes_beli": "123",
    "bank_notes_jual": "123",
    "currency": "ABF",
    "date": "Wed, 16 May 2018 00:00:00 GMT",
    "date_created": "Thu, 02 Apr 2020 05:01:04 GMT",
    "date_modified": "Thu, 02 Apr 2020 05:01:30 GMT",
    "erate_beli": "123",
    "erate_jual": "123",
    "id": 52,
    "tt_counter_beli": "123",
    "tt_counter_jual": "123"
}
```

### Menghapus data kurs yang sudah ada `[DELETE] /api/kurs/<date>`
Endpoint ini akan menghapus data kurs yang sudah ada berdasarkan tanggal yang ditentukan oleh pengguna

#### Contoh pemanggilan
Berikut adalah contoh pemanggilan endpoint ini.

#### Request
Request yang diperlukan pada endpoint ini adalah tanggal yang diinginkan untuk dijadikan sebagai penanda 
bahawa kita ingin menghapus data pada tanggal tersebut. Format tanggal yang digunakan adalah (YYYY-mm-dd)

`[DELETE] /api/kurs/2020-04-02`

#### Response
Response yang dikembalikan adalah pemberitahuan bahwa penghapusan telah berhasil.

```
{
    "message": "kurslists deleted successfully"
}
```

### Mencari data berdasarkan rentang tanggal `[GET] /api/kurs?startdate=:startdate&enddate=:enddate`
Endpoint ini akan memberikan data kurs yang ada pada database berdasarkan rentang tanggal yang ditentukan oleh penggunanya.

#### Contoh Pemanggilan
Berikut adalah contoh pemanggilan endpoint ini.

#### Request
Request yang diperlukan pada endpoint ini adalah rentang tanggal startdate dan enddate dengan format (YYYY-mm-dd) 

`[GET] /api/kurs?startdate=2020-04-02&enddate=2020-04-02`

#### Response
Response yang dikembalikan berdasarkan pemanggilan tersebut adalah data yang ada pada database yang ada di antara rentang waktu
start date dan end date.

```
{
    "data": [
        {
            "bank_notes_beli": "16.250,00",
            "bank_notes_jual": "16.750,00",
            "currency": "USD",
            "date": "Thu, 02 Apr 2020 00:00:00 GMT",
            "date_created": "Thu, 02 Apr 2020 05:00:49 GMT",
            "date_modified": "Thu, 02 Apr 2020 05:00:49 GMT",
            "erate_beli": "16.440,00",
            "erate_jual": "16.590,00",
            "id": 36,
            "tt_counter_beli": "16.275,00",
            "tt_counter_jual": "16.775,00"
        },
        {
            "bank_notes_beli": "11.408,00",
            "bank_notes_jual": "11.767,00",
            "currency": "SGD",
            "date": "Thu, 02 Apr 2020 00:00:00 GMT",
            "date_created": "Thu, 02 Apr 2020 05:00:49 GMT",
            "date_modified": "Thu, 02 Apr 2020 05:00:49 GMT",
            "erate_beli": "11.455,84",
            "erate_jual": "11.573,63",
            "id": 37,
            "tt_counter_beli": "11.343,10",
            "tt_counter_jual": "11.700,10"
        },

        ,,,

        {
            "bank_notes_beli": "429,00",
            "bank_notes_jual": "514,00",
            "currency": "THB",
            "date": "Thu, 02 Apr 2020 00:00:00 GMT",
            "date_created": "Thu, 02 Apr 2020 05:00:49 GMT",
            "date_modified": "Thu, 02 Apr 2020 05:00:49 GMT",
            "erate_beli": "494,93",
            "erate_jual": "504,93",
            "id": 51,
            "tt_counter_beli": "493,00",
            "tt_counter_jual": "508,00"
        }
    ]
}
```

### Mencari data berdasarkan rentang tanggal dan mata uang `[GET] /api/kurs/:symbol?startdate=:startdate&enddate=:enddate`
Endpoint ini akan memberikan data kurs yang ada pada database berdasarkan rentang tanggal dan mata uang yang ditentukan oleh penggunanya.


#### Contoh Pemanggilan
Berikut adalah contoh pemanggilan untuk endpoint ini.

#### Request
Request yang diperlukan pada API ini adalah mata uang yang ingin dicari, dan rentang waktu yang ingin dicari yang terdiri dari start date dan end date dengan format (YYYY-mm-dd)

`[GET] /api/kurs/USD?startdate=2020-04-02&enddate=2020-04-02`

#### Response
Response yang dikembalikan berdasarkan input tersebut adalah data dengan mata uang yang ditentukan yang ada pada rentang waktu yang ditentukan

```.env
{
    "data": [
        {
            "bank_notes_beli": "16.250,00",
            "bank_notes_jual": "16.750,00",
            "currency": "USD",
            "date": "Thu, 02 Apr 2020 00:00:00 GMT",
            "date_created": "Thu, 02 Apr 2020 05:00:49 GMT",
            "date_modified": "Thu, 02 Apr 2020 05:00:49 GMT",
            "erate_beli": "16.440,00",
            "erate_jual": "16.590,00",
            "id": 36,
            "tt_counter_beli": "16.275,00",
            "tt_counter_jual": "16.775,00"
        }
    ]
}
```
