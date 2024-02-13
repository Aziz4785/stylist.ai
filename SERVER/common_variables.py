#when the user search for "Tops", we will also include garments from corresponding_categories["Tops"]
corresponding_categories = {"Tops" : set(["Tops","Outerwear","Other","unknown"]),
    "Bottoms": set(["Bottoms","Other","unknown"]),
    "Outerwear": set(["Outerwear","Tops","Bottoms","Other","unknown"]),
    "Underwear": set(["Underwear","Bottoms","One-Pieces","Other","unknown"]),
    "Footwear": set(["Footwear","Other","unknown"]),
    "Accessories": set(["Accessories","Other","unknown"]),
    "One-Pieces": set(["One-Pieces","Outerwear","Other","unknown"]),
    "Other": set(["Tops","Outerwear","Accessories","One-Pieces","Underwear","Footwear","Bottoms","Other","unknown"]),
    "unknown": set(["Tops","Outerwear","Accessories","One-Pieces","Underwear","Footwear","Bottoms","Other","unknown"])}
    