from image_description import *

#this item below is copy pasted from data_mode-femme.json
item = {
    "url": "https://www.zalando.fr/pullandbear-mom-jean-droit-mottled-black-puc21n0j6-q11.html",
    "brand": "PULL&BEAR",
    "name": "MOM - Jeans fuselé",
    "composition and care (fr)": "Composition: 100% coton, Matière: Denim",
    "composition and care (en)": "Composition: 100% cotton, Material: Denim",
    "more details (fr)": "Taille: Haute, Fermeture: Braguette avec fermeture éclair, Motif / Couleur: Couleur unie, Référence: PUC21N0J6-Q11",
    "more details (en)": "Waist: High, Closure: Zip fly, Pattern / Color: Solid color, Reference: PUC21N0J6-Q11",
    "images": [
        "https://img01.ztat.net/article/spp-media-p1/093b2811e69f4b319a2a9ef45e6886a8/d44c2df7b15f457bb6fad26686153f58.jpg?imwidth=156",
        "https://img01.ztat.net/article/spp-media-p1/7a352848e62c4c25b8fed4f4a2a24c15/af90edd0de574a42aaa1819f5e8fe5c0.jpg?imwidth=156",
        "https://img01.ztat.net/article/spp-media-p1/728cfb021faa4320b79a27e6f4e446a3/6e21b9bd3d28419a849f0266dc20723b.jpg?imwidth=156",
        "https://img01.ztat.net/article/spp-media-p1/b733b57da95d4a5bb6c69821675195ac/08083d4964b24a389e08f910361a16a6.jpg?imwidth=156",
        "https://img01.ztat.net/article/spp-media-p1/650c0544134041b9852a04c6b45a3e43/c42ee5e812294344930a5c807a8b96fe.jpg?imwidth=156",
        "https://img01.ztat.net/article/spp-media-p1/a930c5bf58b64c579918ff67e36bdfc6/3b51799dd4f545d39554d7d2655ba9f7.jpg?imwidth=156&filter=packshot",
        "https://img01.ztat.net/article/spp-media-p1/1f57623102ca4c619b03e5f6f540d9fb/dfd90c96da7c49059cc77173c3b782ad.jpg?imwidth=156"
    ]
}

baseline_elem = generate_baseline_single_elem(item)
print(baseline_elem)