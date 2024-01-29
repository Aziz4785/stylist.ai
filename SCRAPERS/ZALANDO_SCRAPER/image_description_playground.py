from image_description import *

#this item below is copy pasted from data_mode-femme.json
item = {
        "url": "https://www.zalando.fr/puma-rebound-v6-baskets-basses-white-future-pink-black-pu115o0nm-a15.html",
        "brand": "Puma",
        "name": "REBOUND - Baskets basses",
        "composition and care (fr)": "Dessus / Tige: Imitation cuir haute-qualité, Doublure: Textile, Semelle de propreté: Textile, Semelle d'usure: Matière synthétique, Épaisseur de la doublure: Doublure protégeant du froid, Matière: Cuir synthétique",
        "composition and care (en)": "Upper / Upper: High-quality imitation leather, Lining: Textile, Insole: Textile, Outsole: Synthetic material, Lining thickness: Cold-protecting lining, Material: Synthetic leather",
        "more details (fr)": "Bout de la chaussure: Rond, Forme du talon: Plateforme, Fermeture: Laçage, Référence: PU115O0NM-A15",
        "more details (en)": "Shoe toe: Round, Heel shape: Platform, Closure: Lacing, ",
        "images": [
            "https://img01.ztat.net/article/spp-media-p1/4cdefe67f6f44838951b9d282091f68e/e1477bebb1ec45da9210affa516edc8b.jpg?imwidth=156",
            "https://img01.ztat.net/article/spp-media-p1/b7655d72d3ca459f80b38ef6b454b5fc/902019a19f80464ab15b4ddecbddeeac.jpg?imwidth=156",
            "https://img01.ztat.net/article/spp-media-p1/50307f6b0256408aa8c9d2931cd50e4f/6c49691d48e24b44999f5a3e7573237b.jpg?imwidth=156&filter=packshot",
            "https://img01.ztat.net/article/spp-media-p1/4b5a9f378c2945d0afce0923b3b2d9fc/ab00831aa09a43f996fb063466390abe.jpg?imwidth=156",
            "https://img01.ztat.net/article/spp-media-p1/3917eff3ca9146ffae12f0bdb42eaeb0/bfbec8eda6da4666aae50aa18f35a31b.jpg?imwidth=156",
            "https://img01.ztat.net/article/spp-media-p1/bf1d9b9a516b42b69eac588f1e37ae0c/f1e3ecd0d6244c2c907e61fa74cbd927.jpg?imwidth=156",
            "https://img01.ztat.net/article/spp-media-p1/47adc6f487b34fc38af27ded727296a0/be6a102dd601487a8282e0f8dfa51017.jpg?imwidth=156"
        ],
        "id": "#I00005c"
    }

baseline_elem = generate_baseline_single_elem(item)
print(baseline_elem)