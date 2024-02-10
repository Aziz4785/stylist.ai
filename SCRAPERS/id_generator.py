def convert_base_75(pos_decimal_number):
    base75_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_#-$%*:!?()[]"
    if pos_decimal_number == 0:
        return 'A'
    result = ""
    while pos_decimal_number > 0:
        remainder = pos_decimal_number % 75
        result = base75_chars[remainder] + result
        pos_decimal_number = pos_decimal_number // 75
    
    return result
    
def hash_link(url):
    if(len(url)>0):
        return hash(url)
    else:
        return None
    
def generate_ID(url):
    hash_value = hash_link(url)
    id = None
    if(hash_value is not None and hash_value>=0):
        id = convert_base_75(hash_value)
    else:
        if(hash_value is not None):
            hash_value = abs(hash_value)
            id = convert_base_75(hash_value)
            id = "&"+id
    return id

def add_id_to_document(product_data):
    if("url" in product_data):
        product_data["_id"] = generate_ID(product_data["url"])
    return product_data
        

print(generate_ID("https://www.zalando.fr/pier-one-pullover-mottled-dark-blue-pi922qa3p-k11.html"))
print(generate_ID(""))
print(generate_ID("a"))
print(generate_ID("https://www.zalando.fr/petrol-industries-pullover-antique-white-melee-p6822q09e-a11.html"))
print(generate_ID("https://www.zalando.fr/tezenis-mit-paspeltaschen-und-tunnelzug-pantalon-de-survetement-blu-assoluto-teg21a00a-k11.html"))
print(generate_ID("https://www.forever21.com/us/2001261094.html?dwvar_2001261094_color=01"))
print(generate_ID("https://github.com/Aziz4785/stylist.ai/commit/44ad382ff79de4ad938bf8625311783da6ef1a0f"))
print(generate_ID("https://www.zara.com/fr/en/100-wool-knit-top-p05755408.html?v1=313946793&v2=2351499"))
print(generate_ID("https://www.zara.com/fr/en/viscose-blend-knit-polo-shirt-p00304417.html?v1=311297439&v2=2351499"))
print(generate_ID("https://www.uniqlo.com/fr/fr/product/veste-style-sport-466732.html"))