import pandas as pd

#membaca data excel dan assign ke variabel
supplier = pd.read_excel('supplier.xlsx')
print(supplier)
panjang_kolom = len(supplier)

#assign id 
supplier_id = supplier['id']
#assign kualitas 
kualitas = supplier['kualitas']
#assign harga
harga = supplier['harga']

#proses fuzzyfication dengan looping banyaknya data
#inisialisasi list kosong untuk menampung nilai setelah deffuzzyfication
def fuzzi(supplier_id, kualitas, harga ,panjang_kolom):
  fuzzy = []
  #looping dengan range banyaknya data sebanyak 100 kolom
  for i in range(panjang_kolom):
      #inisialisasi array kosong untuk menampung nilai 
      TK = [0, 0, 0, 0] #Tingkat Kualitas
      TH = [0, 0, 0] #Tingkat Harga
      #inisialisasi variabel penilaian = 0
      very_bad = bad = good = very_good = cheap = affordable = expensive = 0
      #conditioning
      #for quality
      if kualitas[i] <= 25:
          very_bad = 1
          TK[0] = very_bad
      elif kualitas[i] > 25 and kualitas[i] < 30:
          bad = -(kualitas[i] - 30)/(30 - 25)
          very_bad = (kualitas[i] - 25)/(30 - 25)
          TK[0] = very_bad
          TK[1] = bad
      elif kualitas[i] >= 30 and kualitas[i] <= 50:
          bad = 1
          TK[1] = bad
      elif kualitas[i] > 50 and kualitas[i] < 55:
          bad = -(kualitas[i] - 55)/(55 - 50)
          good = (kualitas[i] - 50)/(55 - 50)
          TK[1] = bad
          TK[2] = good
      elif kualitas[i] >= 55 and kualitas[i] <= 75:
          good = 1
          TK[2] = good
      elif kualitas[i] > 75 and kualitas[i] < 80:
          good = -(kualitas[i] - 80)/(80 - 75)
          very_good = (kualitas[i] - 75)/(80 - 75)
          TK[2] = good
          TK[3] = very_good
      elif kualitas[i] >= 80:
          very_good = 1
          TK[3] = very_good
              
      #for price
      if harga[i] <= 2:
          cheap = 1
          TH[0] = cheap
      elif harga[i] > 2 and harga[i] < 4:
          cheap = -(kualitas[i] - 4)/(4 - 2)
          affordable = (kualitas[i] - 2)/(4 - 2)
          TH[0] = cheap
          TH[1] = affordable
      elif harga[i] >= 4 and harga[i] <= 6:
          affordable = 1
          TH[1] = affordable
      elif harga[i] > 6 and harga[i] < 8:
          affordable = -(kualitas[i] - 8)/(8 - 6)
          expensive = (kualitas[i] - 6)/(8 - 6)
          TH[1] = affordable
          TH[2] = expensive
      elif harga[i] >= 8:
          expensive = 1
          TH[2] = expensive 

      #inference(fuzzy rules)
      #inisialisasi list kosong untuk rekomendasi
      tinggi = []
      rendah = []
      #conditioning 
      if TH[0] == cheap and TK[0] == very_bad: #1
        #mencari nilai terendah untuk diassign ke list
        rendah.append(min(TK[0], TH[0]))
      if TH[0] == cheap and TK[1] == bad: #2
        #mencari nilai terendah untuk diassign ke list
        tinggi.append(min(TK[1], TH[0]))
      if TH[0] == cheap and TK[2] == good: #3
        #mencari nilai terendah untuk diassign ke list
        tinggi.append(min(TK[2], TH[0]))
      if TH[0] == cheap and TK[3] == very_good: #4
        #mencari nilai terendah untuk diassign ke list
        tinggi.append(min(TK[3], TH[0]))
      if TH[1] == affordable and TK[0] == very_bad: #5
        #mencari nilai terendah untuk diassign ke list
        rendah.append(min(TK[0], TH[1]))
      if TH[1] == affordable and TK[1] == bad: #6
        #mencari nilai terendah untuk diassign ke list
        rendah.append(min(TK[1], TH[1]))
      if TH[1] == affordable and TK[2] == good: #7
        #mencari nilai terendah untuk diassign ke list
        tinggi.append(min(TK[2], TH[1]))
      if TH[1] == affordable and TK[3] == very_good: #8
        #mencari nilai terendah untuk diassign ke list
        tinggi.append(min(TK[3], TH[1]))
      if TH[2] == expensive and TK[0] == very_bad: #9
        #mencari nilai terendah untuk diassign ke list
        rendah.append(min(TK[0], TH[2]))
      if TH[2] == expensive and TK[1] == bad: #10
        #mencari nilai terendah untuk diassign ke list
        rendah.append(min(TK[1], TH[2]))
      if TH[2] == expensive and TK[2] == good: #11
        #mencari nilai terendah untuk diassign ke list
        rendah.append(min(TK[2], TH[2]))
      if TH[2] == expensive and TK[3] == very_good: #12
        #mencari nilai terendah untuk diassign ke list
        tinggi.append(min(TK[3], TH[2]))
                  
      #mencari nilai tertinggi dalam list
      nilai_tinggi = max(tinggi)
      nilai_rendah = max(rendah)

      #deffuzzyfication
      y = ((10 + 20 + 30 + 40 + 50 + 60) * nilai_rendah + (70 + 80 + 90 + 100) * nilai_tinggi)/((6 * nilai_rendah) + (4 * nilai_tinggi))
      #menyimpan data dalam list
      fuzzy.append([supplier_id[i], y, kualitas[i], harga[i]])

  return fuzzy


def main():
  #mengurutkan nilai dari supplier berdasarkan nilai kelayakan dari terbesar ke terkecil
  fuzzy = fuzzi(supplier_id, kualitas, harga ,panjang_kolom)
  after_sorted = sorted(fuzzy, key=lambda x: x[1], reverse=True)
    
  print('-'*120)
  print("sorted supplier: ")
  print(after_sorted)
  #mengambil 5 terbesar dari dalam list
  data = {'best supplier': after_sorted[:5]}
      

  print('-'*120)
  #mengubah data menjadi dataframe
  result_csv = pd.DataFrame(data, columns = ['best supplier'])
  #menyimpan data dalam bentuk csv
  result_csv.to_csv('best_supplier.csv')
  print(data)

if __name__ == "__main__":
  main()