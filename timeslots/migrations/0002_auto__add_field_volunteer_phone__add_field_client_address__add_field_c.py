# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Volunteer.phone'
        db.add_column(u'timeslots_volunteer', 'phone',
                      self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Client.address'
        db.add_column(u'timeslots_client', 'address',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Client.address2'
        db.add_column(u'timeslots_client', 'address2',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Client.city'
        db.add_column(u'timeslots_client', 'city',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Client.state'
        db.add_column(u'timeslots_client', 'state',
                      self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Client.zipcode'
        db.add_column(u'timeslots_client', 'zipcode',
                      self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Client.phone'
        db.add_column(u'timeslots_client', 'phone',
                      self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True),
                      keep_default=False)


        # Changing field 'ClientOpening.notes'
        db.alter_column(u'timeslots_clientopening', 'notes', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

    def backwards(self, orm):
        # Deleting field 'Volunteer.phone'
        db.delete_column(u'timeslots_volunteer', 'phone')

        # Deleting field 'Client.address'
        db.delete_column(u'timeslots_client', 'address')

        # Deleting field 'Client.address2'
        db.delete_column(u'timeslots_client', 'address2')

        # Deleting field 'Client.city'
        db.delete_column(u'timeslots_client', 'city')

        # Deleting field 'Client.state'
        db.delete_column(u'timeslots_client', 'state')

        # Deleting field 'Client.zipcode'
        db.delete_column(u'timeslots_client', 'zipcode')

        # Deleting field 'Client.phone'
        db.delete_column(u'timeslots_client', 'phone')


        # Changing field 'ClientOpening.notes'
        db.alter_column(u'timeslots_clientopening', 'notes', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

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
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'db_column': "'userId'"}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
        u'timeslots.clientopening': {
            'Meta': {'object_name': 'ClientOpening'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'openings'", 'db_column': "'clientId'", 'to': u"orm['timeslots.Client']"}),
            'endDate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
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
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
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