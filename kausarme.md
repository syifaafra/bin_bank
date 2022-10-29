Nama: Kausar Meutuwah NPM: 2106630100

# Impelementasi

## Persiapan Awal(Dikerjakan bersama)

1. Pertama untuk mengawali kita akan membuat project django dengan menclone template
   dari https://github.com/pbp-fasilkom-ui/django-pbp-template.

2. Selajutnya, kita membuat sebuah aplikasi bernama `bin_bank` serta menghapus project `example_app`

```
python manage.py startapp bin_bank
```

3. Daftarkan aplikasi bin_bank ke settings.py

```
INSTALLED_APPS = [ ..., "bin_bank", ... ]
```

4. Buat views dasar untuk ngetes aplikasi

## Menerapkan Models(Dikerjakan bersama)

### 1. Buat Models Transaction untuk menyimpan pesanan dari semua orang

```
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(default=timezone.now())
    amountKg = models.IntegerField()
    branchName = models.CharField(max_length=255)
    isFinished = models.BooleanField(default=False)
```

Transaction menggunakan Foreign Key yaitu user. Karena setiap Transaksi pasti dimiliki oleh tepat satu user.
on_delete = models.CASCADE memastikan saat ForeignKey yaitu user di delete transaksi terkait juga akan terdele.

date menyatakan waktu dan tanggal transaksi yang secara default akan di set menjadi waktu sekarang.
amountKg menyatakan berat sampah.

branchName menyatakan nama CABANg di mana sampah di donasikan 
lalu isFinished menyatakan donasi sudah selesai.


### 2. Membuat models MyUser sebagai custom user 


## Menerapkan views Deposit Sampah

Membuat halaman dasar dengan mengextend dari base.html

```html
{% extend base.html %} 
```

Membuat Form yang diperlukan

Menampilkan data yang diperlukan

Ubah Form sehingga menampilkan dengan modals

## Menerapkan responsive web

Tambahkan bootsrap class pada bagian yang perlu ditambahkan

## Memiliki halaman form yang dapat menerima masukan dari pengguna kemudian diproses oleh views

(contoh: insert ke dalam model, query dari model, update data di dalam model).

## Menerapkan JavaScript dengan pemanggilan AJAX.

Menerapkan filter informasi bagi pengguna yang sudah login saja (contoh: data alamat, umur, nomor HP hanya ditampilkan
ketika sudah login saja).

