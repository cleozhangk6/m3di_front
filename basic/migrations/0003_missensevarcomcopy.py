# Generated by Django 4.0.2 on 2022-02-20 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0002_aaconversion_authgroup_authgrouppermissions_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MissenseVarComCopy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uniprot', models.CharField(blank=True, max_length=10, null=True)),
                ('posuniprot', models.IntegerField(blank=True, null=True)),
                ('pdbpos', models.IntegerField(blank=True, null=True)),
                ('res_wt', models.CharField(blank=True, max_length=4, null=True)),
                ('res_mut', models.CharField(blank=True, max_length=4, null=True)),
                ('missensepred', models.CharField(blank=True, max_length=50, null=True)),
                ('missense_reason', models.CharField(blank=True, max_length=100, null=True)),
                ('comment', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'db_table': 'Missense_Var_Com_Copy',
                'managed': False,
            },
        ),
    ]