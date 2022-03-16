# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Basicinfo2(models.Model):
    uniprot_id = models.CharField(max_length=10, blank=True, null=True)
    protein_link = models.TextField(blank=True, null=True)
    protein_name = models.TextField(blank=True, null=True)
    gene_name = models.TextField(blank=True, null=True)
    gene_link = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'BasicInfo2'


class Bindsite(models.Model):
    uniprot_id = models.CharField(max_length=10, blank=True, null=True)
    substrate = models.CharField(max_length=60, blank=True, null=True)
    bs_position = models.IntegerField(blank=True, null=True)
    eco = models.ForeignKey('Evicodes', models.DO_NOTHING, db_column='eco', blank=True, null=True)
    source = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'BindSite'


class Domainsrev(models.Model):
    uniprot_id = models.CharField(max_length=10, blank=True, null=True)
    protein_name = models.CharField(max_length=50, blank=True, null=True)
    domain_name = models.CharField(max_length=50, blank=True, null=True)
    dm_start = models.IntegerField(blank=True, null=True)
    dm_end = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'DomainsRev'


class Evicodes(models.Model):
    eco = models.CharField(primary_key=True, max_length=20)
    evidence_link = models.TextField(blank=True, null=True)
    label = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'EviCodes'


class Geneinfo(models.Model):
    uniprot_id = models.CharField(max_length=10, blank=True, null=True)
    gene_name = models.TextField(blank=True, null=True)
    gene_link = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'GeneInfo'


class Interactionsurfacefinal(models.Model):
    pdb = models.CharField(db_column='PDB', max_length=10, blank=True, null=True)  # Field name made lowercase.
    resolution = models.FloatField(blank=True, null=True)
    uniprot_p1 = models.CharField(max_length=10, blank=True, null=True)
    aa_p1 = models.CharField(max_length=1, blank=True, null=True)
    pos_p1 = models.IntegerField(blank=True, null=True)
    uniprot_p2 = models.CharField(max_length=10, blank=True, null=True)
    aa_p2 = models.CharField(max_length=1, blank=True, null=True)
    pos_p2 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'InteractionSurfaceFinal'


class Interactome3D(models.Model):
    id = models.IntegerField(primary_key=True)
    prot1 = models.CharField(max_length=10, blank=True, null=True)
    prot2 = models.CharField(max_length=10, blank=True, null=True)
    rank_maj = models.IntegerField(blank=True, null=True)
    rank_min = models.IntegerField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    pdb_id = models.CharField(db_column='PDB_id', max_length=10, blank=True, null=True)  # Field name made lowercase.
    bio_unit = models.CharField(max_length=5, blank=True, null=True)
    chain_1 = models.CharField(max_length=5, blank=True, null=True)
    model_1 = models.CharField(max_length=5, blank=True, null=True)
    seq_ident1 = models.IntegerField(blank=True, null=True)
    coverage1 = models.IntegerField(blank=True, null=True)
    seq_begin1 = models.IntegerField(blank=True, null=True)
    seq_end1 = models.IntegerField(blank=True, null=True)
    domain1 = models.IntegerField(blank=True, null=True)
    chain_2 = models.CharField(max_length=5, blank=True, null=True)
    model_2 = models.CharField(max_length=5, blank=True, null=True)
    seq_ident2 = models.IntegerField(blank=True, null=True)
    coverage2 = models.IntegerField(blank=True, null=True)
    seq_begin2 = models.IntegerField(blank=True, null=True)
    seq_end2 = models.IntegerField(blank=True, null=True)
    domain2 = models.IntegerField(blank=True, null=True)
    filename = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Interactome3d'


class Missense3DVar(models.Model):
    uniprot_id = models.CharField(max_length=10, blank=True, null=True)
    posuniprot = models.IntegerField(blank=True, null=True)
    pdbpos = models.IntegerField(blank=True, null=True)
    res_wt = models.CharField(max_length=4, blank=True, null=True)
    res_mut = models.CharField(max_length=4, blank=True, null=True)
    missensepred = models.CharField(max_length=50, blank=True, null=True)
    missense_reason = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Missense3D_Var'


class Missensevarcom(models.Model):
    uniprot_id = models.CharField(max_length=10, blank=True, null=True)
    posuniprot = models.IntegerField(blank=True, null=True)
    pdbpos = models.IntegerField(blank=True, null=True)
    res_wt = models.CharField(max_length=4, blank=True, null=True)
    res_mut = models.CharField(max_length=4, blank=True, null=True)
    missensepred = models.CharField(max_length=50, blank=True, null=True)
    missense_reason = models.CharField(max_length=100, blank=True, null=True)
    comment = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'MissenseVarCom'


class Ptms(models.Model):
    uniprot_id = models.CharField(max_length=100, blank=True, null=True)
    pos = models.IntegerField(blank=True, null=True)
    aa_one = models.CharField(max_length=1, blank=True, null=True)
    ptm_type = models.CharField(max_length=100, blank=True, null=True)
    eco = models.CharField(max_length=100, blank=True, null=True)
    source_link = models.CharField(max_length=300, blank=True, null=True)
    aa = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'PTMs'


class Pfam(models.Model):
    uniprot_id = models.CharField(max_length=10, blank=True, null=True)
    env_s = models.IntegerField(blank=True, null=True)
    env_e = models.IntegerField(blank=True, null=True)
    pfam_id = models.CharField(max_length=10, blank=True, null=True)
    pfam_name = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    bit = models.IntegerField(blank=True, null=True)
    e_value = models.CharField(max_length=30, blank=True, null=True)
    clan = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Pfam'


class Primtoalias(models.Model):
    primtoalias_id = models.AutoField(db_column='PrimToAlias_id', primary_key=True)  # Field name made lowercase.
    og_uniprot_id = models.CharField(max_length=10, blank=True, null=True)
    alias = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'PrimToAlias'


class Pronameunique(models.Model):
    uniprot_id = models.CharField(primary_key=True, max_length=10)
    protein_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ProNameUnique'


class Pronames(models.Model):
    uniprot_id = models.CharField(max_length=10, blank=True, null=True)
    protein_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ProNames'


class Proteinfunctionl(models.Model):
    uniprot_id = models.CharField(max_length=10, blank=True, null=True)
    function_link = models.TextField(blank=True, null=True)
    function_annotation = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ProteinFunctionl'


class Proteinlink(models.Model):
    id = models.IntegerField(primary_key=True)
    uniprot_id = models.CharField(max_length=100, blank=True, null=True)
    protein_link = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ProteinLink'


class Seqcanonical(models.Model):
    uniprot_id = models.CharField(max_length=10, blank=True, null=True)
    sequence = models.TextField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'SeqCanonical'


class Sequences(models.Model):
    uniprot_id = models.CharField(max_length=10, blank=True, null=True)
    isoform = models.TextField(blank=True, null=True)
    sequence = models.TextField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Sequences'


class Signalpeptide(models.Model):
    uniprot_id = models.CharField(primary_key=True, max_length=100)
    signal_peptide = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'SignalPeptide'


class Stringinteractions(models.Model):
    string_p1 = models.CharField(max_length=20, blank=True, null=True)
    string_p2 = models.CharField(max_length=20, blank=True, null=True)
    experimental = models.IntegerField(blank=True, null=True)
    data_base = models.IntegerField(blank=True, null=True)
    combined_score = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'StringInteractions'


class Stringtouniprot(models.Model):
    uniprot_id = models.CharField(max_length=10, blank=True, null=True)
    string_id = models.CharField(primary_key=True, max_length=25)

    class Meta:
        managed = False
        db_table = 'StringToUniprot'


class Topocellcomp(models.Model):
    uniprot_id = models.CharField(max_length=10, blank=True, null=True)
    topo_link = models.TextField(blank=True, null=True)
    topo_label = models.TextField(blank=True, null=True)
    cellcomp_link = models.TextField(blank=True, null=True)
    cellcomp_label = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'TopoCellComp'


class Topodom(models.Model):
    uniprot = models.ForeignKey(Pronameunique, models.DO_NOTHING, blank=True, null=True)
    topology = models.CharField(max_length=30, blank=True, null=True)
    topo_start = models.IntegerField(blank=True, null=True)
    topo_end = models.IntegerField(blank=True, null=True)
    eco = models.ForeignKey(Evicodes, models.DO_NOTHING, db_column='eco', blank=True, null=True)
    source = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'TopoDom'


class Transmem(models.Model):
    id = models.IntegerField(primary_key=True)
    uniprot_id = models.CharField(max_length=10, blank=True, null=True)
    tm_start = models.IntegerField(blank=True, null=True)
    tm_end = models.IntegerField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    eco = models.CharField(max_length=15, blank=True, null=True)
    source = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'TransMem'


class Variantlinks(models.Model):
    var = models.ForeignKey('Variants', models.DO_NOTHING, blank=True, null=True)
    var_link = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'VariantLinks'


class Variants(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    uniprot_id = models.CharField(max_length=100, blank=True, null=True)
    var_pos = models.IntegerField(blank=True, null=True)
    aa_original = models.CharField(max_length=2, blank=True, null=True)
    aa_substituion = models.CharField(max_length=2, blank=True, null=True)
    comment = models.CharField(max_length=500, blank=True, null=True)
    protein_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Variants'


class AaConversion(models.Model):
    aa_name = models.CharField(max_length=15, blank=True, null=True)
    one_let = models.CharField(max_length=1, blank=True, null=True)
    thr_let_up = models.CharField(max_length=3, blank=True, null=True)
    thr_let_low = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aa_conversion'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
