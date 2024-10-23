import csv
from collections import Counter
import random
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.http import JsonResponse
from django.shortcuts import render, redirect

from app1.utilis import GenerateImageFromSmile

from .models import Prediction
import numpy as np
import csv
import random
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
from django.shortcuts import redirect, render
from .models import Prediction  # Make sure to import your Prediction model



# Create your views here.

def prediction_list(request):
    predictions = Prediction.objects.all().order_by("-id")

    # Get query parameters from the request
    name = request.GET.get("name", "")
    class_field = request.GET.get("class_field", "")
    formula = request.GET.get("formula", "")
    order_by = request.GET.get("order_by", "")

    # Filter based on the provided parameters
    if name:
        predictions = predictions.filter(Name__icontains=name)
    if class_field:
        if class_field == 'nan':
            # Filtrar para obtener filas sin clase (asumiendo que `Class` es el campo que almacena la clase)
            predictions = predictions.filter(Class__isnull=True) | predictions.filter(Class='')
        else:
            # Filtrar por el class_field
            predictions = predictions.filter(Class__icontains=class_field)
    if formula:
        predictions = predictions.filter(Formula__icontains=formula)
    if order_by:
        predictions = predictions.order_by(order_by)

    # Pagination
    paginator = Paginator(predictions, 5)  # Show 5 predictions per page
    page_number = request.GET.get('page')
    
    try:
        predictions_page = paginator.page(page_number)
    except PageNotAnInteger:
        predictions_page = paginator.page(1)
    except EmptyPage:
        predictions_page = paginator.page(paginator.num_pages)

    prediction_data = [
        {
            "id": prediction.id,
            "SMILES": prediction.SMILES,
            "Name": prediction.Name,
            "Class": prediction.Class,
            "Formula": prediction.Formula,
            "Molecular_mass": (
                round(prediction.Molecular_mass, 2)
                if prediction.Molecular_mass is not None
                else None
            ),
            "CN_literature": prediction.CN_literature,
            "CN_predicted": round(prediction.CN_predicted, 2),
            "dnAB": prediction.dnAB,
            
            "dnCCDB": prediction.dnCCDB,
            "dnQC": prediction.dnQC,
            "g_CH3": prediction.g_CH3,
            "g_CH2_linear": prediction.g_CH2_linear,
            "g_OH": prediction.g_OH,
            "g_O_linear": prediction.g_O_linear,
            "g_O_ring": prediction.g_O_ring,
            "Ketone_linear": prediction.Ketone_linear,
            "Ketone_ring": prediction.Ketone_ring,
            "Aldehyde": prediction.Aldehyde,
            "Ester_linear": prediction.Ester_linear,
            "g_CH_linear": prediction.g_CH_linear,
            "g_CHdb_linear": prediction.g_CHdb_linear,
            "g_CHdb_ring": prediction.g_CHdb_ring,
            "g_CH2db_linear": prediction.g_CH2db_linear,
            "g_CH_ring": prediction.g_CH_ring,
            "g_CH2_ring": prediction.g_CH2_ring,
            
            "Carboxylic_acid": prediction.Carboxylic_acid,
            "Mod_Leiden": prediction.Mod_Leiden,
            "image": prediction.image,
        }
        for prediction in predictions_page
    ]

    classes = ['Aromatic', 'cyclo-alkane', 'Ester', 'Ether', 'Ester: saturated', 'Alcohol',
               'n-Alkane', 'Polyfunctional', 'Cyclic Ketone', 'Ester of Dicarboxylic Acids',
               'Cyclic Ether', 'Alkene', 'iso-alkane', 'Cyclic Alcohol',
               'Ester: Unsaturated', 'Carboxylic Acids', 'Ketone', 'Lactone', 'Aldehyde',
               'Naphtenes', 'Furans', 'nan']

    return render(
        request,
        "app1/prediction_list.html",
        {
            "predictions": prediction_data,
            "name": name,
            "class_field": class_field,
            "formula": formula,
            "order_by": order_by,
            "paginator": paginator,
            "page_obj": predictions_page,
            "classes":classes,
        },
    )

def upload_csv(request):
    if request.method == "POST":

        # Load your ML model once at the start of the module
        new_model = tf.keras.models.load_model("./cn_model.keras")
        scaler = StandardScaler()
        file = request.FILES["csv_file"]

        # Attempt to decode as UTF-8
        decoded_file = file.read().decode("utf-8").splitlines()
        reader = csv.reader(decoded_file)

        # Skip the header row
        next(reader)

        # Prepare a list to hold the input data for predictions
        input_data = []
        all_rows_data = []

        for index, row in enumerate(reader):  # Use enumerate to get the index
            # Extract the fields from the CSV based on the provided order

            (
                Name,
                Class,
                SMILES,
                CN_literature,
                dnAB,
                dnCCDB,
                dnQC,
                g_CH3,
                g_CH2_linear,
                g_OH,
                g_O_linear,
                g_O_ring,
                Ketone_linear,
                Ketone_ring,
                Aldehyde,
                Ester_linear,
                g_CH_linear,
                g_CHdb_linear,
                g_CHdb_ring,
                g_CH2db_linear,
                g_CH_ring,
                g_CH2_ring,
                Carboxylic_acid,
                Mod_Leiden,
            ) = row

            # Convert numerical fields to float, stripping whitespace and handling empty strings
            CN_literature = float(CN_literature.strip() or 0.0)
            dnAB = float(dnAB.strip() or 0.0)
            dnCCDB = float(dnCCDB.strip() or 0.0)
            dnQC = float(dnQC.strip() or 0.0)
            g_CH3 = float(g_CH3.strip() or 0.0)
            g_CH2_linear = float(g_CH2_linear.strip() or 0.0)
            g_OH = float(g_OH.strip() or 0.0)
            g_O_linear = float(g_O_linear.strip() or 0.0)
            g_O_ring = float(g_O_ring.strip() or 0.0)
            Ketone_linear = float(Ketone_linear.strip() or 0.0)
            Ketone_ring = float(Ketone_ring.strip() or 0.0)
            Aldehyde = float(Aldehyde.strip() or 0.0)
            Ester_linear = float(Ester_linear.strip() or 0.0)
            g_CH_linear = float(g_CH_linear.strip() or 0.0)
            g_CHdb_linear = float(g_CHdb_linear.strip() or 0.0)
            g_CHdb_ring = float(g_CHdb_ring.strip() or 0.0)
            g_CH2db_linear = float(g_CH2db_linear.strip() or 0.0)
            g_CH_ring = float(g_CH_ring.strip() or 0.0)
            g_CH2_ring = float(g_CH2_ring.strip() or 0.0)
            Carboxylic_acid = float(Carboxylic_acid.strip() or 0.0)
            Mod_Leiden = float(Mod_Leiden.strip() or 0.0)

            # Collect the input features for prediction
            input_data.append([
                dnAB,
                dnCCDB,
                dnQC,
                g_CH3,
                g_CH2_linear,
                g_OH,
                g_O_linear,
                g_O_ring,
                Ketone_linear,
                Ketone_ring,
                Aldehyde,
                Ester_linear,
                g_CH_linear,
                g_CHdb_linear,
                g_CHdb_ring,
                g_CH2db_linear,
                g_CH_ring,
                g_CH2_ring,
                Carboxylic_acid,
                Mod_Leiden,
            ])

            # Store all the row data for later use
            all_rows_data.append({
                "SMILES": SMILES,
                "Name": Name,
                "Class": Class,
                "CN_literature": CN_literature,
                "dnAB": dnAB,
                "dnCCDB": dnCCDB,
                "dnQC": dnQC,
                "g_CH3": g_CH3,
                "g_CH2_linear": g_CH2_linear,
                "g_OH": g_OH,
                "g_O_linear": g_O_linear,
                "g_O_ring": g_O_ring,
                "Ketone_linear": Ketone_linear,
                "Ketone_ring": Ketone_ring,
                "Aldehyde": Aldehyde,
                "Ester_linear": Ester_linear,
                "g_CH_linear": g_CH_linear,
                "g_CHdb_linear": g_CHdb_linear,
                "g_CHdb_ring": g_CHdb_ring,
                "g_CH2db_linear": g_CH2db_linear,
                "g_CH_ring": g_CH_ring,
                "g_CH2_ring": g_CH2_ring,
                "Mod_Leiden": Mod_Leiden,
                "Carboxylic_acid": Carboxylic_acid,
            })

            # Generate a unique image filename using the index
            image_filename = f"{SMILES.replace('/', '_')}_{index}.png"  # Replace '/' with '_' to avoid directory issues
            image_path = GenerateImageFromSmile(SMILES, image_filename)

        # Convert input data to DataFrame for scaling
        input_df = pd.DataFrame(input_data, columns=[
            'dnAB', 'dnCCDB', 'dnQC', 'g_CH3', 'g_CH2_linear', 'g_OH',
            'g_O_linear', 'g_O_ring', 'Ketone_linear', 'Ketone_ring',
            'Aldehyde', 'Ester_linear', 'g_CH_linear', 'g_CHdb_linear',
            'g_CHdb_ring', 'g_CH2db_linear', 'g_CH_ring', 'g_CH2_ring',
            'Carboxylic_acid', 'Mod_Leiden',
        ])

        # Check input_df shape to debug
        print("Input DataFrame shape:", input_df.shape)

        # Standardize the features for the model
        x_new_data = scaler.fit_transform(input_df)

        # Make predictions using the loaded model
        predicted_values = new_model.predict(x_new_data)

        # Save to database, matching predictions to original row data
        for index, predicted_value in enumerate(predicted_values):
            CN_predicted = predicted_value[0]  # Assuming single output

            # Use the corresponding row data for saving
            row_data = all_rows_data[index]

            Prediction.objects.create(
                SMILES=row_data["SMILES"],
                Name=row_data["Name"],
                Class=row_data["Class"],
                CN_literature=row_data["CN_literature"],
                dnAB=row_data["dnAB"],
                dnCCDB=row_data["dnCCDB"],
                dnQC=row_data["dnQC"],
                g_CH3=row_data["g_CH3"],
                g_CH2_linear=row_data["g_CH2_linear"],
                g_OH=row_data["g_OH"],
                g_O_linear=row_data["g_O_linear"],
                g_O_ring=row_data["g_O_ring"],
                Ketone_linear=row_data["Ketone_linear"],
                Ketone_ring=row_data["Ketone_ring"],
                Aldehyde=row_data["Aldehyde"],
                Ester_linear=row_data["Ester_linear"],
                g_CH_linear=row_data["g_CH_linear"],
                g_CHdb_linear=row_data["g_CHdb_linear"],
                g_CHdb_ring=row_data["g_CHdb_ring"],
                g_CH2db_linear=row_data["g_CH2db_linear"],
                g_CH_ring=row_data["g_CH_ring"],
                g_CH2_ring=row_data["g_CH2_ring"],
                Mod_Leiden=row_data["Mod_Leiden"],
                Carboxylic_acid=row_data["Carboxylic_acid"],
                CN_predicted=CN_predicted,  # New predicted field
                image=image_path,  # Store the filename
            )

        return redirect("prediction_list")

    return render(request, "app1/upload.html")


def plot_data(request):

    return render(request, "app1/plot.html")


def get_chart_data(request, plot_type):
    predictions = Prediction.objects.all()

    if plot_type == "predVsExp":
        CN_literature = [pred.CN_literature for pred in predictions]
        CN_predicted = [pred.CN_predicted for pred in predictions]

        return JsonResponse(
            {
                "CN_literature": CN_literature,
                "CN_predicted": CN_predicted,
            }
        )
    elif plot_type == "ceteneDis":
        cetene_values = [
            pred.CN_literature for pred in predictions
        ]  # Use the correct attribute

        # Define the bins for frequency ranges (0 to 100)
        bins = np.arange(0, 101, 10)  # 0-10, 10-20, ..., 90-100
        frequencies, edges = np.histogram(cetene_values, bins=bins)

        print("edges", edges)
        print(
            "cenete_bins",
            [(int(edges[i]), int(edges[i + 1])) for i in range(len(edges) - 1)],
        )

        return JsonResponse(
            {
                "cetene_bins": [
                    (int(edges[i]), int(edges[i + 1])) for i in range(len(edges) - 1)
                ],  # Convert to int
                "frequencies": frequencies.tolist(),  # Convert frequencies to a list
            }
        )
