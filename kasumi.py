
# calculates the bits length
def bitlen(x):
  assert x>=0
  return len(bin(x))-2

def shift(x,s):
  assert bitlen(x)<=16
  return ((x<<s)&0xFFFF)|(x>>(16-s))

def mod(x):
  return ((x-1)%8)+1

# S-boxes
S7 = (
     54, 50, 62, 56, 22, 34, 94, 96, 38,  6, 63, 93, 2,  18,123, 33,
     55,113, 39,114, 21, 67, 65, 12, 47, 73, 46, 27, 25,111,124, 81,
     53,  9,121, 79, 52, 60, 58, 48,101,127, 40,120,104, 70, 71, 43,
     20,122, 72, 61, 23,109, 13,100, 77,  1, 16,  7, 82, 10,105, 98,
    117,116, 76, 11, 89,106,  0,125,118, 99, 86, 69, 30, 57,126, 87,
    112, 51, 17,  5, 95, 14, 90, 84, 91,  8, 35,103, 32, 97, 28, 66,
    102, 31, 26, 45, 75,  4, 85, 92, 37, 74, 80, 49, 68, 29,115, 44,
     64,107,108, 24,110, 83, 36, 78, 42, 19, 15, 41, 88,119, 59,  3,
)

S9 = (    
    167,239,161,379,391,334,  9,338, 38,226, 48,358,452,385, 90,397,
    183,253,147,331,415,340, 51,362,306,500,262, 82,216,159,356,177,
    175,241,489, 37,206, 17,  0,333, 44,254,378, 58,143,220, 81,400,
     95,  3,315,245, 54,235,218,405,472,264,172,494,371,290,399, 76,
    165,197,395,121,257,480,423,212,240, 28,462,176,406,507,288,223,
    501,407,249,265, 89,186,221,428,164, 74,440,196,458,421,350,163,
    232,158,134,354, 13,250,491,142,191, 69,193,425,152,227,366,135,
    344,300,276,242,437,320,113,278, 11,243, 87,317, 36, 93,496, 27,
    487,446,482, 41, 68,156,457,131,326,403,339, 20, 39,115,442,124,
    475,384,508, 53,112,170,479,151,126,169, 73,268,279,321,168,364,
    363,292, 46,499,393,327,324, 24,456,267,157,460,488,426,309,229,
    439,506,208,271,349,401,434,236, 16,209,359, 52, 56,120,199,277,
    465,416,252,287,246,  6, 83,305,420,345,153,502, 65, 61,244,282,
    173,222,418, 67,386,368,261,101,476,291,195,430, 49, 79,166,330,
    280,383,373,128,382,408,155,495,367,388,274,107,459,417, 62,454,
    132,225,203,316,234, 14,301, 91,503,286,424,211,347,307,140,374,
     35,103,125,427, 19,214,453,146,498,314,444,230,256,329,198,285,
     50,116, 78,410, 10,205,510,171,231, 45,139,467, 29, 86,505, 32,
     72, 26,342,150,313,490,431,238,411,325,149,473, 40,119,174,355,
    185,233,389, 71,448,273,372, 55,110,178,322, 12,469,392,369,190,
      1,109,375,137,181, 88, 75,308,260,484, 98,272,370,275,412,111,
    336,318,  4,504,492,259,304, 77,337,435, 21,357,303,332,483, 18,
     47, 85, 25,497,474,289,100,269,296,478,270,106, 31,104,433, 84,
    414,486,394, 96, 99,154,511,148,413,361,409,255,162,215,302,201,
    266,351,343,144,441,365,108,298,251, 34,182,509,138,210,335,133,
    311,352,328,141,396,346,123,319,450,281,429,228,443,481, 92,404,
    485,422,248,297, 23,213,130,466, 22,217,283, 70,294,360,419,127,
    312,377,  7,468,194,  2,117,295,463,258,224,447,247,187, 80,398,
    284,353,105,390,299,471,470,184, 57,200,348, 63,204,188, 33,451,
     97, 30,310,219, 94,160,129,493, 64,179,263,102,189,207,114,402,
    438,477,387,122,192, 42,381,  5,145,118,180,449,293,323,136,380,
     43, 66, 60,455,341,445,202,432,  8,237, 15,376,436,464, 59,461,
)

class Kasumi:
  def __init__(self):
    # subkeys
    self.key_KL1 = [None] * 9
    self.key_KL2 = [None] * 9
    self.key_KO1 = [None] * 9
    self.key_KO2 = [None] * 9
    self.key_KO3 = [None] * 9
    self.key_KI1 = [None] * 9
    self.key_KI2 = [None] * 9
    self.key_KI3 = [None] * 9

  def KeySchedule(self, m_key):
    assert bitlen(m_key) <= 128
    key =  [None]*9
    key_prime = [None]*9 #K'
    # given constant
    Cj = 0x0123456789ABCDEFFEDCBA9876543210
    m_key_prime = m_key ^ Cj
    #build the K'[] keys
    for i in range(1,9):
      key[i] = (m_key >> (16 * (8 - i))) & 0xFFFF
      key_prime[i] = (m_key_prime >> (16 * (8 - i))) & 0xFFFF
    #Construct the various round subkeys
    for i in range(1, 9):
      self.key_KL1[i] = shift(key[mod(i + 0)], 1)
      self.key_KL2[i] = key_prime[mod(i + 2)]
      self.key_KO1[i] = shift(key[mod(i + 1)], 5)
      self.key_KO2[i] = shift(key[mod(i + 5)], 8)
      self.key_KO3[i] = shift(key[mod(i + 6)], 13)
      self.key_KI1[i] = key_prime[mod(i + 4)]
      self.key_KI2[i] = key_prime[mod(i + 3)]
      self.key_KI3[i] = key_prime[mod(i + 7)]


  def FI(self, inp, rk):
    """
    * The sixteen bit input is split into two unequal halves
    * nine bits and seven bits - as is the subkey 
    """
    nine = inp>>7
    seven = inp&0b1111111
    # seven = inp&0x7F
    rk1 = rk >> 9
    rk2 = rk & 0b111111111

    l = seven
    # assert _bitlen(nine)  <= 9
    r = S9[nine] ^ seven

    nine  = r ^ rk2
    # assert _bitlen(l) <= 7
    seven = S7[l] ^ (r & 0b1111111) ^ rk1

    l = seven
    # assert _bitlen(nine)  <= 9
    r = S9[nine] ^ seven

    # assert _bitlen(l) <= 7
    nine  = S7[l] ^ (r & 0b1111111)
    seven = r

    # assert _bitlen(nine)  <= 7
    # assert _bitlen(seven) <= 9
    return (nine << 9) | seven
  def FO(self, inp, index):
    left  = inp >> 16
    right = inp & 0xFFFF

    out_left  = right 
    out_right = self.FI(left ^ self.key_KO1[index],self.key_KI1[index]) ^ right

    left   = out_right 
    right  = self.FI(out_left ^ self.key_KO2[index],self.key_KI2[index]) ^ out_right

    out_left  = right
    out_right = self.FI(left ^ self.key_KO3[index], self.key_KI3[index]) ^ right

    # assert _bitlen(out_left)  <= 16
    # assert _bitlen(out_right) <= 16
    return (out_left << 16) | out_right

  def FL(self, inp, index):
    # assert _bitlen(inp)  <= 32
    # assert index >= 1 and index <= 8

    in_left  = inp >> 16
    in_right = inp & 0xFFFF

    out_right = in_right ^ shift(in_left   & self.key_KL1[index], 1)
    out_left  = in_left  ^ shift(out_right | self.key_KL2[index], 1)

    # assert _bitlen(out_left)  <= 16
    # assert _bitlen(out_right) <= 16
    return (out_left << 16) | out_right

  def f(self, inp, index):
    # assert _bitlen(inp)  <= 32
    # assert index >= 1 and index <= 8

    if index % 2 == 1:
        state  = self.FL(inp, index)
        output = self.FO(state, index)
    else:
        state  = self.FO(inp, index)
        output = self.FL(state, index)

    # assert _bitlen(output) <= 32
    return output
  def enc_1r(self, in_left, in_right, index):
    # assert bitlen(in_left)  <= 32
    # assert bitlen(in_right) <= 32
    # assert index >= 1 and index <= 8

    out_right = in_left 
    out_left  = in_right ^ self.f(in_left, index)

    # assert bitlen(out_left)  <= 32
    # assert bitlen(out_right) <= 32
    return out_left, out_right


  def dec_1r(self, in_left, in_right, index):
    # assert bitlen(in_left)  <= 32
    # assert bitlen(in_right) <= 32
    # assert index >= 1 and index <= 8

    out_left  = in_right
    out_right = self.f(in_right, index) ^ in_left

    # assert bitlen(out_left)  <= 32
    # assert bitlen(out_right) <= 32
    return out_left, out_right


  def enc(self, plaintext):
    assert bitlen(plaintext) <= 64
    left  = plaintext >> 32
    right = plaintext & 0xFFFFFFFF
    for i in range(1, 9):
        left, right = self.enc_1r(left, right, i)
    return (left << 32) | right


  def dec(self, ciphertext):
    assert bitlen(ciphertext) <= 64
    left  = ciphertext >> 32
    right = ciphertext & 0xFFFFFFFF
    for i in range(8, 0, -1):
        left, right = self.dec_1r(left, right, i)
    return (left << 32) | right


