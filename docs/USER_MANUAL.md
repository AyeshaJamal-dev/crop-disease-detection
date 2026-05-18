# User Manual - Crop Disease Detection System

## Getting Started

### Registration

1. Click **Register** on the homepage
2. Fill in your details (email and password are required)
3. Click **Register**
4. Log in with your credentials

### Login

1. Enter your email and password
2. Click **Login**
3. You will be redirected to your dashboard

## Farmer Features

### Dashboard

After logging in, you see:
- **Total Predictions**: Number of analyses you have run
- **Upload New Image**: Quick link to upload
- **View History**: Link to past predictions
- **Recent Predictions**: Table of your latest results

### Uploading an Image

1. Click **Upload** in the navigation or dashboard
2. **Drag and drop** a leaf image onto the upload zone, or **click** to browse
3. Supported formats: JPG, PNG (max 5MB)
4. Ensure the image is clear and shows the leaf clearly
5. Click **Analyze Image**
6. Wait for the result (usually under 3 seconds)

### Viewing Results

After analysis, you see:
- **Uploaded Image**: Your submitted photo
- **Prediction**: Disease name, confidence %, crop type, status (healthy/detected)
- **Treatment & Prevention**: Description, symptoms, causes, treatment, prevention
- **Rate this prediction**: Optional 1-5 star rating and feedback

### History

- Click **History** to view all your past predictions
- Click **View** on any row to see full details again

## Admin Features

Admin users see an **Admin** link in the navigation.

### Admin Dashboard

- Total users
- Total predictions
- Latest model accuracy
- Quick links to metrics, predictions, users, diseases

### Model Metrics

- Historical accuracy, precision, recall, F1 scores
- Confusion matrix (visual)
- Training curves

### Manage Predictions

- View all predictions from all users
- Paginated list
- Filter by page

### Manage Users

- List all registered users
- View user type (farmer/admin), location, join date

### Manage Diseases

- Add, edit, delete disease entries in the knowledge base
- Each disease has: name, crop type, description, symptoms, causes, treatment, prevention, severity

**Add Disease**: Fill in the form and click Save.
**Edit Disease**: Click Edit, modify fields, click Save.
**Delete Disease**: Click Delete and confirm.

## Tips for Best Results

1. **Image Quality**: Use clear, well-lit photos of leaves
2. **Crop Coverage**: The model recognizes Tomato, Potato, Corn, Apple, and Grape
3. **Single Leaf**: Focus on one leaf per image when possible
4. **Feedback**: Rate predictions to help improve the system

## Troubleshooting

**"Model not trained yet"**: Run `python models/train_model.py` after downloading the dataset.

**"Database connection failed"**: Ensure MySQL is running and credentials in config are correct.

**"Invalid file type"**: Use only JPG or PNG images.

**Slow prediction**: First prediction loads the model; subsequent ones are faster.
