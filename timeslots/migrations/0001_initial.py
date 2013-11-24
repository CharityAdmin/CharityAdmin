# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Volunteer'
        db.create_table(u'timeslots_volunteer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, db_column='userId')),
            ('trained', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'timeslots', ['Volunteer'])

        # Adding M2M table for field clients on 'Volunteer'
        m2m_table_name = db.shorten_name(u'timeslots_volunteer_clients')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('volunteer', models.ForeignKey(orm[u'timeslots.volunteer'], null=False)),
            ('client', models.ForeignKey(orm[u'timeslots.client'], null=False))
        ))
        db.create_unique(m2m_table_name, ['volunteer_id', 'client_id'])

        # Adding model 'Client'
        db.create_table(u'timeslots_client', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, db_column='userId')),
        ))
        db.send_create_signal(u'timeslots', ['Client'])

        # Adding model 'ClientOpening'
        db.create_table(u'timeslots_clientopening', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(related_name='openings', db_column='clientId', to=orm['timeslots.Client'])),
            ('startDate', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 19, 0, 0))),
            ('endDate', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='Days of Week', max_length=20)),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'timeslots', ['ClientOpening'])

        # Adding model 'ClientOpeningMetadata'
        db.create_table(u'timeslots_clientopeningmetadata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('clientOpening', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['timeslots.ClientOpening'], db_column='clientOpeningId')),
            ('metadata', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'timeslots', ['ClientOpeningMetadata'])

        # Adding model 'ClientOpeningException'
        db.create_table(u'timeslots_clientopeningexception', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('clientOpening', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['timeslots.ClientOpening'], db_column='clientOpeningId')),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'timeslots', ['ClientOpeningException'])

        # Adding model 'VolunteerCommitment'
        db.create_table(u'timeslots_volunteercommitment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('clientOpening', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['timeslots.ClientOpening'], db_column='clientOpeningId')),
            ('volunteer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='commitments', db_column='volunteerId', to=orm['timeslots.Volunteer'])),
            ('startDate', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('endDate', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='Days of Week', max_length=20)),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'timeslots', ['VolunteerCommitment'])

        # Adding model 'VolunteerCommitmentMetadata'
        db.create_table(u'timeslots_volunteercommitmentmetadata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('volunteerCommitment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['timeslots.VolunteerCommitment'], db_column='volunteerCommitmentId')),
            ('metadata', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'timeslots', ['VolunteerCommitmentMetadata'])

        # Adding model 'VolunteerCommitmentException'
        db.create_table(u'timeslots_volunteercommitmentexception', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('volunteerCommitment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['timeslots.VolunteerCommitment'], db_column='volunteerCommitmentId')),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'timeslots', ['VolunteerCommitmentException'])


    def backwards(self, orm):
        # Deleting model 'Volunteer'
        db.delete_table(u'timeslots_volunteer')

        # Removing M2M table for field clients on 'Volunteer'
        db.delete_table(db.shorten_name(u'timeslots_volunteer_clients'))

        # Deleting model 'Client'
        db.delete_table(u'timeslots_client')

        # Deleting model 'ClientOpening'
        db.delete_table(u'timeslots_clientopening')

        # Deleting model 'ClientOpeningMetadata'
        db.delete_table(u'timeslots_clientopeningmetadata')

        # Deleting model 'ClientOpeningException'
        db.delete_table(u'timeslots_clientopeningexception')

        # Deleting model 'VolunteerCommitment'
        db.delete_table(u'timeslots_volunteercommitment')

        # Deleting model 'VolunteerCommitmentMetadata'
        db.delete_table(u'timeslots_volunteercommitmentmetadata')

        # Deleting model 'VolunteerCommitmentException'
        db.delete_table(u'timeslots_volunteercommitmentexception')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'timeslots.client': {
            'Meta': {'object_name': 'Client'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'db_column': "'userId'"})
        },
        u'timeslots.clientopening': {
            'Meta': {'object_name': 'ClientOpening'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'openings'", 'db_column': "'clientId'", 'to': u"orm['timeslots.Client']"}),
            'endDate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'startDate': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 19, 0, 0)'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'Days of Week'", 'max_length': '20'})
        },
        u'timeslots.clientopeningexception': {
            'Meta': {'object_name': 'ClientOpeningException'},
            'clientOpening': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['timeslots.ClientOpening']", 'db_column': "'clientOpeningId'"}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'timeslots.clientopeningmetadata': {
            'Meta': {'object_name': 'ClientOpeningMetadata'},
            'clientOpening': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['timeslots.ClientOpening']", 'db_column': "'clientOpeningId'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metadata': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'timeslots.volunteer': {
            'Meta': {'object_name': 'Volunteer'},
            'clients': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'volunteers'", 'symmetrical': 'False', 'to': u"orm['timeslots.Client']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'trained': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'db_column': "'userId'"})
        },
        u'timeslots.volunteercommitment': {
            'Meta': {'object_name': 'VolunteerCommitment'},
            'clientOpening': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['timeslots.ClientOpening']", 'db_column': "'clientOpeningId'"}),
            'endDate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'startDate': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'Days of Week'", 'max_length': '20'}),
            'volunteer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'commitments'", 'db_column': "'volunteerId'", 'to': u"orm['timeslots.Volunteer']"})
        },
        u'timeslots.volunteercommitmentexception': {
            'Meta': {'object_name': 'VolunteerCommitmentException'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'volunteerCommitment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['timeslots.VolunteerCommitment']", 'db_column': "'volunteerCommitmentId'"})
        },
        u'timeslots.volunteercommitmentmetadata': {
            'Meta': {'object_name': 'VolunteerCommitmentMetadata'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metadata': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'volunteerCommitment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['timeslots.VolunteerCommitment']", 'db_column': "'volunteerCommitmentId'"})
        }
    }

    complete_apps = ['timeslots']