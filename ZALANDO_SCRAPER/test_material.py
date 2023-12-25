import unittest
from metadata_generator import classify_materials  # Replace 'your_module' with the name of the module where your function is defined

class TestGarmentTypeClassification(unittest.TestCase):
    def test_classification(self):
        test_cases = [
            ("Composition: 95% cotton, 5% elastane, Sleeve composition: 95% cotton, 5% elastane, Material: Ribbed", {"natural", "synthetic"}),
            ("Composition: 51% cotton, 49% polyester, Material: Sweat", {"natural", "synthetic"}),
            ("Composition: 100% cotton, Material: Jersey, Care instructions: Do not tumble dry, machine wash at 30°C, do not bleach", {"natural"}),
            ("Composition: 96% polyester, 4% polyurethane, Lining: 100% polyester, Care instructions: Do not tumble dry, dry clean, do not wash, do not iron", {"synthetic"}),
            ("Composition: 95% cotton, 5% elastane, Material: Jersey, Care instructions: Do not tumble dry, machine wash at 30°C, wash delicate fabrics", {"natural", "synthetic"}),
            ("Composition: 100% cotton, Back composition: 100% cotton, Material: Denim", {"natural"}),
            ("Composition: 100% cotton, Material: Jersey, Care instructions: Do not tumble dry, wash delicate fabrics, machine wash at 30°C ", {"natural"}),
            ("Composition: 100% cotton, Material: Piqué, Care instructions: Machine wash at 40°C, do not tumble dry, wash delicate fabrics", {"natural"}),
            ("Composition: 60% cotton, 20% nylon, 20% viscose, Material: Knit / mesh, Care instructions: Machine wash at 40°C, do not tumble dry, wash on delicate fabrics", {"natural", "synthetic","artificial"}),
            ("Composition: 98% cotton, 2% elastane, Material: Canvas, Care instructions: Machine wash at 30°C", {"natural", "synthetic"}),
            ("Composition: 100% cotton, Material: Piqué, Care instructions: Machine wash at 40°C", {"natural"}),
            ("Composition: 90% polyester, 10% elastane", {"synthetic"}),
            ("Composition: 100% cotton, Material: Piqué, Care instructions: Machine wash at 40°C, do not tumble dry, wash delicate fabrics", {"natural"}),
            ("Composition: 60% cotton, 20% nylon, 20% viscose, Material: Knit / mesh, Care instructions: Machine wash at 40°C, do not tumble dry, wash on delicate fabrics", {"natural", "synthetic","artificial"}),
            ("Composition: 98% cotton, 2% elastane, Material: Canvas, Care instructions: Machine wash at 30°C", {"natural", "synthetic"}),
            ("Composition: 100% cotton, Material: Piqué, Care instructions: Machine wash at 40°C", {"natural"}),
            ("Composition: 90% polyester, 10% elastane", {"synthetic"}),
            ("Composition: 70% cotton, 30% polyester, Material: Sweatshirt, Care instructions: Machine wash at 30°C, do not iron", {"natural","synthetic"}),
            ("Upper / Upper: Leather and textile, Lining: Imitation leather / textile, Insole: Imitation leather, Outsole: Synthetic material, Lining thickness: Lining to protect against the cold, Care instructions: Apply a waterproofer before first use ", {"natural","synthetic"}),
            ("Upper / Upper: High-quality imitation leather, Lining: Textile, Insole: Textile, Outsole: Synthetic material, Lining thickness: Cold-protecting lining, Material: Synthetic leather", {"synthetic"}),
            ("Composition: 100% polyester, Back composition: 100% polyester, Lower part composition: 100% polyester, Yoke composition: 100% polyester, Lining: 100% polyester", {"synthetic"}),
            ("Composition: 100% polyester, Material: Jersey, Technologies: Dri-Fit (Nike), Care instructions: Do not tumble dry, machine wash at 30°C ", {"synthetic"}),
            ("Composition: 70% cotton, 30% polyester, Material: Sweatshirt, Care instructions: Machine wash at 30°C, do not iron", {"natural","synthetic"}),
            ("Upper / Upper: Leather and textile, Lining: Imitation leather / textile, Insole: Imitation leather, Outsole: Synthetic material, Lining thickness: Lining to protect against the cold, Care instructions: Apply a waterproofer before first use ", {"natural","synthetic"}),
            ("Upper / Upper: High-quality imitation leather, Lining: Textile, Insole: Textile, Outsole: Synthetic material, Lining thickness: Cold-protecting lining, Material: Synthetic leather", {"synthetic"}),
            ("Composition: 100% polyester, Back composition: 100% polyester, Lower part composition: 100% polyester, Yoke composition: 100% polyester, Lining: 100% polyester", {"synthetic"}),
            ("Composition: 100% polyester, Material: Jersey, Technologies: Dri-Fit (Nike), Care instructions: Do not tumble dry, machine wash at 30°C ", {"synthetic"}),
            ("Composition: 55% nylon, 45% polyester, Padding material: 100% polyester, Lining: 100% polyester " , {"synthetic"}),
            ("Composition: 37% wool, 34% polyester, 29% polyamide, Lining thickness: Unlined, Material: Knit / mesh, Contains non-textile elements of animal origin: No ", {"natural", "synthetic"}),
            ]

        for description, expected in test_cases:
            with self.subTest(description=description):
                print()
                print("-----------------------")
                print(description)
                print(":")
                result = classify_materials(description)
                #self.assertEqual(result, expected)
                print(result)
                self.assertTrue(result ==expected)

if __name__ == '__main__':
    unittest.main()
