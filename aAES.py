
def HexToInt(arg):
	switcher = {
		"0" : 0,
		"1" : 1,
		"2" : 2,
		"3" : 3,
		"4" : 4,
		"5" : 5,
		"6" : 6,
		"7" : 7,
		"8" : 8,
		"9" : 9,
		"a" : 10,
		"b" : 11,
		"c" : 12,
		"d" : 13,
		"e" : 14,
		"f" : 15
	}
	return switcher.get(arg)

def length(str):
	_length = 0
	for i in str:
		_length = _length + 1
	return _length

def printSquareMatrix(matrix):
	_len = length(matrix)
	for i in range(_len):
		for j in range(_len):
			print(matrix[i][j]),
		print("\n")


def printSquareHexMatrix(matrix):
	_len = length(matrix)
	for i in range(_len):
		for j in range(_len):
			print(hex(matrix[i][j])),
		print("\n")


def ToHexArray(arr):
	_len = length(arr)
	for i in range(_len):
		for j in range(_len):
			arr[i][j] = hex(arr[i][j])
	return arr
"""
  Rijndael Algoritmasi

  Anahtara gore farkli sayida dongusel islem yapilir. 
  Her donguden sonra anahtar yenilenerek veriye uygulanir.
  Bunun anlami tur sayisi kadar anahtar uretimi gerceklestirilmis 
  olur. Tur sayisi ise anahtar uzunluguna baglidir.
 
  Sifreleme ve desifreleme islemlerinde ayni anahtar kullanilir.
 
  Veri bayt dizileri seklinde ifade edilir. 
  128 bit uzunlugundaki veri, 4x4'luk matrislere bolunur. Bu 
  matrislere durum (state) matrisi denir. Matrisin her elemani
  8 bit (1 byte), her satir veya sutun 32 bittir. Her satira 
  kelime (word) denir.
 
  Anahtar da durum matrisine cevrilir.
 
  sifreleme baslangicinda sifresiz metnin durum matrisi ile 
  anahtarin durum matrisi toplanir.
 
  (dataBlock-wordLen-cycleNum)
  Veri Blogu	Kelime Uzunlugu 	Tur Sayisi
  AES-128			4					10
  AES-192			6					12
  AES-256			8					14
 
 
  Matris eleman sayisi n olsun:
  Anahtar uzunlugu 128 olsun. 0<n<16
  Anahtar uzunlugu 192 olsun. 0<n<24
  Anahtar uzunlugu 256 olsun. 0<n<32
 
  Bayt degerleri = {b7,b6,b5,b4,b3,b2,b1,b0}
 
  b7x^7 + b6x^6 + b5x^5 + b4x^4 + b3x^3 + b2x^2 + b1x + b0 = Toplam ((i=0 -> 7) bix^i)
 
  Onaltilik tabanda gosterilebilir. (10:A 11:B 12:C 13:D 14:E 15:F)
 
  Veri: 19 A0 9A E9 3D F4 C6 F8 E3 E2 8D 48 B3 2B 2A 08
  
  Durum Matrisi:	19 3D E3 B3
 					A0 F4 E2 2B
 					9A C6 8D 2A
 					E9 F8 48 08
"""

	#	_data: (string) 	hex value
	#	_len: (integer)		length of the hex val
	#	return: (hex[][])	state matrix
def createStateMatrix(_data,_len):
	stateMatrix = []
	for i in range(_len):
		val = int(_data[i*2:i*2+2],16)
		if i%WORD_LEN == 0:
			stateMatrix.append([val])
		else:
			stateMatrix[i//WORD_LEN].append(val)
	return stateMatrix

Data2 = "19A09AE93DF4C6F8E3E28D48B32B2A08"
len = 16

"""
  ALGORITMA:
 
  Dongu Yapisi
 	1- Bayt Degistirme (SubBytes)
  		- Tek dogrusal olmayan islem
  		- Ilk islem
  		- Degisiklik S-kutusuna bagli
  		- S-kutusu, durum matrisinin elemanlari onaltilik tabanda oldugu icin
  		  S-kutusu da 16x16 onaltilik tabanda bir matristir.
  		- Bu islem tum matrise uygulanir
 			Durum matrisi:		1. satir, 1. sutun degeri: 19
 			S-kutusu matrisi:	1. satir, 9. sutun degeri: D4
 			Durum matrisi:		1. satir, 1. sutun degeri: D4 
  
"""

	#	matrix: (hex[][])	matrix
	#	_len: (integer)		length of the matrix
	#	return: (hex[][])	state matrix - changed matrix
def subBytes(matrix, _len=4):
	for i in range(_len):
		for j in range(_len):
			str = matrix[i][j]
			r = 0
			c = 0
			if length(str) == WORD_LEN:
				r = HexToInt(str[2])
				c = HexToInt(str[3])
			else:
				c = HexToInt(str[2])

			index = r*16 + c
			matrix[i][j] = hex(Sbox[index])
	return matrix

"""
 	2- Satir Kaydirma (ShiftRows)
  		- Her satir, satir sayisinin 1 eksigi kadar elemani bastan cikarip
  		  sona ekler.

"""

	#	matrix: (hex [][]) 	matrix
	#	_len: (integer)		length of the matrix
	#	return: (hex[][])	state matrix - with shifted rows
def shiftRows(matrix, _len=4):
	for row in range(_len):
		for column in range(row):
			temp = matrix[row][0]
			del matrix[row][0]
			matrix[row].append(temp)
	return matrix


"""
 	3- Sutun Karistirma (MixColumns): Son dongude yok
 		- a(x) = {03}x^3 + {01}x^2 + {01}x + {02} 
  		- Islem her sutuna yapilir
  
"""

def multiplyHexMatricesForMC(a, b, _len=4):
	temp = [[0x0,0x0,0x0,0x0],[0x0,0x0,0x0,0x0],[0x0,0x0,0x0,0x0],[0x0,0x0,0x0,0x0]]
	for i in range(_len):
		for j in range(_len):
			sum = 0
			for k in range(_len):
				sum = sum + int(str(a[j][k]),16)*int(str(b[k][i]),16)
			temp[j][i] = hex(sum)
	return temp


	#	matrix: (hex[][]) 	state matrix
	#	_len: (integer) 	length of the matrix
	#	return: (hex[][])	state matrix - with mixed columns
	#	given matrix: a(x) = {03}x^3 + {01}x^2 + {01}x + {02}
def mixColumns(matrix, _len=4):

	givenMatrix= [	[0x02, 0x03, 0x01, 0x01],
					[0x01, 0x02, 0x03, 0x01],
					[0x01, 0x01, 0x02, 0x03],
					[0x03, 0x01, 0x01, 0x02] ]
	givenMatrix = ToHexArray(givenMatrix)
	returned = multiplyHexMatricesForMC(givenMatrix, matrix)

	return returned

"""
  	4- Tur Anahtarini Ekleme (AddRoundKey)
  		- Anahtar uretim blogunun urettigi anahtar ile veri toplanir.
  			Her bit icin (XOR) islemine denk gelir.
  
"""


	#	matrix: (hex[][]) 	state matrix
	#	roundKey: (hex[][]) round key matrix
	#	_len: (integer) 	length of the matrix
	#	return: (hex[][])	state matrix - with added the round key
def addRoundKey(matrix, roundKey, _len=4):
	for i in range(_len):
		for j in range(_len):
			matrix[i][j] = hex(int(str(matrix[i][j]),16) + int(str(roundKey[i][j]),16))
	return matrix



"""
  Anahtarlarin Uretilmesi (GenerateithKey)
  	- Uretim blogu, anahtar uzunlugunu bit dizilerinin uzunluguna gore matrislere 
 	  cevirir.
  	- Tur sayısı N; matris boyutu: 4xK. 
 	  Yapilacak islemlerle genislemis matrisin boyutu: 4x( K*(N+1) )


"""