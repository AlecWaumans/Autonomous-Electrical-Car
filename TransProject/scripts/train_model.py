import os
import numpy as np
import tensorflow as tf
from keras.src.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from keras.src.utils import to_categorical
from tensorflow.keras import regularizers
import cv2
from sklearn.model_selection import train_test_split
from keras._tf_keras.keras.preprocessing.image import ImageDataGenerator

# Paths
data_dir = '../dataset'  # Chemin vers les données
model_path = '../models/traffic_sign_model.h5'  # Chemin pour sauvegarder le modèle

# Hyperparamètres
IMG_HEIGHT, IMG_WIDTH = 64, 64  # Taille des images
BATCH_SIZE = 32
EPOCHS = 400

# Définir les classes et leurs indices
label_names = ['class_0', 'class_1', 'class_2', 'class_3']  # Remplir avec vos classes
label_to_index = {label: idx for idx, label in enumerate(label_names)}
index_to_label = {idx: label for label, idx in label_to_index.items()}  # Pour convertir l'indice en nom de classe

# Fonction pour charger les données (train/validation)
def load_data(data_dir, subset):
    images, labels, image_names = [], [], []

    valid_extensions = ('.jpg', '.jpeg', '.png')

    for label in label_names:
        label_folder = os.path.join(data_dir, subset, label)

        if not os.path.exists(label_folder):
            print(f"Attention: le dossier {label_folder} n'existe pas.")
            continue

        for img_file in os.listdir(label_folder):
            if not img_file.lower().endswith(valid_extensions):
                print(f"Fichier ignoré (extension non valide) : {img_file}")
                continue

            img_path = os.path.join(label_folder, img_file)
            img = cv2.imread(img_path)
            if img is None:
                print(f"Erreur: impossible de lire l'image {img_path}. Ignorée.")
                continue

            try:
                img = cv2.resize(img, (IMG_HEIGHT, IMG_WIDTH))
            except Exception as e:
                print(f"Erreur lors du redimensionnement de l'image {img_path}: {e}")
                continue

            images.append(img)
            labels.append(label_to_index[label])  # Index de la classe
            image_names.append(img_file)  # Nom de l'image

    if len(images) == 0:
        raise ValueError(f"Aucune image valide n'a été chargée dans le dossier {subset}. Vérifiez vos données.")

    images = np.array(images, dtype='float32') / 255.0  # Normaliser
    labels = to_categorical(labels, num_classes=len(label_names))  # Encodage des étiquettes
    return images, labels, image_names

# Fonction pour charger les données de test
def load_test_data(test_dir):
    images, image_names = [], []

    valid_extensions = ('.jpg', '.jpeg', '.png')

    for img_file in os.listdir(test_dir):
        if not img_file.lower().endswith(valid_extensions):
            print(f"Fichier ignoré (extension non valide) : {img_file}")
            continue

        img_path = os.path.join(test_dir, img_file)
        img = cv2.imread(img_path)
        if img is None:
            print(f"Erreur: impossible de lire l'image {img_path}. Ignorée.")
            continue

        try:
            img = cv2.resize(img, (IMG_HEIGHT, IMG_WIDTH))
        except Exception as e:
            print(f"Erreur lors du redimensionnement de l'image {img_path}: {e}")
            continue

        images.append(img)
        image_names.append(img_file)  # Nom de l'image

    if len(images) == 0:
        raise ValueError("Aucune image valide n'a été chargée dans le dossier de test. Vérifiez vos données.")

    images = np.array(images, dtype='float32') / 255.0  # Normaliser
    return images, image_names

# Créer un modèle CNN pour la classification des panneaux
def create_model():
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_HEIGHT, IMG_WIDTH, 3),
               kernel_regularizer=regularizers.l2(0.01)),
        MaxPooling2D(pool_size=(2, 2)),
        BatchNormalization(),

        Conv2D(64, (3, 3), activation='relu', kernel_regularizer=regularizers.l2(0.01)),
        MaxPooling2D(pool_size=(2, 2)),
        BatchNormalization(),

        Conv2D(128, (3, 3), activation='relu', kernel_regularizer=regularizers.l2(0.01)),
        MaxPooling2D(pool_size=(2, 2)),
        BatchNormalization(),

        Conv2D(256, (3, 3), activation='relu', kernel_regularizer=regularizers.l2(0.01)),
        MaxPooling2D(pool_size=(2, 2)),
        BatchNormalization(),

        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(len(label_names), activation='softmax')
    ])

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

if __name__ == "__main__":
    # Charger les données d'entraînement
    print("\nChargement des données d'entraînement...")
    X, y, image_names = load_data(data_dir, 'train')
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Données chargées: {X_train.shape[0]} train, {X_val.shape[0]} validation")

    # Charger les données de test
    print("\nChargement des données de test...")
    test_dir = os.path.join(data_dir, 'test')
    X_test, test_image_names = load_test_data(test_dir)
    print(f"Données de test chargées: {X_test.shape[0]} images")

    # Créer l'augmentation de données avec des transformations conditionnelles
    def conditional_augmentation(X, y):
        """
        Appliquer les transformations d'augmentation en fonction de la classe (sans flip horizontal pour certaines classes).
        """
        datagen = ImageDataGenerator(
            rotation_range=10,  # Rotation aléatoire de -10° à 10°
            width_shift_range=0.1,  # Décalage horizontal
            height_shift_range=0.1,  # Décalage vertical
            zoom_range=0.1,  # Zoom aléatoire
            shear_range=0.2,  # Cisaillement aléatoire
        )

        augmented_images = []
        augmented_labels = []

        for i in range(len(X)):
            img = X[i]
            label = y[i]
            if label_to_index['class_1'] in label or label_to_index['class_2'] in label:
                # Pas de flip horizontal pour 'right' et 'left'
                datagen_no_flip = ImageDataGenerator(
                    rotation_range=10,
                    width_shift_range=0.1,
                    height_shift_range=0.1,
                    zoom_range=0.1,
                    shear_range=0.2
                )
                img = datagen_no_flip.random_transform(img)
            else:
                img = datagen.random_transform(img)

            augmented_images.append(img)
            augmented_labels.append(label)

        return np.array(augmented_images), np.array(augmented_labels)

    X_train, y_train = conditional_augmentation(X_train, y_train)

    # Entraînement du modèle
    tf.keras.utils.set_random_seed(42)
    model = create_model()
    print(model.summary())

    print("\nEntraînement du modèle avec augmentation des données...")
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        verbose=1
    )

    # Sauvegarder le modèle
    print("\nSauvegarde du modèle...")
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    model.save(model_path)
    print(f"Modèle sauvegardé sous {model_path}")

    # Évaluation sur l'ensemble de validation
    print("\nÉvaluation sur l'ensemble de validation...")
    val_loss, val_acc = model.evaluate(X_val, y_val, verbose=1)
    print(f"Précision de validation: {val_acc * 100:.2f}%")

    # Prédictions sur l'ensemble de test
    print("\nPrédictions sur l'ensemble de test...")
    test_predictions = model.predict(X_test)
    test_predicted_classes = np.argmax(test_predictions, axis=1)

    # Afficher les prédictions sur les images de test
    for image_name, pred_class in zip(test_image_names, test_predicted_classes):
        print(f"Image: {image_name} -> Classe prédite: {index_to_label[pred_class]}")
