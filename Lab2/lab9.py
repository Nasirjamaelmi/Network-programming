import math
import random
import zlib

txt = ""

with open('Lab2\\exempeltext.txt', 'r') as f:
    txt = f.read()
    
def makeHisto(byteArr):
    histo = [0] * 256
    for byte in  byteArr:
        histo[byte] += 1
    return histo
    
        

def makeProb(histo):
    total_count = sum(histo)

    prob_distribution = [count / total_count for count in histo]
    
    return prob_distribution

byteArr = bytearray(txt,"utf-8")  
my_bytes = txt.encode('utf-8')
size_of_bytes = len(my_bytes)
print(f"the lengt of the txt {len(txt)}") #29091 symbols
print(f"Number of bytes in the byte-array: {size_of_bytes}") #30491 number of bytes in the bytearray

histo = makeHisto(byteArr)
print(makeProb(histo))


def entropy(prob):  #entrpy is used to get the chanche of an event when it should happen
    epsilon = 1e-10

    prob = [max(p,epsilon) for p in prob]

    entropi_value = -sum(p * math.log2(p) for p in prob)
    return entropi_value

# Calculate probability distribution and en tropy
histo = makeHisto(byteArr)
prob_distribution = makeProb(histo)
result_entropy = entropy(prob_distribution)

# Estimate minimum bits needed
min_bits_needed = result_entropy * len(byteArr)

print(f"Entropy: {result_entropy}")
print(f"Minimum bits needed: {min_bits_needed}")

copytext = txt
text_list = list(copytext)
random.shuffle(text_list)
shuffled_text = ''.join(text_list) #have to have list to shuffle and this to get it in a string format

# (b) Copy the byteArr and shuffle it
byteArr_copy = byteArr.copy()  # Create a copy to avoid modifying the original
random.shuffle(byteArr_copy)

# (c) Verify that byteArr is not erroneously shuffled
# Note: You should compare byteArr with its original state before shuffling
is_byteArr_shuffled = (byteArr != byteArr_copy)

# Display the results
copy_bytes = shuffled_text.encode('utf-8')
size_of_copy = len(copy_bytes)


print(f"Is byteArr shuffled? {is_byteArr_shuffled}")
print(f"Number of bytes in the shuffled byte-array: {size_of_copy}")

code =  zlib.compress(byteArr_copy)

size_of_code_in_bytes = len(code)

size_of_code_in_bits = size_of_code_in_bytes * 8    

number_of_symbol = len(set(code))

bits_per_symbol = size_of_code_in_bytes / number_of_symbol


print(f"Size of the Zip Code in bytes: {size_of_code_in_bytes}")
print(f"Size of the Zip Code in bits: {size_of_code_in_bits}")
print(f"Number of source symbols in the compressed data: {number_of_symbol}")
print(f"Bits per symbol in the compressed data (compression ratio): {bits_per_symbol}")


code2 =  zlib.compress(byteArr)

size_of_code_in_bytes2 = len(code)

size_of_code_in_bits2 = size_of_code_in_bytes2 * 8    

number_of_symbol2 = len(set(code))

bits_per_symbol2 = size_of_code_in_bytes2 / number_of_symbol2


print(f"Size of the Zip Code in bytes unshuffled: {size_of_code_in_bytes2}")
print(f"Size of the Zip Code in bits unshuffled: {size_of_code_in_bits2}")
print(f"Number of source symbols in the compressed data unshuffled: {number_of_symbol2}")
print(f"Bits per symbol in the compressed data (compression ratio) unshuffled: {bits_per_symbol2}")


