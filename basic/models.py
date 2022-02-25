# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Basicinfo2(models.Model):
    uniprot_id = models.CharField(max_length=10, blank=True, primary_key= True)
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


class Domainnameunique(models.Model):
    dm_id = models.AutoField(primary_key=True)
    domain_name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'DomainNameUnique'


class Domains2(models.Model):
    uniprot_id = models.CharField(max_length=10, blank=True, null=True)
    protein_name = models.TextField(blank=True, null=True)
    domain_name = models.TextField(blank=True, null=True)
    dom_start = models.IntegerField(blank=True, null=True)
    dom_end = models.IntegerField(blank=True, null=True)
    eco = models.CharField(max_length=20, blank=True, null=True)
    source = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Domains2'


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


class Genelink(models.Model):
    gene_name = models.TextField(blank=True, null=True)
    gene_link = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'GeneLink'


class Genename(models.Model):
    g_uniprot = models.ForeignKey('Pronameunique', models.DO_NOTHING, blank=True, null=True)
    gene_name = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'GeneName'





class Missense3DVar(models.Model):
    uniprot = models.CharField(max_length=10, blank=True, null=True)
    posuniprot = models.IntegerField(blank=True, null=True)
    pdbpos = models.IntegerField(blank=True, null=True)
    res_wt = models.CharField(max_length=4, blank=True, null=True)
    res_mut = models.CharField(max_length=4, blank=True, null=True)
    missensepred = models.CharField(max_length=50, blank=True, null=True)
    missense_reason = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Missense3D_Var'


class MissenseVarCom(models.Model):
    uniprot = models.CharField(max_length=10, blank=True, null=True)
    posuniprot = models.IntegerField(blank=True, null=True)
    pdbpos = models.IntegerField(blank=True, null=True)
    res_wt = models.CharField(max_length=4, blank=True, null=True)
    res_mut = models.CharField(max_length=4, blank=True, null=True)
    missensepred = models.CharField(max_length=50, blank=True, null=True)
    missense_reason = models.CharField(max_length=100, blank=True, null=True)
    comment = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Missense_Var_Com'

class MissenseVarComCopy(models.Model):
    uniprot = models.CharField(max_length=10, blank=True, null=True)
    posuniprot = models.IntegerField(blank=True, null=True)
    pdbpos = models.IntegerField(blank=True, null=True)
    res_wt = models.CharField(max_length=4, blank=True, null=True)
    res_mut = models.CharField(max_length=4, blank=True, null=True)
    missensepred = models.CharField(max_length=50, blank=True, null=True)
    missense_reason = models.CharField(max_length=100, blank=True, null=True)
    comment = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Missense_Var_Com_Copy'


class Ptms(models.Model):
    ptm_uniprot_id = models.CharField(max_length=100, blank=True, null=True)
    pos = models.IntegerField(blank=True, null=True)
    aa_one = models.CharField(max_length=1, blank=True, null=True)
    ptm_type = models.CharField(max_length=100, blank=True, null=True)
    eco = models.CharField(max_length=100, blank=True, null=True)
    source_link = models.CharField(max_length=300, blank=True, null=True)
    aa = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'PTMs'


class Ptmsdemo(models.Model):
    ptm_uniprot_id = models.CharField(max_length=100, blank=True, null=True)
    isoform = models.CharField(max_length=100, blank=True, null=True)
    pos = models.IntegerField(blank=True, null=True)
    aa = models.CharField(max_length=1, blank=True, null=True)
    ptm_type = models.CharField(max_length=100, blank=True, null=True)
    evidence_code = models.CharField(max_length=100, blank=True, null=True)
    source_link = models.CharField(max_length=300, blank=True, null=True)
    ptm_id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'PTMsDemo'


class PtmsOld(models.Model):
    ptm_uniprot_id = models.CharField(max_length=100, blank=True, null=True)
    pos = models.IntegerField(blank=True, null=True)
    aa = models.CharField(max_length=1, blank=True, null=True)
    ptm_type = models.CharField(max_length=100, blank=True, null=True)
    evidence_code = models.ForeignKey(Evicodes, models.DO_NOTHING, db_column='evidence_code', blank=True, null=True)
    source_link = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'PTMs_old'


class Pfam(models.Model):
    pf_uniprot_id = models.CharField(max_length=10, blank=True, null=True)
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


class Pfamdemo(models.Model):
    pf_uniprot_id = models.CharField(max_length=10, blank=True, null=True)
    align_s = models.IntegerField(blank=True, null=True)
    align_e = models.IntegerField(blank=True, null=True)
    env_s = models.IntegerField(blank=True, null=True)
    env_e = models.IntegerField(blank=True, null=True)
    pfam_id = models.CharField(max_length=10, blank=True, null=True)
    pfam_name = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    hmm_s = models.IntegerField(blank=True, null=True)
    hmm_e = models.IntegerField(blank=True, null=True)
    hmm_len = models.IntegerField(blank=True, null=True)
    bit = models.IntegerField(blank=True, null=True)
    e_value = models.CharField(max_length=30, blank=True, null=True)
    clan = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'PfamDemo'


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


class Proteinlink(models.Model):
    id = models.IntegerField(primary_key=True)
    uniprot_id = models.CharField(max_length=100, blank=True, null=True)
    protein_link = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ProteinLink'


class SeqCanonical(models.Model):
    uniprot_id = models.CharField(max_length=10, blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    sequence = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Seq_canonical'


class Sequences(models.Model):
    uniprot_id = models.CharField(max_length=10, blank=True, null=True)
    isoform = models.TextField(blank=True, null=True)
    sequence = models.TextField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Sequences'


class Signalpeptide(models.Model):
    sp_uniprot_id = models.CharField(max_length=100, blank=True, null=False, primary_key=True)
    signal_peptide = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'SignalPeptide'


class StringidToUniprot(models.Model):
    uniprot_id = models.CharField(max_length=10, blank=True, null=True)
    str_id = models.CharField(db_column='Str_id', max_length=25, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'StringID_to_Uniprot'


class StringAcAll(models.Model):
    str_id = models.CharField(db_column='Str_id', max_length=25, blank=True, null=True)  # Field name made lowercase.
    uniprot_id = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'String_AC_all'


class StringInt(models.Model):
    string_p1 = models.CharField(max_length=20, blank=True, null=True)
    string_p2 = models.CharField(max_length=20, blank=True, null=True)
    combined_score = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'String_int'



class Topodom(models.Model):
    uniprot = models.ForeignKey(Pronameunique, models.DO_NOTHING, db_column='uniprot', blank=True, null=True)
    topology = models.CharField(max_length=30, blank=True, null=True)
    topo_start = models.IntegerField(blank=True, null=True)
    topo_end = models.IntegerField(blank=True, null=True)
    eco = models.ForeignKey(Evicodes, models.DO_NOTHING, db_column='eco', blank=True, null=True)
    source = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'TopoDom'


class Transmem(models.Model):
    tm_uniprot_id = models.CharField(max_length=10, blank=True, null=True)
    tm_start = models.IntegerField(blank=True, null=True)
    tm_end = models.IntegerField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    eco = models.CharField(max_length=15, blank=True, null=True)
    source = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'TransMem'


class Uniprotstringgenename(models.Model):
    uniprot_id = models.CharField(max_length=10, blank=True, null=True)
    string_id = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'UniprotStringGeneName'


class Variantlinks(models.Model):
    var = models.ForeignKey('Variants', models.DO_NOTHING, blank=True, null=True)
    var_link = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'VariantLinks'


class Variants(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    var_uniprot_id = models.CharField(max_length=100, blank=True, null=True)
    var_pos = models.IntegerField(blank=True, null=True)
    aa_original = models.CharField(max_length=2, blank=True, null=True)
    aa_substituion = models.CharField(max_length=2, blank=True, null=True)
    comment = models.CharField(max_length=500, blank=True, null=True)
    protein_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Variants'


class Variantsdemo(models.Model):
    var_id = models.CharField(max_length=100, blank=True, null=True)
    var_uniprot_id = models.CharField(max_length=100, blank=True, null=True)
    var_pos = models.IntegerField(blank=True, null=True)
    aa_original = models.CharField(max_length=2, blank=True, null=True)
    aa_substituion = models.CharField(max_length=2, blank=True, null=True)
    comment = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'VariantsDemo'


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


class FkProDom(models.Model):
    uniprot_id = models.CharField(max_length=10, blank=True, null=True)
    dm_id = models.IntegerField(blank=True, null=True)
    dm_start = models.IntegerField(blank=True, null=True)
    dm_end = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fk_Pro_Dom'








class Prosite(models.Model):
    uniprot_id = models.CharField(max_length=10, blank=True, null=True)
    source = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'prosite'


class StringIdGeneName(models.Model):
    string_id = models.CharField(max_length=20, blank=True, null=True)
    gene_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'string_id_gene_name'




class StringInteractionUniprot(models.Model): 
    id = models.IntegerField(primary_key=True)
    uniprot_p1 = models.CharField(max_length=10, blank=True, null=True)
    string_p1 = models.CharField(max_length=20, blank=True, null=True)
    uniprot_p2 = models.CharField(max_length=10, blank=True, null=True)
    string_p2 = models.CharField(max_length=20, blank=True, null=True)
    combined_score = models.IntegerField(blank=True, null=True)
    

    class Meta:
        managed = False
