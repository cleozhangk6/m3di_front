from django.db import models

# Create your models here.

# class Pronameunique(models.Model):
#     id = models.IntegerField(primary_key=True)
#     uniprot_id = models.CharField(max_length=100, blank=True, null=True)
#     protein_name = models.CharField(max_length=100, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'ProNameUnique'


# class Sigpep(models.Model):
#     sp_uniprot_id = models.CharField(max_length=100, blank=True,primary_key=True)
#     signal_peptide = models.CharField(max_length=5, blank=True, null=True)
#     protein = models.ForeignKey(Pronameunique, models.DO_NOTHING, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'SigPep'


# class Basicbackup(models.Model):
#     id = models.IntegerField(primary_key=True)
#     uniprot_id = models.CharField(max_length=100, blank=True, null=True)
#     protein_link = models.CharField(max_length=300, blank=True, null=True)
#     protein_name = models.CharField(max_length=100, blank=True, null=True)
#     gene_name = models.CharField(max_length=150, blank=True, null=True)
#     gene_link = models.CharField(max_length=300, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'BasicBackup'

#     def __str__(self):
#         return f''


class Basicinfo2(models.Model):
    uniprot_id = models.CharField(max_length=10, blank=True, primary_key=True)
    protein_link = models.TextField(blank=True, null=True)
    protein_name = models.TextField(blank=True, null=True)
    gene_name = models.TextField(blank=True, null=True)
    gene_link = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'BasicInfo2'

class Signalpeptide(models.Model):
    sp_uniprot_id = models.CharField(max_length=100, blank=True, primary_key=True)
    signal_peptide = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'SignalPeptide'