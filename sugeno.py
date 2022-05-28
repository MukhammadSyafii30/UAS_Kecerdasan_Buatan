#Nama   : Mukammad Syafi'i
#NIM    : 191011401770
#Kelas  : 06TPLE025
#Fuzzy Sugeno
#Studi Kasus : Penjualan Sirup Marjan

#Permintaan Barang  : min 50 botol, max 100 botol.
#Persediaan Barang  : sedikit 500, stabil 500, dan banyak 1000.
#Penjualan Barang   : min 50, max 1000

def down(x, xmin, xmax):
    return (xmax- x) / (xmax - xmin)

def up(x, xmin, xmax):
    return (x - xmin) / (xmax - xmin)

class Permintaan():
    minimum = 50
    maximum = 100

    def turun(self, x):
        if x >= self.maximum:
            return 0
        elif x <= self.minimum:
            return 1
        else:
            return down(x, self.minimum, self.maximum)

    def naik(self, x):
        if x >= self.maximum:
            return 1
        elif x <= self.minimum:
            return 0
        else:
            return up(x, self.minimum, self.maximum)

class Persediaan():
    minimum = 100
    medium = 500
    maximum = 1000

    def sedikit(self, x):
        if x >= self.medium:
            return 0
        elif x <= self.minimum:
            return 1
        else:
            return down(x, self.minimum, self.medium)
    
    def cukup(self, x):
        if self.minimum < x < self.medium:
            return up(x, self.minimum, self.medium)
        elif self.medium < x < self.maximum:
            return down(x, self.medium, self.maximum)
        elif x == self.medium:
            return 1
        else:
            return 0

    def banyak(self, x):
        if x >= self.maximum:
            return 1
        elif x <= self.medium:
            return 0
        else:
            return up(x, self.medium, self.maximum)

class Penjualan():
    minimum = 50
    maximum = 1000
    
    def kurang(self, α):
        return self.maximum - α * (self.maximum-self.minimum)

    def tambah(self, α):
        return α *(self.maximum - self.minimum) + self.minimum

    # 2 permintaan 3 persediaan
    def inferensi(self, jmlh_request, jmlh_persediaan):
        rqt = Permintaan()
        rsa = Persediaan()
        result = []
        # [R1] JIKA Permintaan TURUN, dan Persediaan BANYAK, 
        #     MAKA Penjualan Barang BERKURANG.
        α1 = min(rqt.turun(jmlh_request), rsa.banyak(jmlh_persediaan))
        z1 = self.kurang(α1)
        result.append((α1, z1))

        # [R2] JIKA Permintaan TURUN, dan Persediaan SEDIKIT, 
        #     MAKA Penjualan Barang BERKURANG.
        α2 = min(rqt.turun(jmlh_request), rsa.sedikit(jmlh_persediaan))
        z2 = self.kurang(α2)
        result.append((α2, z2))

        # [R3] JIKA Permintaan NAIK, dan Persediaan BANYAK, 
        #     MAKA Penjualan Barang BERTAMBAH.
        α3 = min(rqt.naik(jmlh_request), rsa.banyak(jmlh_persediaan))
        z3 = self.tambah(α3)
        result.append((α3, z3))

        # [R4] JIKA Permintaan NAIK, dan Persediaan SEDIKIT,
        #     MAKA Penjualan Barang BERTAMBAH * 2
        α4 = min(rqt.naik(jmlh_request), rsa.sedikit(jmlh_persediaan))
        z4 = self.tambah(α4) * 2
        result.append((α4, z4))

        # [R5] JIKA Permintaan NAIK, dan Persediaan CUKUP,
        #     MAKA Penjualan Barang BERKURANG / 2
        α5 = min(rqt.naik(jmlh_request), rsa.cukup(jmlh_persediaan))
        z5 = self.kurang(α5) / 2
        result.append((α5, z5))

        # [R6] JIKA Permintaan NAIK, dan Persediaan CUKUP,
        #     MAKA Penjualan Barang BERTAMBAH.
        α6 = min(rqt.turun(jmlh_request), rsa.cukup(jmlh_persediaan))
        z6 = self.tambah(α6)
        result.append((α6, z6))

        return result
    
    def defuzifikasi(self, jmlh_requst, jmlh_persediaan):
        inferensi_values = self.inferensi(jmlh_request, jmlh_persediaan)
        return sum([(value[0]* value[1]) for value in inferensi_values]) / sum([value[0] for value in inferensi_values])