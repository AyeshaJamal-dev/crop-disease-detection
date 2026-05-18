-- Seed data for Crop Disease Detection
-- Run after schema.sql
-- Note: Create admin user via app (Register as admin) or run: python -c "from database.db_connection import create_user; create_user('Admin','admin@cropdisease.com','admin123','admin')"

USE crop_disease_db;

-- Diseases knowledge base (PlantVillage classes: Tomato, Potato, Corn, Apple, Grape)
INSERT IGNORE INTO diseases (disease_name, crop_type, description, symptoms, causes, treatment, prevention, severity_level) VALUES
-- Tomato
('Tomato___Bacterial_spot', 'Tomato', 'Bacterial spot is a common tomato disease caused by Xanthomonas bacteria.', 'Small dark spots on leaves, stems, and fruits; spots may have yellow halos', 'Bacteria spread by rain, irrigation, or contaminated tools', 'Apply copper-based fungicide; remove infected plant parts', 'Use disease-free seeds; rotate crops; avoid overhead watering', 'high'),
('Tomato___Early_blight', 'Tomato', 'Early blight is caused by Alternaria solani fungus.', 'Brown spots with concentric rings on lower leaves; leaf yellowing', 'Warm, humid conditions; infected plant debris', 'Apply chlorothalonil or mancozeb fungicide', 'Remove infected debris; space plants for air circulation', 'medium'),
('Tomato___Late_blight', 'Tomato', 'Late blight is a devastating disease caused by Phytophthora infestans.', 'Dark water-soaked spots on leaves; white mold in humid conditions', 'Cool, wet weather; infected tubers or transplants', 'Apply copper fungicide or specific late blight products', 'Use resistant varieties; avoid overhead irrigation', 'high'),
('Tomato___Leaf_Mold', 'Tomato', 'Leaf mold is caused by Passalora fulva fungus.', 'Yellow patches on upper leaf surface; olive-green mold underneath', 'High humidity and moderate temperatures', 'Apply fungicide; improve ventilation in greenhouses', 'Reduce humidity; use resistant varieties', 'medium'),
('Tomato___Septoria_leaf_spot', 'Tomato', 'Septoria leaf spot is caused by Septoria lycopersici.', 'Small circular spots with gray centers and dark borders', 'Wet conditions; splashing water', 'Apply fungicide; remove infected leaves', 'Mulch to prevent soil splash; rotate crops', 'medium'),
('Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato', 'Two-spotted spider mite infestation.', 'Stippling on leaves; webbing; leaf bronzing', 'Hot, dry conditions; dust', 'Apply miticide or insecticidal soap', 'Increase humidity; avoid over-fertilizing', 'medium'),
('Tomato___Target_Spot', 'Tomato', 'Target spot caused by Corynespora cassiicola.', 'Brown spots with target-like rings', 'Warm, humid conditions', 'Apply fungicide; remove infected tissue', 'Improve air circulation; avoid overhead watering', 'medium'),
('Tomato___Tomato_mosaic_virus', 'Tomato', 'Viral disease affecting tomato plants.', 'Mottled yellow and green leaves; leaf distortion', 'Virus transmitted by contact or insects', 'No cure; remove infected plants', 'Use virus-free seeds; control aphids', 'high'),
('Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato', 'Viral disease transmitted by whiteflies.', 'Yellow curled leaves; stunted growth', 'Whitefly vectors', 'No cure; remove infected plants; control whiteflies', 'Use resistant varieties; insect netting', 'high'),
('Tomato___healthy', 'Tomato', 'Healthy tomato plant with no visible disease.', 'No symptoms', 'N/A', 'Continue good cultural practices', 'Maintain plant health; monitor regularly', 'low'),
-- Potato
('Potato___Early_blight', 'Potato', 'Early blight on potato caused by Alternaria solani.', 'Dark brown spots with concentric rings on leaves', 'Warm, humid weather; infected debris', 'Apply fungicide; remove infected foliage', 'Rotate crops; remove volunteer plants', 'medium'),
('Potato___Late_blight', 'Potato', 'Late blight on potato - same pathogen as tomato.', 'Dark lesions on leaves and stems; tuber rot', 'Cool, wet conditions', 'Apply fungicide preventively', 'Use certified seed; destroy cull piles', 'high'),
('Potato___healthy', 'Potato', 'Healthy potato plant.', 'No symptoms', 'N/A', 'Maintain good practices', 'Monitor for pests and diseases', 'low'),
-- Corn
('Corn___Cercospora_leaf_spot Gray_leaf_spot', 'Corn', 'Gray leaf spot of corn caused by Cercospora zeae-maydis.', 'Rectangular gray to tan lesions on leaves', 'Warm, humid conditions; corn residue', 'Apply fungicide if needed', 'Tillage to bury residue; resistant hybrids', 'medium'),
('Corn___Common_rust', 'Corn', 'Common rust of corn caused by Puccinia sorghi.', 'Small cinnamon-brown pustules on leaves', 'Moderate temperatures; moisture', 'Apply fungicide for high-value corn', 'Plant resistant hybrids', 'medium'),
('Corn___Northern_Leaf_Blight', 'Corn', 'Northern corn leaf blight caused by Setosphaeria turcica.', 'Long elliptical gray-green lesions', 'Cool, wet weather', 'Apply fungicide; use resistant hybrids', 'Crop rotation; residue management', 'medium'),
('Corn___healthy', 'Corn', 'Healthy corn plant.', 'No symptoms', 'N/A', 'Continue monitoring', 'Good cultural practices', 'low'),
-- Apple
('Apple___Apple_scab', 'Apple', 'Apple scab caused by Venturia inaequalis.', 'Olive-green spots on leaves and fruit', 'Wet spring weather', 'Apply fungicide (captan, sulfur)', 'Remove fallen leaves; plant resistant varieties', 'high'),
('Apple___Black_rot', 'Apple', 'Black rot of apple caused by Botryosphaeria obtusa.', 'Frogeye leaf spots; fruit rot', 'Wet conditions; infected mummies', 'Prune cankers; apply fungicide', 'Remove mummified fruit; prune dead wood', 'medium'),
('Apple___Cedar_apple_rust', 'Apple', 'Cedar-apple rust requires both apple and juniper.', 'Orange spots on leaves; fruit deformities', 'Alternate host (juniper) nearby', 'Apply fungicide in spring', 'Remove junipers nearby; resistant varieties', 'medium'),
('Apple___healthy', 'Apple', 'Healthy apple tree.', 'No symptoms', 'N/A', 'Continue routine care', 'Annual pruning; pest monitoring', 'low'),
-- Grape
('Grape___Black_rot', 'Grape', 'Black rot of grape caused by Guignardia bidwellii.', 'Brown spots on leaves; black shriveled berries', 'Warm, wet weather', 'Apply fungicide (captan, mancozeb)', 'Remove mummies; improve air flow', 'high'),
('Grape___Esca_(Black_Measles)', 'Grape', 'Esca or black measles - trunk disease.', 'Tiger-stripe leaf pattern; wood decay', 'Fungal infection in wood', 'Prune infected wood; no effective fungicide', 'Plant healthy vines; avoid wounding', 'high'),
('Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape', 'Grape leaf blight.', 'Brown spots on leaves', 'Fungal pathogen; humid conditions', 'Apply fungicide', 'Good canopy management', 'medium'),
('Grape___healthy', 'Grape', 'Healthy grapevine.', 'No symptoms', 'N/A', 'Routine vineyard care', 'Monitor for pests and diseases', 'low');
