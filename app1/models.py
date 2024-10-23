from django.db import models


class Prediction(models.Model):

    SMILES = models.CharField(max_length=255, null=True, blank=True)
    Name = models.CharField(max_length=255, null=True, blank=True)
    Class = models.CharField(max_length=255, null=True, blank=True)
    Formula = models.CharField(max_length=255, null=True, blank=True)
    Molecular_mass = models.FloatField(
        null=True, blank=True, verbose_name="Molecular mass (g/mol)"
    )


    CN_literature = models.FloatField(null=True, blank=True)
    CN_predicted = models.FloatField(null=True, blank=True)


    dnAB = models.FloatField(null=True, blank=True)
    # C_C = models.FloatField(null=True, blank=True, verbose_name="C=C")
    # c = models.FloatField(null=True, blank=True)
    dnCCDB = models.FloatField(null=True, blank=True)
    dnQC = models.FloatField(null=True, blank=True)
    g_CH3 = models.FloatField(null=True, blank=True)
    g_CH2_linear = models.FloatField(null=True, blank=True)
    g_OH = models.FloatField(null=True, blank=True)
    g_O_linear = models.FloatField(null=True, blank=True)
    g_O_ring = models.FloatField(null=True, blank=True)
    Ketone_linear = models.FloatField(null=True, blank=True)
    Ketone_ring = models.FloatField(null=True, blank=True)
    Aldehyde = models.FloatField(null=True, blank=True)
    Ester_linear = models.FloatField(null=True, blank=True)
    g_CH_linear = models.FloatField(null=True, blank=True)
    g_CHdb_linear = models.FloatField(
        null=True, blank=True, verbose_name="g_CHdb_linear"
    )
    g_CHdb_ring = models.FloatField(null=True, blank=True)
    g_CH2db_linear = models.FloatField(null=True, blank=True)
    g_CH_ring = models.FloatField(null=True, blank=True)
    g_CH2_ring = models.FloatField(null=True, blank=True)
    # dnOHprim = models.FloatField(null=True, blank=True)
    # dnOHsec = models.FloatField(null=True, blank=True)
    # dnOHter = models.FloatField(null=True, blank=True)
    # phenol = models.FloatField(null=True, blank=True)
    Carboxylic_acid = models.FloatField(null=True, blank=True)
    Mod_Leiden = models.FloatField(null=True, blank=True)

    CN_predicted = models.FloatField(null=True, blank=True)
    image = models.ImageField(upload_to="molecules", null=True, blank=True)

    def __str__(self):
        return f"{self.SMILES}, {self.Name}, {self.Class}, {self.Formula}"


# dnAB	dnCCDB	dnQC	g_CH3	g_CH2_linear	g_OH	g_O_linear	g_O_ring	Ketone_linear	Ketone_ring	Aldehyde	Ester_linear	g_CH_linear	g_CHdb_linear	g_CHdb_ring	g_CH2db_linear	g_CH_ring	g_CH2_ring	Carboxylic_acid	Mod_Leiden